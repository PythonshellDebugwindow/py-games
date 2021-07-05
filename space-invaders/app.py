'''
    Main App file
    Simply instantiates the Game class and runs it
    with the config parameters specified in
    "window_size" and "title"
'''
import pygame, sys
from engine.game_env import Game

def main():
    fl = open("assets/txt/SCORE.txt", "w")
    fl.write("0")
    fl.close()
    window_size = (1000, 750)
    title = "Space Reinvaders"
    g = Game(window_size, title)
    g.run()

if __name__ == "__main__":
    try:
        main()
##    except SystemExit as e:
    except Exception as e:
        print("ERROR", e)
        import time
        pygame.quit()
        print("Sleeping for 2s")
        time.sleep(2)
        sys.exit()
##    except Exception as e:
##        main()
    finally:
        print("Bye bye")
        pygame.quit()
        sys.exit()
