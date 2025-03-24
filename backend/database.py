from tortoise.exceptions import DoesNotExist
from models import Master, Administered, Task, User  # 新增User模型导入
from tortoise import Tortoise
from tortoise_config import TORTOISE_ORM
from tortoise.expressions import Q
from fastapi import HTTPException, status
from datetime import datetime
from uuid import UUID


async def init():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()


async def login_user(username: str, password: str):
    """支持所有用户类型的登录验证"""
    user = await User.get_or_none(name=username)
    if user and user.check_password(password):
        return user
    return None

async def check_user_exists(username: str, email: str) -> bool:
    """检查用户名或邮箱是否已存在"""
    return await User.filter(Q(name=username) | Q(email=email)).exists()


async def create_user(username: str, password: str, email: str, is_admin: bool = False) -> User:
    """创建用户（带完整校验）"""
    # 存在性检查
    if await check_user_exists(username, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名或邮箱已被使用"
        )

    # 密码复杂度检查
    if len(password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="密码长度至少8位"
        )

    try:
        user = User(
            name=username,
            email=email,
            is_admin=is_admin,
            role='user'  # 默认角色
        )
        user.set_password(password)
        await user.save()
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"用户创建失败: {str(e)}"
        )

async def delete_user(user_id: str, is_master: bool = True):
    user = await User.get(id=user_id)
    await user.delete()

async def update_user(user_id: str, update_data: dict, is_master: bool = True):
    user = await User.get(id=user_id)
    for key, value in update_data.items():
        setattr(user, key, value)
    await user.save()
    return user

async def get_user(user_id: str, is_master: bool = True):
    return await User.get(id=user_id)

async def get_user_id_by_name(username: str):
    """支持查询所有用户类型"""
    user = await User.get_or_none(name=username)
    if user:
        return user.id
    raise HTTPException(status_code=404, detail="用户不存在")

async def get_designees_by_task(task_data, current_user_id):
    try:
        current_user = await User.get(id=current_user_id)
    except DoesNotExist:
        raise HTTPException(status_code=403, detail="用户不存在")

    designee = await User.get_or_none(name=task_data.designee_name)
    if not designee:
        raise HTTPException(status_code=403, detail="指派用户不存在")

    return await Task.create(
        title=task_data.title,
        content=task_data.content,
        creator=current_user,
        designee=designee,
        status=task_data.status if hasattr(task_data, 'status') else '未完成',  # 直接访问属性
        complete_time=task_data.complete_time
    )


# 通过id查询任务
async def query_task_by_id(task_id):
    try:
        print("开始查询", task_id)
        task = await Task.get(id=task_id)
        print("查询", task)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"任务ID {task_id} 不存在")
    return task

# 更新任务
async def update_task(task_id: str, task_data, current_user_id: str):
    try:
        task = await Task.get(id=task_id).prefetch_related("creator", "designee")
        current_user = await User.get(id=current_user_id)

        # 权限验证
        if (str(task.creator_id) != current_user_id
            and str(task.designee_id) != current_user_id
            and not current_user.is_admin):
            raise HTTPException(403, "无权限修改此任务")

        # 数据转换
        update_data = task_data if isinstance(task_data, dict) else task_data.model_dump(exclude_unset=True)

        # 字段验证
        valid_fields = {'title', 'content', 'status', 'designee_id', 'complete_time'}
        if any(key not in valid_fields for key in update_data):
            raise HTTPException(400, detail="包含无效字段")

        # 状态自动更新逻辑
        if 'complete_time' in update_data:
            update_data['status'] = "已完成"

        # 更新字段
        for key, value in update_data.items():
            setattr(task, key, value)

        task.update_time = datetime.now()
        await task.save()
        return task
    except DoesNotExist:
        raise HTTPException(404, detail=f"任务ID {task_id} 不存在")
    except Exception as e:
        raise HTTPException(500, detail=str(e))

# 删除任务
async def delete_task(task_id: str, current_user_id: str):
    try:
        task = await Task.get(id=task_id).prefetch_related("creator")

        # 权限验证
        if str(task.creator_id) != current_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="无权限删除此任务"
            )

        await task.delete()
        return True
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"任务ID {task_id} 不存在"
        )

# 新增：模糊查询任务
async def query_tasks_fuzzy(query_str: str):
    tasks = await Task.filter(
        Q(title__icontains=query_str) | Q(id__icontains=query_str)
    ).all()
    return tasks

async def query_tasks_by_user_or_designee(user_id: str, designee_id: str):
    """查询与用户或指派者相关的任务"""
    tasks = await Task.filter(
        Q(creator_id=user_id) | Q(designee_id=designee_id)
    ).prefetch_related("creator", "designee")
    return tasks
