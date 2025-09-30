# 代码生成时间: 2025-10-01 03:58:21
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import base64
# 导入OCR库，这里假设使用tesseract-ocr
import pytesseract
from PIL import Image

# Pydantic模型定义
class OcrImage(BaseModel):
    file: UploadFile = File(...)

# 初始化FastAPI应用
app = FastAPI(title="OCR Service", description="A Simple OCR Service")

# OCR文字识别端点
@app.post("/ocr")
async def ocr(image: OcrImage):
    # 读取图片文件
    try:
        content = await image.file.read()
        # 将文件内容转换为PIL图像对象
        image_obj = Image.open(BytesIO(content))
    except Exception as e:
        # 错误处理
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": f"Failed to read the image: {e}"}
        )

    # 调用OCR库进行文字识别
    try:
        # 将PIL图像对象转换为OCR库需要的格式
        image_text = pytesseract.image_to_string(image_obj)
    except Exception as e:
        # 错误处理
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": f"OCR processing failed: {e}"}
        )

    # 返回识别结果
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"text": image_text}
    )

# FastAPI最佳实践：添加错误处理异常处理器
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": "Validation error", "errors": exc.errors()}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)