from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from numpy import floor

from game.noise import Noise
from game.chunk import Chunk
from game.player import Player
from game.util import BoundingBox

app = Ursina()

chunk_size = 8

terrain = Entity(model=None, collider=None)

noise = Noise(seed = 100, amp=5, freq=24, octaves=2)

chunks = {}

for x in range(-2, 2):
    for z in range(-2, 2):
        print("Generating chunk: ", x, z)
        offset = (x, z)
        chunk = Chunk(noise=noise, chunk_size=chunk_size, parent=terrain, chunk_offset=offset)

        chunk.generate_blocks()
        
        chunks[offset] = chunk
    
terrain.combine()
terrain.collider = 'mesh'
terrain.texture = 'white_cube'

player = Player()


@player.event.listen("chunk_changed")
def position_change(**kwargs):
    chunk = kwargs['chunk']
    # last_chunk = kwargs['last_chunk']
    
    # difference_x = last_chunk[0] - chunk[0]
    # difference_z = last_chunk[1] - chunk[1]
    # print(f"Chunk changed to {chunk[0] - difference_x}, {chunk[1] - difference_z}")

    # offset = (chunk[0] - difference_x, chunk[1] - difference_z)
    # if offset not in chunks:
    #     # Only generate if chunk isn't already generated
    #     chunk = Chunk(noise=noise, chunk_size=chunk_size, parent=terrain, chunk_offset=offset)

    #     chunk.generate_blocks()
        
    #     terrain.combine()
    #     terrain.collider = 'mesh'
    # print("Chunk already exists")
    box = BoundingBox.from_centre_chunk(chunk, radius=2)
    
    # Get all chunks inside of this bounding box
    product = box.get_chunks()
    
    # existing_chunks = list(set(product) & set(chunks.keys()))
    non_existing_chunks = list(set(product) - set(chunks.keys()))
    
    print(f"{len(product) - len(non_existing_chunks)} chunks are not rendered in this box.")
    
    for offset in non_existing_chunks:
        print(f"Rendering new chunk: {offset}")
        chunk = Chunk(noise=noise, chunk_size=chunk_size, parent=terrain, chunk_offset=offset)

        chunk.generate_blocks()
        
        chunks[offset] = chunk
        
    terrain.combine()
    terrain.collider = 'mesh'

def update():
    player._update(chunk_size)

def start():
    app.run()