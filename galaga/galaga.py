import pygame, sys

class EnemyShip:
    enemy_imgs = [pygame.image.load(f"assets/enemy-{i}.png") for i in range(1)]
    
    def __init__(self, x, y, img_idx):
        self.x = x
        self.y = y
        self.rot = 0
        self.img_idx = img_idx
    def get_formation_pos(self, fmtn, fmtn_idx):
        pass
    def draw(self, screen):
        screen.blit(EnemyShip.enemy_imgs[self.img_idx], (self.x, self.y))

def die():
    pygame.quit()
    sys.exit()

def main():
    pygame.init()
    size = width, height = (800, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Galaga")
    
    player_img = pygame.image.load("assets/ship.png")
    player_width, player_height = player_img.get_size()
    
    player_xmax = width - player_width - 10
    player_ymax = height - player_height - 10

    player_x = (width // 2) - (width // 2) % 10
    player_y = player_ymax

    player_x_speed = 10
    
    bullet_positions = []
    bullet_speed = 5
    bullet_img = pygame.image.load("assets/bullet.png")
    
    bullet_fire_tick = 0
    bullet_fire_delay = 8

    enemies = []
##    enemies.append(Enemy(40,40))#TEST

    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
##                s = (15, 26)
##                pygame.image.save(pygame.transform.scale(bullet_img,s),"assets/bullet4.png")
                die()

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and player_x>10:
            player_x -= player_x_speed
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and player_x<player_xmax:
            player_x += player_x_speed
        bullet_fire_tick += 1
        if keys[pygame.K_SPACE] and bullet_fire_tick >= bullet_fire_delay:
            bullet_positions.append([player_x + 19, player_y])
            bullet_fire_tick = 0
        
        screen.fill((0, 0, 0))
        
        screen.blit(player_img, (player_x, player_y))

        i = 0
        while i < len(bullet_positions):
            bullet_positions[i][1] -= bullet_speed
            if bullet_positions[i][1] < -26:
                bullet_positions.pop(i)
            else:
                screen.blit(bullet_img, bullet_positions[i])
                i += 1
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("ERROR", e)
        print("TYPE", type(e))
        die()
