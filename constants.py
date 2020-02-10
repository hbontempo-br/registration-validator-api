import os

from utils.environment import get_environment_variable

SERVICE_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SERVICE_ROOT, os.pardir))
SCHEMA_FILE = os.path.join(SERVICE_ROOT, "api", "schemas", "api_schema.yaml")
SERVICE_NAME = get_environment_variable("SERVICE_NAME", "cpf-validator-api")
COMMIT = get_environment_variable("COMMIT", "COMMIT")
