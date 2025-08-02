# 代码生成时间: 2025-08-03 03:24:49
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from zipfile import ZipFile, BadZipFile
from io import BytesIO
import os
import shutil

app = FastAPI()

class UnzipRequest(BaseModel):
    file: UploadFile  # Pydantic模型，用于接收上传的文件

# 错误处理和文档生成
@app.exception_handler(BadZipFile)
async def bad_zip_file_exception_handler(request, exc):
    return JSONResponse(
        content={"detail": "Bad zip file provided"},
        status_code=status.HTTP_400_BAD_REQUEST
    )

@app.post("/unzip")
async def unzip(file: UnzipRequest):
    # 错误处理
    try:
        # 读取上传的zip文件
        zip_file = await file.file.read()
        zip_content = BytesIO(zip_file)
        
        # 解压文件
        with ZipFile(zip_content, 'r') as zip_ref:
            zip_ref.extractall(path="./extracted_files")
            
        # 返回成功消息
        return {"message": "Files have been successfully extracted."}
    except BadZipFile:
        # 如果文件不是zip格式，抛出异常
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad zip file provided.")
    except Exception as e:
        # 其他异常
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 测试端点
@app.post("/test")
async def test():
    return {"message": "Hello World"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)