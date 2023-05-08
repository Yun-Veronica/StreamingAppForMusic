from fastapi import FastAPI
from src.streaming.routers import genres, musician, playlist, tracks
from src.auth.routers import router as user_router
# from pagination import router as pagination_router

app = FastAPI()

# app.include_router(pagination_router)
app.include_router(genres.router)
app.include_router(musician.router)
app.include_router(playlist.router)
app.include_router(tracks.router)
app.include_router(user_router)
