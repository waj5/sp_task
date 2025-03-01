from tortoise.exceptions import DoesNotExist
from models import Master, Administered,Task
from tortoise import Tortoise
from tortoise_config import TORTOISE_ORM
from tortoise.expressions import Q


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



async def query_tasks_by_user_or_designee(user_id: str, designee_id: str):
    tasks = await Task.filter(Q(create_user_id=user_id) | Q(designee_id=designee_id)).all()
    return tasks