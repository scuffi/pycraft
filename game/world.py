from ursina import Entity, destroy

from game.noise import Noise
from game.config import WorldSettings
from game.chunk import Chunk
from game.block import Block

class World:
    
    def __init__(self, seed: int) -> None:
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
                
    def _generate_chunk(self, offset: tuple[int, int], player):
        chunk = Chunk(noise=self.noise, chunk_size=WorldSettings.CHUNK_SIZE, chunk_offset=offset, world=self, player=player)

        chunk.generate_blocks()
        
        self.chunks[offset] = chunk
        
    def _remove_chunk(self, offset: tuple[int, int]):
        if offset in self.chunks:
            for block in self.chunks[offset].blocks:
                self.break_block(block)
                    
    def break_block(self, block: Block):
        destroy(block)
        
        if block in self.blocks:
            del self.blocks[block]
        else:
            print("Attempted to delete block that doesn't exist!")
