class ConversationManager:
    def __init__(self):
        self.history = []

    def add_message(self, role, content):
        self.history.append({
            "role": role,
            "content": content
        })

    def get_history(self):
        return self.history

    def clear(self):
        self.history.clear()


if __name__ == "__main__":
    conversation = ConversationManager()

    conversation.add_message("user", "Hello VoxMate!")
    conversation.add_message("assistant", "Hello! How can I help you?")

    print("Conversation History:")
    print(conversation.get_history())

    conversation.clear()

    print("\nAfter clearing:")
    print(conversation.get_history())