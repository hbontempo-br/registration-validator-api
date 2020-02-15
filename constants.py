import os

from utils.environment import get_environment_variable

SERVICE_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SERVICE_ROOT, os.pardir))
SCHEMA_FILE = os.path.join(SERVICE_ROOT, "api", "schemas", "api_schema.yaml")
SERVICE_NAME = get_environment_variable("SERVICE_NAME", "registration-validator-api")
COMMIT = get_environment_variable("COMMIT", None)


DB_USER = get_environment_variable("DB_USER")
DB_PASSWORD = get_environment_variable("DB_PASSWORD")
DB_ADDRESS = get_environment_variable("DB_ADDRESS")
DB_DATABASE = get_environment_variable("DB_DATABASE", "registration_validator")
