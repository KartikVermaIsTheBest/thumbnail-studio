from pydantic import BaseModel
from datetime import datetime

class ThumbnailCreate(BaseModel):
    prompt: str
    width: int = 1280
    height: int = 720


class ThumbnailResponse(BaseModel):
    id: int
    prompt: str
    image_url: str
    width: int
    height: int
    is_public: bool
    created_at: datetime


    class Config:
        from_attributes = True