# 代码生成时间: 2025-08-07 15:54:20
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import pandas as pd
# 添加错误处理
import xlsxwriter
import io


# Pydantic模型定义
class ExcelData(BaseModel):
    column_names: List[str]
    rows: List[List[str]]


# FastAPI实例化
app = FastAPI()


# 错误处理装饰器
async def validation_decorator(func):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            return JSONResponse(status_code=400, content=f"{{"error": "{str(e)}"}}\)
    return wrapper



# Excel自动生成器端点
@app.post("/generate-excel")
@validation_decorator
async def generate_excel(data: ExcelData):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {
        "in_memory": True
    })
    worksheet = workbook.add_worksheet()
    worksheet.write_row(0, 0, data.column_names)
    for i, row in enumerate(data.rows, start=1):
        worksheet.write_row(i, 0, row)
    workbook.close()
# 添加错误处理
    output.seek(0)
    output_name = "generated_excel.xlsx"
    headers = {
        "Content-Disposition": f"attachment; filename={output_name}"
    }
    return File(output, filename=output_name), headers
# 增强安全性


# Swagger UI 设置
app.include_router(
    fastapi.security.docs.get_docs_router(),
# FIXME: 处理边界情况
    prefix="/docs",
    tags=["Documentation"],
)
app.include_router(
    fastapi.security.redoc.get_redoc_router(),
    prefix="/redoc",
    tags=["Documentation"],
)


# 错误处理
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(status_code=500, content=f"{{"error": "Internal Server Error"}}\)

# FastAPI最佳实践
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# 扩展功能模块