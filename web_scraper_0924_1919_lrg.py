# 代码生成时间: 2025-09-24 19:19:26
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests
from bs4 import BeautifulSoup
import re


# Pydantic模型
# 增强安全性
class ScrapeRequest(BaseModel):
# 添加错误处理
    url: str

app = FastAPI()

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )
# 添加错误处理

# FastAPI端点
@app.post("/scraper")
async def scrape(request: ScrapeRequest):
    """网页内容抓取工具
    
    Args:
        request (ScrapeRequest): Pydantic模型，包含URL
    
    Returns:
        str: 网页内容
    
    Raises:
        HTTPException: 如果请求无效或网页抓取失败
    """
    try:
        # 发送HTTP请求
        response = requests.get(request.url)
# 添加错误处理
        response.raise_for_status()  # 检查请求是否成功
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"请求失败：{e}")
    try:
        # 解析网页内容
        soup = BeautifulSoup(response.text, "html.parser")
        # 使用正则表达式移除HTML标签
        text = re.sub("<[^>]*>", "", str(soup))
        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"网页抓取失败：{e}")
