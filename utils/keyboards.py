from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# ==============================
# JOIN BUTTON
# ==============================
def join_keyboard():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("⚔ Join Dominion", callback_data="join")]]
    )


# ==============================
# PLAYER TARGET BUTTONS
# ==============================
def player_kb(players, prefix):

    buttons = []

    for uid, user in players.items():
        buttons.append(
            [InlineKeyboardButton(
                user.first_name,
                callback_data=f"{prefix}_{uid}"
            )]
        )

    return InlineKeyboardMarkup(buttons)
