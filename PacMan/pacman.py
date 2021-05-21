import pygame, sys, math, random
from ghost import Ghost
from collectible import Collectible
from maze import Maze

def die():
    pygame.quit()
    sys.exit()

def main():
    size = width, height = 800, 550
    pygame.init()
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pac-Man")
    
    maze = Maze()
    
    pacman_pos = [400, 270]
    pacman_speed = 20
    game_delay = 200
    game_tick = game_delay
    
    pacman_dir = 1 #0123 = URDL
    pacman_mouth_size = 0
    pacman_mouth_speed = 0.1
    
    pacman_img = pygame.image.load("assets/pacman.png")
    pacman_img_y = 0
    
    pacman_score = 0
    pacman_lives = 3
    pacman_life_img = pygame.image.load("assets/pacman.png")
    pacman_life_img = pacman_life_img.subsurface(0, 0, 50, 50)
    pacman_life_img = pygame.transform.scale(pacman_life_img, (35, 35))
    pacman_life_img = pygame.transform.rotate(pacman_life_img, 270)
    
    pacman_has_pellet = False
    pacman_pellet_duration = 30
    pacman_pellet_tick = 0
    pacman_pellet_mini_img = pygame.image.load("assets/pac-dot.png")
    pacman_pellet_mini_img = pygame.transform.scale(pacman_pellet_mini_img,
                                                    (30, 30))
    
    ghosts = [Ghost([360, 310], random.randint(0, 3), "assets/inky.png"),
              Ghost([400, 310], random.randint(0, 3), "assets/blinky.png"),
              Ghost([360, 350], random.randint(0, 3), "assets/pinky.png"),
              Ghost([400, 350], random.randint(0, 3), "assets/clyde.png")]
    
    collectibles = Collectible.get_collectibles()
    num_pac_dots = len([c for c in collectibles if c.type == "pac-dot"])
    
    font = pygame.font.Font("assets/Mozart-NBP.ttf", 50)
    text_lives = font.render("Lives:", False, (255, 255, 255))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                die()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    pacman_dir = 0
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    pacman_dir = 1  
                elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    pacman_dir = 2
                elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    pacman_dir = 3
                elif event.key==pygame.K_BACKSLASH:pacman_lives-=1
                elif event.key==pygame.K_p:pacman_has_pellet=True
        
        game_tick += 1
        if game_tick > game_delay:
            game_tick = 0
            
            if pacman_dir == 0:
                pacman_pos[1] -= pacman_speed
            elif pacman_dir == 1:
                pacman_pos[0] += pacman_speed
            elif pacman_dir == 2:
                pacman_pos[1] += pacman_speed
            elif pacman_dir == 3:
                pacman_pos[0] -= pacman_speed

            if pacman_pos[0] < 0:
                pacman_pos[0] = 800
            elif pacman_pos[0] >= 800:
                pacman_pos[0] = 0
            
            if maze.is_colliding(pacman_pos, 40):
                pacman_dir = (pacman_dir % 2 * 2 + 2) - pacman_dir
                
                if pacman_dir == 0:
                    pacman_pos[1] -= pacman_speed
                elif pacman_dir == 1:
                    pacman_pos[0] += pacman_speed
                elif pacman_dir == 2:
                    pacman_pos[1] += pacman_speed
                elif pacman_dir == 3:
                    pacman_pos[0] -= pacman_speed
            
            pacman_img_y += 58
            if pacman_img_y >= 409:
                pacman_img_y = 0
            
            pacman_mouth_size += pacman_mouth_speed
            if pacman_mouth_size <= 0 or pacman_mouth_size >= 45:
                pacman_mouth_speed *= -1
            
            if pacman_has_pellet:
                pacman_pellet_tick += 1
                if pacman_pellet_tick >= pacman_pellet_duration:
                    pacman_pellet_tick = 0
                    pacman_has_pellet = False
            
            for i in range(len(collectibles)):
                if collectibles[i].is_colliding(pacman_pos):
                    if collectibles[i].type == "pac-dot":
                        num_pac_dots -= 1
                        if num_pac_dots <= 0:
                            print("You won the level! Exiting...")
                            die()
                    elif collectibles[i].type == "fruit":
                        pacman_score += 5
                    elif collectibles[i].type == "pac-pellet":
                        pacman_has_pellet = True
                    collectibles.pop(i)
                    break
            
            for i in range(len(ghosts)):
                ghosts[i].move(maze)
                if ghosts[i].is_colliding(pacman_pos, 40):
                    if pacman_has_pellet:
                        pacman_score += 15
                        if i == 0:
                            ghosts[0].pos = [360, 310]
                        elif i == 1:
                            ghosts[1].pos = [400, 310]
                        elif i == 2:
                            ghosts[2].pos = [360, 350]
                        elif i == 3:
                            ghosts[3].pos = [400, 350]
                        ghosts[i].dir = random.randint(0, 3)
                    else:
                        pacman_lives -= 1
                        if pacman_lives <= 0:
                            print("You died! Exiting...")
                            die()
        
        screen.fill((0, 0, 0))
        
        maze.draw(screen)
        
        for c in collectibles:
            c.draw(screen)
        
        img = pygame.transform.scale(pacman_img.subsurface(0,pacman_img_y,
                                                           50,50),(40,40))
        screen.blit(pygame.transform.rotate(img, pacman_dir * -90), pacman_pos)
        
        for ghost in ghosts:
            ghost.draw(screen, pacman_has_pellet)
        
        screen.blit(font.render("Score: " + str(pacman_score), False,
                                (255, 255, 255)), (27, 13))
        screen.blit(text_lives, (417, 13))
        for i in range(pacman_lives):
            screen.blit(pacman_life_img, (537 + i * 50, 13))
        if pacman_has_pellet:
            w = pacman_pellet_duration - pacman_pellet_tick
            screen.blit(pacman_pellet_mini_img.subsurface(0,0,w,30),(737,17))
        
        pygame.display.flip()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR", e)
        print("TYPE", type(e))
        die()
    finally:
        print("Bye Bye")
        die()
