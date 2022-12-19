from ursina import Entity, color
import math

from game.config import Settings

class Block(Entity):
    
    def __init__(self, player, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.player = player
        
        self.collider = 'box'
        self.collision = False
        
    # def update(self):
    #     if self.collision:
    #         self.collision = False
            # self.color = color.black
    
    def distance(self, x1, y1, z1, x2, y2, z2):
        d = math.sqrt(math.pow(x2 - x1, 2) +
                    math.pow(y2 - y1, 2) +
                    math.pow(z2 - z1, 2)* 1.0)
        
        return d