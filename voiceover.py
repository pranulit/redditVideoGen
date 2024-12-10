from gtts import gTTS
import os

voiceoverDir = "Voiceovers"

def create_voice_over(fileName, text):
    os.makedirs(voiceoverDir, exist_ok=True)
    filePath = f"{voiceoverDir}/{fileName}.mp3"
    
    # Create a TTS object and save the file
    tts = gTTS(text=text, lang='en')
    tts.save(filePath)
    
    return filePath



