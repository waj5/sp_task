import secrets
import platform
# 生成一个 32 字节的随机字符串作为 SECRET_KEY
SECRET_KEY = "your-fixed-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if platform.system() == "Windows":
    DB_CONFIG={
        "name":"sp_task_test",
        "password":"123456"
    }
else:
    DB_CONFIG={
        "name":"sp_task",
        "password":"Wangai@163.com"
    }