from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.database import login_user,init
import jwt
from datetime import datetime, timedelta
from backend.config import SECRET_KEY,ALGORITHM
router = APIRouter(prefix="/auth", tags=["Authentication"])


# 登录请求数据模型
class LoginRequest(BaseModel):
    username: str
    password: str

# 登录接口
@router.post("/login")
async def login(request: LoginRequest):
    await init()  # 初始化 Tortoise ORM

    # 从请求中获取用户名和密码
    username = request.username
    password = request.password

    # 调用登录用户的函数进行用户验证
    user = await login_user(username, password)

    # 检查用户是否存在以及密码是否匹配
    if user:
        token = jwt.encode({
            'user_id': str(user.id),
            'exp': datetime.utcnow() + timedelta(hours=1)  # Token 有效期 1 小时
        }, SECRET_KEY, algorithm=ALGORITHM)
        return {'token': token}
    else:
        return '登录失败'