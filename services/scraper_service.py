import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class ScraperService:

    @staticmethod
    def scrape_site_info(url: str):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except Exception as e:
            return {"title": "Unknown Website", "desc": str(e), "img": None}

        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.title.string.strip() if soup.title and soup.title.string else "Discover Something Amazing"

        desc_tag = soup.find("meta", attrs={"name": "description"})
        desc = desc_tag["content"] if desc_tag and desc_tag.get("content") else "Explore the website for more!"

        og_img = soup.find("meta", property="og:image")
        img_url = og_img["content"] if og_img and og_img.get("content") else None

        if not img_url:
            img = soup.find("img")
            img_url = img["src"] if img and img.get("src") else None

        if img_url:
            img_url = urljoin(url, img_url)

        return {"title": title, "desc": desc, "img": img_url}