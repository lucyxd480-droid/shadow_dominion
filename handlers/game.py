from pyrogram import filters
from core.engine import start_game
from core.manager import manager
from database.db import get_rating, leaderboard
from utils.keyboards import join_keyboard
from config import MIN_PLAYERS


def register_game(app):

    # ==============================
    # AWAKEN (JOIN PHASE + START)
    # ==============================
    @app.on_message(filters.command("awaken") & filters.group)
    async def awaken(_, message):

        session = manager.get(message.chat.id)

        # First time → Start joining phase
        if session.phase == "idle":
            session.phase = "joining"
            session.players = {}

            await message.reply(
                "Shadow Dominion is forming...\nClick Join to enter.",
                reply_markup=join_keyboard()
            )
            return

        # Second time → Try start game
        if session.phase == "joining":

            if len(session.players) < MIN_PLAYERS:
                return await message.reply("Not enough players.")

            await start_game(app, message)


    # ==============================
    # JOIN BUTTON
    # ==============================
    @app.on_callback_query(filters.regex("^join$"))
    async def join(_, cb):

        session = manager.get(cb.message.chat.id)

        if session.phase != "joining":
            return await cb.answer("Joining closed.", show_alert=True)

        session.players[cb.from_user.id] = cb.from_user

        await cb.answer("Joined.")


    # ==============================
    # PLAYER RATING
    # ==============================
    @app.on_message(filters.command("rank"))
    async def rank(_, message):

        rating = get_rating(message.from_user.id)

        await message.reply(f"🏆 Your rating: {rating}")


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
