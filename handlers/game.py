from pyrogram import filters
from core.engine import start_game
from core.manager import manager

def register_game(app):

    @app.on_message(filters.command("awaken") & filters.group)
    async def awaken(_, message):
        await start_game(app, message)

    @app.on_callback_query(filters.regex("^join$"))
    async def join(_, cb):

        session = manager.get(cb.message.chat.id)

        if session.phase != "idle" and session.phase != "joining":
            return await cb.answer("Game already started", show_alert=True)

        session.phase = "joining"
        session.players[cb.from_user.id] = cb.from_user

        await cb.answer("Joined.")
