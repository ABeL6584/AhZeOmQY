# 代码生成时间: 2025-08-19 10:30:20
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import subprocess
from typing import List

# Pydantic模型定义
class ProcessInfo(BaseModel):
    process_id: int
    process_name: str
    status: str

# 创建FastAPI应用
app = FastAPI()

# 获取当前运行的进程列表
@app.get("/processes")
async def get_processes():
    try:
        # 使用subprocess执行命令获取进程信息
        # 这里使用的是Unix系统的ps命令，Windows系统需要使用不同的命令
        output = subprocess.check_output(["ps", "-ef"]).decode("utf-8")
        # 将输出解析为进程列表
        processes = [ProcessInfo(process_id=int(line.split()[1]), process_name=line.split()[-1], status="running") for line in output.strip().split("
") if line]
        return processes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 添加错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# FastAPI文档页面
@app.get("/docs")
async def custom_swagger_ui():
    return RedirectResponse(url="/")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)