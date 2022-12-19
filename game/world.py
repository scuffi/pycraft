from ursina import Entity, destroy

from .noise import Noise
from .config import WorldSettings, NoiseSettings
from .chunk import Chunk
from .block import Block
from .util import BoundingBox

class World:
    """World relates to the world itself, holding all functionality to manipulate the terrain.
    """
    
    def __init__(self, seed: int) -> None:
        """
        Create a new world.
        
        Args:
          seed (int): int = The seed for the world.
        """
        self.noise = Noise(seed=seed, amp=NoiseSettings.AMPLITUDE, freq=NoiseSettings.FREQUENCY, octaves=NoiseSettings.OCTAVES)
        
        self.chunks: dict[tuple, Chunk] = {}
        # self.chunks: list[Chunk] = []
        
        self.blocks: list[Entity] = {}
        
    def pregen_world(self, radius: int):
        """
        Generate chunks around 0,0
        
        Args:
          radius (int): The radius of the world to generate.

        Note: Radius must be > 0
        """ 
        for x in range(0-radius, radius):
            for z in range(0-radius, radius):
                offset = (x, z)
                self._generate_chunk(offset)
                
    def _generate_chunk(self, offset: tuple[int, int]):
        """
        It generates a chunk of blocks based on the noise function and the chunk's offset
        
        Args:
          offset (tuple[int, int]): tuple[int, int]
        """
        chunk = Chunk(noise=self.noise, chunk_size=WorldSettings.CHUNK_SIZE, chunk_offset=offset, world=self)

        chunk.generate_blocks()
        
        self.chunks[offset] = chunk
        
    def _remove_chunk(self, offset: tuple[int, int]):
        """
        It removes a chunk from the world
        
        Args:
          offset (tuple[int, int]): The offset of the chunk to remove.
        """
        if offset in self.chunks:
            for block in self.chunks[offset].blocks:
                self.break_block(block)
                
            del self.chunks[offset]
            
    def generate_terrain(self, current_location):
        """
        "If a chunk is not currently rendered, but should be, render it. If a chunk is currently rendered,
        but shouldn't be, remove it."
        
        This is the core of the terrain generation system. It's a simple, but effective system that allows
        us to render only the chunks that are in our render distance
        
        Args:
          current_location: The location of the player
        """
        box = BoundingBox.from_centre_chunk(current_location, width=WorldSettings.RENDER_DISTANCE)
    
        # Get all chunks inside of this bounding box
        product = box.get_product()
        
        # Iterate over all the chunks that SHOULD exist
        for chunk_offset in product:
            # Check if chunk is currently rendered
            if chunk_offset not in self.chunks:
                
                # If it's not, we know it should be, so render it
                self._generate_chunk(chunk_offset)
                
        # Iterate over all the currently rendered chunks
        for chunk_offset in self.chunks.copy():
            # If the chunk is NOT in the product, it's not in our render distance
            if chunk_offset not in product:
                # ...so we can remove the chunk as it's too far away to care about
                self._remove_chunk(chunk_offset)
                    
    def break_block(self, block: Block):
        """
        Attempt to destroy a block from the World.
        
        Args:
          block (Block): The block to be destroyed.
        """
        destroy(block)
        
        if block in self.blocks:
            del self.blocks[block]
