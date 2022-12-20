from ursina import Entity, color, load_model
from ursina.scene import instance as scene
from numpy import floor

import random

from .noise import Noise
from .block import Block
from .config import DebugSettings
from .game_types import BlockType

class Chunk:
    """Chunk relates to the generation of the terrain and nothing else. We have a block store in here, but that is only for deleting a chunk."""
    def __init__(self, noise: Noise, chunk_size, chunk_offset: tuple[int, int], world) -> None:
        """
        It creates a chunk object, which is a collection of blocks
        
        Args:
          noise (Noise): Noise object
          chunk_size: The size of the chunk in blocks.
          chunk_offset (tuple[int, int]): The offset of the chunk in the world.
          world: The world object that the chunk is in.
        """
        self.noise = noise
        self.chunk_size = chunk_size
        
        self.block = load_model('block.obj', use_deepcopy=True)
        
        self.blocks: dict[tuple, Entity] = {}
        self.offset_x = (chunk_offset[0] * chunk_size)
        self.offset_z = (chunk_offset[1] * chunk_size)
        
        self.world = world
        
        
        self.color = color.rgba(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
        
    def generate_chunk(self, default_block: BlockType):
        """
        It creates a block for each coordinate in the chunk, and adds it to the world
        
        Args:
          default_block (BlockType): The type of block to generate by default.
        """
        for i in range(self.chunk_size*self.chunk_size):
            
            # Create the block and set its position
            block = Block(model='cube', parent=scene, block_type=default_block)
            block.x = floor((i/self.chunk_size) + self.offset_x)
            block.z = floor((i%self.chunk_size) + self.offset_z)
            block.y = floor(self.noise.get_y(block.x, block.z))
            
            # Add the block to the worlds block registry
            self.world.blocks[(block.x,block.y,block.z)] = block
            
            # If the debug setting is enabled, add the colour to this block
            if DebugSettings.CHUNK_COLOURS:
                block.color = self.color
            
            # Add the block to the chunks block registry
            self.blocks[(block.x, block.y, block.z)] = block
            
    def _render_chunk(self):
        """
        Enables all the blocks in the chunk
        """
        for block in list(self.blocks.values()):
            block.enable()
        
    def _derender_chunk(self):
        """
        Disables all the blocks in the chunk
        """
        for block in list(self.blocks.values()):
            block.disable()