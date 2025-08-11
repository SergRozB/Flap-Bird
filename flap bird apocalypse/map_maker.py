import pygame

map1_1 = """\
                        W         W         W         W         W         W         W         W          
                        W         W         W         W         W         W         W         W          
                        W         W                   W         W         W         W         W          
                        W         W                             W         W         W         W          
                        W         W                                       W         W         W         W
                                  W                                       W         W         W         W
                                  W         W                             W                   W         W
                                  W         W         W                   W                   W         W
                                  W         W         W         W                             W         W
                        W         W         W         W         W                             W         W
                        W                   W         W         W                   W         W         W
                        W                   W         W         W                   W         W         W
                        W                   W         W         W         W         W         W         W
                        W                   W         W         W         W         W         W         W
                        W         W         W         W         W         W         W                   W
                        W         W         W         W         W         W         W                   W
                        W         W         W         W         W         W         W                   W
                        W         W         W         W         W         W         W                   W
                        W         W         W         W         W         W         W         W         W
"""
map1_2 = """\
         W         W         W         W         W         W         W         W         W
         W         W         W         W         W         W         W         W         W
                   W         W         W         W                   W         W         W
                   W         W         W         W                   W         W         W
                   W         W         W                             W                   W
                   W         W         W                             W                   W
         W         W         W         W                   W         W                   W
         W         W         W         W                   W                              
         W                   W         W         W         W                   W          
         W                             W         W         W                   W          
         W                             W         W         W                   W          
         W                             W         W         W         W         W         W
         W         W                   W         W         W         W         W         W
         W         W         W         W         W         W         W         W         W
         W         W         W                   W         W         W         W         W
         W         W         W                   W         W         W         W         W
         W         W         W                   W         W         W         W         W
         W         W         W                   W         W         W         W         W
         W         W         W         W         W         W         W         W         W
"""

map1_1 = map1_1.splitlines()
map1_2 = map1_2.splitlines()
for i in range(len(map1_1)):
    map1_1[i] = map1_1[i] + map1_2[i]
map1 = map1_1
#map = map.splitlines()
max_x = len(map1[0])*32

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("SpriteImages\Tile1.png")
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.hitbox_rect = self.image.get_rect(topleft = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.old_rect = self.hitbox_rect.copy()

def CreateMap(map):
    wall_list = []
    offset = 32
    for y, line in enumerate(map):
        for x, character in enumerate(line):
            if y > 0:
                if character == "W":
                    wall_list.append(Wall((x*offset, y*offset)))
            elif character == "W":
                wall_list.append(Wall((x*offset, y*offset)))
    return wall_list