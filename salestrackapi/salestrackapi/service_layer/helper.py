from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DatabaseError
from fastapi import Request, HTTPException

from salestrackapi.schemas import schema
from salestrackapi.domain.models import Family, Product


async def create_family_in_db(request: Request, payload: schema.FamilyBaseSchema):
    try:
        db = request.app.state.db
        new_family = Family(**payload.model_dump())
        db.add(new_family)
        db.commit()
        db.refresh(new_family)
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
    return new_family


async def create_product_in_db(request: Request, payload: schema.ProductBaseSchema):
    try:
        db = request.app.state.db
        product = db.query(Product).filter(Product.name == payload.name).first()
        if not product:
            product = Product(**payload.model_dump())
            db.add(product)
            db.commit()
            db.refresh(product)

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
    return product