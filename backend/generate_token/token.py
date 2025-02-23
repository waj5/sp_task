from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from backend.models import Master, Administered, Task
from backend.database import login_user, init

app = FastAPI()

# 密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 生成 JWT 令牌
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 验证用户
async def login_user(username: str, password: str):
    master_user = await Master.filter(username=username).first()
    if master_user and master_user.verify_password(password):
        return master_user

    administered_user = await Administered.filter(username=username).first()
    if administered_user and administered_user.verify_password(password):
        return administered_user

    return None

# 获取当前用户
async def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_type: str = payload.get("user_type")
        if username is None or user_type is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    if user_type == "Master":
        user = await Master.filter(username=username).first()
    elif user_type == "Administered":
        user = await Administered.filter(username=username).first()
    else:
        raise credentials_exception

    if user is None:
        raise credentials_exception
    return user

# 登录接口
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await login_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 根据用户类型生成 token
    if isinstance(user, Master):
        token = return_token(user, Master)
    elif isinstance(user, Administered):
        token = return_token(user, Administered)
    else:
        raise HTTPException(status_code=401, detail="Invalid user type")

    return {"access_token": token, "token_type": "bearer"}

# 获取用户任务的接口
@app.get("/tasks")
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