from PIL import Image
import os
import cv2
import time
import shutil

ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

def v2f(video_path, output_folder="frames", width=80):
    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)
    os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        resized_frame = cv2.resize(gray_frame, (width, int(gray_frame.shape[0] * (width / gray_frame.shape[1]))))
        img = Image.fromarray(resized_frame)
        img.save(os.path.join(output_folder, f"frame{frame_count:04d}.png"))
        frame_count += 1

    cap.release()

def f2a(image_path, width=80):
    try:
        image = Image.open(image_path)
    except Exception as e:
        return ""
    
    aspect_ratio = image.height / image.width
    new_height = int(aspect_ratio * width)
    image = image.resize((width, new_height)).convert('L')
    
    pixels = image.getdata()
    ascii_str = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    ascii_str_len = len(ascii_str)
    ascii_img = "\n".join([ascii_str[index:index + width] for index in range(0, ascii_str_len, width)])
    
    return ascii_img

def bar(current_frame, total_frames, bar_length=80):
    progress = current_frame / total_frames
    filled_length = int(bar_length * progress)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    return f"[{bar}] {int(progress * 100)}%"

video_path = input("Enter the path to the video file: ").strip('"')
v2f(video_path, output_folder="frames", width=80)

frames = sorted(os.listdir('frames'))
if not frames:
    exit("No frames found")

clear_command = 'cls' if os.name == 'nt' else 'clear'
frame_delay = 0.05
total_frames = len(frames)

for index, frame in enumerate(frames):
    frame_path = os.path.join('frames', frame)
    ascii_art = f2a(frame_path, width=80)
    os.system(clear_command)
    print(ascii_art)
    progress_bar = bar(index + 1, total_frames)
    print(f"\n{progress_bar}")

    time.sleep(frame_delay)

os.system(clear_command)
print("\n" * 10)
print(" " * 20 + "The End")
time.sleep(2)

