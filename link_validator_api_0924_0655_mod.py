# 代码生成时间: 2025-09-24 06:55:04
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, validator
from urllib.parse import urlparse
import requests


# Pydantic模型用于数据验证
class Link(BaseModel):
    url: str

    # 确保URL格式正确
    @validator("url")
    def validate_url(cls, value):
        try:
            result = urlparse(value)
            assert all([result.scheme, result.netloc])
            return value
        except:
            raise ValueError("Invalid URL")


app = FastAPI()

# 端点实现URL链接有效性验证
@app.post("/validate")
async def validate_link(link: Link):
    # 尝试请求URL以验证其有效性
    try:
        response = requests.head(link.url, timeout=5)
        if response.status_code == 200:
            return {"message": "The URL is valid."}
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"URL is not accessible, status code: {response.status_code}"
            )
    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error occurred while accessing the URL: {str(e)}"
        )

# 错误处理
@app.exception_handler(ValueError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": exc.args[0]}
    )

# 启动FastAPI应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)