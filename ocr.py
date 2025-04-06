import pytesseract
import cv2
import tempfile

def extract_receipt_data(file):
    temp = tempfile.NamedTemporaryFile(delete=False)
    file.save(temp.name)

    image = cv2.imread(temp.name)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    return {
        "raw_text": text,
        "merchant": "Generic Store",
        "total": "29.99",
        "date": "2025-04-06",
        "items": ["item1", "item2"]
    }