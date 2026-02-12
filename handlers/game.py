from pyrogram import filters
from core.engine import start_game
from core.manager import manager
from database.db import get_rating, leaderboard


def register_game(app):

    # ==============================
    # START GAME
    # ==============================
    @app.on_message(filters.command("awaken") & filters.group)
    async def awaken(_, message):
        await start_game(app, message)


    # ==============================
    # JOIN BUTTON
    # ==============================
    @app.on_callback_query(filters.regex("^join$"))
    async def join(_, cb):

        session = manager.get(cb.message.chat.id)

        if session.phase not in ["idle", "joining"]:
            return await cb.answer(
                "Game already started.",
                show_alert=True
            )

        session.phase = "joining"
        session.players[cb.from_user.id] = cb.from_user

        await cb.answer("Joined")


    # ==============================
    # PLAYER RATING
    # ==============================
    @app.on_message(filters.command("rank"))
    async def rank(_, message):

        rating = get_rating(message.from_user.id)

        await message.reply(
            f"🏆 Your rating: {rating}"
        )


    # ==============================
    # LEADERBOARD
    # ==============================
    @app.on_message(filters.command("top"))
    async def top(_, message):

        data = leaderboard()

        if not data:
            return await message.reply("No players ranked yet.")

        text = "🏅 Dominion Leaderboard\n\n"

        for i, (uid, rating, wins) in enumerate(data, 1):
            text += f"{i}. {uid} — {rating} ({wins} wins)\n"

        await message.reply(text)
