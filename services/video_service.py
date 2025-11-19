import os
import textwrap
from moviepy.editor import (
    TextClip, ColorClip, CompositeVideoClip,
    concatenate_videoclips, AudioFileClip
)
from services.util_service import generate_filename
from moviepy.config import change_settings

change_settings({"IMAGEMAGICK_BINARY": "magick"})

class VideoService:

    @staticmethod
    def create_promo_video(site_info, image_clip=None):
        clips = []

        # Gradient-style fallback background
        bg = ColorClip(size=(1280, 720), color=(20, 20, 20))

        # Title screen
        title_clip = TextClip(
            site_info["title"],
            fontsize=60,
            color="white",
            size=(1280, 720),
            method="caption"
        ).set_duration(3)

        title_clip = CompositeVideoClip([bg.set_duration(3), title_clip])
        clips.append(title_clip)

        # Description screen
        desc_text = "\n".join(textwrap.wrap(site_info["desc"], 40))
        desc_clip = TextClip(
            desc_text,
            fontsize=40,
            color="white",
            size=(1280, 720),
            method="caption"
        ).set_duration(4)

        desc_clip = CompositeVideoClip([bg.set_duration(4), desc_clip])
        clips.append(desc_clip)

        # Image (if exists)
        if image_clip:
            clips.append(image_clip)

        for c in clips:
            print("Clip:", c, "Duration:", c.duration)

        final = concatenate_videoclips(clips, method="compose")

        # Optional audio
        try:
            music = AudioFileClip("background.mp3").volumex(0.3)
            final = final.set_audio(music)
        except:
            pass

        # Ensure output dir
        os.makedirs("output", exist_ok=True)

        filename = generate_filename(site_info["title"])
        output_path = os.path.join("output", filename)

        final.write_videofile(output_path, fps=24)
        return output_path