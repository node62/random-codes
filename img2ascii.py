"""
This script converts images or videos into ASCII art with customizable colors.

Usage:
- For images:
  python img2ascii.py <path_to_image> [width] [--color <color_name>]

- For videos:
  python img2ascii.py <path_to_video> [width] [--color <color_name>]

Arguments:
- <path_to_image>/<path_to_video>: Path to the input image or video file.
- [width]: Optional. Width of the output ASCII art (default: 60).
- [--color <color_name>]: Optional. Specifies the color of the ASCII characters. Available colors are:
  red, green, blue, yellow, cyan, magenta, white, black, pink.

Example:
- python img2ascii.py image.png --color red
- python img2ascii.py video.mp4 80 --color blue
"""

import sys
import os
from PIL import Image
import cv2

ASCII_CHARS = ["@", "%", "#", "S", "?", "*", "+", ";", ":", ",", ".", " "]

COLOR_MAP = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "cyan": (0, 255, 255),
    "magenta": (255, 0, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "pink": (255, 192, 203),
}

def composite_background(image, bg_color=(255, 255, 255)):
    if image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    ):
        image = image.convert("RGBA")
        bg = Image.new("RGBA", image.size, bg_color + (255,))
        image = Image.alpha_composite(bg, image)
    return image

def resize_image(image, new_width=60):
    w, h = image.size
    aspect_ratio = h / w
    new_height = int(aspect_ratio * new_width)
    try:
        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
    except AttributeError:
        return image.resize((new_width, new_height), Image.LANCZOS)

def to_grayscale(image):
    return image.convert("L")

def map_pixels_to_ascii(image_gray):
    pixels = list(image_gray.getdata())
    ascii_list = []
    n_chars = len(ASCII_CHARS)
    for val in pixels:
        idx = int((val / 255) * (n_chars - 1))
        ascii_list.append(ASCII_CHARS[idx])
    return "".join(ascii_list)

def color_ascii_one_color(ascii_str, color, width, height):
    (r, g, b) = color
    lines = []
    idx = 0
    for _ in range(height):
        line_chars = []
        for _ in range(width):
            ch = ascii_str[idx]
            colored = f"\033[38;2;{r};{g};{b}m{ch}\033[0m"
            line_chars.append(colored)
            idx += 1
        line_str = "".join(line_chars).rstrip()
        lines.append(line_str)
    return "\n".join(lines)

def generate_single_color_ascii(image, color, new_width=60):
    image = composite_background(image)
    image = resize_image(image, new_width)
    gray_img = to_grayscale(image)
    ascii_str = map_pixels_to_ascii(gray_img)
    w, h = image.size
    return color_ascii_one_color(ascii_str, color, w, h)

def process_image(path, color, new_width=60):
    try:
        img = Image.open(path)
    except Exception as e:
        sys.exit(f"Could not open image: {e}")
    return generate_single_color_ascii(img, color, new_width)

def process_video(path, color, new_width=60):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        sys.exit(f"Could not open video file: {path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 24
    delay = int(1000 / fps)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)

            ascii_art = generate_single_color_ascii(pil_img, color, new_width)

            print("\033c", end="")
            print(ascii_art)

            cv2.waitKey(delay)

    except KeyboardInterrupt:
        pass
    finally:
        cap.release()

def is_video_file(path):
    ext = os.path.splitext(path)[1].lower()
    video_exts = (".mp4", ".avi", ".mov", ".mkv", ".webm")
    return ext in video_exts

def main():
    if len(sys.argv) < 2:
        print("Usage: python ascii_color_art.py <path> [width] [--color <color_name>]")
        sys.exit(1)

    path = sys.argv[1]
    new_width = int(sys.argv[2]) if len(sys.argv) > 2 else 60

    color_name = "white"
    if "--color" in sys.argv:
        color_index = sys.argv.index("--color") + 1
        if color_index < len(sys.argv):
            color_name = sys.argv[color_index].lower()

    if color_name not in COLOR_MAP:
        sys.exit(f"Invalid color name: {color_name}. Available colors: {', '.join(COLOR_MAP.keys())}")

    color = COLOR_MAP[color_name]

    if is_video_file(path):
        process_video(path, color, new_width)
    else:
        art = process_image(path, color, new_width)
        print(art)

if __name__ == "__main__":
    main()
