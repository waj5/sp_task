from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

# 模拟用户数据库
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "password": "123456",  # 仅用于演示，实际中请加密存储
    }
}

# 登录请求数据模型
class LoginRequest(BaseModel):
    username: str
    password: str

# 登录接口
@router.post("/login")
def login(request: LoginRequest):
    user = fake_users_db.get(request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    return {"message": "登录成功", "username": request.username}