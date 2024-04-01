from flask import jsonify
from flask_openapi3 import OpenAPI
from flask_migrate import Migrate
from flask_seeder import FlaskSeeder
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import psycopg2
from flask_cors import CORS
from urllib.parse import urlparse
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from .common.exceptions import BaseAPIException

from .config.open_api import security_schemes, info
from .logger import logger
from .routes import register_blueprints
from .common.base_model import Base

TEST_DATABASE_NAME = 'tms_test'

db = SQLAlchemy(model_class=Base)


def create_app(config):
    # sentry_sdk.init(
    #     dsn=config.get('SENTRY_DSN'),
    #     enable_tracing=True,
    #     integrations=[FlaskIntegration()]
    # )

    app = OpenAPI(__name__, info=info, security_schemes=security_schemes,
                  doc_ui=config.get('FLASK_ENV') == "development")
    app.config.update(**config)

    CORS(app)

    __init_db(app)

    __init_exception(app)

    __init_jwt(app)

    __init_migrations(app, db, "src/database/migrations")

    __init_seeds(app, db)

    register_blueprints(app)

    return app


def __init_db(app: OpenAPI):
    __create_database(app.config['SQLALCHEMY_DATABASE_URI'], app.config.get('TESTING', False))
    db.init_app(app)


def __init_jwt(app: OpenAPI):
    jwt = JWTManager(app)

    @jwt.user_lookup_loader
    def user_lookup_loader_callback(_, identity):
        from src.modules.user.model.user import User

        user = User.query.get(identity["sub"]["id"])
        return user


def __init_migrations(app: OpenAPI, database: SQLAlchemy, dir_path: str):
    Migrate(app, database, directory=dir_path)

    # migrations models to tracking changes
    from src.modules.user.model import user, role, permission, user_role_permission


def __init_seeds(app: OpenAPI, database: SQLAlchemy):
    seeder = FlaskSeeder()
    seeder.init_app(app, database)


def __init_exception(app: OpenAPI):
    @app.errorhandler(Exception)
    def handler(e):
        if isinstance(e, BaseAPIException):
            return e

        response = {
            'status': 'fail',
            'code': 'STANDARD_ERROR',
            'data': {
                'message': str(e)
            }
        }

        logger.error(str(e))
        return jsonify(response), 500

    @app.errorhandler(BaseAPIException)
    def handle_exception(e):
        response = {
            'status': 'fail',
            'code': e.code,
            'data': {
                'message': e.message
            }
        }

        return jsonify(response), e.status_code


def __create_database(connection_url, is_testing):
    # Extract host and database name from the connection URL
    parsed_url = urlparse(connection_url)

    host = parsed_url.hostname
    new_database = TEST_DATABASE_NAME if is_testing else parsed_url.path[1:]

    # Connect to the default PostgreSQL database
    default_conn = psycopg2.connect(
        host=host,
        user=parsed_url.username,
        password=parsed_url.password,
        database='postgres',
        port=parsed_url.port
    )
    default_conn.autocommit = True
    default_cursor = default_conn.cursor()

    # Check if the specified database exists
    default_cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{new_database}';")
    exists = default_cursor.fetchone()

    if not exists:  # pragma: no cover
        # Create the specified database if it doesn't exist
        default_cursor.execute(f"CREATE DATABASE {new_database};")
        print(f"Warning: Database {new_database} doesn't exist so it was created")

    default_cursor.close()
    default_conn.close()
