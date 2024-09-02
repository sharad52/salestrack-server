import csv
from datetime import datetime
from typing import List
from fastapi import APIRouter
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session

from salestrack.schemas import schema
from salestrack.domain import models
from salestrack.dbconfig.db_config import get_db


router = APIRouter(prefix="/sales", tags=["Sales"])

@router.get("/family", response_model=List[schema.AddFamily])
async def list_family(
    db: Session = Depends(get_db)
):
    
    family = db.query(models.Family).all()
    return family


@router.post("/load_data/")
async def load_data(csv_file: str, db: Session = Depends(get_db)):
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # code block to handle family
            family = db.query(models.Family).filter(models.Family.name == row['Family']).first()
            if not family:
                family = models.Family(name=row['Family'])
                db.add(family)
                db.commit()
                db.refresh(family)
            
            #code to handle product
            product = db.query(models.Product).filter(models.Product.id == row['Product ID']).first()
            if not product:
                product = models.Product(
                    id=row["Product ID"],
                    name=row["Product Name"],
                    price=row["Price"],
                    family_id=family.id,
                )
                db.add(product)
                db.commit()
                db.refresh(product)
            #code to handle Sales
            for month, sales in row.items():
                if month.startswith("2024"):
                    sale_date = datetime.strptime(month, "%Y-%m")
                    sale = models.Sales(
                        product_id=product.id,
                        month=sale_date,
                        sales_amount=int(sales),
                    )
                    db.add(sale)
                    db.commit()


@router.get("/products/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail=f"No product found for id: {product_id}")
    sales = db.query(models.Sales).filter(models.Sales.product_id == product_id).all()
    return {
        "product": product.name,
        "family": product.family.name,
        "price": product.price,
        "sales": [{"month": sale.month, "amount": sale.sales_amount} for sale in sales]
    }


@router.get("/products/")
async def list_products(db: Session = Depends(get_db)):
    products = db.query(models.Product).all()
    return [{
        "id": product.id, 
        "name": product.name, 
        "family": product.family.name, 
        "price": product.price
        } for product in products
    ]
