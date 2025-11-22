from PIL import Image, ImageDraw, ImageFont
import numpy as np
import moviepy.editor as mpy

def pil_text_clip(text, fontsize=48, color="white", bg=(20, 20, 20),
                  size=(1280, 720), duration=3):

    # Create background
    img = Image.new("RGB", size, bg)
    draw = ImageDraw.Draw(img)

    # Font
    try:
        font = ImageFont.truetype("arial.ttf", fontsize)
    except:
        font = ImageFont.load_default()

    # Utility to measure text width
    def text_width(txt):
        bbox = draw.textbbox((0, 0), txt, font=font)
        return bbox[2] - bbox[0]

    # Word wrap
    lines = []
    words = text.split(" ")
    line = ""

    for word in words:
        t = (line + " " + word).strip()
        if text_width(t) < size[0] - 100:
            line = t
        else:
            lines.append(line)
            line = word
    lines.append(line)

    # Center text vertically
    line_height = fontsize + 10
    total_height = len(lines) * line_height
    y = (size[1] - total_height) // 2

    # Draw each line
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        w = bbox[2] - bbox[0]
        x = (size[0] - w) // 2
        draw.text((x, y), line, font=font, fill=color)
        y += line_height

    # Convert PIL image → moviepy clip
    frame = np.array(img)
    return mpy.ImageClip(frame).set_duration(duration)
