import whisper
import os

class SpeechToText:

    def __init__(self, model_name="tiny"):
        print("Loading Whisper model...")
        self.model = whisper.load_model(model_name)
        print("Whisper model loaded successfully!")

    def transcribe(self, audio_path):

        if not audio_path:
            return "No audio file provided."

        if not os.path.exists(audio_path):
            return "Audio file not found."

        try:
            result = self.model.transcribe(
                audio_path,
                fp16=False
            )

            return result["text"].strip()

        except Exception as e:
            return f"Transcription error: {str(e)}"


if __name__ == "__main__":

    assistant = SpeechToText()

    audio_file = input("Enter audio file path: ")

    text = assistant.transcribe(audio_file)

    print("\nTranscribed Text:")
    print(text)