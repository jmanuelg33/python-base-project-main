from werkzeug.security import check_password_hash, generate_password_hash

from src.common.base_model import Base
from src import db


class User(Base, db.Model):
    __tablename__ = 'user'

    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    active = db.Column(db.Boolean, default=False)
    code = db.Column(db.String(150))
    roles = db.relationship("Role", secondary="user_role", backref="users")

    def set_password(self, raw):
        self.password = generate_password_hash(raw)

    def check_password(self, raw):
        if not self.password:
            return False

        return check_password_hash(self.password, generate_password_hash(raw))

    def __repr__(self) -> str:  # pragma: no cover
        return f'User>>> {self.email} - role: {self.roles}'
