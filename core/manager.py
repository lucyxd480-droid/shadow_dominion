from core.session import GameSession

class SessionManager:
    def __init__(self):
        self.sessions = {}

    def get(self, chat_id):
        if chat_id not in self.sessions:
            self.sessions[chat_id] = GameSession(chat_id)
        return self.sessions[chat_id]

manager = SessionManager()
