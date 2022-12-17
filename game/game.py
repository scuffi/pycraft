from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from numpy import floor

app = Ursina()

terrain = Entity(model=None, collider=None)
noise =PerlinNoise(octaves=2, seed=100)
freq = 24
amp = 5

terrain_width = 30

for i in range(terrain_width*terrain_width):
    block = Entity(model='cube', color=color.white)
    block.x = floor(i/terrain_width)
    block.z = floor(i%terrain_width)
    block.y = floor(noise([block.x/freq, block.z/freq]) * amp)
    block.parent = terrain
    
terrain.combine()
terrain.collider = 'mesh'
terrain.texture = 'white_cube'

subject = FirstPersonController()

def start():
    app.run()