from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import FileResponse
from services.ai_scraper_service import AIScraperService
from services.video_service import VideoService
from services.image_service import ImageService
from services.scraper_service import ScraperService
import os
import uuid
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Site2Reel API",
    description="Generate promotional videos from website URLs",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # For now allow all. Later we can lock this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
        # 1. Fetch structured data + script via OpenAI
        site = AIScraperService.fetch_site_data_and_script(req.url)
        
        print(site)
        
        # Create promo video
        output_path = VideoService.create_promo_video(site)

        # Return downloadable video
        return FileResponse(
            output_path,
            media_type="video/mp4",
            filename=os.path.basename(output_path)
        )

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