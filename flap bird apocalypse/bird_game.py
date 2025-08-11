import pygame
import time
import map_maker
import camera
import backrooms

run = True
pygame.init()
screenW = 900
screenH = 600
screen = pygame.display.set_mode([screenW, screenH])
dt = 0
last_time = 0
max_x = map_maker.max_x # Maximum x value the bird can travel to

########## CLASSES ##########

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

        self.acceleration = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)

        self.max_x_vel = 0

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
        """Adds the input x value to the x position if no collisions are detected."""
        newX = self.pos.x + x
        if newX > 0 and newX < max_x:
            self.pos.x = newX
            self.hitbox_rect.center = self.pos
            self.rect.center = self.pos
    
    def modify_pos_y(self, y):
        """Adds the input x value to the x position if no collisions are detected."""
        newY = self.pos.y + y
        if newY > 0 and newY < screenH:
            self.pos.y = newY
            self.hitbox_rect.center = self.pos
            self.rect.center = self.pos
        else:
            self.velocity.y = 0

    def apply_gravity(self):
        self.acceleration.y += 1
    
    def update(self):
        self.old_rect = self.hitbox_rect.copy()

        self.velocity += self.acceleration
        self.modify_pos_x(self.velocity.x*dt)
        if self.allow_collisions:
            self.check_collision('horizontal')
        self.modify_pos_y(self.velocity.y*dt)
        if self.allow_collisions:
            self.check_collision('vertical')

class bird(move_object):
    def __init__(self, startingPos):
        super().__init__(startingPos, "SpriteImages/bird_sprite.png", 1)
        self.hitbox_rect.scale_by(0.9, 0.9)
        self.jump_time = 0
        self.move_x_val = 50 
        self.max_x_vel = 100
        self.jump_force = -250
        self.change_dir_multiplier = 1.75
        self.old_velocity_x = 0
        self.touched_bottom = False

    def update(self):
        self.old_velocity_x = self.velocity.x
        super().update()
        if not self.is_colliding and self.pos.y + 0.01 < screenH:
            keys = pygame.key.get_pressed()
            self.jump_logic(keys)
        else:
            self.velocity.x = 100
            self.allow_collisions = False
            if self.pos.y + 0.01 >= screenH:
                self.touched_bottom = True
        self.flip_sprite()

    def flip_sprite(self):
        #print("old:", self.old_velocity_x, "| new:", self.velocity.x)
        if self.velocity.x > 0 and self.old_velocity_x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        
        if self.velocity.x < 0 and self.old_velocity_x > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def check_jump(self, keys):
        if keys[pygame.K_SPACE]:
            return True
    
    def jump_logic(self, keys):
        if self.check_jump(keys) and (time.time()-self.jump_time) > 0.25:
            self.jump_time = time.time()
            self.velocity.y = self.jump_force
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
    
    def check_left_input(self, keys):
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            return True
    
    def check_right_input(self, keys):
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            return True

def update_sprites(sprite_group):
    for sprite in sprite_group:
        sprite.update()

player_bird = bird((screenW/2, screenH/2))

all_sprites = pygame.sprite.Group()
all_sprites.add(player_bird)
live_sprites = pygame.sprite.Group()
live_sprites.add(player_bird)
wall_list = map_maker.CreateMap(map_maker.map1)
for wall_sprite in wall_list:
    all_sprites.add(wall_sprite)

player_bird.apply_gravity()
player_bird.define_collision_list(all_sprites)
camera = camera.Camera(player_bird, (screenW, screenH), max_x)

########## MAIN LOOP ##########

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
    if player_bird.touched_bottom:
        # Here run backrooms game
        run = False
    pygame.display.update()
pygame.quit()