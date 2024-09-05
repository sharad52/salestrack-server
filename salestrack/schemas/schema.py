from enum import Enum
from typing import Optional
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


class ProductBaseSchema(BaseModel):
    id: int | None = None
    name: str = Field(
        ..., description="The name of the Product", examples="Candy"
    )
    family_id: int = Field(
        ..., description="The id of the family", examples=1
    )
    price: float = Field(
        ..., description="Price of an product", examples=12.0
    )

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True


class ProductResponse(BaseModel):
    Status: Status
    Product: ProductBaseSchema


class SalesBaseSchema(BaseModel):
    id: int | None = None
    productt_id: int = Field(
        ..., description="The id of the Product", examples=1
    )
    sales_date: str = Field(
        ..., description="The date of sale", examples="2024-09-01"
    )
    sales_amount: int = Field(
        ..., description="Sales amount of product in given month", examples=125487.0
    )

    class Config:
        from_attributes = True
        populate_by_name = True
        arbitrary_types_allowed = True


class SalesResponse(BaseModel):
    Status: Status
    Product: SalesBaseSchema


