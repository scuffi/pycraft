from ursina import Entity, color, destroy, load_model, Vec2, Audio

from .config import Settings
from .game_types import BlockType

class Block(Entity):
    """Block is a block on the screen. This handles the entity itself and more including hover effects.
    """
    
    def __init__(self, block_type: BlockType, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
        self.collider = 'box'
        self.collision = False
        
        self.hovered_box = None
        
        self.block_type = block_type
        
        self.texture = block_type.texture
        
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
        
    def remove(self, by_player: bool = False):
        """
        Remove the block from the game
        
        Args:
          by_player (bool): Whether the block was broken by the player or not. Defaults to False
        """
        if by_player:
            self.block_type.break_sound.play()
        self.on_mouse_exit()
        destroy(self)
        