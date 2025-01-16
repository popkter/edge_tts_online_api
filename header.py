import uvicorn
from fastapi import FastAPI, Header, HTTPException, Query, Depends
from pydantic import BaseModel

app = FastAPI()


# 定义 GET 请求的查询参数模型
class QueryParams(BaseModel):
    param1: str
    param2: int
    param3: str = "default_value"  # 带默认值的参数


# 校验 Header 的依赖函数
def get_authorization_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")

    # 检查格式是否正确
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization format")

    # 提取 Token
    token = authorization[7:]  # 去掉 "Bearer " 前缀
    return token


# 定义 GET 请求处理逻辑
@app.get("/secure-data/")
async def secure_data(
        token: str = Depends(get_authorization_token),  # Header 校验
        params: QueryParams = Depends()  # 解析查询参数
):
    return {
        "message": "Access granted",
        "token": token,
        "params": params.model_dump(),  # 将查询参数转为字典
    }

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8080)