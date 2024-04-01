from flask_seeder import Seeder
from werkzeug.security import generate_password_hash

from src.modules.user.model.permission import Permission
from src.modules.user.model.role import Role
from src.logger import logger
from src.modules.user.model.user import User
from src.config.permission_groups import PermissionGroup

SKIP = False


class RoleSeed(Seeder):
    priority = 1

    def run(self):
        if SKIP:
            logger.info(f"{self.name}.py skipped script")

            return

        all_granted_permission = Permission(name=PermissionGroup.ALL_GRANTED, module="ALL_MODULES")
        self.db.session.add(all_granted_permission)

        admin_role = Role(name="ADMIN")

        admin_role.permissions.append(all_granted_permission)

        self.db.session.add(admin_role)

        admin_user = User(
            email="admin@gmail.com",
            password=generate_password_hash("admin"),
            active=True,
            code="12345"
        )

        admin_user.roles.append(admin_role)

        self.db.session.add(admin_user)

        self.db.session.commit()
