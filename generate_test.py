# generate_test.py
from moviepy.editor import TextClip, ImageClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip
from PIL import Image, ImageDraw
from gtts import gTTS
import numpy as np
import os

# ------------------ SETTINGS ------------------
DURATION = 20                   # Duration of each video
TEXT_COLOR = "white"            # Text color
MUSIC_VOLUME = 0.3              # Background music volume (0-1)
FONT = "arial.ttf"              # Path to a valid TTF font file
FONTSIZE = 80                   # Font size for the verse text

# ------------------ FOLDERS ------------------
os.makedirs("output/youtube", exist_ok=True)
os.makedirs("output/reels", exist_ok=True)

# ------------------ READ VERSE ------------------
with open("verses.txt", "r", encoding="utf-8") as f:
    verse = f.readlines()[0].strip()  # Read the first verse

# ------------------ CREATE BACKGROUNDS ------------------
def create_bg(w, h, name):
    """Creates a simple gradient/circle background image."""
    img = Image.new("RGB", (w, h), (25, 40, 80))
    draw = ImageDraw.Draw(img)
    draw.ellipse((-300, -300, w+300, h+300), fill=(60, 90, 160))
    img.save(name)

create_bg(1920, 1080, "bg_youtube.jpg")
create_bg(1080, 1920, "bg_reels.jpg")

# ------------------ VOICEOVER ------------------
tts = gTTS(text=verse, lang="en")
tts.save("voice.mp3")

voice = AudioFileClip("voice.mp3").set_duration(DURATION)

# ------------------ BACKGROUND MUSIC ------------------
# Make sure you have a file music.mp3 in the folder
music = AudioFileClip("music.mp3").volumex(MUSIC_VOLUME).set_duration(DURATION)

# Combine music + voice
audio = CompositeAudioClip([music, voice])

# ------------------ CREATE VIDEO FUNCTION ------------------
def make_video(bg_image, size, output_file):
    """Creates a video with background, text, and audio."""
    # Background
    background = ImageClip(bg_image).set_duration(DURATION)
    
    # TextClip: text first, fontsize and font as kwargs
    text = TextClip(
        txt=verse,
        fontsize=FONTSIZE,
        font=FONT,
        color=TEXT_COLOR,
        method="label"  # ensures TTF fonts work
    )
    text = text.resize(width=size[0]-200).set_duration(DURATION).set_position("center")
    
    # Composite video + audio
    video = CompositeVideoClip([background, text]).set_audio(audio)
    video.write_videofile(output_file, fps=24)

# ------------------ GENERATE VIDEOS ------------------
make_video("bg_youtube.jpg", (1920,1080), "output/youtube/test.mp4")
make_video("bg_reels.jpg", (1080,1920), "output/reels/test.mp4")
