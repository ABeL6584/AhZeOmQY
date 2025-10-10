# 代码生成时间: 2025-10-10 18:02:54
from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
from typing import Optional
import requests
from bs4 import BeautifulSoup


# Pydantic模型定义
class ScrapeRequest(BaseModel):
    url: str
    element: str
    attribute: Optional[str] = None

# FastAPI应用
app = FastAPI()

# 路由
router = APIRouter()

@router.post("/scraper")
async def scrape_website(request: ScrapeRequest):
    # 错误处理
    try:
        # 发起HTTP请求
        response = requests.get(request.url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    # 解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    element = soup.select_one(request.element)
    if not element:
        raise HTTPException(status_code=404, detail=f"Element {request.element} not found")

    # 根据属性返回内容
    if request.attribute:
        return {request.attribute: element.get(request.attribute)}
    else:
        return {
            "text": element.get_text()
        }

# 将路由添加到FastAPI应用中
app.include_router(router)

# FastAPI将自动生成API文档，无需额外代码
