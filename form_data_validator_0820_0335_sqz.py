# 代码生成时间: 2025-08-20 03:35:07
from fastapi import FastAPI, HTTPException, Form
from pydantic import BaseModel, ValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

# Pydantic模型用于表单数据验证
class FormData(BaseModel):
    name: str
    age: int
    email: str

# 表单数据验证器端点
@app.post("/form-data")
async def form_data_validator(name: str = Form(...), age: int = Form(...), email: str = Form(...)):
    try:
        # 创建Pydantic模型实例
        data = FormData(name=name, age=age, email=email)
        # 验证表单数据
        data = jsonable_encoder(data)
        return JSONResponse(content=data, status_code=200)
    except ValidationError as e:
        # 错误处理：返回错误信息
        error_messages = e.errors()[0]
        detail = {"detail": f"{error_messages['type']}: {error_messages['msg']}"}
        raise HTTPException(status_code=422, detail=jsonable_encoder(detail))

# 启动应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)