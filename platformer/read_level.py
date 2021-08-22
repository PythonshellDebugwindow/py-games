from player import Player
from surfaces import Platform, Barrier

def read_level(n):
    f = open(f"assets/levels/{n}.txt")
    player = None
    platforms = []
    cur = ""
    
    for line in filter(None, f.read().split("\n")):
        if line == "" or line[0] == "#":
            pass
        elif line[0] == "[":
            cur = line[1:-1]
        elif cur == "Platform":
            platforms.append(Platform(*get_ints(line)))
        elif cur == "NonSolidPlatform":
            platforms.append(Platform(*get_ints(line), is_solid=False))
        elif cur == "Barrier":
            platforms.append(Barrier(*get_ints(line)))
        elif cur == "Player":
            player = Player(*get_ints(line))
    
    f.close()
    assert player != None, f"No player provided in Level {n}"
    return (player, platforms)

def get_ints(s):
    return map(int, s.split())
