TORTOISE_ORM={
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",#mysql引擎
            "credentials": {
                "host": "127.0.0.1",
                "port": "3306",
                "user": "root",
                "password": "Wangai@163.com",
                "database": "sp_task",
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
