from roles.base import Role

class Overseer(Role):
    name = "Overseer"
    faction = "corrupted"
    priority = 3

class Shade(Role):
    name = "Shade"
    faction = "corrupted"
    priority = 3

class Corruptor(Role):
    name = "Corruptor"
    faction = "corrupted"
    priority = 4
    convert_once = True

class Ravager(Role):
    name = "Ravager"
    faction = "corrupted"
    priority = 2
    double_used = False
