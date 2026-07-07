from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from ai_template.models.database import User
from ai_template.models.engine import db_session
from ai_template.modules.auth.schema import LoginUser, RegisterUser
from ai_template.modules.auth.utils import hash_password, verify_password

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/register")
def register_user(body: RegisterUser, db: Session = Depends(db_session)):
    hashed_password = hash_password(plain_password=body.password)
    new_user = User(name=body.name, email=body.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User register success!"}


@auth_router.post("/login")
def login_user(body: LoginUser, db: Session = Depends(db_session)):
    user = db.exec(select(User).where(User.email == body.email)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials!",
        )
    if not verify_password(plain_password=body.password, hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials!",
        )
    return {"message": "User login success!"}
