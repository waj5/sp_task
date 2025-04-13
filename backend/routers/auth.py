from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from typing import Optional
import os,sys

from backend.app.main import project_dir

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(os.path.abspath(current_dir))
sys.path.append(project_dir)
from backend.database.database import login_user, init, create_user
import jwt
from datetime import datetime, timedelta
from backend.config.config import SECRET_KEY, ALGORITHM
import re
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
    is_master: bool
    master_id: Optional[str] = None

    @field_validator('email')
    def validate_email(cls, v):
        if not re.match(r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$', v):
            raise ValueError('无效邮箱格式')
        return v

    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('密码至少8位')
        if not any(c.isupper() for c in v):
            raise ValueError('需要大写字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('需要数字')
        return v

    @field_validator('master_id')
    def validate_master_id(cls, v, values):
        if not values.data.get('is_master') and not v:
            raise ValueError('普通用户需指定管理员ID')
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
# 修改注册接口实现
@router.post("/register", status_code=201)
async def register(user: UserCreate):
    try:
        new_user = await create_user(
            username=user.name,
            password=user.password,
            email=user.email,
            is_master=user.is_master,
            master_id=user.master_id
        )
        return {
            "message": "注册成功",
            "user_id": str(new_user.id),
            "username": new_user.name,
            "role": "管理员" if user.is_master else "普通用户"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"服务器错误: {str(e)}"
        )