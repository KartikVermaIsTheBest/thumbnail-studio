from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.db.database import get_db
from app.models.favorite import Favorite
from app.models.thumbnail import Thumbnail
from app.schemas.favorite import FavoriteResponse
from app.core.security import get_current_user,can_view_thumbnail
from app.models.user import User

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.post("/{thumbnail_id}", response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
async def add_favorite(
    thumbnail_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Thumbnail).where(Thumbnail.id == thumbnail_id))
    thumbnail = result.scalar_one_or_none()
    if thumbnail is None or not can_view_thumbnail(thumbnail, current_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thumbnail not found")

    new_favorite = Favorite(user_id=current_user.id, thumbnail_id=thumbnail_id)
    db.add(new_favorite)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already favorited")

    await db.refresh(new_favorite)
    return new_favorite


@router.delete("/{thumbnail_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_favorite(
    thumbnail_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Favorite).where(
            Favorite.user_id == current_user.id, Favorite.thumbnail_id == thumbnail_id
        )
    )
    favorite = result.scalar_one_or_none()
    if favorite is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Favorite not found")

    await db.delete(favorite)
    await db.commit()


@router.get("/", response_model=list[FavoriteResponse])
async def list_favorites(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Favorite).where(Favorite.user_id == current_user.id))
    return result.scalars().all()