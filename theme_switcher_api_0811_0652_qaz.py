# 代码生成时间: 2025-08-11 06:52:24
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# Pydantic model for theme change request
class ThemeChangeRequest(BaseModel):
    theme: str

app = FastAPI()

# In-memory data structure to store the current theme
current_theme = "light"

# GET endpoint to retrieve the current theme
@app.get("/current-theme")
async def get_current_theme():
    return JSONResponse(content={"current_theme": current_theme})

# POST endpoint to change the theme
@app.post("/change-theme\)
async def change_theme(request: ThemeChangeRequest):
    global current_theme
    try:
        # Validate the theme
        if request.theme not in ["light", "dark"]:
            raise ValueError("Invalid theme")
        # Change the theme
        current_theme = request.theme
        return JSONResponse(content=jsonable_encoder({"message": f"Theme changed to {current_theme}"}))
    except ValueError as e:
        # Error handling
        raise HTTPException(status_code=400, detail=str(e))

# Swagger UI for API documentation
@app.get("/docs")
async def swagger_ui():
    return JSONResponse(content="Redirect to Swagger UI")

# Redoc for API documentation
@app.get("/redoc")
async def redoc_ui():
    return JSONResponse(content="Redirect to Redoc")