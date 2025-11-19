from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from services.video_service import VideoService
from services.image_service import ImageService
import os
import uuid

app = FastAPI(
    title="Site2Reel API",
    description="Generate promotional videos from website URLs",
    version="1.0.0"
)

# -------------------------------
# Request Model
# -------------------------------
class SiteRequest(BaseModel):
    url: str


# -------------------------------
# Root check
# -------------------------------
@app.get("/")
def home():
    return {"message": "Site2Reel backend is running!"}


# -------------------------------
# Generate Video Endpoint
# -------------------------------
@app.post("/generate")
def generate_video(req: SiteRequest):

    try:
        # Scrape site_info and extract image
        # (You already have a scraper, but inserting placeholder here)
        site_info = {
            "title": "Website Promo",
            "description": "Auto-generated Reel",
            "url": req.url
        }

        # Download preview image (replace with real scraper image)
        image_clip = ImageService.download_image(req.url)

        if image_clip is None:
            raise HTTPException(400, "Could not fetch image from URL")

        # Generate output filename
        output_path = f"output_{uuid.uuid4().hex}.mp4"

        # Create promo video
        final_path = VideoService.create_promo_video(site_info, image_clip, output_path)

        # Return downloadable video
        return {"video": final_path}

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(500, f"Video generation failed: {str(e)}")


# -------------------------------
# Return Actual MP4 File (Optional)
# -------------------------------
@app.get("/download")
def download(path: str):
    if not os.path.exists(path):
        raise HTTPException(404, "File not found")

    return FileResponse(
        path,
        media_type="video/mp4",
        filename=os.path.basename(path)
    )