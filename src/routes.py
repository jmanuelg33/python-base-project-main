from src.modules.public.controller.public_controller import public_bp
from src.modules.user.controller.user_controller import user_bp


def register_blueprints(app):
    app.register_api(public_bp)
    app.register_api(user_bp)
