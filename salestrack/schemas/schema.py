from pydantic import BaseModel


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
    family_name: str


class AddSales(BaseModel):
    product_id: int
    quantity: int