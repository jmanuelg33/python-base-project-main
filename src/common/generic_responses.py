from pydantic import BaseModel, Field


class Unauthorized(BaseModel):
    code: int = Field(401, description="Status Code")
    message: str = Field("Unauthorized!", description="Exception Information")


class UnprocessableEntity(BaseModel):
    code: int = Field(422, description="Status Code")
    message: str = Field("UnprocessableEntity",
                         description="Exception Information")  # TODO: Define error 422 generic message


class ServerError(BaseModel):
    code: int = Field(500, description="Status Code")
    message: str = Field("'Unknown error. Please check the logs for more details'", description="Exception Information")
