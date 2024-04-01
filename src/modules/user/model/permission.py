from src.common.base_model import Base
from src import db


class Permission(Base, db.Model):
    __tablename__ = 'permission'

    name = db.Column(db.String(32), unique=True)
    module = db.Column(db.String(32))
