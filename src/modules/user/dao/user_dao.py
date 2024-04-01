class UserDAO:
    def search(self, **kwargs) -> list:
        return self.model.query.filter_by(**kwargs).all()

    @property
    def model(self):
        from src.modules.user.model.user import User

        return User
