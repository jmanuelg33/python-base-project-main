from flask_openapi3 import APIBlueprint, Tag
from flask_jwt_extended import verify_jwt_in_request, get_current_user

from src.common.exceptions.user_exception import JwtException
from src.common.utils.api_helpers import ok_response
from src.common.utils.jwt_auth.jwt_tools import get_token
from src.modules.public.dto.login_dto import LoginDTO
from src.modules.user.service.user_service import UserService

tag = Tag(name='Public routes', description='Public service api')

public_bp = APIBlueprint("public", __name__, abp_tags=[tag], url_prefix="/api/v1")

user_service = UserService()


@public_bp.get('/health-check', summary="Health Check Service")
def health_check():
    return ok_response()


@public_bp.post("/login", summary="Login attempt")
def login(body: LoginDTO):
    params = LoginDTO.model_validate(body.dict())

    user = user_service.verify_login(params)

    access_token, refresh_token = get_token(user)

    return ok_response(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token
        })


@public_bp.get("/refresh", summary="Refresh token")
def refresh():
    try:
        verify_jwt_in_request(refresh=True)
    except Exception:
        raise JwtException(message="invalid refresh token")

    user = get_current_user()

    if not user:
        raise JwtException(message="invalid token")

    access_token, refresh_token = get_token(user)

    return ok_response(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token
        })
