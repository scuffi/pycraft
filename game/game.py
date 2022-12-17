from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from numpy import floor

from game.noise import Noise
from game.chunk import Chunk
from game.player import Player

app = Ursina()

chunk_size = 8

terrain = Entity(model=None, collider=None)

noise = Noise(seed = 100, amp=5, freq=24, octaves=2)

for x in range(-2, 2):
    for z in range(-2, 2):
        print("Generating chunk: ", x, z)
        chunk = Chunk(noise=noise, chunk_size=chunk_size, parent=terrain, chunk_offset=(x, z))

        chunk.generate_blocks()
# noise =PerlinNoise(octaves=2, seed=100)
# freq = 24
# amp = 5

# terrain_width = 30

# for i in range(terrain_width*terrain_width):
#     block = Entity(model='cube', color=color.white)
#     block.x = floor(i/terrain_width)
#     block.z = floor(i%terrain_width)
#     block.y = floor(noise([block.x/freq, block.z/freq]) * amp)
#     block.parent = terrain
    
terrain.combine()
terrain.collider = 'mesh'
terrain.texture = 'white_cube'

player = Player()

@player.event.listen("chunk_changed")
def position_change(**kwargs):
    print(f"Chunk changed to {kwargs['chunk']}")

def update():
    player._update(chunk_size)

def start():
    app.run()