from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from services.video_service import VideoService
from services.image_service import ImageService
from services.scraper_service import ScraperService
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
        site_info = ScraperService.scrape_site_info(req.url)
        print("➡️ Scraped:", site_info["title"])

        img_clip = None
        if site_info["img"]:
            img_clip = ImageService.download_image(site_info["img"])

        # Generate output filename
        output_path = f"output_{uuid.uuid4().hex}.mp4"

        # Create promo video
        final_path = VideoService.create_promo_video(site_info, img_clip, output_path)

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