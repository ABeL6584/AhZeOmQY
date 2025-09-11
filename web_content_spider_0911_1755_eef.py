# 代码生成时间: 2025-09-11 17:55:23
from fastapi import FastAPI, HTTPException, Request, Form
from pydantic import BaseModel
from typing import Optional
import requests
from bs4 import BeautifulSoup

# Pydantic模型定义
class URL(BaseModel):
    url: str

# 创建FastAPI Web应用
app = FastAPI()

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

# FastAPI端点实现网页内容抓取
@app.post("/fetch-content/")
async def fetch_content(url: URL):
    # 检查URL的有效性
    if not url.url.startswith("http"):
        raise HTTPException(status_code=400, detail="URL must start with 'http'")
    try:
        response = requests.get(url.url)
        response.raise_for_status()  # 如果响应状态码不是200，抛出HTTPException
        soup = BeautifulSoup(response.text, 'html.parser')
        # 这里可以根据需要提取网页内容，例如提取标题
        title = soup.title.string if soup.title else "No title found"
        return {"url": url.url, "title": title}
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

# 运行以下代码启动服务器
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)