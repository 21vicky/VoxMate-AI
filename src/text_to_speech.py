
import asyncio
import edge_tts
import os


class TextToSpeech:
    def __init__(self, voice="en-US-AriaNeural"):
        self.voice = voice

    async def _generate_audio(self, text, output_path):
        communicate = edge_tts.Communicate(
            text,
            self.voice
        )

        await communicate.save(output_path)

    def generate_speech(self, text):
        """Generate audio and return its file path."""
        if not text:
            return None

        try:
            output_path = "outputs/response.mp3"

            os.makedirs("outputs", exist_ok=True)

            asyncio.run(
                self._generate_audio(text, output_path)
            )

            return os.path.abspath(output_path)

        except Exception as e:
            print(f"Speech generation error: {e}")
            return None

    def speak(self, text):
        if not text:
            return "No text provided."

        try:
            audio_path = self.generate_speech(text)

            if not audio_path:
                return "Speech generation failed."

            print(f"Audio saved: {audio_path}")

            os.startfile(audio_path)

            return "Speech generated successfully!"

        except Exception as e:
            return f"Text-to-Speech error: {str(e)}"


if __name__ == "__main__":
    tts = TextToSpeech()

    message = input("Enter text for VoxMate to speak: ")

    result = tts.speak(message)

    print(result)
