import sys

from ursina import Entity, destroy, scene, Mesh, Vec3, Vec2, load_model

from .noise import Noise
from .config import WorldSettings, NoiseSettings
from .chunk import Chunk
from .block import Block
from .util import BoundingBox
from .game_types import BlockType

class World:
    """World relates to the world itself, holding all functionality to manipulate the terrain.
    """
    
    def __init__(self, seed: int, block_registry: dict[str, BlockType]) -> None:
        """
        Create a new world.
        
        Args:
          seed (int): int = The seed for the world.
        """
        self.noise = Noise(seed=seed, amp=NoiseSettings.AMPLITUDE, freq=NoiseSettings.FREQUENCY, octaves=NoiseSettings.OCTAVES)
        
        self.enabled_chunks: dict[tuple, Chunk] = {}
        self.disabled_chunks: dict[tuple, Chunk] = {}
        
        self.blocks: list[Entity] = {}
        
        self.block_registry = block_registry
        
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
        if offset not in self.disabled_chunks:
          chunk = Chunk(noise=self.noise, chunk_size=WorldSettings.CHUNK_SIZE, chunk_offset=offset, world=self)
          
          # Check if the default block exists in the registry
          if WorldSettings.DEFAULT_BLOCK not in self.block_registry:
              print("Default block was not found in configuration, please amend.")
              sys.exit(1)

          chunk.generate_chunk(self.block_registry[WorldSettings.DEFAULT_BLOCK])
        else:
          chunk = self.disabled_chunks[offset]
          chunk._render_chunk()
          del self.disabled_chunks[offset]
        
        self.enabled_chunks[offset] = chunk
        
    def _derender_chunk(self, offset: tuple[int, int]):
        """
        It removes a chunk from the world
        
        Args:
          offset (tuple[int, int]): The offset of the chunk to remove.
        """
        if offset in self.enabled_chunks:
            # for block in self.chunks[offset].blocks:
            #     self.break_block(block)
                
            chunk_object = self.enabled_chunks[offset]
            chunk_object._derender_chunk()
            
            self.disabled_chunks[offset] = chunk_object
            
            del self.enabled_chunks[offset]
            
            
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
            if chunk_offset not in self.enabled_chunks:
                
                # If it's not, we know it should be, so render it
                self._generate_chunk(chunk_offset)
                
        # Iterate over all the currently rendered chunks
        for chunk_offset in self.enabled_chunks.copy():
            # If the chunk is NOT in the product, it's not in our render distance
            if chunk_offset not in product:
                # ...so we can remove the chunk as it's too far away to care about
                self._derender_chunk(chunk_offset)
                
    def place_block(self, location: tuple, block_type: BlockType):
        block = Block(model='cube', parent=scene, position=location, block_type=block_type)
        
        block.collision = True
        
        # TODO: Possibly a future iteration using a custom block object to extend the vertices for complex textures?
        # block = Block(
        #     model=Mesh(),
        #     parent=scene,
        #     position=location,
        #     texture=texture
        # )
        
        # block_model = load_model('block.obj', use_deepcopy=True)
        
        # block.model.vertices.extend([Vec3(block.x,block.y,block.z) + v for v in 
        #                     block_model.vertices])
        
        # block.model.uvs.extend([Vec2(0,0) + u for u in block_model.uvs])
        
        # block.model.generate()
        
        self.blocks[(block.x,block.y,block.z)] = block
        
        if block_type.place_sound:
            block_type.place_sound.play()
        
    def break_block(self, block: Block, by_player: bool = False):
        """
        Attempt to destroy a block from the World.
        
        Args:
          block (Block): The block to be destroyed.
        """
        block.remove(by_player)
        
        if block in self.blocks:
            del self.blocks[block]
