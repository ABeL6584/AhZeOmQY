# 代码生成时间: 2025-08-03 10:44:17
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import zipfile
import shutil
import os
from pathlib import Path

# Pydantic model for receiving file data
class FileData(BaseModel):
    file: UploadFile  # The uploaded file

app = FastAPI()

# Endpoint for decompressing files
@app.post("/decompress/")
async def decompress_file(data: FileData = File(...)):
    # Check if the file is a zip file
    if not data.file.filename.endswith(".zip"):
        return JSONResponse(status_code=400, content={"message": "It's not a zip file."})
    
    # Create a temporary directory for extraction
    temp_dir = Path("./temp")
    temp_dir.mkdir(exist_ok=True)
    
    # Save the uploaded file to a temporary location
    temp_file_path = temp_dir / data.file.filename
    with open(temp_file_path, "wb") as f:
        f.write(await data.file.read())
    
    try:
        # Extract the zip file
        with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Optionally, you can handle the extracted files here
        # For demonstration, we just send a success message
        return {"message": "Decompression successful."}
    except zipfile.BadZipFile:
        # Return an error message if the file is corrupted
        return JSONResponse(status_code=500, content={"message": "The file is corrupted or not a zip file."})
    finally:
        # Clean up the temporary files
        shutil.rmtree(temp_dir)

# Add Swagger UI for API documentation
app.include_router(fastapi docs, prefix="/docs")

# Error handling
@app.exception_handler(Exception)
async def http_exception_handler(request, exc):
    return JSONResponse(status_code=500, content={"message": str(exc)})

# Start the server with uvicorn by running: uvicorn file_decompression_api:app --reload