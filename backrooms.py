import pygame
import time
import camera_script
import map_maker
import math

run = True
pygame.init()
screenW = 900
screenH = 600
screen = pygame.display.set_mode([screenW, screenH])
dt = 0
last_time = 0
black = (0, 0, 0)
player_spawn_point = (0, 0)

########## SFX ##########
walking_sound = pygame.mixer.Sound("Sounds/carpet_footsteps_walking.wav")
walking_sound.set_volume(0.4)

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
                        
                        # if self == player and sprite in obstacles:
                        #     print("horz  left 1|| old wall right:", sprite.old_rect.right, "| old player left:", self.old_rect.left, "|| new wall right:", rect.right, "| new player left:", self.hitbox_rect.left)

                        # If collision on the left
                        if self.hitbox_rect.left <= rect.right and self.old_rect.left >= sprite.old_rect.right:
                            self.hitbox_rect.left = rect.right 
                            self.pos.x = self.hitbox_rect.centerx
                        
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
                    
                    #print("self old right:", self.old_rect.right, "|other old left:", self.old_rect.left)
                    # If collision on the top
                    if self.hitbox_rect.top <= rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.hitbox_rect.top = rect.bottom
                        self.pos.y = self.hitbox_rect.centery
        else:
            self.is_colliding = False

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
        super().__init__(startingPos, "SpriteImages/bird_top_down.png", 1)
        self.hitbox_rect.width = 16
        self.hitbox_rect.height = 16
        self.speed = 100
        self.playing_walking_sound = False

    def update(self):
        self.check_controls()
        super().update()
        self.rotate_to_mouse()
        if self.direction.length() > 0:
            if not self.playing_walking_sound:
                walking_sound.play(-1)
                self.playing_walking_sound = True
        elif self.playing_walking_sound:
            walking_sound.stop()
            self.playing_walking_sound = False

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
        
        self.direction = self.direction.normalize() if self.direction.length() > 0 else pygame.math.Vector2(0, 0)
    
    def rotate_to_mouse(self):
        x = self.hitbox_rect.centerx 
        y = self.hitbox_rect.centery 
        Mx, My = pygame.mouse.get_pos()
        Mx /= camera.zoom_level
        My /= camera.zoom_level
        xDist = (Mx - x) + camera.offset.x 
        yDist = (My - y) + camera.offset.y 
        self.lookDirection = pygame.math.Vector2(xDist, yDist)
        self.lookDirection = self.lookDirection.normalize()
        self.angle = math.degrees(math.atan2(yDist, xDist)) + 90
        self.image = pygame.transform.rotate(self.base_image, -self.angle)
        self.rect = self.image.get_rect(center = self.hitbox_rect.center)
        #startPosX = (self.hitbox_rect.centerx - camera.offset.x) * zoomLevel
        #startPosY = (self.hitbox_rect.centery - camera.offset.y) * zoomLevel
        #pygame.draw.line(screen, "green", (startPosX, startPosY), (startPosX + self.lookDirection.x * 20, startPosY + self.lookDirection.y * 20)) 
        

########### FUNCTIONS ###########

def update_sprites(sprite_group):
    for sprite in sprite_group:
        sprite.update()

def is_on_screen(position):
    screenPosX = position[0] 
    screenPosY = position[1] 
    #print("offset:", (camera.offset.x, camera.offset.y))
    screenWLimit = (screenW/camera.zoom_level) + camera.offset.x 
    screenHLimit = (screenH/camera.zoom_level) + camera.offset.y 
    if (screenPosX <= screenWLimit and screenPosX >= (screenWLimit-screenW)) and (screenPosY <= screenHLimit and screenPosY >= (screenHLimit-screenH)):
        return True
    else:
        return False

def draw_sprites(sprite_group, screen, offset, zoom_level):
    for sprite in sprite_group:
        if is_on_screen(sprite.pos):
            drawn_rect = sprite.rect.copy()
            drawn_rect.width = sprite.rect.width * zoom_level
            drawn_rect.height = sprite.rect.height * zoom_level
            screen.blit(pygame.transform.scale(sprite.image, (sprite.image.get_rect().w*zoom_level, sprite.image.get_rect().h*zoom_level)), 
                        ((drawn_rect.x - offset.x)*zoom_level, (drawn_rect.y - offset.y)*zoom_level))

########## INITIALIZATIONS ##########
wall_list, floor_list, player_spawn_point = map_maker.create_map(map_maker.map)
player = bird(player_spawn_point)
camera = camera_script.camera(player, (screenW, screenH))

live_sprites = pygame.sprite.Group()
live_sprites.add(player)
all_sprites = pygame.sprite.Group()
floor_sprites = pygame.sprite.Group()
collision_list = pygame.sprite.Group()

for wall_sprite in wall_list:
    all_sprites.add(wall_sprite)
    collision_list.add(wall_sprite)
for floor_sprite in floor_list:
    floor_sprites.add(floor_sprite)

player.define_collision_list(collision_list)
clock = pygame.time.Clock()
########## MAIN LOOP ##########

def backrooms_game(screen):
    global run, dt, last_time, camera, live_sprites, all_sprites
    pygame.mixer.init()
    pygame.mixer.music.load("Sounds/light_hum.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    while run:
        clock.tick(60)
        dt = time.time() - last_time
        last_time = time.time()
        screen.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        camera.scroll()
        draw_sprites(floor_sprites, screen, camera.offset, camera.zoom_level)
        draw_sprites(all_sprites, screen, camera.offset, camera.zoom_level)
        player_rect = player.rect.copy()
        screen.blit(pygame.transform.scale(player.image, (player.image.get_rect().w*camera.zoom_level, player.image.get_rect().h*camera.zoom_level)), 
                        ((player_rect.x-camera.offset.x)*camera.zoom_level, (player_rect.y-camera.offset.y)*camera.zoom_level))
        update_sprites(live_sprites)
        pygame.display.update()

backrooms_game(screen)

pygame.quit()