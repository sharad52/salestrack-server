from enum import Enum
from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str
    hashed_password: str
    is_active: bool

    class config:
        orm_mode: True


class AddUser(UserBase):
    class config:
        orm_mode = True


class AddFamily(BaseModel):
    name: str


class AddProduct(BaseModel):
    name: str
    family_id: int
    price: float


class AddSales(BaseModel):
    product_id: int
    sales_date: str
    sales_amount: int


class FamilyBaseSchema(BaseModel):
    id: int | None = None
    name: str = Field(
        ..., description="The name of the family", examples="Candy"
    )

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True


class Status(Enum):
    Success = "Success"
    Failed = "Failed"


class FamilyResponse(BaseModel):
    Status: Status
    Family: FamilyBaseSchema