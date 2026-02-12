# ===============================
# NIGHT RESOLUTION ENGINE
# ===============================

async def resolve_night(app, session):

    protected = set()

    # 🛡 PROTECT PHASE
    for actor, target in session.actions["protect"].items():
        if actor in session.alive:
            protected.add(target)


    # 🔮 SCAN PHASE
    for actor, target in session.actions["scan"].items():
        if actor in session.alive and target in session.roles:

            faction = session.roles[target].faction

            await app.send_message(
                actor,
                f"{session.players[target].first_name} is {faction}"
            )


    # ☠ CONVERT PHASE
    for actor, target in session.actions["convert"].items():

        if actor not in session.alive:
            continue

        if target not in session.alive:
            continue

        if session.roles[target].faction == "pure":

            from roles.corrupted import Shade

            session.roles[target] = Shade(target)

            session.corrupted_team.add(target)
            session.pure_team.discard(target)

            await app.send_message(
                session.chat_id,
                f"{session.players[target].first_name} has fallen to corruption..."
            )


    # 🗡 KILL PHASE
    for actor, target in session.actions["kill"].items():

        if actor not in session.alive:
            continue

        if target not in session.alive:
            continue

        if target in protected:
            continue

        # Kill happens
        session.alive.remove(target)

        await app.send_message(
            session.chat_id,
            f"{session.players[target].first_name} was consumed."
        )

        # 🎯 Hunter revenge trigger
        if session.roles[target].name == "Hunter":
            await hunter_revenge(app, session, target)

        break   # Only first valid kill executes



# ===============================
# HUNTER REVENGE FUNCTION
# ===============================

async def hunter_revenge(app, session, hunter_id):

    # Find corrupted players alive
    targets = [
        u for u in session.alive
        if session.roles[u].faction == "corrupted"
    ]

    if targets:

        target = targets[0]  # first corrupted

        session.alive.remove(target)

        await app.send_message(
            session.chat_id,
            f"Hunter's final shot eliminated {session.players[target].first_name}."
        )
