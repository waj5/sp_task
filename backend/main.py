from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth
import uvicorn

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源（生产环境建议限制为特定域名）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)


# 注册路由
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI backend!"}

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)