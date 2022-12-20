import sys

from ursina import Entity, scene

from numpy import floor

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
              # Iterate over the area to generate chunks all around the users x and z
              offset = (x, z)
              # Generate the chunk at the given offset
              self._generate_chunk(offset)
                
    def _generate_chunk(self, offset: tuple[int, int]):
      """
      It generates a chunk of blocks based on the noise function and the chunk's offset
      
      Args:
        offset (tuple[int, int]): tuple[int, int]
      """
      # Check if the offset already exists, just not enabled
      if offset not in self.disabled_chunks:
        chunk = Chunk(noise=self.noise, chunk_size=WorldSettings.CHUNK_SIZE, chunk_offset=offset, world=self)
        
        # Check if the default block exists in the registry
        if WorldSettings.DEFAULT_BLOCK not in self.block_registry:
            print("Default block was not found in configuration, please amend.")
            sys.exit(1)

        # Generate the chunk, passing the configured default block
        chunk.generate_chunk(self.block_registry[WorldSettings.DEFAULT_BLOCK])
      else:
        # If it does exist, load it from the dictionary, save time on running already done calculations
        chunk = self.disabled_chunks[offset]
        chunk._render_chunk()
        
        # Delete from disabled chunks, as it's no longer disabled
        del self.disabled_chunks[offset]
      
      # After all processes, the chunk object should be enabled
      self.enabled_chunks[offset] = chunk
        
    def _derender_chunk(self, offset: tuple[int, int]):
      """
      It removes a chunk from the world
      
      Args:
        offset (tuple[int, int]): The offset of the chunk to remove.
      """
      # Only derender the chunk if it's not enabled
      if offset in self.enabled_chunks:
      
        # Get the chunk from the dictionary, and derender it
        chunk_object = self.enabled_chunks[offset]
        chunk_object._derender_chunk()
        
        # Add to disabled chunks, as it still exists, but is no longer rendered
        self.disabled_chunks[offset] = chunk_object
        
        # Remove from enabled chunks, as it's not enabled
        del self.enabled_chunks[offset]
            
            
    def generate_terrain(self, current_location: tuple[float, float]):
      """
      If a chunk is not currently rendered, but should be, render it. If a chunk is currently rendered,
      but shouldn't be, remove it.
      
      This is the core of the terrain generation system. It's a simple, but effective system that allows
      us to render only the chunks that are in our render distance
      
      Args:
        current_location: The location of the player
      """
      # Generate a 2D bounding box around a chunk, where the width is our render distance
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
      """
      It places a block at a given location, and adds it to the world and chunk registries
      
      Args:
        location (tuple): The location of the block to be placed.
        block_type (BlockType): The type of block to place.
      """
      # Find what chunk was the interaction performed in
      chunk = self._get_interacted_chunk(location)
      
      # Instantiate the block object
      block = Block(model='cube', parent=scene, position=location, block_type=block_type)
      
      # As we just placed this, it must be close enough to be collidable
      block.collision = True
      
      # Add the block to the world registry, and the chunk registry
      self.blocks[(block.x,block.y,block.z)] = block
      chunk.blocks[(block.x,block.y,block.z)] = block
      
      # Play the placing sound
      if block_type.place_sound:
          block_type.place_sound.play()
        
    def break_block(self, block: Block, by_player: bool = False):
      """
      Attempt to destroy a block from the World.
      
      Args:
        block (Block): The block to be destroyed.
      """
      # Find what chunk was the interaction performed in
      chunk = self._get_interacted_chunk(block.position)
      
      # Remove the block from the world
      block.remove(by_player)
      
      # Delete from the world registry -> stateless from 'block'
      if block in self.blocks:
          del self.blocks[block]
        
      # Delete from the chunk registry -> stateless from 'block'
      if block in chunk.blocks:
          del chunk.blocks[block]
            
    #! Private functions
    def _get_interacted_chunk(self, location: tuple) -> Chunk:
      """
      It takes a location and returns the chunk that the location is in
      
      Args:
        location (tuple): The location of the player.
      
      Returns:
        A chunk object.
      """
      x,z = floor(location[0] / 8), floor(location[2] / 8)
      chunk = self.enabled_chunks[(x,z)]
      
      return chunk
