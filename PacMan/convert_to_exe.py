import cx_Freeze

description = "Pac-Man written in Python with Pygame."
include_files = ["assets/blinky.png",
                 "assets/cherry.png",
                 "assets/clyde.png",
                 "assets/COLLECTIBLES.txt",
                 "assets/ghost-pellet.png",
                 "assets/inky.png",
                 "assets/Mozart-NBP.ttf",
                 "assets/pac-dot.png",
                 "assets/pacman.png",
                 "assets/pinky.png",
                 "assets/WALLS.txt"]

cx_Freeze.setup(name = "pacman",
      version = "1.1",
      description = description,
      options = {"build.exe": {"packages": ["pygame"],
                               "include_files": include_files}},
      executables = [cx_Freeze.Executable("pacman.py")])
