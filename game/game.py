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

# Pregeneration of world & boxes
world.pregen_world(WorldSettings.RENDER_DISTANCE)
player.generate_bounding_area(world)

@player.event.listen("chunk_changed", background=False)
def chunk_change(args: dict):
    chunk_location = args['chunk']
    
    box = BoundingBox.from_centre_chunk(chunk_location, radius=WorldSettings.RENDER_DISTANCE)
    
    # Get all chunks inside of this bounding box
    product = box.get_product()
    
    # Iterate over all the chunks that SHOULD exist
    for chunk_offset in product:
        # Check if chunk is currently rendered
        if chunk_offset not in world.chunks:
            
            # If it's not, we know it should be, so render it
            world._generate_chunk(chunk_offset)
            
    # Iterate over all the currently rendered chunks
    for chunk_offset in world.chunks.copy():
        # If the chunk is NOT in the product, it's not in our render distance
        if chunk_offset not in product:
            # ...so we can remove the chunk as it's too far away to care about
            world._remove_chunk(chunk_offset)
    
Entity(model='cube', collider='box')

@player.event.listen("position_changed")
def position_change(args: dict):
    # Generate the players bounding area
    player.generate_bounding_area(world)
        
def update():
    player._update(WorldSettings.CHUNK_SIZE)
    
def start():
    app.run()