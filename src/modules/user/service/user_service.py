from src.modules.public.dto.login_dto import LoginDTO
from src.modules.user.dao.user_dao import UserDAO
from src.common.exceptions.user_exception import EmailNotRegisteredException, InvalidCredentialsException


class UserService:
    def __init__(self):
        self.__user_dao = UserDAO()

    def verify_login(self, dto: LoginDTO):
        users = self.__user_dao.search(email=dto.email)

        if not len(users) > 0:
            raise EmailNotRegisteredException(message="email not registered")

        if users[0].check_password(dto.password):
            raise InvalidCredentialsException(message="invalid credentials")

        return users[0]
