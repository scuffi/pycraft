from ursina import *

from game.noise import Noise
from game.config import WorldSettings
from game.chunk import Chunk

class World:
    
    def __init__(self, seed: int) -> None:
        self.terrain = Entity(model=None, collider=None)
        self.noise = Noise(seed=seed, amp=5, freq=24, octaves=2)
        
        self.chunks: list[Chunk] = {}
        
        self.blocks: list[Entity] = {}
        
    def pregen_world(self, radius: int):
        """
        Note: Radius must be > 0
        """ 
        for x in range(0-radius, radius):
            for z in range(0-radius, radius):
                offset = (x, z)
                self._generate_chunk(offset)
                
        self._build_terrain()
        
    def _build_terrain(self):
        self.terrain.combine()
        # self.terrain.collider = 'mesh'
        self.terrain.texture = 'grass'
        
    def _generate_chunk(self, offset: tuple[int, int]):
        chunk = Chunk(noise=self.noise, chunk_size=WorldSettings.CHUNK_SIZE, parent=self.terrain, chunk_offset=offset, world=self)

        chunk.generate_blocks()
        
        self.chunks[offset] = chunk
        
    def _remove_chunk(self, offset: tuple[int, int]):
        if offset in self.chunks:
            # self.chunks[offset].delete()
            for block in self.chunks[offset].blocks:
                if block in self.terrain.children:
                    self.terrain.children.remove(block)
                    destroy(block)
