from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate , UserResponse, UserLogin
from app.core.security import hash_password, verify_password, create_access_token
from app.core.security import get_current_user

router = APIRouter()


@router.post("/register", response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_in.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code = status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    new_user = User(
        name = user_in.name,
        email=user_in.email,
        hashed_password=hash_password(user_in.password)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user


@router.post("/login")
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == credentials.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(credentials.password , user.hashed_password):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
        )

    access_token = create_access_token(data={"sub" : str(user.id)})
    return {"access_token": access_token, "token_type":"bearer"}


@router.get("/me" , response_model = UserResponse)
async def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user