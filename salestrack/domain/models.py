from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Date

from salestrack.dbconfig.db_config import Base


class Family(Base):
    __tablename__ = 'family'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    family_id = Column(Integer, ForeignKey("family.id"))
    price = Column(Float)

    family = relationship('Family')


class Sales(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("product.id"))
    sales_date = Column(Date)
    sales_amount = Column(Integer)

    product = relationship('Product')

    @hybrid_property
    def year_month(self):
        return self.sales_date.strftime("%Y-%m")


