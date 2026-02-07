import os
from PIL import Image
from moviepy.editor import (
    ImageClip,
    TextClip,
    CompositeVideoClip,
    AudioFileClip,
    CompositeAudioClip
)
from gtts import gTTS
from io import BytesIO
import requests
from diffusers import StableDiffusionPipeline
import torch

# ----------------------------
# CONFIGURATION
# ----------------------------
VERSE = "The Lord is my shepherd; I shall not want. — Psalm 23:1"
OUTPUT_VIDEO = "output_video.mp4"
VIDEO_SIZE = (1920, 1080)
DURATION = 12  # seconds
MUSIC_FILE = "music.mp3"
VOICE_FILE = "voice.mp3"
FONT_SIZE = 80
TEXT_COLOR = "white"
FONT = "Arial-Bold"

# ----------------------------
# 1. Generate background image with Stable Diffusion
# ----------------------------
def generate_background(verse):
    model_id = "runwayml/stable-diffusion-v1-5"  # You can pick another SD model
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")  # use GPU
    prompt = f"high quality, cinematic, realistic, inspirational, {verse}"
    image = pipe(prompt, height=1080, width=1920).images[0]
    image.save("background.jpg")
    return "background.jpg"

# ----------------------------
# 2. Generate voiceover using gTTS
# ----------------------------
def generate_voice(verse):
    tts = gTTS(text=verse, lang="en")
    tts.save(VOICE_FILE)
    return VOICE_FILE

# ----------------------------
# 3. Create video with MoviePy
# ----------------------------
def create_video(bg_path, voice_path, music_path):
    # Background clip
    bg_clip = ImageClip(bg_path).resize(VIDEO_SIZE).set_duration(DURATION)

    # Text clip
    txt_clip = TextClip(
        VERSE,
        fontsize=FONT_SIZE,
        font=FONT,
        color=TEXT_COLOR,
        method="label",
        size=(VIDEO_SIZE[0] - 200, None)  # wrap text nicely
    ).set_position("center").set_duration(DURATION)

    # Audio
    voice_clip = AudioFileClip(voice_path).set_duration(DURATION)
    if os.path.exists(music_path):
        music_clip = AudioFileClip(music_path).volumex(0.2).set_duration(DURATION)
        audio = CompositeAudioClip([voice_clip, music_clip])
    else:
        audio = voice_clip

    # Compose video
    video = CompositeVideoClip([bg_clip, txt_clip])
    video = video.set_audio(audio)
    video.write_videofile(OUTPUT_VIDEO, fps=24, codec="libx264", audio_codec="aac")

# ----------------------------
# MAIN
# ----------------------------
if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    bg = generate_background(VERSE)
    voice = generate_voice(VERSE)
    create_video(bg, voice, MUSIC_FILE)
    print("✅ Video generation complete!")
