import pygame

class Camera():
    def __init__(self, player, screenValues, max_x):
        self.player = player
        self.offset = pygame.math.Vector2(0, 0)
        self.offsetFloat = pygame.math.Vector2(0, 0)
        self.displayW, self.displayH = screenValues[0], screenValues[1]
        self.const = pygame.math.Vector2((-self.displayW /2 + player.hitbox_rect.width / 2), -self.displayH/2) 
        self.max_x = max_x

    def scroll(self):
        temp_x = (self.player.hitbox_rect.x - self.offsetFloat.x + self.const.x)
        screen_left_pos = (self.player.pos.x - (self.player.hitbox_rect.width/2) - (self.displayW/2))
        screen_right_pos = (self.player.pos.x + (self.player.hitbox_rect.width/2) + (self.displayW/2))
        #print("Left:", screen_left_pos, "| Right:", screen_right_pos)
        if screen_left_pos > 0 and screen_right_pos < self.max_x:
            self.offsetFloat.x += temp_x
        #self.offsetFloat.y += (self.player.hitbox_rect.y - self.offsetFloat.y + self.const.y) 
        self.offset.x, self.offset.y = int(self.offsetFloat.x), int(self.offsetFloat.y)
    
    def returnFutureValues(self):
        offset = self.offset
        offsetFloat = self.offsetFloat
        offsetFloat.x += (self.player.hitbox_rect.x - self.offsetFloat.x + self.const.x) 
        #offsetFloat.y += (self.player.hitbox_rect.y - self.offsetFloat.y + self.const.y) 
        offset.x, offset.y = int(self.offsetFloat.x), int(self.offsetFloat.y)
        return offset
    
    def ResetFocus(self, player):
        self.player = player