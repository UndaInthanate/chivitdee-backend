from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/scan", tags=["scan"])


class ScanRequest(BaseModel):
    image_base64: str
    mime_type: str = "image/jpeg"


class ScanResult(BaseModel):
    amount: float | None = None
    date: str | None = None
    description: str | None = None
    category: str | None = None
    raw_text: str | None = None


@router.post("/receipt", response_model=ScanResult)
async def scan_receipt(req: ScanRequest):
    raise HTTPException(status_code=503, detail="ฟีเจอร์สแกนสลิปยังไม่พร้อมใช้งานบน server นี้")
