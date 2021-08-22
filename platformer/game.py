import pygame, sys
from read_level import read_level

def die():
    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    
    SIZE = 800, 600
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("Platformer")

    cur_level = 1
    player, platforms = read_level(cur_level)

    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                die()
        
        screen.fill((65, 180, 245))

        player.set_is_falling(True)
        for platform in platforms:
            if platform.is_colliding(*player.get_xy_wh()):
                player.set_is_falling(False)
            platform.draw(screen)
        
        player.move_from_keys(pygame.key.get_pressed())
        player.update()
        if player.y > SIZE[1]:
            player.lose_health()
            if player.is_dead():
                print("You have Died! How Unfortunate!")
            h = player.health
            player, platforms = read_level(cur_level)
            if h > 0:
                player.health = h
        elif player.x > SIZE[0]:
            print("Next level")
            cur_level += 1
            h = player.health
            player, platforms = read_level(cur_level)
            player.health = h
##        cur_level==3 and print(player.x,round(player.y))
        
        player.draw(screen)
        
        pygame.display.flip()
        clock.tick(100)
