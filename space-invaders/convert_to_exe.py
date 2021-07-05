import cx_Freeze

description = "A Space Invaders-style game written in Python with Pygame."
include_files = ["assets/images/background.jpg",
                 "assets/images/bullet-fire-sml1.png",
                 "assets/images/bullet-ms-sml1.png",
                 "assets/images/player1.png",
                 "assets/images/enemy-xsml.png",
                 "assets/images/mothership.png",
                 "assets/images/heart.png"]

cx_Freeze.setup(name = "space_reinvaders",
      version = "1.1",
      description = description,
      options = {"build.exe": {"packages": ["pygame"],
                               "include_files": include_files}},
      executables = [cx_Freeze.Executable("app.py")])
