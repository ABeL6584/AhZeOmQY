# 代码生成时间: 2025-09-13 20:08:48
from fastapi import FastAPI, HTTPException, status, APIRouter
from pydantic import BaseModel
from typing import List, Optional
import psutil
import asyncio

class ProcessInfo(BaseModel):
    pid: int
    name: str
    status: str

    
class ProcessList(BaseModel):
    processes: List[ProcessInfo]

class ProcessManagerRouter(APIRouter):
    def __init__(self):
        super().__init__(tags=['Process Manager'])

    async def get(self):
        """ Get a list of running processes. """
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'status']):
            if proc.status() == psutil.STATUS_ZOMBIE:
                continue
            processes.append(ProcessInfo(
                pid=proc.pid,
                name=proc.info['name'],
                status=proc.status()
            ))
        return ProcessList(processes=processes)

    async def post(self, process_info: ProcessInfo):
        """ Start a new process. """
        try:
            process = await asyncio.create_subprocess_exec(
                process_info.name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            return {"pid": process.pid}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    async def put(self, process_info: ProcessInfo):
        """ Modify a running process. """
        try:
            proc = psutil.Process(process_info.pid)
            if proc.status() == psutil.STATUS_ZOMBIE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Process with pid {process_info.pid} is not running."
                )
            proc.terminate()
            return {"message": "Process terminated."}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

    async def delete(self, pid: int):
        """ Terminate a process by its PID. """
        try:
            proc = psutil.Process(pid)
            if proc.status() == psutil.STATUS_ZOMBIE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Process with pid {pid} is not running."
                )
            proc.terminate()
            return {"message": "Process terminated."}
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e)
            )

app = FastAPI()
app.include_router(ProcessManagerRouter())

# Run the application with uvicorn
# uvicorn process_manager:app --reload