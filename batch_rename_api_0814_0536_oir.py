# 代码生成时间: 2025-08-14 05:36:15
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import shutil

# Pydantic模型定义
class RenameItem(BaseModel):
    filename: str
    newname: str

# 创建FastAPI实例
app = FastAPI()

# 端点：批量文件重命名
@app.post("/rename/")
async def rename_files(items: list[RenameItem]) -> JSONResponse:
    # 错误处理
    try:
        # 遍历文件列表进行重命名
        for item in items:
            old_path = os.path.join("./", item.filename)
            new_path = os.path.join("./", item.newname)
            # 检查文件是否存在
            if not os.path.exists(old_path):
                return JSONResponse(status_code=404, content={"message": f"File {item.filename} not found"})
            # 检查新文件名是否被占用
            if os.path.exists(new_path):
                return JSONResponse(status_code=409, content={"message": f"File {item.newname} already exists"})
            # 重命名文件
            shutil.move(old_path, new_path)
        # 返回成功信息
        return JSONResponse(status_code=200, content={"message": "Files renamed successfully"})
    except Exception as e:
        # 通用错误处理
        return JSONResponse(status_code=500, content={"message": str(e)})

# 可以添加额外的路由和逻辑以满足额外的需求

# 如果需要能够上传文件并重命名，可以添加如下端点
@app.post("/upload_and_rename/")
async def upload_and_rename(file: UploadFile = File(...)) -> JSONResponse:
    # 保存文件
    try:
        file_location = f"./{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file.file.close()
        # 重命名文件
        new_filename = "new_file.txt"
        new_file_location = f"./{new_filename}"
        shutil.move(file_location, new_file_location)
        return JSONResponse(status_code=200, content={"message": "File uploaded and renamed successfully"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


# 启动服务后，访问http://localhost:8000/docs 可以查看API文档

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)