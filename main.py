import sys

if __name__ == "__main__":
    
    # Need to import everything here as Multiprocessing does NOT like ursina engine
    # ! As of 19/12/2022 -> Multiprocessing is not used because Ursina is ALLERGIC, leave this here as will continue to try and fix
    from ursina import Ursina
    from game import register_listeners, World, Player, WorldSettings, NoiseSettings, load_blocks, Settings
    
    # Our game object
    app = Ursina()
    
    block_registry = load_blocks(Settings.BLOCK_CONFIG)
    
    # Instantiate a world and a player
    world = World(seed=NoiseSettings.SEED, block_registry=block_registry)
    player = Player(list(block_registry.values()))
    
    # Perform some pre-generation
    world.pregen_world(WorldSettings.RENDER_DISTANCE)
    player.generate_bounding_area(world)
    
    # This function will be automatically called by ursina everytime the engine updates, so here we can call our sub-update functions
    def update():
        player._update(WorldSettings.CHUNK_SIZE)
        
    # This function is also automatically called by ursina on any keypress by the user
    def input(key):
        # Check if the player is interacting with the world
        player.is_interacting(key, world)
        
        # Quit the game if escape is pressed
        if key == "escape":
            sys.exit(0)
                
    # Register all our listeners so the code will properly execute on events
    register_listeners(player, world)
    
    # Finally, run the game.
    app.run()