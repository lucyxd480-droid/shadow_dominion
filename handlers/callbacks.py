from pyrogram import filters
from core.manager import manager

def register_callbacks(app):

    @app.on_callback_query(filters.regex("^act_"))
    async def act(_, cb):

        session = manager.get(cb.message.chat.id)
        target = int(cb.data.split("_")[1])

        session.actions[cb.from_user.id] = target
        await cb.answer("Action locked.")

    @app.on_callback_query(filters.regex("^vote_"))
    async def vote(_, cb):

        session = manager.get(cb.message.chat.id)
        target = int(cb.data.split("_")[1])

        session.votes[target] = session.votes.get(target, 0) + 1
        await cb.answer("Vote counted.")
