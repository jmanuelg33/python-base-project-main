from pydantic import BaseModel, Field, EmailStr


class LoginDTO(BaseModel):
    email: EmailStr = Field(..., description="Email required")
    password: str = Field(..., description="Password required")
