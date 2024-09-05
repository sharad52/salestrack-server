import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property


Base = declarative_base()

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
    family_id = sa.Column(sa.Integer, sa.ForeignKey("family.id"))
    price = sa.Column(sa.Float)

    family = sa.orm.relationship('Family')


class Sales(Base):
    __tablename__ = "sales"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    product_id = sa.Column(sa.Integer, sa.ForeignKey("product.id"))
    sales_date = sa.Column(sa.Date)
    sales_amount = sa.Column(sa.Float)

    product = sa.orm.relationship('Product')

    @hybrid_property
    def year_month(self):
        return self.sales_date.strftime("%Y-%m")


