TORTOISE_ORM={
    "connections": {
        "default": {
            "engine": "tortoise.backends.mysql",#mysql引擎
            "credentials": {
                "host": "127.0.0.1",
                "port": "3306",
                "user": "root",
                "password": "123456",
                "database": "sp_task_test",
                "minsize": 1,
                "maxsize": 10,
                "charset": "utf8mb4",
                "echo": True
                }
            }
        },
    "apps": {
        "models": {
            "models": ["models", "aerich.models"],
            "default_connection": "default",
        }
    },
    "use_tz": False,
    "timezone": "Asia/Shanghai",
}