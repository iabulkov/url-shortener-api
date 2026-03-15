import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app/app'))

try:
    from main import app
    print("Successfully imported app from app/app/main.py")
except ImportError as e:
    print(f"Import error: {e}")
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {
            "message": "URL Shortener API",
            "status": "working",
            "note": "Using fallback app - fix import path"
        }
    
    @app.get("/links/test")
    async def test():
        return {"message": "Test endpoint"}