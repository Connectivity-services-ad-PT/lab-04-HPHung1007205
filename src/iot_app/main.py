import os
import datetime
import uvicorn
from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from typing import Optional

app = FastAPI(
    title="IoT Ingestion Service",
    description="FIT4110 Lab 04 - Docker Packaging",
    version="1.0.0"
)

# Cơ sở dữ liệu lưu trữ tạm thời
db = {}

# --- 1. Hàm kiểm tra Quyền truy cập ---
def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing token")
    
    try:
        token_type, token = auth_header.split(" ")
        if token_type.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        if "wrong" in token.lower() or "invalid" in token.lower():
            raise HTTPException(status_code=401, detail="Wrong token")
            
        return
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token format")

# --- 2. Bộ xử lý lỗi ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "type": "validation_error",
            "status": 422,
            "detail": exc.errors()
        }
    )
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": "error",
            "title": "Request Error",
            "status": exc.status_code,
            "detail": exc.detail
        }
    )
# --- 3. Endpoints ---

@app.get("/health", status_code=200)
async def health_check():
    return {"status": "ok", "service": "IoT Ingestion Service", "version": "1.0.0"}

@app.post("/readings", status_code=201)
async def create_reading(request: Request, response: Response, _ = Depends(verify_token)):
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Invalid JSON")

    if "device_id" not in body or not body["device_id"]:
        raise HTTPException(status_code=422, detail="device_id is required")

    temp_raw = body.get("temperature") if body.get("temperature") is not None else body.get("value")
    if temp_raw is None:
        raise HTTPException(status_code=422, detail="temperature or value is required")
        
    try:
        temp_value = float(temp_raw)
    except ValueError:
        raise HTTPException(status_code=422, detail="temperature must be a number")

    if temp_value > 80:
        raise HTTPException(status_code=422, detail="Temperature out of bounds")
        
    if temp_value == 80:
        response.headers["Warning"] = '199 Missing Technology - High temperature detected'
        response.headers["X-Warning"] = "True"

    reading_id = f"R-{datetime.datetime.now().strftime('%Y%m%d')}-{len(db) + 1:04d}"
    timestamp_str = datetime.datetime.utcnow().isoformat()
    
    payload = {
    "reading_id": reading_id,
    "device_id": body["device_id"],
    "metric": "temperature",
    "temperature": temp_value,
    "timestamp": timestamp_str,
    "accepted": True
    }
    
    db[reading_id] = payload
    return payload

@app.get("/readings/latest", status_code=200)
async def get_latest_readings(device_id: str, limit: int = 5):
    filtered_items = [item for item in db.values() if item["device_id"] == device_id]
    return {"items": filtered_items[-limit:], "count": len(filtered_items)}

@app.get("/readings/{reading_id}", status_code=200)
async def get_reading_by_id(reading_id: str):
    if reading_id not in db:
        raise HTTPException(status_code=404, detail="Reading not found")
    return db[reading_id]

# --- ĐOẠN QUAN TRỌNG ĐỂ KHÔNG BỊ TIMED OUT ---
if __name__ == "__main__":
    uvicorn.run(...)