class GameSession:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.phase = "idle"

        self.players = {}        # user_id: user_obj
        self.roles = {}          # user_id: Role instance
        self.alive = set()

        self.actions = {}        # night actions
        self.votes = {}          # secret votes

        self.corrupted_team = set()
        self.pure_team = set()

        self.mode = {
            "infection": False,
            "silent": False,
            "double": False
        }
