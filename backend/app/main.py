from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import thumbnails
from app.api import auth 
from app.api import favorites

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(thumbnails.router)
app.include_router(auth.router, prefix = "/auth", tags=["auth"])
app.include_router(favorites.router)


@app.get("/")
async def read_root():
    return {"message" : "Thumbnail Studio API is running"}

