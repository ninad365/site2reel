import re
from datetime import datetime

def slugify(text: str):
    return re.sub(r'[^a-zA-Z0-9]+', '_', text).strip('_')

def generate_filename(title: str):
    safe = slugify(title)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{safe}_{ts}.mp4"