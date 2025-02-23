from tortoise.exceptions import DoesNotExist
from models import Master, Administered
from tortoise import Tortoise
from tortoise_config import TORTOISE_ORM

async def init():
    # 初始化 Tortoise ORM
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()

async def login_user(username: str, password: str, is_master: bool = True):
    """
    改进版登录验证函数（直接返回用户对象或None）
    """
    try:
        user_model = Master if is_master else Administered
        user = await user_model.get(name=username)
        if user.check_password(password):
            return user
        return None
    except DoesNotExist:
        return None