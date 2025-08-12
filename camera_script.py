import pygame

class camera():
    def __init__(self, player, screen_values):
        self.zoom_level = 1.5
        self.player = player
        self.offset = pygame.math.Vector2(0, 0)
        self.offset_float = pygame.math.Vector2(0, 0)
        self.display_w, self.display_h = screen_values[0], screen_values[1]
        self.const = pygame.math.Vector2((-self.display_w /2 + player.hitbox_rect.width / 2)/self.zoom_level, -self.display_h/2 / self.zoom_level) 

    def scroll(self):
        self.offset_float.x += (self.player.hitbox_rect.x - self.offset_float.x + self.const.x) 
        self.offset_float.y += (self.player.hitbox_rect.y - self.offset_float.y + self.const.y) 
        self.offset.x, self.offset.y = int(self.offset_float.x), int(self.offset_float.y)
    
    def returnFutureValues(self):
        offset = self.offset
        offset_float = self.offset_float
        offset_float.x += (self.player.hitbox_rect.x - self.offset_float.x + self.const.x) 
        offset_float.y += (self.player.hitbox_rect.y - self.offset_float.y + self.const.y) 
        offset.x, offset.y = int(self.offset_float.x), int(self.offset_float.y)
        return offset
    
    def ResetFocus(self, player):
        self.player = player