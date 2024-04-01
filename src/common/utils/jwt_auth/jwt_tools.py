from datetime import timedelta
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, create_access_token, \
    create_refresh_token, get_current_user

from src.config.permission_groups import PermissionGroup


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        return func(*args, **kwargs)

    return wrapper


def roles_required(*roles_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            user = get_current_user()

            for role in roles_name:
                if role in user.user_roles:
                    return func(*args, **kwargs)
            return jsonify(message="Unauthorized"), 403

        return wrapper

    return decorator


def permissions_required(*permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()

            user = get_current_user()

            for p in permissions:
                if __is_user_allowed(user, p.name, PermissionGroup.ALL_GRANTED):
                    return func(*args, **kwargs)

            return jsonify(message="Unauthorized"), 403

        return wrapper

    return decorator


def get_token(user):
    from src.app import CONFIG

    identity = {"id": user.id}

    roles_name = [role.name for role in user.roles]

    access_expires_time = timedelta(seconds=CONFIG.get("ACCESS_TOKEN_EXPIRES"))
    refresh_expires_time = timedelta(seconds=CONFIG.get("REFRESH_TOKEN_EXPIRES"))

    access_token = create_access_token(identity=identity, additional_claims={"roles": roles_name},
                                       expires_delta=access_expires_time)
    refresh_token = create_refresh_token(identity=identity, expires_delta=refresh_expires_time)
    return access_token, refresh_token


def __is_user_allowed(user, permission_name, default_permission):
    permissions_list = [p.name for role in user.roles for p in role.permissions]

    if default_permission in permissions_list:
        return True

    return permission_name in permissions_list
