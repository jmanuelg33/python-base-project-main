from flask_openapi3 import Info
from src.common.generic_responses import Unauthorized, ServerError, UnprocessableEntity

info = Info(title="TMS API", version="1.0.0",
            description="This API, developed for Traxporta's Transportation Management System (TMS). In this API "
                        "documentation, users will find detailed descriptions of the available services. Each "
                        "endpoint is clearly documented with required parameters, possible responses, and behavior "
                        "under various scenarios. The API is crafted to be user-friendly, ensuring seamless "
                        "integration into your existing systems. The version of this API reflects our latest "
                        "advancements and improvements.")

jwt = {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}

security_schemes = {"jwt": jwt}

generic_responses = {
    "401": Unauthorized,
    "500": ServerError,
    "422": UnprocessableEntity,
}
