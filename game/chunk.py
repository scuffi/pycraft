from ursina import Entity, color, load_model, destroy
from ursina.scene import instance as scene
from numpy import floor

import random

from game.noise import Noise
from game.block import Block
from game.config import DebugSettings

class Chunk:
    def __init__(self, noise: Noise, chunk_size, chunk_offset: tuple[int, int], world) -> None:
        self.noise = noise
        self.chunk_size = chunk_size
        
        self.block = load_model('block.obj', use_deepcopy=True)
        
        self.blocks: list[Entity] = []
        # self.chunk = Entity(model=None, collider=None)
        self.offset_x = (chunk_offset[0] * chunk_size)
        self.offset_z = (chunk_offset[1] * chunk_size)
        
        self.world = world
        
        
        self.color = color.rgba(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
        
    def generate_blocks(self):
        for i in range(self.chunk_size*self.chunk_size):
            # block = Block(
            #     model=Mesh(),
            #     color=self.color,
            #     parent=scene,
            #     player=self.player
            # )
            
            # x = floor((i/self.chunk_size) + self.offset_x)
            # z = floor((i%self.chunk_size) + self.offset_z)
            # y = self.noise.get_y(x, z)
            
            # block.model.vertices.extend([Vec3(x,y,z) + v for v in 
            #                     self.block.vertices])
            
            # block.model.generate()
            
            
            
            block = Block(model='cube', parent=scene, texture='grass')
            block.x = floor((i/self.chunk_size) + self.offset_x)
            block.z = floor((i%self.chunk_size) + self.offset_z)
            block.y = floor(self.noise.get_y(block.x, block.z))
            
            self.world.blocks[(block.x,block.y,block.z)] = block
            
            if DebugSettings.CHUNK_COLOURS:
                block.color = self.color
            
            self.blocks.append(block)