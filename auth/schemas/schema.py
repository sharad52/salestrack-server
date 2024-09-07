from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from salestrack.schemas.schema import Status
from datetime import datetime


class TokenBaseSchema(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT Refresh token")

class TokenResponse(BaseModel):
    Status: Status
    User: TokenBaseSchema


class TokenCreateSchema(TokenBaseSchema):
    user_id: int
    status: bool
    created_date: datetime


class TokenCreateResponse(BaseModel):
    Status: Status
    Token: TokenCreateSchema


class UserBaseSchema(BaseModel):
    id: Optional[int] = None
    email: EmailStr = Field(
        ..., description="The login email of user", examples='abc@example.com'
    )
    password: str = Field(
        ..., description="The password of user", examples="Password@123"
    )

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True


class UserResponse(BaseModel):
    Status: Status
    User: UserBaseSchema


class ChangePaaswordBaseSchema(BaseModel):
    email: EmailStr = Field(
        ..., description="The login email address", examples="abc@example.com"
    )
    old_password: str = Field(
        ..., description="Old login password."
    )
    new_password: str = Field(
        ..., description="New Password."
    )

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True

    

