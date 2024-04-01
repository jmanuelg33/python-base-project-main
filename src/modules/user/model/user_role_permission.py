from src import db
from sqlalchemy.dialects.postgresql import UUID

user_role = db.Table(
    "user_role",
    db.Column("user_id", UUID(as_uuid=True), db.ForeignKey("user.id")),
    db.Column("role_id", UUID(as_uuid=True), db.ForeignKey("role.id"))
)

role_permission = db.Table(
    "role_permission",
    db.Column("role_id", UUID(as_uuid=True), db.ForeignKey("role.id")),
    db.Column("permission_id", UUID(as_uuid=True), db.ForeignKey("permission.id"))
)
