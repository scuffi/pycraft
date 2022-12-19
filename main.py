from ursina import Ursina

from game.world import World
from game.player import Player
from game.config import WorldSettings

import game

if __name__ == "__main__":
    app = Ursina()
    
    world = World(seed=2341253425)
    player = Player()
    
    world.pregen_world(WorldSettings.RENDER_DISTANCE)
    player.generate_bounding_area(world)
    
    def update():
        player._update(WorldSettings.CHUNK_SIZE)
    
    game.register_listeners(player, world)

    app.run()