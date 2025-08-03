import pygame
import time

run = True
pygame.init()
screenW = 900
screenH = 600
screen = pygame.display.set_mode([screenW, screenH])
dt = 0
last_time = 0

########## CLASSES ##########

class move_object(pygame.sprite.Sprite):
    def __init__(self, startingPos):
        super().__init__()
        self.pos = pygame.math.Vector2(startingPos[0], startingPos[1])
        self.image = pygame.transform.rotozoom(
            pygame.image.load("SpriteImages\Default.png").convert_alpha(), 0, 0.05)
        self.baseImage = self.image
        self.hitboxRect = self.baseImage.get_rect(center = self.pos)
        self.rect = self.hitboxRect.copy()

        self.acceleration = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)

    def modify_pos_x(self, x):
        """Adds the input x value to the x position if no collisions are detected."""
        newX = self.pos.x + x
        if newX > 0 and newX < screenW:
            self.pos.x = newX
    
    def modify_pos_y(self, y):
        """Adds the input x value to the x position if no collisions are detected."""
        newY = self.pos.y + y
        if newY > 0 and newY < screenH:
            self.pos.y = newY
        else:
            self.velocity.y = 0

    def apply_gravity(self):
        self.acceleration.y += 1
    
    def update(self):
        self.hitboxRect.center = self.pos
        self.rect.center = self.pos

        self.velocity += self.acceleration
        self.modify_pos_x(self.velocity.x*dt)
        self.modify_pos_y(self.velocity.y*dt)

class bird(move_object):
    def __init__(self, startingPos):
        super().__init__(startingPos)
        self.image = pygame.transform.rotozoom(
            pygame.image.load("SpriteImages\BirdSprite.png").convert_alpha(), 0, 0.05)
        self.baseImage = self.image
        self.hitboxRect = self.baseImage.get_rect(center = self.pos)
        self.rect = self.hitboxRect.copy()

        self.jump_time = 0
        self.move_x_val = 50 
        self.max_x_vel = 100
        self.change_dir_multiplier = 1.75
    
    def update(self):
        super().update()
        keys = pygame.key.get_pressed()
        if self.check_jump(keys) and (time.time()-self.jump_time) > 0.25:
            self.jump_time = time.time()
            self.velocity.y = -350
            if self.check_left_input(keys):
                if self.velocity.x > -self.max_x_vel:
                    if self.velocity.x <= 0:
                        self.velocity.x += -self.move_x_val
                    else:
                        self.velocity.x += -self.move_x_val*self.change_dir_multiplier
            if self.check_right_input(keys):
                if self.velocity.x < self.max_x_vel:
                    if self.velocity.x >= 0:
                        self.velocity.x += self.move_x_val
                    else:
                        self.velocity.x += self.move_x_val*self.change_dir_multiplier
    
    def check_jump(self, keys):
        if keys[pygame.K_SPACE]:
            return True
    
    def check_left_input(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            return True
    
    def check_right_input(self, keys):
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            return True

def update_sprites(sprite_group):
    for sprite in sprite_group:
        sprite.update()

player_bird = bird((100, 100))

all_sprites = pygame.sprite.Group()
all_sprites.add(player_bird)
live_sprites = pygame.sprite.Group()
live_sprites.add(player_bird)

player_bird.apply_gravity()

########## MAIN LOOP ##########

while run:
    dt = time.time() - last_time
    last_time = time.time()
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    for sprite in all_sprites:
        drawnRect = sprite.rect.copy()
        screen.blit(pygame.transform.scale(sprite.image, (sprite.image.get_rect().w, sprite.image.get_rect().h)), 
                    (drawnRect.x, drawnRect.y))
    update_sprites(live_sprites)
    pygame.display.update()
pygame.quit()