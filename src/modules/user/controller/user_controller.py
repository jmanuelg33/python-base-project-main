from flask_openapi3 import APIBlueprint, Tag
from flask_jwt_extended import get_current_user

from src.common.utils.api_helpers import ok_response
from src.common.utils.jwt_auth.jwt_tools import login_required

tag = Tag(name='user routes', description='User service api')

user_bp = APIBlueprint("user", __name__, abp_tags=[tag], url_prefix="/api/v1/user")


@user_bp.get('/info', summary="Get user authenticated info")
@login_required
def get_info():
    user = get_current_user()

    data = {
        "id": user.id,
        "email": user.email,
        "roles": [role.name for role in user.roles],
        "permissions": [p.name for role in user.roles for p in role.permissions]
    }

    return ok_response(data=data)
