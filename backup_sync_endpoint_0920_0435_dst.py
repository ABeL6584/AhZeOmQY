# 代码生成时间: 2025-09-20 04:35:17
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import shutil
import os

# Pydantic模型定义
class BackupSyncSettings(BaseModel):
    source_path: str = Field(..., description="The source directory path")
    destination_path: str = Field(..., description="The destination directory path")
    backup: bool = Field(default=False, description="Whether to backup before syncing")

# FastAPI应用实例
app = FastAPI()

# 文件备份和同步端点
@app.post("/backup_sync/")
async def backup_sync(settings: BackupSyncSettings):
    # 错误处理
    try:
        # 检查源路径是否存在
        if not os.path.exists(settings.source_path):
            raise HTTPException(status_code=404, detail="Source path does not exist")
        
        # 检查目标路径是否存在
        if not os.path.exists(settings.destination_path):
            os.makedirs(settings.destination_path)
    
        # 备份（如果需要）
        if settings.backup:
            backup_destination = settings.destination_path + "_backup"
            shutil.copytree(settings.source_path, backup_destination)
        
        # 同步文件
        for item in os.listdir(settings.source_path):
            source = os.path.join(settings.source_path, item)
            destination = os.path.join(settings.destination_path, item)
            if os.path.isdir(source):
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
        
        return {"message": "Backup and sync completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Swagger UI和ReDoc
@app.get("/docs")
def get_documentation():
    return {"message": "Redirect to /docs for API documentation"}

@app.get("/redoc")
def get_redoc():
    return {"message": "Redirect to /redoc for API documentation"}
