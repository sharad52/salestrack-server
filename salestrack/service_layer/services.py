import io
import csv
import pandas as pd
from datetime import datetime, timedelta
from typing import List
# from fastapi import HTTPException, Depends, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DatabaseError
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends, status


from salestrack.schemas import schema
from salestrack.domain import models
from salestrack.service_layer import helper
from salestrack.dbconfig.db_config import get_db
from auth.utils.jwt_utils import jwt_bearer, token_required


router = APIRouter(prefix="/sales", tags=["Sales"])


@token_required
@router.get("/family", response_model=List[schema.AddFamily])
async def list_family(
    db: Session = Depends(get_db)
):
    
    family = db.query(models.Family).all()
    return family


@token_required
@router.get("/family/{id}", status_code=status.HTTP_200_OK, response_model=schema.FamilyResponse)
async def get_family(id: int, db: Session = Depends(get_db)):
    family = db.query(models.Family).filter(models.Family.id == id).first()
    if not family:
        raise HTTPException(status_code=404, detail=f"No product found for id: {id}")
    family_schema = schema.FamilyBaseSchema.model_validate(family)
    return schema.FamilyResponse(Status=schema.Status.Success, Family=family_schema)


@token_required
@router.post("/family", status_code=status.HTTP_201_CREATED, response_model=schema.FamilyResponse)
async def create_family(post_family: schema.AddFamily, db: Session = Depends(get_db)):
    new_family = await helper.create_family_in_db(post_family, db)
    family_schema = schema.FamilyBaseSchema.model_validate(new_family)
    return schema.FamilyResponse(Status=schema.Status.Success, Family=family_schema)
    

@token_required
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


@token_required
@router.get("/product/{id}", status_code=status.HTTP_200_OK, response_model=schema.ProductResponse)
async def get_product(id: int, db: Session = Depends(get_db)):
    product_query = db.query(models.Product).filter(models.Product.id == id)
    product = product_query.first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No product found for id: {id}")
    product_schema = schema.ProductBaseSchema.model_validate(product)
    return schema.ProductResponse(Status=schema.Status.Success, Product=product_schema)


@token_required
@router.post("/product", status_code=status.HTTP_201_CREATED, response_model=schema.ProductResponse)
async def create_product(payload: schema.ProductBaseSchema, db: Session = Depends(get_db)):
    product = await helper.create_product_in_db(payload, db)
    product_schema = schema.ProductBaseSchema.model_validate(product)
    return schema.ProductResponse(Status=schema.Status.Success, Product=product_schema)


@token_required
@router.patch("/product/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=schema.ProductResponse)
async def update_product(id: int, payload: schema.UpdateProductSchema, db: Session = Depends(get_db)):
    product_query = db.query(models.Product).filter(models.Product.id == id).first()
    if not product_query:
        raise HTTPException(status_code=404, detail=f"No product found for id: {id}")
    try:
        data = payload.model_dump(exclude_unset=True)
        for key, value in data.items():
            setattr(product_query, key, value)
        db.add(product_query)
        db.commit()
        db.refresh(product_query)
        product_schema = schema.ProductBaseSchema.model_validate(product_query)
        return schema.ProductResponse(Status=schema.Status.Success, Product=product_schema)
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A Product with the given details already exist"
        ) from e
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured while updating product."
        ) from e
    

@token_required
@router.post("/load-data")
async def load_data(type: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = file.file.read()
    data = io.BytesIO(contents)
    df = pd.read_excel(data, engine='openpyxl')
    for index, row in df.iterrows():
        # process excel data for db
        family_name = row.get("Family")
        # if family_name:
        family = db.query(models.Family).filter(models.Family.name == family_name).first()
        if not family:
            new_family_data = {"name": family_name}
            family = await helper.create_family_in_db(schema.FamilyBaseSchema(**new_family_data), db)
        # product 
        family_id = family.Family.id if isinstance(family, schema.FamilyResponse) else family.id
        product_name = row.get("Product Name")
        product_id = int(row.get("Product ID"))
        price = float(row.get("Price"))

        # if product_id:
        product = db.query(models.Product).filter(models.Product.name == product_name).first()
        if not product:
            new_product_data = {"id": product_id, "name": product_name, "family_id": family_id, "price": price}
            product = await helper.create_product_in_db(schema.ProductBaseSchema(**new_product_data), db)

        # Sales
        sales_dates = [date for date in df.columns if isinstance(date, datetime)]
        for each in sales_dates:
            product_id = product.Product.id if isinstance(product, schema.ProductResponse) else product.id
            month_wise_sales = db.query(models.Sales).filter(
                (models.Sales.sales_date == each) & (models.Sales.product_id == product_id)
            ).first()
            if not month_wise_sales:
                sales_data = {
                    "product_id": product_id, 
                    "sales_date": each, 
                    "sales_amount": int(row.get(each))
                }
                month_wise_sales = models.Sales(**sales_data)
                db.add(month_wise_sales)
                db.commit()
                db.refresh(month_wise_sales)
    data.close()
    file.file.close()
    return {
        "Status": schema.Status.Success,
        "status_code": status.HTTP_201_CREATED,
        "message": "excel data loaded successfully"
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
