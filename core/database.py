import logging
import os
import functools
import inspect

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

from core.custom_exception import AppRuntimeException, handle_exception
from models import base_model


logger = logging.getLogger(__name__)  # Create or Get logger

default_db = os.getenv("DB_TYPE", default="postgres")


def postgresql_engine():
    connection_dict = get_connection_map()
    _SQLALCHEMY_DATABASE_URL = connection_dict["connection_string"]
    _engine = create_engine(_SQLALCHEMY_DATABASE_URL, pool_recycle=3600, pool_pre_ping=True)
    return _engine


DB_ENGINE_MAPPING = {
    "postgres": postgresql_engine,
}


def get_connection_map():
    from core.config import APP_CONFIG

    _SQLALCHEMY_DATABASE_URL = ""
    _db_session_props = {
        "host": os.getenv("DB_HOST", APP_CONFIG.get("db_host", "localhost")),
        "port": os.getenv("DB_PORT", APP_CONFIG.get("db_port", "5432")),
        "user": os.getenv("DB_USER", APP_CONFIG.get("db_user", "udaan")),
        "db": os.getenv("DB_NAME", APP_CONFIG.get("db_name", "postgres")),
        "password": os.getenv("DB_PASSWORD", APP_CONFIG.get("db_password", "password")),
    }

    _SQLALCHEMY_DATABASE_URL = URL(
        drivername="postgresql",
        username=_db_session_props["user"],
        password=_db_session_props["password"],
        host=_db_session_props["host"],
        port=_db_session_props["port"],
        database=_db_session_props["db"],
        query={},
    )

    return {"db_name": default_db, "connection_string": _SQLALCHEMY_DATABASE_URL}


def get_active_engine():
    logger.info(f'Getting active db engine, default db is set as "{default_db}"')
    _engine = None
    try:
        _engine = DB_ENGINE_MAPPING[default_db]()
    except KeyError:
        logger.error(f"DB Type not supported: {default_db}")
        raise AppRuntimeException(500, "DB Type not supported in the system")

    return _engine


def get_session():
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_active_engine(), expire_on_commit=False)
    return _SessionLocal()


class DbConnector:
    def __init__(self):
        try:
            self._bind_tables()
            self._create_session()
        except:
            handle_exception(message="Error in db initialization")

    def _create_session(self):
        self.Session = get_session()

    def _bind_tables(self):
        base_model.Base.metadata.create_all(bind=get_active_engine())

    def close_session(self):
        try:
            if self.Session is not None:
                self.Session.close()
        except:
            logger.error("Exception happened during db close", exc_info=True)

    def roll_back_transaction(self):
        if self.Session is not None:
            try:
                self.Session.rollback()
            except Exception:
                logger.error("Additional Exception happened during rollback", exc_info=True)


def get_db() -> DbConnector:
    try:
        db = DbConnector()
        if db:
            return db
    except:
        logger.error("Error on getting Db", exc_info=True)
        raise AppRuntimeException(500, "Error on getting DB")


async def call_function(func, *args, **kwargs):
    if inspect.iscoroutinefunction(func):
        result = await func(*args, **kwargs)
    else:
        result = func(*args, **kwargs)
    return result


def managed_transaction(func):
    logger.debug(f"Initializing managed_transaction with func.__name__: {func.__name__}")

    @functools.wraps(func)
    async def wrap_func(*args, **kwargs):
        logger.debug(f"Start of wrap function")
        if "db" in kwargs and kwargs["db"] is not None:
            return await call_function(func, *args, **kwargs)
        else:
            db: DbConnector = get_db()
            kwargs["db"] = db

        try:
            result = await call_function(func, *args, **kwargs)
            db.Session.commit()
            logger.debug(f"Post call to the wrapped func: {func.__name__}")
        except AppRuntimeException as e:
            logger.error(f"Error raised and now doing rollback", exc_info=False)
            db.roll_back_transaction()
            raise e
        except Exception as e:
            logger.exception(str(e), exc_info=True)
            logger.error(f"Error raised and now doing rollback")
            db.roll_back_transaction()
            handle_exception()
        finally:
            logger.debug(f"Finally called and will close session now")
            db.close_session()

        logger.debug("End of wrap function. Returning result now")
        return result

    logger.debug(f"Initialization complete of managed_transaction returning func.__name__: {func.__name__}")
    return wrap_func
