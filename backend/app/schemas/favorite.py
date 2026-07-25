from pydantic import BaseModel
from datetime import datetime

class FavoriteResponse(BaseModel):
    id: int
    thumbnail_id: int
    favorited_at: datetime

    class config:
        from_attributes: True