import json
import os
import logging

from security.auth_controller import AuthController
from security.authentication import DatabaseAuthenticator, JWTTokenStrategy

logger = logging.getLogger(__name__)


app_config_file_path = os.path.join("config", "app.json")

public_endpoints_file_path = os.path.join("config", "public_endpoint.json")


env_config_file_path = os.path.join("config", "env.json")
if not os.path.isfile(env_config_file_path):
    environment_in_use = os.getenv("env_type") if os.getenv("env_type") else "local"
else:
    try:
        environment_in_use = json.load(open(env_config_file_path)).get("env_type", "local")
    except:
        environment_in_use = "local"

APP_CONFIG: dict = json.load(open(app_config_file_path))

APP_CONFIG.update(APP_CONFIG[environment_in_use])

PUBLIC_ENDPOINTS = json.load(open(public_endpoints_file_path))


AUTH_CONTROLLER = AuthController(DatabaseAuthenticator(), JWTTokenStrategy("Test"))
