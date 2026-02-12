class Role:
    name = "Base"
    faction = "neutral"
    priority = 0

    def __init__(self, user_id):
        self.user_id = user_id

    async def night_action(self, session, target):
        pass
