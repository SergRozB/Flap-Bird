import pygame
import time
import camera_script

run = True
pygame.init()
screenW = 900
screenH = 600
screen = pygame.display.set_mode([screenW, screenH])
dt = 0
last_time = 0

##########  CLASSES  ##########

class move_object(pygame.sprite.Sprite):
    def __init__(self, starting_pos, image_path="SpriteImages\Default.png", size=0.05):
        super().__init__()
        self.pos = pygame.math.Vector2(starting_pos[0], starting_pos[1])
        self.image = pygame.transform.rotozoom(
            pygame.image.load(image_path).convert_alpha(), 0, size)
        self.base_image = self.image
        self.hitbox_rect = self.base_image.get_rect(center = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.old_rect = self.hitbox_rect.copy()

        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 50

        self.is_colliding = False
        self.local_rects = {}
        self.allow_collisions = True

    def define_collision_list(self, sprite_list):
        for sprite in sprite_list:
            if sprite != self:
                self.local_rects[sprite] = sprite.hitbox_rect
    
    def check_collision(self, direction):
        collision_list = self.hitbox_rect.collidedictall(self.local_rects)
        if len(collision_list) > 0:
            self.is_colliding = True
            if direction == 'horizontal':
                for sprite, rect in collision_list:
                        # If collision on the right
                        if self.hitbox_rect.right >= rect.left and self.old_rect.right <= sprite.old_rect.left:
                            self.hitbox_rect.right = rect.left
                            self.pos.x = self.hitbox_rect.centerx
                            self.velocity.x = self.max_x_vel/5
                        
                        # if self == player and sprite in obstacles:
                        #     print("horz  left 1|| old wall right:", sprite.old_rect.right, "| old player left:", self.old_rect.left, "|| new wall right:", rect.right, "| new player left:", self.hitbox_rect.left)

                        # If collision on the left
                        if self.hitbox_rect.left <= rect.right and self.old_rect.left >= sprite.old_rect.right:
                            self.hitbox_rect.left = rect.right 
                            self.pos.x = self.hitbox_rect.centerx
                            self.velocity.x = -self.max_x_vel/5
                        
                        # if self == player and sprite in obstacles:
                        #     print("horz left 2|| old wall right:", sprite.old_rect.right, "| old player left:", self.old_rect.left, "|| new wall right:", rect.right, "| new player left:", self.hitbox_rect.left, "\n")

            if direction == 'vertical':
                for sprite, rect in collision_list:
                    #if self == player:
                        #print("vert colliding with:", sprite)
                    # If collision on the bottom
                    if self.hitbox_rect.bottom >= rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.hitbox_rect.bottom = rect.top 
                        self.pos.y = self.hitbox_rect.centery
                        self.velocity.y = 0
                    
                    #print("self old right:", self.old_rect.right, "|other old left:", self.old_rect.left)
                    # If collision on the top
                    if self.hitbox_rect.top <= rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.hitbox_rect.top = rect.bottom
                        self.pos.y = self.hitbox_rect.centery
                        self.velocity.y = 0
        #else:
        #    self.is_colliding = False

    def modify_pos_x(self, x):
        """Adds the input x value to the x position."""
        self.pos.x += x
        self.hitbox_rect.center = self.pos
        self.rect.center = self.pos
    
    def modify_pos_y(self, y):
        """Adds the input y value to the y position."""
        self.pos.y += y
        self.hitbox_rect.center = self.pos
        self.rect.center = self.pos
    
    def update(self):
        self.old_rect = self.hitbox_rect.copy()

        self.modify_pos_x(self.direction.x*self.speed*dt)
        if self.allow_collisions:
            self.check_collision('horizontal')
        self.modify_pos_y(self.direction.y*self.speed*dt)
        if self.allow_collisions:
            self.check_collision('vertical')

class bird(move_object):
    def __init__(self, startingPos):
        super().__init__(startingPos, "SpriteImages/bird_sprite.png", 1)
        self.hitbox_rect.scale_by(0.9, 0.9)

    def update(self):
        self.check_controls()
        super().update()

    def check_controls(self):
        keys = pygame.key.get_pressed()
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
 
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1

########### FUNCTIONS ###########

def update_sprites(sprite_group):
    for sprite in sprite_group:
        sprite.update()

########## INITIALIZATIONS ##########

player = bird((screenW/2, screenH/2))
camera = camera_script.camera(player, (screenW, screenH))
live_sprites = pygame.sprite.Group()
live_sprites.add(player)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

########## MAIN LOOP ##########
def backrooms_game():
    global run, dt, last_time, screen, camera, live_sprites, all_sprites
    while run:
        dt = time.time() - last_time
        last_time = time.time()
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        camera.scroll()
        for sprite in all_sprites:
            drawnRect = sprite.rect.copy()
            screen.blit(pygame.transform.scale(sprite.image, (sprite.image.get_rect().w, sprite.image.get_rect().h)), 
                        (drawnRect.x-camera.offset.x, drawnRect.y-camera.offset.y))
        update_sprites(live_sprites)
        pygame.display.update()
pygame.quit()