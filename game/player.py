from ursina import raycast, Vec3, color
from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor

from game.event import EventHandler
from game.world import World
from game.util import BoundingBox3D
from game.config import DebugSettings

class Player:
    def __init__(self) -> None:
        self.controller = FirstPersonController()
        
        self.event = EventHandler()
        
        self.last_location = None
        self.last_chunk = None
        
        self.interactive_blocks: list = []
        
        # self.controller.input = self.input
        
    @property
    def position(self):
        return self.controller.position
    
    # For your code
    def input(self, key):
        if key == 'right shift down':
            print('pressed right shift button')
        
        
    def generate_bounding_area(self, world: World):
        box = BoundingBox3D.from_centre(self.position, 4)
    
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
        self.event.trigger("position_changed", **kwargs)
        
    def _chunk_changed(self, **kwargs):
        self.event.trigger("chunk_changed", **kwargs)
        
    def _update(self, chunk_size: int):
        if self.position != self.last_location:
            self._position_changed(position=self.position)
            self.last_location = self.position
            
            chunk = (chunk_x, chunk_z) = (floor(self.position.x / chunk_size), floor(self.position.z / chunk_size))
            if chunk != self.last_chunk:
                self._chunk_changed(chunk=chunk, last_chunk=self.last_chunk if self.last_chunk is not None else (0, 0))
                self.last_chunk = chunk
               
        # hit_info = raycast(self.controller.world_position + Vec3(0,1,0), self.controller.forward, 30, ignore=(self,))
        # # print(hit_info)
        # if hit_info:
        #     hit_info.entity.color = color.blue