# 代码生成时间: 2025-08-22 17:14:11
from fastapi import FastAPI, APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List
import os

# Pydantic model for file renaming
class FileRename(BaseModel):
    old_name: str
    new_name: str

# API router
router = APIRouter()

# Instantiate the FastAPI app
app = FastAPI(title="Batch Renamer API", description="API to rename multiple files")
app.include_router(router)


# Endpoint to rename files in batch
@router.post("/rename", response_model=List[str], status_code=status.HTTP_200_OK)
async def batch_rename(files: List[FileRename]):
    """
    Endpoint to batch rename files.
    Args:
        files (List[FileRename]): List of files to rename.
    Returns:
        List[str]: List of results for each file rename operation.
    Raises:
        HTTPException: If a file does not exist or cannot be renamed.
    """
    results = []
    for file in files:
        old_path = file.old_name
        new_path = file.new_name
        if not os.path.exists(old_path):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"File {old_path} not found")
        try:
            os.rename(old_path, new_path)
            results.append(f"Renamed {old_path} to {new_path}")
        except OSError as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to rename {old_path} to {new_path}: {str(e)}")
    return results
