# 代码生成时间: 2025-09-03 11:31:55
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import logging
import re

# 设置日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic模型定义日志行
class LogEntry(BaseModel):
    timestamp: str
    level: str
    message: str

# FastAPI应用实例
app = FastAPI()

# 文件上传端点
@app.post("/parse-logs/")
async def parse_logs(file: UploadFile = File(...)):
    # 检查文件是否为空
    if not file.content_type:
        raise HTTPException(status_code=400, detail="File is empty")

    # 读取文件内容
    try:
        contents = await file.read()
    except Exception as e:
        logger.error(f"Failed to read file: {e}")
        raise HTTPException(status_code=500, detail="Failed to read file")

    # 解析日志文件内容
    logs = parse_log_contents(contents)
    return logs

# 日志文件内容解析函数
def parse_log_contents(contents: bytes) -> list:
    # 定义日志行的正则表达式
    log_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:\.\d+)?) ([A-Z]+) (.*)")

    # 将字节内容转换为字符串
    logs = []
    for line in contents.decode().splitlines():
        match = log_pattern.match(line)
        if match:
            timestamp, level, message = match.groups()
            logs.append(LogEntry(timestamp=timestamp, level=level, message=message))
        else:
            logger.warning(f"Unmatched log line: {line}")
    return logs

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# 运行Uvicorn服务器
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)