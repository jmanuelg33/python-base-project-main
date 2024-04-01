import os
from dotenv import load_dotenv

from src import create_app

load_dotenv()

CONFIG = {
    'SQLALCHEMY_DATABASE_URI': os.getenv('SQLALCHEMY_DATABASE_URI'),
    'COGNITO_REGION': os.getenv('COGNITO_REGION'),
    'COGNITO_USER_POOL_ID': os.getenv('COGNITO_USER_POOL_ID'),
    'SENTRY_DSN': os.getenv('SENTRY_DSN'),
    'FLASK_ENV': os.getenv('FLASK_ENV', 'development'),
    'JWT_SECRET_KEY': os.getenv('JWT_SECRET_KEY'),
    'ACCESS_TOKEN_EXPIRES': int(os.getenv('ACCESS_TOKEN_EXPIRES', 3600)),
    'REFRESH_TOKEN_EXPIRES': int(os.getenv('REFRESH_TOKEN_EXPIRES', 86400))
}

app = create_app(config=CONFIG)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
