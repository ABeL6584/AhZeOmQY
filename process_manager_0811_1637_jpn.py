# 代码生成时间: 2025-08-11 16:37:50
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List
import psutil

# Pydantic模型，用于序列化请求和响应数据
class ProcessInfo(BaseModel):
    pid: int
    name: str
    status: str

# 创建FastAPI应用实例
app = FastAPI()

# 获取所有进程的端点
@app.get("/processes", response_model=List[ProcessInfo])
async def get_processes():
    # 获取所有进程信息
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'status']):
        try:
            process_info = ProcessInfo(
                pid=proc.info['pid'],
                name=proc.info['name'],
                status=proc.info['status']
            )
            processes.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return processes

# 终止进程的端点
@app.post("/process/{pid}")
async def terminate_process(pid: int):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        proc.wait()  # 等待进程终止
        return {"message": "Process terminated"}
    except psutil.NoSuchProcess:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Process not found")
    except psutil.AccessDenied:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

# 启动FastAPI应用的如果文件被直接运行
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)