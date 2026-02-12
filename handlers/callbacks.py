@ app.on_callback_query(filters.regex("^act_"))
async def act(_, cb):

    session = manager.get(cb.message.chat.id)

    role = session.roles.get(cb.from_user.id)
    if not role:
        return

    target = int(cb.data.split("_")[1])

    if role.name in ["Overseer", "Shade", "Ravager"]:
        session.actions["kill"][cb.from_user.id] = target

    elif role.name == "Guardian":
        session.actions["protect"][cb.from_user.id] = target

    elif role.name == "Oracle":
        session.actions["scan"][cb.from_user.id] = target

    elif role.name == "Corruptor" and session.mode["infection"]:
        session.actions["convert"][cb.from_user.id] = target

    await cb.answer("Action locked.")
