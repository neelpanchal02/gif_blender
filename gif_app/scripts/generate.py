import sys
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

def generate_image(text):
    width = 400
    height = 80
    image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)

    font_size = 50

    # Get the relative path for the font
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the current script directory
    font_path = os.path.join(base_dir, "static","banner", "fonts", "arialbd.ttf")  # Construct the relative path
    print(font_path)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    max_width = width - 20
    max_height = height - 10

    def fits_within_height(font_size):
        font = ImageFont.truetype(font_path, font_size)
        wrapped_text = textwrap.fill(text, width=char_per_line(font_size))
        line_height = (font.getbbox("A")[3] - font.getbbox("A")[1]) * 1.2
        lines = wrapped_text.split('\n')
        total_text_height = len(lines) * line_height
        return total_text_height <= max_height

    def char_per_line(font_size):
        if font_size >= 50:
            return 12
        elif font_size >= 40:
            return 15
        elif font_size >= 30:
            return 18
        else:
            return 20

    while not fits_within_height(font_size):
        font_size -= 2
        if font_size < 10:
            break

    font = ImageFont.truetype(font_path, font_size)
    wrapped_text = textwrap.fill(text, width=char_per_line(font_size))
    line_height = (font.getbbox("A")[3] - font.getbbox("A")[1]) * 1.2
    lines = wrapped_text.split('\n')
    total_text_height = len(lines) * line_height
    start_y = (height - total_text_height) / 2

    for i, line in enumerate(lines):
        text_width = font.getbbox(line)[2] - font.getbbox(line)[0]
        start_x = (width - text_width) / 2
        draw.text((start_x, start_y + i * line_height), line, font=font, fill=(0, 0, 0))

    image.save("static/banner/output.png", "PNG")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        generate_image(user_input)
    else:
        print("No text provided")
