from tortoise.exceptions import DoesNotExist
from models import Master, Administered,Task
from tortoise import Tortoise
from tortoise_config import TORTOISE_ORM
from tortoise.expressions import Q
from fastapi  import HTTPException, status
from datetime import datetime

async def init():
    # 初始化 Tortoise ORM
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

async def login_user(username: str, password: str, is_master: bool = True):
    """
    根据用户名和密码登录用户。

    :param username: 用户名
    :param password: 用户输入的密码
    :param is_master: 是否为 Master 用户，默认为 True。如果为 False，则查询 Administered 用户。
    :return: 如果登录成功，返回用户对象；否则返回 None。
    """
    try:
        # 根据 is_master 参数决定查询 Master 还是 Administered
        user_model = Master if is_master else Administered

        # 查询用户
        user = await user_model.get(name=username)

        # 检查密码是否匹配
        if user.check_password(password):
            return user
        else:
            return None  # 密码不匹配
    except DoesNotExist:
        return None  # 用户不存在



#查询用户创建的任务
async def query_tasks_by_user_or_designee(user_id: str, designee_id: str):
    tasks = await Task.filter(Q(create_user_id=user_id) | Q(designee_id=designee_id)).all()
    return tasks

#获取指派者的 id
async def get_user_id_by_name(username: str):
    try:
        designee= await Administered.get(name=username)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="被指派者不存在"
        )
    return designee.id
async def get_designees_by_task(task_data,current_user_id):
    designee_id = await get_user_id_by_name(task_data.designee_name)
    task = await Task.create(
        title=task_data.title,
        content=task_data.content,
        create_user_id=current_user_id,  # 任务创建者
        designee_id=designee_id,  # 被指派者
        create_time=datetime.now(), # 创建时间
        complete_time=task_data.complete_time  # 完成时间（可选）
    )
    return task


#通过id查询任务
async def query_task_by_id(task_id):
    try:
        print("开始查询",task_id)
        task = await Task.get(id=task_id)
        print("查询", task)
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"任务ID {task_id} 不存在")
    return task

#更新任务
async def update_task(task_id: str, task_data):
    try:
        task = await Task.get(id=task_id)
        update_data = task_data.model_dump(exclude_unset=True)

        # 处理designee_name转换（如果存在）
        if 'designee_name' in update_data:
            designee_id = await get_user_id_by_name(update_data['designee_name'])
            update_data['designee_id'] = designee_id
            del update_data['designee_name']

        # 更新字段
        for key, value in update_data.items():
            setattr(task, key, value)

        task.create_time = datetime.now()  # 更新修改时间
        await task.save()
        return task
    except DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"任务ID {task_id} 不存在"
        )
