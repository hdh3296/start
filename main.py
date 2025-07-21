from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os

from app.api import todos

# 환경변수로 경로 prefix 설정
ROOT_PATH = os.getenv("ROOT_PATH", "/todo")

app = FastAPI(
    title="Todo App", 
    version="1.0.0",
    root_path=ROOT_PATH
)

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

# 루트 경로에서 index.html 제공 (경로 수정)
@app.get("/")
async def read_index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # 경로를 동적으로 변경
    html_content = html_content.replace('href="/static/', f'href="{ROOT_PATH}/static/')
    html_content = html_content.replace('src="/static/', f'src="{ROOT_PATH}/static/')
    
    return HTMLResponse(content=html_content)

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}