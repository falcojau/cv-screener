from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.upload import router as upload_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="CV Screener API",
    description="API for receiving and processing CVs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")

@app.get("/")
def root():
    return {"status": "CV Screener API running"}