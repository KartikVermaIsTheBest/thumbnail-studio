import asyncio
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.thumbnail import Thumbnail
from app.schemas.thumbnail import ThumbnailCreate, ThumbnailResponse
from app.services.image_service import generate_thumbnail_image
from app.services.storage_service import upload_image_to_storage
from app.core.security import get_current_user,can_view_thumbnail
from app.models.user import User
import httpx
from fastapi.responses import StreamingResponse
import io



router = APIRouter(prefix="/thumbnails", tags=["thumbnails"])


@router.post("/", response_model=ThumbnailResponse, status_code=status.HTTP_201_CREATED)
async def create_thumbnail(
    payload: ThumbnailCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        image_bytes = await generate_thumbnail_image(
            payload.prompt, payload.width, payload.height
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(e))

    image_url = await asyncio.to_thread(upload_image_to_storage, image_bytes)

    new_thumbnail = Thumbnail(
        user_id=current_user.id,
        prompt=payload.prompt,
        image_url=image_url,
        width=payload.width,
        height=payload.height,
    )
    db.add(new_thumbnail)
    await db.commit()
    await db.refresh(new_thumbnail)

    return new_thumbnail


@router.get("/", response_model = list[ThumbnailResponse])
async def list_my_thumbnails(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Thumbnail)
        .where(Thumbnail.user_id == current_user.id)
        .order_by(Thumbnail.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

@router.get("/{thumbnail_id}" , response_model = ThumbnailResponse)
async def get_thumbnail(
    thumbnail_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Thumbnail).where(Thumbnail.id == thumbnail_id))
    thumbnail = result.scalar_one_or_none()

    if thumbnail is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thumbnail not found")

    if not can_view_thumbnail(thumbnail, current_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thumbnail not found")

    return thumbnail


@router.get("/{thumbnail_id}/download")
async def download_thumbnail(
    thumbnail_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Thumbnail).where(Thumbnail.id == thumbnail_id))
    thumbnail = result.scalar_one_or_none()
    if thumbnail is None or not can_view_thumbnail(thumbnail, current_user):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Thumbnail not found")

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(thumbnail.image_url)

    return StreamingResponse(
        io.BytesIO(response.content),
        media_type="image/png",
        headers={"Content-Disposition": f"attachment; filename=thumbnail_{thumbnail_id}.png"},
    )