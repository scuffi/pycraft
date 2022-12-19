from ursina import color
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor

from .event import EventHandler
from .util import BoundingBox3D
from .config import DebugSettings, Settings
from .world import World

class Player:
    """Player class is the class relating to the player, including data and manipulation functions
    """
    
    def __init__(self) -> None:
        self.controller = FirstPersonController()
        
        self.event = EventHandler()
        
        self.last_location = None
        self.last_chunk = None
        
        self.interactive_blocks: list = []
        
    @property
    def position(self):
        return self.controller.position
    
    def generate_bounding_area(self, world: World):
        """
        Generate the area of interactive blocks around the player.
        
        Args:
          world: The world object
        """
        box = BoundingBox3D.from_centre(self.position, Settings.REACH)
    
        product = box.get_product()
        
        for old_block in self.interactive_blocks.copy():
            # Check if the block isn't still meant to be interactive
            if old_block not in product:
                
                # If it's not in our existing bounding box it means that the block is now too far away from the player to be interactive
                old_block.collision = False
                
                if DebugSettings.TRAIL:
                    old_block.color = color.black
                
                self.interactive_blocks.remove(old_block)
        
        for block_location in product:
            if block_location in world.blocks:
                block = world.blocks[block_location]
                block.collision = True
                
                if DebugSettings.BOUNDING_BOX:
                    block.color = color.red
                
                self.interactive_blocks.append(block)
                
    # ! Private functions
    def _position_changed(self, **kwargs):
        """
        The function is called when the position of the slider changes. It triggers an event called
        "position_changed" and passes the new position as a keyword argument
        """
        self.event.trigger("position_changed", **kwargs)
        
    def _chunk_changed(self, **kwargs):
        """
        It takes a chunk of text, and then it triggers an event called "chunk_changed" with the chunk of
        text as a parameter
        """
        self.event.trigger("chunk_changed", **kwargs)
        
    def _update(self, chunk_size: int):
        """
        Update anything relating to the player. Such as position.
        
        Args:
          chunk_size (int): The size of the chunks in the world.
        """
        if self.position != self.last_location:
            self._position_changed(position=self.position)
            self.last_location = self.position
            
            chunk = (floor(self.position.x / chunk_size), floor(self.position.z / chunk_size))
            if chunk != self.last_chunk:
                self._chunk_changed(chunk=chunk, last_chunk=self.last_chunk if self.last_chunk is not None else (0, 0))
                self.last_chunk = chunk