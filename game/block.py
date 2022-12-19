from ursina import Entity, color
import math

class Block(Entity):
    
    def __init__(self, player, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.player = player
    
    def update(self):
        # print("Updated")
        player_pos = self.player.position
        distance = self.distance(player_pos.x, player_pos.y, player_pos.z, self.x, self.y, self.z)
        if distance < 6:
            self.color = color.white
            self.collider = 'box'
        else:
            self.color = color.black
            self.collider = None
    
    def distance(self, x1, y1, z1, x2, y2, z2):
        d = math.sqrt(math.pow(x2 - x1, 2) +
                    math.pow(y2 - y1, 2) +
                    math.pow(z2 - z1, 2)* 1.0)
        
        return d