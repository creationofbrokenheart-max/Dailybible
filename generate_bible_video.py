import os
from gtts import gTTS
from moviepy.editor import ImageClip, TextClip, CompositeVideoClip, AudioFileClip, CompositeAudioClip

# ---------- CONFIG ----------
VERSE = "The Lord is my shepherd; I shall not want. — Psalm 23:1"
BG_IMAGE = "bg_youtube.jpg"  # Make sure you have a good image here
OUTPUT_VIDEO = "output/youtube/test.mp4"
FONT = "Arial-Bold"  # Ensure GitHub runner has a basic font
TEXT_COLOR = "white"
VIDEO_SIZE = (1920, 1080)
DURATION = 15  # seconds
VOICE_FILE = "voice.mp3"
MUSIC_FILE = "music.mp3"
MUSIC_VOLUME = 0.2
# -----------------------------

os.makedirs(os.path.dirname(OUTPUT_VIDEO), exist_ok=True)

# 1️⃣ Create voiceover using gTTS
tts = gTTS(VERSE)
tts.save(VOICE_FILE)

# 2️⃣ Load audio clips
voice = AudioFileClip(VOICE_FILE)

if os.path.exists(MUSIC_FILE):
    music = AudioFileClip(MUSIC_FILE).volumex(MUSIC_VOLUME)
else:
    music = None

# 3️⃣ Combine audio
if music:
    audio = CompositeAudioClip([voice.set_duration(DURATION), music.set_duration(DURATION)])
else:
    audio = voice.set_duration(DURATION)

# 4️⃣ Create text clip
text_clip = TextClip(
    VERSE,
    fontsize=70,
    font=FONT,
    color=TEXT_COLOR,
    method="label",
    size=(VIDEO_SIZE[0] - 200, None),
    align="center"
).set_position("center").set_duration(DURATION)

# 5️⃣ Create background clip
background_clip = ImageClip(BG_IMAGE).resize(VIDEO_SIZE).set_duration(DURATION)

# 6️⃣ Composite video
video = CompositeVideoClip([background_clip, text_clip])
video = video.set_audio(audio)

# 7️⃣ Export
video.write_videofile(OUTPUT_VIDEO, fps=24)
print("Video generated successfully!")
