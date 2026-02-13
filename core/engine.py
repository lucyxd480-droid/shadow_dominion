import asyncio
from config import *
from utils.texts import NIGHT, DAY, VOTE
from utils.scaling import assign_roles
from core.manager import manager
from core.resolver import resolve_night
from database.db import add_win, add_loss
from utils.keyboards import player_kb


# ==============================
# GAME START
# ==============================

async def start_game(app, message):

    chat_id = message.chat.id
    session = manager.get(chat_id)

    if session.phase not in ["idle", "joining"]:
    return await message.reply("Game already running.")

    if len(session.players) < MIN_PLAYERS:
        return await message.reply("Not enough players.")

    session.phase = "starting"

    role_objects = assign_roles(list(session.players.keys()))

    session.roles = {}
    session.alive = set()
    session.corrupted_team = set()
    session.pure_team = set()

    for role in role_objects:
        session.roles[role.user_id] = role
        session.alive.add(role.user_id)

        if role.faction == "corrupted":
            session.corrupted_team.add(role.user_id)
        else:
            session.pure_team.add(role.user_id)

    # DM roles
    for uid, role in session.roles.items():
        await app.send_message(uid, f"Your role: {role.name}")

    # Secret corrupted reveal
    for uid in session.corrupted_team:
        others = [
            session.players[x].first_name
            for x in session.corrupted_team if x != uid
        ]
        if others:
            await app.send_message(uid, "Corrupted team:\n" + "\n".join(others))

    await asyncio.sleep(2)

    await night_phase(app, session)


# ==============================
# NIGHT PHASE
# ==============================

async def night_phase(app, session):

    session.phase = "night"

    session.actions = {
        "kill": {},
        "protect": {},
        "scan": {},
        "convert": {}
    }

    await app.send_message(session.chat_id, NIGHT)

    for uid in session.alive:

        role = session.roles[uid]

        targets = {
            x: session.players[x]
            for x in session.alive
            if x != uid
        }

        if role.name in ["Overseer", "Shade", "Ravager"]:
            await app.send_message(
                uid,
                "🗡 Choose target to eliminate:",
                reply_markup=player_kb(targets, "act")
            )

        elif role.name == "Guardian":
            await app.send_message(
                uid,
                "🛡 Choose someone to protect:",
                reply_markup=player_kb(targets, "act")
            )

        elif role.name == "Oracle":
            await app.send_message(
                uid,
                "🔮 Choose someone to scan:",
                reply_markup=player_kb(targets, "act")
            )

        elif role.name == "Corruptor" and session.mode["infection"]:
            await app.send_message(
                uid,
                "☠ Choose someone to convert:",
                reply_markup=player_kb(targets, "act")
            )

    await asyncio.sleep(NIGHT_TIME)

    await resolve_night(app, session)

    await day_phase(app, session)


# ==============================
# DAY PHASE
# ==============================

async def day_phase(app, session):

    session.phase = "day"

    await app.send_message(session.chat_id, DAY)

    await asyncio.sleep(DAY_TIME)

    await vote_phase(app, session)


# ==============================
# VOTE PHASE
# ==============================

async def vote_phase(app, session):

    session.phase = "vote"
    session.votes = {}

    alive_players = {
        uid: session.players[uid]
        for uid in session.alive
    }

    await app.send_message(
        session.chat_id,
        VOTE,
        reply_markup=player_kb(alive_players, "vote")
    )

    await asyncio.sleep(VOTE_TIME)

    if session.votes:
        target = max(session.votes, key=session.votes.get)

        if target in session.alive:
            session.alive.remove(target)

            await app.send_message(
                session.chat_id,
                f"{session.players[target].first_name} was executed."
            )

    await win_check(app, session)


# ==============================
# WIN CHECK (CONNECTED TO RANKING)
# ==============================

async def win_check(app, session):

    corrupted_alive = sum(
        1 for u in session.alive
        if session.roles[u].faction == "corrupted"
    )

    pure_alive = sum(
        1 for u in session.alive
        if session.roles[u].faction == "pure"
    )

    # 🌕 PURE WIN
    if corrupted_alive == 0:

        await app.send_message(session.chat_id, "🌕 Pure wins.")

        for uid, role in session.roles.items():
            if role.faction == "pure":
                survived = uid in session.alive
                add_win(uid, survived)
            else:
                add_loss(uid)

        reset_session(session)
        return


    # 🌑 CORRUPTED WIN
    if corrupted_alive >= pure_alive:

        await app.send_message(session.chat_id, "🌑 Corrupted wins.")

        for uid, role in session.roles.items():
            if role.faction == "corrupted":
                survived = uid in session.alive
                add_win(uid, survived)
            else:
                add_loss(uid)

        reset_session(session)
        return


    # Continue game
    await night_phase(app, session)


# ==============================
# RESET SESSION
# ==============================

def reset_session(session):

    session.phase = "idle"
    session.alive.clear()
    session.players.clear()
    session.roles.clear()
    session.corrupted_team.clear()
    session.pure_team.clear()
    session.actions.clear()
