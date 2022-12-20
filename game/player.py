from ursina import color, mouse, Text
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor

from .event import EventHandler
from .util import BoundingBox3D
from .config import DebugSettings, Settings
from .world import World
from .inventory import Inventory
from .game_types import BlockType

class Player:
    """Player class is the class relating to the player, including data and manipulation functions
    """
    
    def __init__(self, blocks: list[BlockType]) -> None:
        """
        Create a player.
        
        Args:
          blocks (list[BlockType]): list[BlockType]
        """
        self.controller = FirstPersonController()
        
        self.event = EventHandler()
        
        self.last_location = None
        self.last_chunk = None
        
        self.interactive_blocks: list = []
        
        self.inventory = Inventory(blocks)
        
    @property
    def position(self):
        return self.controller.position
    
    def generate_bounding_area(self, world: World):
        """
        Generate the area of interactive blocks around the player.
        
        Args:
          world: The world object
        """
        # Create a bounding box from the players position, with a width of whatever the configurated reach is
        box = BoundingBox3D.from_centre(self.position, Settings.REACH)
    
        # Get the product from our bounding box, this gives us every possible coordinate trio in the box
        product = box.get_product()
        
        # Iterate over a copy, as we will edit the dictionary in the loop
        for old_block in self.interactive_blocks.copy():
            # Check if the block isn't still meant to be interactive
            if old_block not in product:
                
                # If it's not in our existing bounding box it means that the block is now too far away from the player to be interactive
                old_block.collision = False
                
                # If the trail setting is on, change the colour
                if DebugSettings.TRAIL:
                    old_block.color = color.black
                
                # Remove the old block from the interactive blocks dictionary
                self.interactive_blocks.remove(old_block)
        
        # Iterate over the product
        for block_location in product:
            # If the block is in our registry
            if block_location in world.blocks:
                
                # Enable the collision of this block
                block = world.blocks[block_location]
                block.collision = True
                
                # If the bounding box setting is enabled, colour it in red
                if DebugSettings.BOUNDING_BOX:
                    block.color = color.red
                
                # Add this block to our interactive blocks dictionary so we keep track of what block is collidable
                self.interactive_blocks.append(block)
                
    def is_interacting(self, key, world: World):
        """
        If the left mouse button is pressed, place a block at the position of the mouse cursor. If the right
        mouse button is pressed, break the block at the position of the mouse cursor
        
        Args:
          key: The key that was pressed.
          world (World): The world object.
        """
        if key == 'left mouse down':
            hovered_block = mouse.hovered_entity
            # Get and check the hovered entity exists
            if hovered_block:
                # ...if it does, place the block!
                world.place_block(hovered_block.position + mouse.normal, self.inventory.current_block)
        elif key == 'right mouse down':
            hovered_block = mouse.hovered_entity
            # Get and check the hovered entity exists
            if hovered_block:
                # ...if it does, break the block!
                world.break_block(hovered_block, by_player=True)
                
        # Run the inventory check to check if this interaction was actually a scroll
        self.inventory.is_scrolling(key)
                
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
        # Check if the position has changed since the last location
        if self.position != self.last_location:
            # Trigger the position changed events
            self._position_changed(position=self.position)
            
            # Now our last location has updated
            self.last_location = self.position
            
            # Get the chunk offset from the position
            chunk = (floor(self.position.x / chunk_size), floor(self.position.z / chunk_size))
            
            # Check if the chunk position has changed
            if chunk != self.last_chunk:
                # ...if it has, trigger the chunk change event
                self._chunk_changed(chunk=chunk, last_chunk=self.last_chunk if self.last_chunk is not None else (0, 0))
                
                # Set the last chunk to this chunk
                self.last_chunk = chunk