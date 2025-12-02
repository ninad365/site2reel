# services/ai_scraper_service.py

import os
import json
from openai import OpenAI
from models.models import AIScraperResult

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class AIScraperService:

    @staticmethod
    def fetch_site_data_and_script(url: str) -> AIScraperResult:
        """
        Scrapes a webpage using OpenAI web fetch, extracts structured data,
        and returns a parsed AIScraperResult model.
        """

        response = client.responses.create(
            model="gpt-5.1",
            input=f"""
You are a web-scraping + marketing expert.

Scrape this webpage: {url}

Return ONLY JSON with this structure:

{{
  "title": "...",
  "description": "...",
  "best_image_url": "...",
  "script": {{
    "title_slide": "...",
    "description_slide": "...",
    "narration": "...",
    "highlights": ["...", "...", "..."]
  }}
}}
"""
        )

        raw_json = response.output[0].content[0].text

        data = json.loads(raw_json)

        # ⬅ Convert into validated Pydantic model
        return AIScraperResult(**data)
