from pydantic import BaseModel
from typing import List
from typing import List, Optional

class ScriptModel(BaseModel):
    """
    Represents the structured video script generated from a scraped webpage.

    Attributes:
        title_slide (str): 
            The headline or introductory title to be shown on the first slide 
            of the promo video.

        description_slide (str): 
            A short descriptive text used on the second slide, summarizing the 
            product or service.

        narration (str): 
            A marketing-style narration script to be spoken in the video 
            (e.g., text-to-speech audio).

        highlights (List[str]): 
            A list of key features, selling points, or advantages extracted 
            from the webpage to showcase in the video.
    """
    title_slide: str
    description_slide: str
    narration: str
    highlights: List[str]

class AIScraperResult(BaseModel):
    """
    The top-level structured output returned by the AI scraper.

    Attributes:
        title (str): 
            The primary product or page title extracted from the target website.

        description (str): 
            A high-level summary of what the page is about, written in 
            user-friendly marketing language.

        best_image_url (str): 
            A URL pointing to the most suitable image found on the page for 
            use in the promotional video (e.g., product photo, hero image).

        script (ScriptModel): 
            The generated video script including slides, narration, and 
            highlight points.
    """
    title: str
    description: str
    best_image_url: str
    script: ScriptModel

class SiteVideoData(BaseModel):
    title: str
    description: str
    image_url: Optional[str] = None

    # List of textual frames/scenes for the video
    frames: List[str] = []

    # If AI generates structured scenes
    script: Optional[List[str]] = None