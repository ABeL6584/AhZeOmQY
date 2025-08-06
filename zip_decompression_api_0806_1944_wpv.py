# 代码生成时间: 2025-08-06 19:44:02
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from zipfile import ZipFile
from io import BytesIO
import shutil
import os
from typing import Optional

# Pydantic model for request body
class DecompressionRequest(BaseModel):
    file: UploadFile  # The file to decompress
    destination: str = "./decompressed"  # Optional destination directory

# FastAPI instance
app = FastAPI()

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# Route for decompressing a zip file
@app.post("/decompress/")
async def decompress_zip(request: DecompressionRequest):
    # Check if the destination directory exists, create if not
    if not os.path.exists(request.destination):
        os.makedirs(request.destination)

    # Read the file content
    file_content = await request.file.read()
    try:
        # Open the zip file
        zip_file = ZipFile(BytesIO(file_content))
        # Extract all the contents into the destination directory
        zip_file.extractall(path=request.destination)
        # Return a success response
        return JSONResponse(content={"message": "File decompressed successfully"}, status_code=200)
    except BadZipFile:
        # Return an error response if the file is not a zip file
        return JSONResponse(content={"detail": "Invalid zip file"}, status_code=400)
    finally:
        # Close the zip file
        zip_file.close()

# Additional route to serve API documentation (automatically handled by FastAPI)
@app.get("/docs")
async def serve_docs():
    return "API documentation is available at /docs"

# Additional route for Swagger UI (automatically handled by FastAPI)
@app.get("/redoc")
async def serve_redoc():
    return "Swagger UI is available at /redoc"
