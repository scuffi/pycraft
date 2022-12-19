from ursina import Entity, Ursina, color
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from numpy import floor

from game.world import World
from game.chunk import Chunk
from game.player import Player
from game.util import BoundingBox, BoundingBox3D
from game.config import WorldSettings, DebugSettings

app = Ursina()

world = World(seed=100)
player = Player()

@player.event.listen("chunk_changed", background=False)
def chunk_change(args: dict):
    chunk = args['chunk']
    
    box = BoundingBox.from_centre_chunk(chunk, radius=2)
    
    # Get all chunks inside of this bounding box
    product = box.get_product()
    
    non_existing_chunks = list(set(product) - set(world.chunks.keys()))
    old_chunks = list(set(world.chunks.keys()) - set(product))
    
    for old_chunk in old_chunks:
        # TODO: Not working, idk why (can't delete an entity??)
        world._remove_chunk(old_chunk)
    
    for new_chunk in non_existing_chunks:
        world._generate_chunk(new_chunk, player)
        
Entity(model='cube', collider='box', color=color.white)

@player.event.listen("position_changed")
def position_change(args: dict):
    # Get users position
    position = args['position']
    # Generate a collision box around 5x5? around the user, using normal chunk generation
    box = BoundingBox3D.from_centre(position, 4)
    
    product = box.get_product()
    
    for old_block in player.interactive_blocks.copy():
        # Check if the block isn't still meant to be interactive
        if old_block not in product:
            
            # If it's not in our existing bounding box it means that the block is now too far away from the player to be interactive
            old_block.collision = False
            
            if DebugSettings.TRAIL:
                old_block.color = color.black
            
            player.interactive_blocks.remove(old_block)
    
    for block_location in product:
        if block_location in world.blocks:
            block = world.blocks[block_location]
            block.collision = True
            
            if DebugSettings.BOUNDING_BOX:
                block.color = color.red
            
            player.interactive_blocks.append(block)
        
def update():
    player._update(WorldSettings.CHUNK_SIZE)
    
def start():
    app.run()