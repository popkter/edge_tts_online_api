import asyncio
from time import sleep

import jwt
from datetime import datetime, timedelta, timezone

# 配置
SECRET_KEY = "your_secret_key"  # 用于签名的密钥
ALGORITHM = "HS256"  # 使用的加密算法
ACCESS_TOKEN_EXPIRE_MINUTES = 5  # Token 过期时间（分钟）

# 生成 Token 的函数
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # 添加过期时间
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")

async def main():
    payload = {"user_id": "123", "role": "admin"}
    token = create_access_token(payload)
    print("Generated Token:", token)
    sleep(6)
    try:
        decoded = decode_access_token(token)
        print("Decoded Payload:", decoded)
    except ValueError as e:
        print("Error:", str(e))

# 示例
if __name__ == '__main__':
    asyncio.run(main())
