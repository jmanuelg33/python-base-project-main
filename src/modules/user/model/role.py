from src.common.base_model import Base
from src import db


class Role(Base,db.Model):
    __tablename__ = "role"

    name = db.Column(db.String(50), unique=True, nullable=False)
    permissions = db.relationship("Permission", secondary="role_permission", backref='roles')

    def __repr__(self) -> str:  # pragma: no cover
        return f'Role>>> {self.name}'
