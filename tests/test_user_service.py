import pytest
from unittest.mock import MagicMock, patch

from src.modules.public.dto.login_dto import LoginDTO
from src.modules.user.dao.user_dao import UserDAO
from src.modules.user.model.permission import Permission
from src.modules.user.model.role import Role
from src.common.exceptions.user_exception import EmailNotRegisteredException, InvalidCredentialsException
from src.modules.user.model.user import User
from src.modules.user.service.user_service import UserService


@pytest.fixture
def login_dto(app):
    return LoginDTO(email="test@example.com", password="password123")


@pytest.fixture
def admin_role_mock(app):
    admin_role_mock = Role(name="admin")
    admin_role_mock.permissions = [Permission(
        name="ALL_GRANTED",
        module="ALL_MODULES"
    )]

    return admin_role_mock


@pytest.fixture
def user_mock(app, admin_role_mock):
    user_mock = User()
    user_mock.email = "test@example.com"
    user_mock.password = "hashed_password"
    user_mock.active = True
    user_mock.roles = [admin_role_mock]

    return user_mock


def test_verify_login_with_valid_credentials(app, login_dto, user_mock):
    user_model_mock = MagicMock()
    user_model_mock.query.filter_by.return_value.all.return_value = [user_mock]

    with patch.object(UserDAO, "model", user_model_mock):
        user_service = UserService()

        assert user_service.verify_login(login_dto) is not None


def test_verify_login_with_invalid_email(app, login_dto):
    user_model_mock = MagicMock()
    user_model_mock.query.filter_by.return_value.all.return_value = []

    with pytest.raises(EmailNotRegisteredException):
        with patch.object(UserDAO, "model", user_model_mock):
            user_service = UserService()

            assert user_service.verify_login(login_dto) is None


def test_verify_login_with_invalid_password(app, login_dto, user_mock):
    user_model_mock = MagicMock()
    user_model_mock.query.filter_by.return_value.all.return_value = [user_mock]

    with pytest.raises(InvalidCredentialsException):
        with patch.object(user_mock, "check_password", MagicMock(check_password=False)):
            with patch.object(UserDAO, "model", user_model_mock):
                user_service = UserService()

                assert user_service.verify_login(login_dto) is None
