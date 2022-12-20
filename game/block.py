from ursina import Entity, color, destroy, load_model, Vec2

from .config import Settings

class Block(Entity):
    """Block is a block on the screen. This handles the entity itself and more including hover effects.
    """
    
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.collider = 'mesh'
        self.collision = False
        
        # self.texture_scale*=(Settings.TEXTURE_SIZE * 4)/self.texture.width
        
        
        self.hovered_box = None
        
    def on_mouse_enter(self):
        """
        If the mouse is over the button, and the hovered_box is not already created, create a new
        hovered_box
        """
        # Check if there isn't already a hovered box here
        if not self.hovered_box:
            self.hovered_box = Entity(model='cube', collider=None, color=color.rgba(*Settings.HOVER_COLOUR), scale=(1.1,1.1,1.1), position=self.position)
        
    def on_mouse_exit(self):
        """Destroy the hovered box when mouse leaves."""
        destroy(self.hovered_box)
        self.hovered_box = None
        
    def remove(self):
        self.on_mouse_exit()
        destroy(self)