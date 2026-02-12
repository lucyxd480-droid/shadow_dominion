from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def join_kb():
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("Join Dominion", callback_data="join")]]
    )

def player_kb(players, prefix):
    buttons = []
    for uid, user in players.items():
        buttons.append(
            [InlineKeyboardButton(user.first_name, callback_data=f"{prefix}_{uid}")]
        )
    return InlineKeyboardMarkup(buttons)
