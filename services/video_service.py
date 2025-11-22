import os
import textwrap
import moviepy.editor as mpy
from services.util_service import generate_filename
from services.pil_text import pil_text_clip  # ← your new helper

class VideoService:

    @staticmethod
    def create_promo_video(site_info, image_clip=None):
        clips = []

        # Title
        title_text = site_info.get("title") or "Website Preview"
        title_clip = pil_text_clip(title_text, fontsize=60, duration=3)
        clips.append(title_clip)

        # Description
        desc = site_info.get("desc") or "Description"
        desc_clip = pil_text_clip(desc, fontsize=40, duration=4)
        clips.append(desc_clip)

        # Image (if exists)
        if image_clip:
            image_clip = image_clip.set_duration(4).resize((1280, 720))
            clips.append(image_clip)

        if not clips:
            raise Exception("No clips to concatenate")

        final = mpy.concatenate_videoclips(clips, method="compose")

        # Optional audio
        try:
            music = mpy.AudioFileClip("background.mp3").volumex(0.3)
            final = final.set_audio(music)
        except:
            pass

        os.makedirs("output", exist_ok=True)
        filename = generate_filename(site_info.get("title"))
        output_path = os.path.join("output", filename)

        final.write_videofile(output_path, fps=24)
        return output_path
