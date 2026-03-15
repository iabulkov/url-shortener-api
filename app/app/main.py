from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, links

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="URL Shortener API",
    description="Сервис для сокращения ссылок",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(links.router)

@app.get("/{short_code}")
async def root_redirect(short_code: str):
    from app.routers.links import redirect_to_original
    from app.database import get_db
    db = next(get_db())
    return await redirect_to_original(short_code, db)

@app.get("/")
async def root():
    return {
        "message": "URL Shortener API",
        "docs": "/docs"
    }