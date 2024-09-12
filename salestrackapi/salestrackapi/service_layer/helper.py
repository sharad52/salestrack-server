from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, DatabaseError
from fastapi import status, Depends, HTTPException

from salestrackapifjf.schemas import schema
from salestrackapifjf.domain.models import Family, Product
from salestrackapifjf.dbconfig.db_config import get_db


async def create_family_in_db(payload: schema.FamilyBaseSchema, db: Session=Depends(get_db)):
    try:
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


async def create_product_in_db(payload: schema.ProductBaseSchema, db: Session = Depends(get_db)):
    try:
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