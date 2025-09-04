# 代码生成时间: 2025-09-04 21:09:11
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from pydantic import BaseModel
import zipfile
import shutil
import os

# Pydantic模型用于接收文件
class FileUpload(BaseModel):
    file: UploadFile  # 压缩文件上传
    
# 创建FastAPI实例
app = FastAPI()

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# 解压文件的端点
@app.post("/unzip")
async def unzip_file(upload: FileUpload):
    # 检查文件是否为ZIP格式
    if not upload.file.filename.endswith(".zip"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only ZIP files are allowed")
        
    try:
        # 临时保存ZIP文件
        temp_zip_path = f"temp/{upload.file.filename}"
        with open(temp_zip_path, "wb") as buffer:
            shutil.copyfileobj(upload.file.file, buffer)
        
        # 解压文件
        with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
            zip_ref.extractall("extracted_files")
        
        # 删除临时ZIP文件
        os.remove(temp_zip_path)
        
        return {"message": "File was successfully unzipped."}
    except zipfile.BadZipFile:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The file is not a zip file or it is corrupted.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 依赖注入用于文件上传
def file_upload(file: UploadFile = File(...)):
    return FileUpload(file=file)
