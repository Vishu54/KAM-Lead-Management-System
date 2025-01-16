import asyncio
import logging
import argparse
from fastapi import APIRouter, FastAPI
from hypercorn.config import Config
from hypercorn.asyncio import serve
from contextlib import asynccontextmanager

from core.config import APP_CONFIG, AUTH_CONTROLLER
from core.custom_exception import AppRuntimeException
from core.database import get_db
from middleware.auth_middleware import AuthMiddleware
from middleware.exception_middleware import ExceptionMiddleware
from router.restaurant import router as restaurant_router
from router.user import router as user_router
from router.interaction import router as interaction_router
from router.call_plan import router as call_plan_router
from router.order import router as order_router
from router.performance import router as performance_router
from router.auth import router as auth_router


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up application...")
    try:
        get_db()
        logger.info("Database initialization completed")
        yield
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        AppRuntimeException(error_code=500, message="Failed to start the database")


app = FastAPI(title=APP_CONFIG["app_name"], description=APP_CONFIG["description"], version=APP_CONFIG["version"])

# Version1 API
v1_app = APIRouter(prefix="/v1")

# Middleware
app.add_middleware(AuthMiddleware, auth_controller=AUTH_CONTROLLER)
app.add_middleware(ExceptionMiddleware)


@app.get("/health")
async def health():
    return {"status": "OK"}


v1_app.include_router(auth_router)
v1_app.include_router(user_router)
v1_app.include_router(restaurant_router)
v1_app.include_router(interaction_router)
v1_app.include_router(call_plan_router)
v1_app.include_router(order_router)
v1_app.include_router(performance_router)


app.include_router(v1_app)


def _get_command_line_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--PORT", help="Port")
    parser.add_argument("-ip", "--IP", help="IP Binding")
    args = parser.parse_args()
    ip_to_run_on = args.IP if args.IP else APP_CONFIG.get("host")
    port_to_run_on = args.PORT if args.PORT else APP_CONFIG.get("port")
    return ip_to_run_on, port_to_run_on


if __name__ == "__main__":
    ip_to_bind, port_to_bind = _get_command_line_args()
    logger.info(f"Starting the app with IP:{ip_to_bind} and port:{port_to_bind}")
    config = Config()
    config.bind = [ip_to_bind + ":" + port_to_bind]
    asyncio.run(serve(app, config))
