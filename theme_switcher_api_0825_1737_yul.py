# 代码生成时间: 2025-08-25 17:37:53
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Pydantic model to represent the theme
class Theme(BaseModel):
    theme: str

# In-memory variable to store the current theme
current_theme = "light"

@app.get("/current-theme")
async def read_theme():
    return {
        "theme": current_theme
    }

@app.post("/change-theme")
async def change_theme(request: Request, new_theme: Theme):
    global current_theme
    if new_theme.theme not in ["light", "dark"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid theme. Choose 'light' or 'dark'."
        )
    current_theme = new_theme.theme
    return JSONResponse(
        status_code=200,
        content={
            "message": "Theme changed successfully.",
            "new_theme": current_theme
        }
    )

# Error handler for 404 errors
@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={
            "message": "Not found"
        }
    )

# Error handler for internal server errors
@app.exception_handler(500)
async def server_error_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error"
        }
    )