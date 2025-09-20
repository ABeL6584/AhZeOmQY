# 代码生成时间: 2025-09-21 07:02:37
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
from typing import Optional
from fastapi.encoders import jsonable_encoder

app = FastAPI()

# Pydantic模型定义
class Document(BaseModel):
    content: str
    target_format: str
    optional_metadata: Optional[dict] = None

# 错误处理
@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    detail = jsonable_encoder({'detail': exc.errors(), 'model': 'Document'})
    return JSONResponse(content=detail, status_code=HTTPException.status_code)

# 转换文档格式的端点
@app.post("/convert")
async def convert_document(document: Document):
    try:
        # 这里模拟文档转换逻辑
        # 真实应用中应替换为实际的文档转换代码
        converted_document = f"Converted content in {document.target_format}"
        return {"content": converted_document, "source": document.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# FastAPI文档
@app.get("/docs")
async def read_docs():
    return "API Documentation is available at /docs"