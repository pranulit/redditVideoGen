# from gtts import gTTS
# import os

# voiceoverDir = "Voiceovers"

# def create_voice_over(fileName, text):
#     os.makedirs(voiceoverDir, exist_ok=True)
#     filePath = f"{voiceoverDir}/{fileName}.mp3"
    
#     # Create a TTS object and save the file
#     tts = gTTS(text=text, lang='en')
#     tts.save(filePath)
    
#     return filePath



from gtts import gTTS
import os

voiceoverDir = "Voiceovers"

def create_voice_over(fileName, text):
    # If the comment is deleted or removed, skip creating a voiceover
    if text.strip().lower() in ["[deleted]", "[removed]"]:
        print(f"Skipping voiceover for {fileName}: Comment is deleted/removed.")
        return None
    
    os.makedirs(voiceoverDir, exist_ok=True)
    filePath = f"{voiceoverDir}/{fileName}.mp3"
    
    # Create a TTS object and save the file
    tts = gTTS(text=text, lang='en')
    tts.save(filePath)
    
    return filePath
