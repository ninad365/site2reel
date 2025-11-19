import requests
import io
from moviepy.editor import ImageClip
from PIL import Image
import numpy as np

class ImageService:

    @staticmethod
    def download_image(url):
        try:
            res = requests.get(url, timeout=8)
            res.raise_for_status()
        except:
            return None

        try:
            # Load image with PIL
            image_bytes = io.BytesIO(res.content)
            img = Image.open(image_bytes).convert("RGB")

            # Convert to numpy array
            frame = np.array(img)

            # Create ImageClip correctly
            clip = ImageClip(frame)

            # Resize to clean 720p
            clip = clip.resize(height=720)
            clip = clip.set_duration(5)
            return clip

        except Exception as e:
            print("ImageService error:", e)
            return None
