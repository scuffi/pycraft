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
world.pregen_world(WorldSettings.PRE_GENERATION_SIZE)
player.generate_bounding_area(world)

@player.event.listen("chunk_changed", background=False)
def chunk_change(args: dict):
    chunk = args['chunk']
    
    box = BoundingBox.from_centre_chunk(chunk, radius=2)
    
    # Get all chunks inside of this bounding box
    product = box.get_product()
    
    non_existing_chunks = list(set(product) - set(world.chunks.keys()))
    old_chunks = list(set(world.chunks.keys()) - set(product))
    
    # TODO: Fix as this does not work
    for old_chunk in old_chunks:
        world._remove_chunk(old_chunk)
    
    for new_chunk in non_existing_chunks:
        world._generate_chunk(new_chunk)
        
@player.event.listen("position_changed")
def position_change(args: dict):
    # Generate the players bounding area
    player.generate_bounding_area(world)
        
def update():
    player._update(WorldSettings.CHUNK_SIZE)
    
def start():
    app.run()