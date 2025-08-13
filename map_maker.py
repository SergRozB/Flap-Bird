import pygame

map = """\
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
W                       W         W         W         W         W         W         W         W         W
W         WW        WWWWWW        W         W         W         W         W         W         W         W
W         WW            W         W                   W         W         W         W         W         W
W         WW            W         W                             W         W         W         W         W
W                       W         W                                       W         W         W         W
W                                 W                                       W         W         W         W
W                                 W         W                             W                   W         W
W                                 W         W         W                   W                   W         W
W                                 W         W         W         W                             W         W
W                       WWWWWWWWWWW         W         W         W                             W         W
W                       W                   W         W         W                   W         W         W
W        W              W                   W         W         W                   W         W         W
W      WWWWW            W         W         W         W         W         W         W         W         W
W                                 W         W         W         W         W         W         W         W
W                                 W         W         W         W         W         W                   W
W                       W         W         W         W         W         W         W                   W
W                       W         W         W         W         W         W         W                   W
W                       W         W         W         W         W         W         W                   W
W                       W         W         W         W         W         W         W         W         W
WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW
"""

map = open("map.txt", "r").readlines()
for n in range(len(map)):
    map[n] = map[n].rstrip("\n")

#map = map.splitlines()

class wall(pygame.sprite.Sprite):
    def __init__(self, pos, map_pos):
        super().__init__()
        self.image = pygame.image.load("SpriteImages/wall_vert_closed.png")
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.hitbox_rect = self.image.get_rect(topleft = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.old_rect = self.hitbox_rect.copy()
        self.map_pos = map_pos  # Store the map position for reference
    
    def change_image(self, image_path, rotation=0):
        if rotation == 0:
            self.image = pygame.image.load(image_path)
        else:
            self.image = pygame.transform.rotate(pygame.image.load(image_path), rotation)
        self.hitbox_rect = self.image.get_rect(topleft = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.old_rect = self.hitbox_rect.copy()

class floor(pygame.sprite.Sprite):
    def __init__(self, pos, image_path="SpriteImages/floor_1.png", rotation=0):
        super().__init__()
        if rotation == 0:
            self.image = pygame.image.load(image_path)
        else:
            self.image = pygame.transform.rotate(pygame.image.load(image_path), rotation)
        self.pos = pygame.math.Vector2(pos[0], pos[1])
        self.hitbox_rect = self.image.get_rect(topleft = self.pos)
        self.rect = self.hitbox_rect.copy()
        self.old_rect = self.hitbox_rect.copy()


def wall_sprite_manager(wall_list, map_list):
    for wall_sprite in wall_list:
        neighbours_list = get_wall_neighbours(map_list, wall_sprite.map_pos)
        #print("Neighbours for", wall_sprite.map_pos, ": \n", neighbours_list[:3], "\n", neighbours_list[3:6], "\n", neighbours_list[6:9])
        dict_neighbours_all_dir = {
            (0, 1, 0, 
            0, 1, 0, 
            0, 1, 0): ("SpriteImages/wall_vert_open.png", 0),
            (0, 0, 0,
            1, 1, 1,
            0, 0, 0): ("SpriteImages/wall_vert_open.png", 90),
            (0, 0, 0,
            0, 1, 0,
            0, 1, 0): ("SpriteImages/wall_vert_closed.png", 0),
            (0, 0, 0,
            0, 1, 1,
            0, 0, 0): ("SpriteImages/wall_vert_closed.png", 90),
            (0, 1, 0, 
            0, 1, 0,
            0, 0, 0): ("SpriteImages/wall_vert_closed.png", 180),
            (0, 0, 0,
            1, 1, 0,
            0, 0, 0): ("SpriteImages/wall_vert_closed.png", 270),
            (0, 0, 0, 
            0, 1, 1,
            0, 1, 0): ("SpriteImages/wall_corner.png", 0),
            (0, 1, 0,
            0, 1, 1,
            0, 0, 0): ("SpriteImages/wall_corner.png", 90),
            (0, 1, 0,
            1, 1, 0,
            0, 0, 0): ("SpriteImages/wall_corner.png", 180),
            (0, 0, 0,
            1, 1, 0,
            0, 1, 0): ("SpriteImages/wall_corner.png", 270),
            (1, 1, 1,
            1, 1, 1,
            1, 1, 1): ("SpriteImages/wall_surrounded.png", 0),
            (0, 1, 1,
            0, 1, 1,
            0, 1, 1): ("SpriteImages/wall_vert_full.png", 0),
            (1, 1, 1,
            1, 1, 1, 
            0, 0, 0): ("SpriteImages/wall_vert_full.png", 90),
            (1, 1, 0,
            1, 1, 0,
            1, 1, 0): ("SpriteImages/wall_vert_full.png", 180),
            (0, 0, 0,
            1, 1, 1,
            1, 1, 1): ("SpriteImages/wall_vert_full.png", 270), 
            (0, 0, 0,
            0, 1, 1,
            0, 1, 1): ("SpriteImages/wall_corner_full.png", 0),
            (0, 1, 1,
            0, 1, 1,
            0, 0, 0): ("SpriteImages/wall_corner_full.png", 90),
            (1, 1, 0,
            1, 1, 0,
            0, 0, 0): ("SpriteImages/wall_corner_full.png", 180),
            (0, 0, 0,
            1, 1, 0,
            1, 1, 0): ("SpriteImages/wall_corner_full.png", 270),
            (0, 0, 0,
            1, 1, 1,
            1, 1, 0) : ("SpriteImages/wall_corner_full_2.png", 0),
            (0, 1, 0,
            0, 1, 1,
            0, 1, 1) : ("SpriteImages/wall_corner_full_2.png", 90),
            (0, 1, 1,
            1, 1, 1,
            0, 0, 0) : ("SpriteImages/wall_corner_full_2.png", 180),
            (1, 1, 0,
            1, 1, 0,
            0, 1, 0) : ("SpriteImages/wall_corner_full_2.png", 270),
            (1, 1, 0,
            1, 1, 1,
            0, 0, 0) : ("SpriteImages/wall_corner_full_3.png", 0),
            (0, 1, 0,
            1, 1, 0,
            1, 1, 0) : ("SpriteImages/wall_corner_full_3.png", 90),
            (0, 0, 0,
            1, 1, 1,
            0, 1, 1) : ("SpriteImages/wall_corner_full_3.png", 180),
            (0, 1, 1,
            0, 1, 1,
            0, 1, 0) : ("SpriteImages/wall_corner_full_3.png", 270),
            (0, 1, 0,
            1, 1, 1, 
            0, 1, 0): ("SpriteImages/wall_intersection.png", 0),
            (0, 0, 0,
            0, 1, 0,
            0, 0, 0): ("SpriteImages/wall_pillar.png", 0)
        }
        dict_neighbours_four_dir = {
            (1,
            0, 0,
            1): ("SpriteImages/wall_vert_open.png", 0),
            (0, 
            1, 1,
            0): ("SpriteImages/wall_vert_open.png", 90),
            (0,
            0, 0,
            1): ("SpriteImages/wall_vert_closed.png", 0),
            (0,
            0, 1,
            0): ("SpriteImages/wall_vert_closed.png", 90),
            (1,
            0, 0,
            0): ("SpriteImages/wall_vert_closed.png", 180),
            (0,
            1, 0,
            0): ("SpriteImages/wall_vert_closed.png", 270),
            (0,
            0, 1,
            1): ("SpriteImages/wall_corner.png", 0),
            (1,
            0, 1,
            0): ("SpriteImages/wall_corner.png", 90),
            (1,
            1, 0,
            0): ("SpriteImages/wall_corner.png", 180),
            (0,
            1, 0,
            1): ("SpriteImages/wall_corner.png", 270),
            (0,
            1, 1,
            1): ("SpriteImages/wall_t.png", 0),
            (1,
            0, 1,
            1): ("SpriteImages/wall_t.png", 90),
            (1,
            1, 1,
            0): ("SpriteImages/wall_t.png", 180),
            (1, 
            1, 0,
            1): ("SpriteImages/wall_t.png", 270),
            (0, 
            0, 0,
            0): ("SpriteImages/wall_pillar.png", 0),
            (1,
            1, 1,
            1): ("SpriteImages/wall_intersection.png", 0)
        }
        if neighbours_list in dict_neighbours_all_dir.keys():
            image_path, rotation = dict_neighbours_all_dir[neighbours_list]
        else:
            neighbours_list_vert_horz = (neighbours_list[1], neighbours_list[3], neighbours_list[5], neighbours_list[7])
            if neighbours_list_vert_horz in dict_neighbours_four_dir.keys():
                image_path, rotation = dict_neighbours_four_dir[neighbours_list_vert_horz]
            else:
                image_path, rotation = "SpriteImages/wall_pillar.png", 0
        wall_sprite.change_image(image_path, rotation)
        """
        if neighbours_list == [0, 1, 0, 
                               0, 0, 
                               0, 1, 0]:
            wall_sprite.change_image("SpriteImages/wall_vert_open.png")
        elif neighbours_list == [0, 1, 0, 
                                 0, 0, 
                                 0, 0, 0]:
            wall_sprite.change_image("SpriteImages/wall_vert_closed.png", 180)
        elif neighbours_list == [0, 0, 0, 
                                 1, 1, 
                                 0, 0, 0]:
            wall_sprite.change_image("SpriteImages/wall_vert_open.png", 180)
        elif neighbours_list == [0, 0, 0, 
                                 0, 1, 
                                 0, 0, 0]:
            wall_sprite.change_image("SpriteImages/wall_vert_closed.png", 90)
        elif neighbours_list == [0, 0, 0, 
                                 1, 0, 
                                 0, 0, 0]:
            wall_sprite.change_image("SpriteImages/wall_vert_open.png", 270)
        elif neighbours_list == [0, 0, 0, 
                                 0, 1, 
                                 0, 1, 0]:
            wall_sprite.change_image("SpriteImages/wall_corner.png")
        elif neighbours_list == [0, 0, 0, 
                                 1, 0, 
                                 0, 1, 0]:
            wall_sprite.change_image("SpriteImages/wall_corner.png", 90)
        elif neighbours_list == [0, 0, 0, 
                                 0, 0, 
                                 0, 1, 0]:
            wall_sprite.change_image("SpriteImages/wall_corner.png", 180)
        """

def get_wall_neighbours(map_list, map_pos):
    char_list = ["W", "B"]
    top_left = (map_pos[0] - 1, map_pos[1] - 1)
    top = (map_pos[0], map_pos[1] - 1)
    top_right = (map_pos[0] + 1, map_pos[1] - 1)
    left = (map_pos[0] - 1, map_pos[1])
    right = (map_pos[0] + 1, map_pos[1])
    bottom_left = (map_pos[0] - 1, map_pos[1] + 1)   
    bottom = (map_pos[0], map_pos[1] + 1)
    bottom_right = (map_pos[0] + 1, map_pos[1] + 1)
    if map_pos[0] > 0 and map_pos[1] > 0:
        if map_list[top_left[1]][top_left[0]] in char_list:
            top_left = 1
        else:
            top_left = 0
    else:
        top_left = 0
    if map_pos[1] > 0:
        if map_list[top[1]][top[0]] in char_list:
            top = 1  
        else:
            top = 0  
    else:
        top = 0
    if map_pos[0] < len(map_list[0]) - 1 and map_pos[1] > 0:
        if map_list[top_right[1]][top_right[0]] in char_list:
            top_right = 1
        else:
            top_right = 0
    else:
        top_right = 0
    if map_pos[0] > 0:
        if map_list[left[1]][left[0]] in char_list:
            left = 1
        else:
            left = 0
    else:
        left = 0
    if map_pos[0] < len(map_list[0]) - 1:
        if map_list[right[1]][right[0]] in char_list:
            right = 1
        else:
            right = 0
    else:
        right = 0
    if map_pos[0] > 0 and map_pos[1] < len(map_list) - 1:
        if map_list[bottom_left[1]][bottom_left[0]] in char_list:
            bottom_left = 1
        else:
            bottom_left = 0
    else:
        bottom_left = 0
    if map_pos[1] < len(map_list) - 1:
        if map_list[bottom[1]][bottom[0]] in char_list:
            bottom = 1
        else:
            bottom = 0
    else:
        bottom = 0
    if map_pos[0] < len(map_list[0]) - 1 and map_pos[1] < len(map_list) - 1:
        if map_list[bottom_right[1]][bottom_right[0]] in char_list:
            bottom_right = 1
        else:
            bottom_right = 0
    else:
        bottom_right = 0
    return (top_left, top, top_right, left, 1, right, bottom_left, bottom, bottom_right)

def create_map(map):
    wall_list = []
    floor_list = []
    offset = 32
    map_list = []
    map_floor_corners_dict = {
        (0, 0): ("SpriteImages/quarter_floor.png", 0),
        (0, len(map)-1): ("SpriteImages/quarter_floor.png", 90)
    }
    spawn_point = (0, 0)
    for y, line in enumerate(map):
        map_list.append([])
        for x, character in enumerate(line):
            map_floor_corners_dict[(len(line) - 1, 0)] = ("SpriteImages/quarter_floor.png", 270)
            map_floor_corners_dict[(len(line) - 1, len(map) - 1)] = ("SpriteImages/quarter_floor.png", 180)
            map_list[-1].append(character)
            if character != "B":
                if x != 0 and x != len(line) - 1 and y != 0 and y != len(map) - 1:
                    floor_list.append(floor((x*offset, y*offset)))
                elif x == 0 and y != 0 and y != len(map) - 1:
                    floor_list.append(floor((x*offset, y*offset), "SpriteImages/half_floor_1.png", rotation=90))
                elif x == len(line) - 1 and y != 0 and y != len(map) - 1:
                    floor_list.append(floor((x*offset, y*offset), "SpriteImages/half_floor_1.png", rotation=270))
                elif y == 0 and x != 0 and x != len(line) - 1:
                    floor_list.append(floor((x*offset, y*offset), "SpriteImages/half_floor_1.png", rotation=0))
                elif y == len(map) - 1 and x != 0 and x != len(line) - 1:
                    floor_list.append(floor((x*offset, y*offset), "SpriteImages/half_floor_1.png", rotation=180))
                else:
                    if (x, y) in map_floor_corners_dict.keys():
                        image_path, rotation = map_floor_corners_dict[(x, y)]
                        floor_list.append(floor((x*offset, y*offset), image_path, rotation))
            else:
                floor_list.append(floor((x*offset, y*offset), "SpriteImages/wall_surrounded.png"))
            if character == "W":
                wall_list.append(wall((x*offset, y*offset), (x, y)))
            if character == "O":
                spawn_point = (x*offset, y*offset)
    wall_sprite_manager(wall_list, map_list)
    return wall_list, floor_list, spawn_point