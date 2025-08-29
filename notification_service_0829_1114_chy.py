# 代码生成时间: 2025-08-29 11:14:41
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Pydantic model for notification
class Notification(BaseModel):
    title: str
    message: str
    timestamp: Optional[datetime] = None

# Pydantic model for response
class NotificationResponse(BaseModel):
    notification_id: int
    title: str
    message: str
    timestamp: Optional[str] = None

# Instantiate FastAPI app
app = FastAPI(title="Notification Service", description="API for sending notifications")

# In-memory database
notifications_db = []
notification_id = 1

# Error handler
@app.exception_handler(ValueError)
async def value_error_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message": str(exc)}
    )

# Endpoint for sending notifications
@app.post("/notifications/")
async def create_notification(notification: Notification):
    global notification_id
    new_notification = {
        "notification_id": notification_id,
        "title": notification.title,
        "message": notification.message,
        "timestamp": notification.timestamp.isoformat() if notification.timestamp else None
    }
    notifications_db.append(new_notification)
    notification_id += 1
    return JSONResponse(content=NotificationResponse(**new_notification).dict(), status_code=status.HTTP_201_CREATED)

# Endpoint for getting notifications
@app.get("/notifications/")
async def read_notifications():
    return JSONResponse(content=[NotificationResponse(**n).dict() for n in notifications_db], status_code=status.HTTP_200_OK)
