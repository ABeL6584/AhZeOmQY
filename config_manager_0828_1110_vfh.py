# 代码生成时间: 2025-08-28 11:10:18
from typing import Optional
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, BaseSettings
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import uvicorn


# Pydantic模型用于配置文件
class ConfigItem(BaseModel):
    key: str
    value: str

# 定义FastAPI应用
app = FastAPI(title="配置文件管理器")

# 配置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置OAuth2密码Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 模拟配置文件存储
fake_config_storage = {}

# 获取配置文件的端点
@app.get("/configs/{key}")
async def get_config(key: str):
    config = fake_config_storage.get(key)
    if not config:
        raise HTTPException(status_code=404, detail="Config not found")
    return config

# 添加配置文件的端点
@app.post("/configs/")
async def add_config(config_item: ConfigItem):
    fake_config_storage[config_item.key] = config_item.value
    return JSONResponse(content={"message": "Config added successfully"}, media_type="application/json")

# 更新配置文件的端点
@app.put("/configs/{key}")
async def update_config(key: str, config_item: ConfigItem):
    if key in fake_config_storage:
        fake_config_storage[key] = config_item.value
        return JSONResponse(content={"message": "Config updated successfully"}, media_type="application/json")
    raise HTTPException(status_code=404, detail="Config not found")

# 删除配置文件的端点
@app.delete("/configs/{key}")
async def delete_config(key: str):
    if key in fake_config_storage:
        del fake_config_storage[key]
        return JSONResponse(content={"message": "Config deleted successfully"}, media_type="application/json")
    raise HTTPException(status_code=404, detail="Config not found")

# 错误处理
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder(
            {
                "detail": exc.errors(),
                "errors": exc.errors()
            }
        ),
    )

# 运行服务器
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    
# 格式化OpenAPI
def custom_openapi():
    openapi_schema = get_openapi(
        title="配置文件管理器",
        version="1.0.0",
        description="配置文件管理器接口",
        routes=app.routes,
    )
    openapi_schema[