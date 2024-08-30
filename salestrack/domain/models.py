import sqlalchemy as sa
# from sqlalchemy.orm import relationship
from salestrack.databases.config import Base


class User(Base):
    __tablename__ = 'users'
    
    id = sa.Column(sa.Integer, primary_key=True)
    email = sa.Column(sa.String, unique=True, index=True)
    hashed_password = sa.Column(sa.String)
    is_active = sa.Column(sa.Boolean, default=True)


class Family(Base):
    __tablename__ = 'family'
    
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, index=True)


class Product(Base):
    __tablename__ = "product"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    name = sa.Column(sa.String, index=True)
    family_name = sa.Column(sa.String, sa.ForeignKey("family.name"))

    family = sa.orm.relationship("Family")


class Sales(Base):
    __tablename__ = "sales"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    product_id = sa.Column(sa.Integer, sa.ForeignKey("product.id"))
    quantity = sa.Column(sa.Integer)

    product = sa.orm.relationship("product")
