# from datetime import datetime
# from moviepy import AudioFileClip
# import voiceover

# MAX_WORDS_PER_COMMENT = 100
# MIN_COMMENTS_FOR_FINISH = 4
# MIN_DURATION = 20
# MAX_DURATION = 58

# class VideoScript:
#     title = ""
#     fileName = ""
#     titleSCFile = ""
#     url = ""
#     totalDuration = 0
#     frames = []

#     def __init__(self, url, title, fileId) -> None:
#         self.fileName = f"{datetime.today().strftime('%Y-%m-%d')}-{fileId}"
#         self.url = url
#         self.title = title
#         self.titleAudioClip = self.__createVoiceOver("title", title)

#     def canBeFinished(self) -> bool:
#         return (len(self.frames) > 0) and (self.totalDuration > MIN_DURATION)

#     def canQuickFinish(self) -> bool:
#         return (len(self.frames) >= MIN_COMMENTS_FOR_FINISH) and (self.totalDuration > MIN_DURATION)

#     def addCommentScene(self, text, commentId) -> None:
#         wordCount = len(text.split())
#         if (wordCount > MAX_WORDS_PER_COMMENT):
#             return True
#         frame = ScreenshotScene(text, commentId)
#         frame.audioClip = self.__createVoiceOver(commentId, text)
#         if (frame.audioClip == None):
#             return True
#         self.frames.append(frame)

#     def getDuration(self):
#         return self.totalDuration

#     def getFileName(self):
#         return self.fileName

#     def __createVoiceOver(self, name, text):
#         file_path = voiceover.create_voice_over(f"{self.fileName}-{name}", text)
#         audioClip = AudioFileClip(file_path)
#         if (self.totalDuration + audioClip.duration > MAX_DURATION):
#             return None
#         self.totalDuration += audioClip.duration
#         return audioClip


# class ScreenshotScene:
#     text = ""
#     screenShotFile = ""
#     commentId = ""

#     def __init__(self, text, commentId) -> None:
#         self.text = text
#         self.commentId = commentId


from datetime import datetime
from moviepy import AudioFileClip
import voiceover

MAX_WORDS_PER_COMMENT = 100
MIN_COMMENTS_FOR_FINISH = 4
MIN_DURATION = 20
MAX_DURATION = 58

class VideoScript:
    title = ""
    fileName = ""
    titleSCFile = ""
    url = ""
    totalDuration = 0
    frames = []

    def __init__(self, url, title, fileId) -> None:
        self.fileName = f"{datetime.today().strftime('%Y-%m-%d')}-{fileId}"
        self.url = url
        self.title = title
        self.titleAudioClip = self.__createVoiceOver("title", title)
        # If titleAudioClip is None, it means title was deleted/removed (unlikely, but possible)
        # Handle that case if needed

    def canBeFinished(self) -> bool:
        return (len(self.frames) > 0) and (self.totalDuration > MIN_DURATION)

    def canQuickFinish(self) -> bool:
        return (len(self.frames) >= MIN_COMMENTS_FOR_FINISH) and (self.totalDuration > MIN_DURATION)

    def addCommentScene(self, text, commentId) -> None:
        wordCount = len(text.split())
        if wordCount > MAX_WORDS_PER_COMMENT:
            # Too long, skip it but return True so we don't try again
            return True

        file_path = voiceover.create_voice_over(f"{self.fileName}-{commentId}", text)

        # If no voiceover file was created (deleted or removed comment), skip this scene
        if file_path is None:
            print(f"Skipping comment {commentId} because no voiceover was generated.")
            return True

        # Now we know we have a file_path, let's try to create the clip
        audioClip = AudioFileClip(file_path)

        # Check if adding this clip exceeds max duration
        if self.totalDuration + audioClip.duration > MAX_DURATION:
            # If it exceeds, return True to stop adding more scenes
            return True

        self.totalDuration += audioClip.duration

        frame = ScreenshotScene(text, commentId)
        frame.audioClip = audioClip
        self.frames.append(frame)
        # Returning nothing means we added the scene successfully

    def getDuration(self):
        return self.totalDuration

    def getFileName(self):
        return self.fileName

    def __createVoiceOver(self, name, text):
        file_path = voiceover.create_voice_over(f"{self.fileName}-{name}", text)

        # If voiceover wasn't created (None), return None
        if file_path is None:
            return None

        audioClip = AudioFileClip(file_path)
        if self.totalDuration + audioClip.duration > MAX_DURATION:
            # If adding this would exceed max duration, return None
            return None

        self.totalDuration += audioClip.duration
        return audioClip


class ScreenshotScene:
    text = ""
    screenShotFile = ""
    commentId = ""

    def __init__(self, text, commentId) -> None:
        self.text = text
        self.commentId = commentId
