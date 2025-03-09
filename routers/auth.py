from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pydantic.v1 import validator

from backend.database import login_user, init, create_user
import jwt
from datetime import datetime, timedelta
from backend.config import SECRET_KEY, ALGORITHM
router = APIRouter(prefix="/auth", tags=["Authentication"])


# 登录请求数据模型
class LoginRequest(BaseModel):
    username: str
    password: str

# 用户创建请求数据模型
class UserCreate(BaseModel):
    name: str
    password: str
    email: str
    is_admin: bool = True
    sex: str = "未知"  # 默认值为“未知”
    age: int = 0  # 默认值为0

    @validator('sex')
    def validate_sex(cls, v):
        if v is None:  # 如果没有传值，不进行校验
            return v
        if v not in ["男", "女", "未知"]:
            raise ValueError('性别必须是“男”、“女”或“未知”')
        return v

    @validator('age')
    def validate_age(cls, v):
        if v is None:  # 如果没有传值，不进行校验
            return v
        if v < 0 or v > 150:
            raise ValueError('年龄必须在0到150之间')
        return v

# 登录接口
@router.post("/login")
async def login(request: LoginRequest):
    # await init()  # 初始化 Tortoise ORM
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

# 注册接口
@router.post("/register")
async def register(user: UserCreate):
    try:
        # 调用 create_user 函数创建用户
        new_user = await create_user(user.name, user.password, user.email, user.is_admin)
        return {"message": "用户注册成功", "user_id": str(new_user.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))