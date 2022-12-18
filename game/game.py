from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from numpy import floor

from game.world import World
from game.chunk import Chunk
from game.player import Player
from game.util import BoundingBox
from game.config import WorldSettings

app = Ursina()

world = World(seed=100)
player = Player()

@player.event.listen("chunk_changed")
def chunk_change(**kwargs):
    chunk = kwargs['chunk']
    box = BoundingBox.from_centre_chunk(chunk, radius=2)
    
    # Get all chunks inside of this bounding box
    product = box.get_product()
    
    # existing_chunks = list(set(product) & set(chunks.keys()))
    non_existing_chunks = list(set(product) - set(world.chunks.keys()))
    old_chunks = list(set(world.chunks.keys()) - set(product))
    
    for old_chunk in old_chunks:
        # TODO: Not working, idk why (can't delete an entity??)
        world._remove_chunk(old_chunk)
    
    for new_chunk in non_existing_chunks:
        world._generate_chunk(new_chunk)
        
    world._build_terrain()
    
shellRadius = 3
shells = [Entity(model='block.obj', collider='box', highlight_color=color.lime) for i in range(shellRadius * shellRadius)]

@player.event.listen("position_changed")
def position_change(**kwargs):
    # Get users position
    position = kwargs['position']
    # Generate a collision box around 5x5? around the user, using normal chunk generation
    for i in range(len(shells)):
        x = shells[i].x = floor((i/shellRadius) + player.position.x)
        z = shells[i].z = floor((i%shellRadius) + player.position.z)
        shells[i].y = world.noise.get_y(x, z)

def update():
    player._update(WorldSettings.CHUNK_SIZE)
    
def start():
    app.run()