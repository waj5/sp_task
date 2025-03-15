from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, task
from backend.tortoise_config import TORTOISE_ORM
from tortoise import Tortoise
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时初始化
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
    yield
    # 应用关闭时清理
    await Tortoise.close_connections()

app = FastAPI(lifespan=lifespan)

# 正确配置 CORS
app.add_middleware(
    CORSMiddleware,  # 直接传递类
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(task.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI backend!"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
