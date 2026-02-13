from pyrogram import filters
from core.manager import manager


def register_callbacks(app):

    # ==============================
    # NIGHT ACTION HANDLER
    # ==============================

    @app.on_callback_query(filters.regex("^act_"))
    async def act(_, cb):

        session = manager.get(cb.message.chat.id)

        if session.phase != "night":
            return await cb.answer("Not night phase.", show_alert=True)

        role = session.roles.get(cb.from_user.id)

        if not role:
            return await cb.answer("You are not in this game.", show_alert=True)

        try:
            target = int(cb.data.split("_")[1])
        except:
            return await cb.answer("Invalid target.", show_alert=True)

        # 🗡 Kill roles
        if role.name in ["Overseer", "Shade", "Ravager"]:
            session.actions["kill"][cb.from_user.id] = target

        # 🛡 Guardian
        elif role.name == "Guardian":
            session.actions["protect"][cb.from_user.id] = target

        # 🔮 Oracle
        elif role.name == "Oracle":
            session.actions["scan"][cb.from_user.id] = target

        # ☠ Corruptor
        elif role.name == "Corruptor" and session.mode.get("infection"):
            session.actions["convert"][cb.from_user.id] = target

        else:
            return await cb.answer("You cannot act.", show_alert=True)

        await cb.answer("Action locked.")
