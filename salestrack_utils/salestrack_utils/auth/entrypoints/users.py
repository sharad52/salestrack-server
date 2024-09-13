import jwt
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import status, APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError, DatabaseError

from salestrack_utils.auth.schemas import schema
from salestrack_utils.auth.domain.models import User, Token
from salestrack_utils.auth.utils import jwt_utils
from salestrackapi.dbconfig.db_config import get_db
from salestrackapi.schemas.schema import Status as status_enum
# from salestrackapi.c import settings


router = APIRouter(prefix="/user", tags=["User"])

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


@router.post("/login", response_model=schema.TokenCreateResponse)
async def login(payload: schema.UserBaseSchema, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == payload.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No user found with this email")
        hashed_password = user.password
        if not jwt_utils.verify_password(payload.password, hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incorrect Password."
            )
        access_token = jwt_utils.create_access_token(data={"sub": user.id})
        refresh_token = jwt_utils.create_refresh_token(data={"sub": user.id})
        token_db = Token(
            user_id=user.id,
            access_token=access_token,
            refresh_token=refresh_token,
            status=True
        )
        db.add(token_db)
        db.commit()
        db.refresh(token_db)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Couldn't login")
    except DatabaseError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error Occur in DB.")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}")
    token_data = {
        "user_id": token_db.user_id,
        "access_token": token_db.access_token,
        "refresh_token": token_db.refresh_token,
        "status": token_db.status,
        "created_date": token_db.created_date
    }
    token_schema = schema.TokenCreateSchema.model_validate(token_data)
    return schema.TokenCreateResponse(Status=status_enum.Success, Token=token_schema)


@router.post('/logout')
async def logout(dependencies=Depends(jwt_utils.jwt_bearer), db: Session = Depends(get_db)):
    try:
        token = dependencies
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, settings.ALGORITHM)
        user_id = payload.get("sub")
        get_all_user_tokens = db.query(Token).all()
        info = []
        for each in get_all_user_tokens:
            if (datetime.now(timezone.utc) - each.created_date.replace(tzinfo=timezone.utc)).days > 1:
                info.append(each.user_id)
        if info: 
            existing_token = db.query(Token).where(Token.user_id.in_(info)).delete()
            db.commit()
        existing_token = db.query(Token).filter(Token.user_id == user_id, Token.access_token == token).first()
        if existing_token:
            existing_token.status=False
            db.add(existing_token)
            db.commit()
            db.refresh(existing_token)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}")

    return {
        "message": "Successfully Logout"
    }


@router.post("/change-password")
def change_password(payload: schema.ChangePaaswordBaseSchema, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == payload.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User not found.")
        if not jwt_utils.verify_password(payload.old_password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password doesnot match")
        hashed_password = jwt_utils.get_hashed_password(payload.new_password)
        user.password = hashed_password
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error: {e}")

    return {
        "message": "Your Password has been changes Successfully.", "success": True, "status_code": status.HTTP_200_OK
    }