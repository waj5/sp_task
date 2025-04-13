import os,sys
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)
from config import DB_CONFIG
TORTOISE_ORM={
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",#mysql引擎
            "credentials": {
                "host": "127.0.0.1",
                "port": "3306",
                "user": "root",
                "password": DB_CONFIG["password"],
                "database": DB_CONFIG["name"],
                "minsize": 1,
                "maxsize": 10,
                "charset": "utf8mb4",
                "echo": True
                }
            }
        },
    "apps": {
        "models": {
            "models": ["backend.models.models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}
