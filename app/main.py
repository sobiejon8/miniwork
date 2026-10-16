from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

@app.get("/")
async def root():
    return {"message": "MiniWork API muvaffaqiyatli ishga tushdi! 🚀"}