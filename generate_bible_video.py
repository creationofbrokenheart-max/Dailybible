import os
from gtts import gTTS
# Video clips
from moviepy.video.VideoClip import TextClip, ImageClip, CompositeVideoClip

# Audio clips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.CompositeAudioClip import CompositeAudioClip

print("moviepy is working")



# --- Configuration ---
VERSE = "The Lord is my shepherd; I shall not want. — Psalm 23:1"
VOICE_FILE = "voice.mp3"
MUSIC_FILE = "music.mp3"  # Put your background music here
OUTPUT_FILE = "output_video.mp4"
VIDEO_SIZE = (1920, 1080)
DURATION = 15  # seconds for the video
TEXT_COLOR = "white"
FONT_SIZE = 70
FONT = "Arial-Bold"  # Make sure this font is available on runner or OS

# --- Generate voiceover ---
tts = gTTS(text=VERSE, lang='en')
tts.save(VOICE_FILE)

# --- Optional: Use your own cinematic image ---
# For real AI-generated backgrounds, you can integrate Stable Diffusion here
BACKGROUND_IMAGE = "bg_youtube.jpg"  # Replace with your cinematic image

# --- Load clips ---
voice = AudioFileClip(VOICE_FILE)

# Music (optional)
if os.path.exists(MUSIC_FILE):
    music = AudioFileClip(MUSIC_FILE).volumex(0.3).set_duration(DURATION)
    audio = CompositeAudioClip([voice.set_duration(DURATION), music])
else:
    audio = voice.set_duration(DURATION)

# Background image clip
background = ImageClip(BACKGROUND_IMAGE).set_duration(DURATION).resize(VIDEO_SIZE)

# Text overlay
text = TextClip(
    VERSE,
    fontsize=FONT_SIZE,
    color=TEXT_COLOR,
    font=FONT,
    method="caption",
    size=(VIDEO_SIZE[0]*0.8, None),  # wrap text to 80% width
).set_position("center").set_duration(DURATION)

# Composite video
final_clip = CompositeVideoClip([background, text])
final_clip = final_clip.set_audio(audio)

# Ensure output directory exists
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

# Write final video
final_clip.write_videofile(OUTPUT_FILE, fps=24)
