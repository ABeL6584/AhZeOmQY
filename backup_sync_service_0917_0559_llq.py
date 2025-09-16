# 代码生成时间: 2025-09-17 05:59:52
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import shutil
import os

# Pydantic模型用于解析请求数据
class BackupSyncRequest(BaseModel):
    src: str
    dest: str
    recursive: Optional[bool] = True

# 初始化FastAPI应用
app = FastAPI()

# 文件备份和同步的端点
@app.post("/backup_sync/")
async def backup_sync(file: UploadFile = File(...), request: BackupSyncRequest):
    # 检查源和目标路径
    if not os.path.exists(request.src):
        return JSONResponse(
            status_code=404,
            content={"message": f"Source path '{request.src}' does not exist"}
        )
    if not os.path.exists(os.path.dirname(request.dest)):
        return JSONResponse(
            status_code=404,
            content={"message": f"Destination path '{request.dest}' does not exist"}
        )

    try:
        # 备份和同步文件
        if request.recursive:
            shutil.copytree(request.src, request.dest)
        else:
            shutil.copy(request.src, request.dest)
        return {"message": "Backup and sync completed successfully"}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"An error occurred: {str(e)}"}
        )

# 错误处理
@app.exception_handler(404)
async def not_found_exception(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Not found"}
    )

@app.exception_handler(500)
async def internal_server_error_exception(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

# 启动FastAPI应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)