async def resolve_night(app, session):

    if not session.actions:
        return

    # Sort by role priority
    sorted_actions = sorted(
        session.actions.items(),
        key=lambda x: session.roles[x[0]].priority,
        reverse=True
    )

    for actor, target in sorted_actions:

        if actor not in session.alive:
            continue

        if target not in session.alive:
            continue

        role = session.roles[actor]

        if role.faction == "corrupted":
            session.alive.remove(target)
            await app.send_message(
                session.chat_id,
                f"{session.players[target].first_name} was consumed."
            )
            break
