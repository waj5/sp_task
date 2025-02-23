import secrets

# 生成一个 32 字节的随机字符串作为 SECRET_KEY
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30