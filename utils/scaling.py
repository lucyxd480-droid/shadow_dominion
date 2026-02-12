import random
from roles.corrupted import Overseer, Shade, Corruptor, Ravager
from roles.pure import Luminary, Oracle, Guardian, Hunter, Watcher, Martyr

def assign_roles(player_ids):

    total = len(player_ids)
    random.shuffle(player_ids)

    corrupted_count = max(1, total // 5)

    corrupted_roles = []
    pure_roles = []

    if corrupted_count >= 1:
        corrupted_roles.append(Overseer(player_ids[0]))

    for i in range(1, corrupted_count):
        corrupted_roles.append(Shade(player_ids[i]))

    pure_ids = player_ids[corrupted_count:]

    # Special pure roles
    specials = []

    if total >= 4:
        specials.append(Oracle)
    if total >= 5:
        specials.append(Guardian)
    if total >= 6:
        specials.append(Hunter)
    if total >= 8:
        specials.append(Watcher)
    if total >= 10:
        specials.append(Martyr)

    for role_cls in specials:
        if pure_ids:
            pure_roles.append(role_cls(pure_ids.pop(0)))

    for uid in pure_ids:
        pure_roles.append(Luminary(uid))

    return corrupted_roles + pure_roles
