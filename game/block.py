from ursina import Entity, color, destroy
import math

from game.config import Settings

class Block(Entity):
    
    def __init__(self, player, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.player = player
        
        self.collider = 'box'
        self.collision = False
        
        self.hovered_box = None
        
    def on_mouse_enter(self):
        # Check if there isn't already a hovered box here
        if not self.hovered_box:
            self.hovered_box = Entity(model='cube', collider=None, color=color.rgba(*Settings.HOVER_COLOUR), scale=(1.1,1.1,1.1), position=self.position)
        
    def on_mouse_exit(self):
        destroy(self.hovered_box)
        self.hovered_box = None