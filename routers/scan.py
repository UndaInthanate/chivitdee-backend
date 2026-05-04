import base64, re, io
from datetime import date
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from PIL import Image
import pytesseract

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


def extract_amount(text: str) -> float | None:
    # หาตัวเลขที่เป็นจำนวนเงิน เช่น 1,250.00 / 250.50 / 1250
    patterns = [
        r'(?:จำนวน|ยอด|รวม|Total|Amount)[^\d]*(\d[\d,]*\.?\d*)',
        r'(\d{1,3}(?:,\d{3})*\.\d{2})',
        r'(\d{2,6}(?:\.\d{2})?)',
    ]
    for p in patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            try:
                return float(m.group(1).replace(',', ''))
            except:
                continue
    return None


def extract_date(text: str) -> str | None:
    today = date.today().isoformat()
    # รูปแบบ DD/MM/YYYY หรือ DD-MM-YYYY
    m = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})', text)
    if m:
        d, mo, y = m.group(1), m.group(2), m.group(3)
        if len(y) == 2:
            y = '20' + y
        # ถ้าปีเป็นพ.ศ. แปลงเป็น ค.ศ.
        if int(y) > 2100:
            y = str(int(y) - 543)
        try:
            return f"{y}-{mo.zfill(2)}-{d.zfill(2)}"
        except:
            pass
    return today


def guess_category(text: str) -> str:
    text_lower = text.lower()
    if any(w in text_lower for w in ['food', 'ร้านอาหาร', 'อาหาร', 'กาแฟ', 'coffee', 'ข้าว', 'ก๋วยเตี๋ยว', 'ส้มตำ']):
        return 'อาหาร'
    if any(w in text_lower for w in ['grab', 'bolt', 'taxi', 'บขส', 'mrt', 'bts', 'รถ', 'น้ำมัน', 'parking']):
        return 'เดินทาง'
    if any(w in text_lower for w in ['hospital', 'clinic', 'โรงพยาบาล', 'ร้านขายยา', 'pharmacy']):
        return 'สุขภาพ'
    if any(w in text_lower for w in ['lazada', 'shopee', 'amazon', 'shop', 'mall', 'ห้าง', 'ซื้อ']):
        return 'ช้อปปิ้ง'
    if any(w in text_lower for w in ['ไฟฟ้า', 'น้ำประปา', 'internet', 'true', 'ais', 'dtac', 'electric', 'water']):
        return 'ค่าน้ำไฟ'
    if any(w in text_lower for w in ['cinema', 'โรงหนัง', 'netflix', 'game', 'concert']):
        return 'บันเทิง'
    return 'อื่นๆ'


def extract_description(text: str) -> str:
    # เอาบรรทัดแรกที่ไม่ใช่ตัวเลขล้วน
    lines = [l.strip() for l in text.split('\n') if l.strip() and not re.match(r'^[\d\s\-/:.]+$', l.strip())]
    return lines[0][:60] if lines else ''


@router.post("/receipt", response_model=ScanResult)
async def scan_receipt(req: ScanRequest):
    try:
        img_data = base64.b64decode(req.image_base64)
        image = Image.open(io.BytesIO(img_data))

        # OCR ภาษาไทย + อังกฤษ
        text = pytesseract.image_to_string(image, lang='tha+eng')

        return ScanResult(
            amount=extract_amount(text),
            date=extract_date(text),
            description=extract_description(text),
            category=guess_category(text),
            raw_text=text[:500],
        )

    except Exception as e:
        raise HTTPException(status_code=422, detail=f"ไม่สามารถอ่านสลิปได้: {str(e)}")
