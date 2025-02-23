from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from backend.database import login_user,init
from backend.generate_token.token import return_token,get_current_user
from backend.models import Master,Administered,Task
router = APIRouter(prefix="/auth", tags=["Authentication"])

# 登录请求数据模型
class LoginRequest(BaseModel):
    username: str
    password: str

# 登录接口
@router.post("/login")
async def login(request: LoginRequest):
    await init()  # 确保 ORM 已初始化

    # 调用登录验证函数
    user = await login_user(request.username, request.password)

    if not user:
        # 统一返回模糊错误提示（安全考虑）
        raise HTTPException(status_code=401, detail="用户名或密码错误")

    # 根据用户类型生成 token
    if isinstance(user, Master):
        token = return_token(user, Master)
    elif isinstance(user, Administered):
        token = return_token(user, Administered)
    else:
        raise HTTPException(status_code=401, detail="无效的用户类型")

    return {"message": "登录成功", "username": request.username, "token": token}

@router.get("/tasks")
async def get_tasks(current_user: Master = Depends(get_current_user)):
    """
    根据当前登录用户查询任务
    """
    if isinstance(current_user, Master):
        # 查询 Master 用户创建的任务
        tasks = await Task.filter(create_user_id=current_user.id).all()
        return tasks
    elif isinstance(current_user, Administered):
        # 查询 Administered 用户被指派的任务
        tasks = await Task.filter(designee_id=current_user.id).all()
        return tasks
    else:
        raise HTTPException(status_code=403, detail="无权访问任务")