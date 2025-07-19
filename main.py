from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api import todos

app = FastAPI(title="Todo App", version="1.0.0")

# CORS $ (`���@ ��D t)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #  X��� �� origin ȩ
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API |�0 �]
app.include_router(todos.router, prefix="/api/todos", tags=["todos"])

# Static | Y
app.mount("/static", StaticFiles(directory="static"), name="static")

# � �\� index.html X
@app.get("/")
async def read_index():
    return FileResponse("templates/index.html")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}