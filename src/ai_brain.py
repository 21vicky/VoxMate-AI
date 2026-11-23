import ollama
from src.conversation import ConversationManager


class AIBrain:
    def __init__(self, model="qwen2.5:1.5b"):
        self.model = model
        self.conversation = ConversationManager()

        self.system_prompt = {
            "role": "system",
            "content": (
                "You are VoxMate, a friendly personal AI voice assistant. "
                "Give clear, helpful and conversational answers. "
                "Keep responses concise and easy to understand."
            )
        }

        print("Connecting to VoxMate AI Brain...")

        try:
            ollama.chat(
                model=self.model,
                messages=[
                    self.system_prompt,
                    {"role": "user", "content": "Hello"}
                ]
            )
            print("VoxMate AI Brain connected successfully!")

        except Exception as e:
            print(f"AI connection error: {e}")

    def generate_response(self, user_message):
        try:
            self.conversation.add_message("user", user_message)

            messages = [
                self.system_prompt,
                *self.conversation.get_history()
            ]

            response = ollama.chat(
                model=self.model,
                messages=messages
            )

            answer = response["message"]["content"].strip()

            self.conversation.add_message("assistant", answer)

            return answer

        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"


if __name__ == "__main__":
    assistant = AIBrain()

    while True:
        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("VoxMate: Goodbye!")
            break

        answer = assistant.generate_response(user_input)
        print(f"\nVoxMate: {answer}")