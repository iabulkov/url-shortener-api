import sys
import os

print("=== Current directory contents ===")
print(os.listdir('.'))

print("\n=== Parent directory contents ===")
print(os.listdir('..'))

print("\n=== Python path ===")
for path in sys.path:
    print(path)

print("\n=== Trying to import ===")
try:
    from main import app
    print("✅ Successfully imported app from main")
except ImportError as e:
    print(f"❌ Import error: {e}")
    # Пробуем найти main.py
    print("\n=== Searching for main.py ===")
    for root, dirs, files in os.walk('.'):
        if 'main.py' in files:
            print(f"Found main.py in: {root}")
    
    # Если ничего не нашли, создадим простой fallback
    from fastapi import FastAPI
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {"message": "Fallback app - main.py not found", "cwd": os.getcwd(), "files": os.listdir('.')}
    
    print("✅ Created fallback app")