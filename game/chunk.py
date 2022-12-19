from ursina import *
from ursina.scene import instance as scene
from numpy import floor

import random

from game.noise import Noise
from game.block import Block

class Chunk:
    def __init__(self, noise: Noise, chunk_size, parent, chunk_offset: tuple[int, int], world, player) -> None:
        self.noise = noise
        self.chunk_size = chunk_size
        
        self.block = load_model('block.obj', use_deepcopy=True)
        
        self.blocks: list[Entity] = []
        self.parent = parent
        # self.chunk = Entity(model=None, collider=None)
        self.offset_x = (chunk_offset[0] * chunk_size)
        self.offset_z = (chunk_offset[1] * chunk_size)
        
        self.world = world
        self.player = player
        
        
        self.color = color.rgba(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)
        
    def generate_blocks(self):
        for i in range(self.chunk_size*self.chunk_size):
            # block = Entity(
            #     model=Mesh(),
            #     color=self.color,
            #     texture='grass',
            #     parent=scene
            # )
            
            # x = floor((i/self.chunk_size) + self.offset_x)
            # z = floor((i%self.chunk_size) + self.offset_z)
            # y = self.noise.get_y(x, z)
            
            # block.model.vertices.extend([Vec3(x,y,z) + v for v in 
            #                     self.block.vertices])
            
            # block.parent = self.parent
            
            
            
            block = Block(model='cube', color=self.color, parent=scene, texture='grass', player=self.player)
            block.x = floor((i/self.chunk_size) + self.offset_x)
            block.z = floor((i%self.chunk_size) + self.offset_z)
            block.y = floor(self.noise.get_y(block.x, block.z))
            # block.parent = self.parent
            
            self.world.blocks[(block.x,block.y,block.z)] = block
            
            self.blocks.append(block)
            
    def delete(self):
        for block in self.blocks:
            block.parent = None
            destroy(block)