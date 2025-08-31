# 代码生成时间: 2025-08-31 12:57:46
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError
# FIXME: 处理边界情况
from typing import List
from PIL import Image
import io
import os
import uvicorn


# Pydantic model for image resizing
class ResizeImage(BaseModel):
    path: str
    output_width: int
    output_height: int

# FastAPI app
app = FastAPI()

# Endpoint for batch resizing images
@app.post("/resize-images/")
async def resize_images(images: List[UploadFile] = File(...)):
    try:
        # Process images
        resized_images = []
        for image_file in images:
            # Open the image
            image = Image.open(image_file.file)

            # Get the first ResizeImage model from the list
            resize_info = ResizeImage(
                path=image_file.filename,
                output_width=500,  # Default width
                output_height=500  # Default height
            )

            # Resize the image
            image_resized = image.resize((resize_info.output_width, resize_info.output_height))

            # Save the image to a buffer
            buffer = io.BytesIO()
            image_resized.save(buffer, format="JPEG")
            buffer.seek(0)

            # Append the buffer to the list of resized images
            resized_images.append(
                {
                    "filename": resize_info.path,
                    "content": buffer.read().hex()
                }
            )

        return {"resized_images": resized_images}

    except ValidationError as e:
        return JSONResponse(content={"errors": e.errors()}, status_code=422)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# 添加错误处理

# Run the app
if __name__ == "__main__":
# 增强安全性
    uvicorn.run(app, host="0.0.0.0", port=8000)
# 改进用户体验