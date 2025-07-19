from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api import todos

app = FastAPI(title="Todo App", version="1.0.0")

# 프록시 헤더 처리를 위한 설정
app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["*"]
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록 - trailing slash 제거
app.include_router(todos.router, prefix="/api/todos", tags=["todos"])

# Static 파일 제공
app.mount("/static", StaticFiles(directory="static"), name="static")

# 루트 경로에서 index.html 제공
@app.get("/")
async def read_index():
    return FileResponse("templates/index.html")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}