import csv
from datetime import datetime, timedelta
from typing import List
from fastapi import APIRouter
from fastapi import HTTPException, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DatabaseError

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


@router.post("/family")
async def create_family(post_family: schema.AddFamily, db: Session = Depends(get_db)):
    try:
        new_family = models.Family(**post_family.model_dump())
        db.add(new_family)
        db.commit()
        db.refresh(new_family)
        return [new_family]
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Couldn't Create Family"
        )
    except DatabaseError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error occured in DB"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {e}"
        )
    

@router.patch("/family/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schema.FamilyResponse)
async def update_family(id: int, payload: schema.FamilyBaseSchema, db: Session = Depends(get_db)):
    family = db.query(models.Family).filter(models.Family.id == id).first()
    if not family: 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f" No Family found with the given id: {id}"
        )
    try:
        update_data = payload.model_dump(exclude_unset=True)
        family.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(family)
        family_schema = schema.FamilyBaseSchema.model_validate(family)
        return schema.FamilyResponse(status=schema.Status.Success, Family=family_schema)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A Family with given details already exists.",
        ) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured while updating the Family."
        ) from e
    


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


@router.get("/product/{product_id}")
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
    products = await db.query(models.Product).all()
    return [{
        "id": product.id, 
        "name": product.name, 
        "family": product.family.name, 
        "price": product.price
        } for product in products
    ]

@router.put("/product/{product_id}")
async def update_product(update_data: schema.AddProduct, product_id: int, db: Session = Depends(get_db)):
    updated_product = db.query(models.Product).filter(models.Product.id == product_id)
    if updated_product.first() is None:
        raise HTTPException(status_code=404, detail=f"No product found for id: {product_id}")
    updated_product.update(update_data.model_dump(), synchronize_session=False)
    db.commit()
    return updated_product.first()

@router.get("/product/{product_id}/last_year_sales")
async def get_sales_last_year(product_id: int, db: Session = Depends(get_db)):
    today = datetime.today()
    last_year = today - timedelta(days=365)
    
    sales_sum = (
        db.query(func.sum(models.Sales.sales_amount))
        .filter(models.Sales.product_id == product_id)
        .filter(models.Sales.sales_date >= last_year)
        .scalar()
    )

    if sales_sum is None:
        raise HTTPException(status_code=404, detail="No Sales data found")
    return {"product_id": product_id, "total_last_year_sales": sales_sum}
