
from sqlalchemy.orm import Session
from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, DatabaseError

from auth.schemas import schema
from auth.domain.models import User
from auth.utils import jwt_utils
from salestrack.dbconfig.db_config import get_db
from salestrack.schemas.schema import Status as status_enum


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schema.UserResponse)
async def create_user(payload: schema.UserBaseSchema, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter_by(email=payload.email).first()
        if existing_user:
            raise HTTPException(status_code=201, detail=f"The User with this email: {payload.email} is already registered.")
        hashed_password = jwt_utils.get_hashed_password(payload.password)
        user = User(
            email=payload.email,
            password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Couldn't signup user.")
    except DatabaseError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error Occur in DB.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}")
    user_schema = schema.UserBaseSchema.model_validate(user)
    return schema.UserResponse(Status=status_enum.Success, User=user_schema)