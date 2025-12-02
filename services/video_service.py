import os
import textwrap
import moviepy.editor as mpy
from models.models import AIScraperResult
from services.util_service import generate_filename
from services.pil_text import pil_text_clip  # ← your new helper

class VideoService:

    @staticmethod
    def create_promo_video(site: AIScraperResult, image_clip=None):
        """
        Creates a promotional video using the structured AI scraper result.

        Args:
            site (AIScraperResult):
                Strongly-typed model containing title, description,
                best image, and script slides.
            image_clip (VideoClip | None):
                Optional image/video clip to include.

        Returns:
            str: Final generated video path.
        """

        clips = []

        # -------------------------------------------------------
        # 1) Title Slide
        # -------------------------------------------------------
        title_text = site.script.title_slide or site.title
        title_clip = pil_text_clip(title_text, fontsize=60, duration=3)
        clips.append(title_clip)

        # -------------------------------------------------------
        # 2) Description Slide
        # -------------------------------------------------------
        desc_text = site.script.description_slide or site.description
        desc_clip = pil_text_clip(desc_text, fontsize=40, duration=4)
        clips.append(desc_clip)

        # -------------------------------------------------------
        # 3) Highlights (each as its own slide)
        # -------------------------------------------------------
        for hl in site.script.highlights:
            highlight_clip = pil_text_clip(hl, fontsize=45, duration=3)
            clips.append(highlight_clip)

        # -------------------------------------------------------
        # 4) Image Slide (optional)
        # -------------------------------------------------------
        if image_clip:
            image_clip = image_clip.set_duration(4).resize((1280, 720))
            clips.append(image_clip)

        if not clips:
            raise Exception("No clips to concatenate")

        # -------------------------------------------------------
        # 5) Final video assembly
        # -------------------------------------------------------
        final = mpy.concatenate_videoclips(clips, method="compose")

        # Optional background music
        try:
            music = mpy.AudioFileClip("background.mp3").volumex(0.3)
            final = final.set_audio(music)
        except Exception:
            pass

        # -------------------------------------------------------
        # 6) Save output
        # -------------------------------------------------------
        os.makedirs("output", exist_ok=True)
        filename = generate_filename(site.title)
        output_path = os.path.join("output", filename)

        final.write_videofile(output_path, fps=24)
        return output_path