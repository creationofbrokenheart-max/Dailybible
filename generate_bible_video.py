import os
from gtts import gTTS
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
from moviepy.audio.fx.all import volumex
import requests
from io import BytesIO
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline

# Constants
VERSE = "The Lord is my shepherd; I shall not want. — Psalm 23:1"
VIDEO_SIZE = (1920, 1080)
DURATION = 15  # seconds
FONT_SIZE = 70
TEXT_COLOR = "white"
FONT = "Arial-Bold"
MUSIC_FILE = "music.mp3"  # Place your music file here
OUTPUT_FILE = "output/youtube/test.mp4"
BG_IMAGE_FILE = "bg_youtube.jpg"

os.makedirs("output/youtube", exist_ok=True)

# 1️⃣ Generate a relevant AI background image
def generate_image(prompt, path):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16 if device=="cuda" else torch.float32
    )
    pipe = pipe.to(device)
    image = pipe(prompt, height=VIDEO_SIZE[1], width=VIDEO_SIZE[0]).images[0]
    image.save(path)

if not os.path.exists(BG_IMAGE_FILE):
    print("Generating AI background image...")
    generate_image(f"{VERSE}, cinematic, epic, high quality, ultra-detailed", BG_IMAGE_FILE)

# 2️⃣ Generate voice-over
voice_file = "voice.mp3"
if not os.path.exists(voice_file):
    print("Generating voice-over...")
    tts = gTTS(text=VERSE, lang="en")
    tts.save(voice_file)

# 3️⃣ Load background music and voice
voice = AudioFileClip(voice_file).set_duration(DURATION)
music = AudioFileClip(MUSIC_FILE).set_duration(DURATION).fx(volumex, 0.2)
audio = CompositeAudioClip([voice, music])

# 4️⃣ Create video clips
background = ImageClip(BG_IMAGE_FILE).with_duration(DURATION)
text = TextClip(
    VERSE,
    fontsize=FONT_SIZE,
    color=TEXT_COLOR,
    font=FONT,
    method="label"
).with_duration(DURATION).set_position("center")

video = CompositeVideoClip([background, text])
video = video.set_audio(audio)
video.write_videofile(OUTPUT_FILE, fps=24, codec="libx264")
