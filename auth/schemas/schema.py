from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from salestrack.schemas.schema import Status



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




        
