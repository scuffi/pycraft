from multiprocess import Process

if __name__ == "__main__":
    
    # Need to import everything here as Multiprocessing does NOT like ursina engine
    # ! As of 19/12/2022 -> Multiprocessing is not used because Ursina is ALLERGIC, leave this here as will continue to try and fix
    from ursina import Ursina, raycast, camera, mouse
    from game import register_listeners, World, Player, WorldSettings, NoiseSettings
    
    # Our game object
    app = Ursina()
    
    # Instantiate a world and a player
    world = World(seed=NoiseSettings.SEED)
    player = Player()
    
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
                
    # Register all our listeners so the code will properly execute on events
    register_listeners(player, world)
    
    # TODO: Implement multiprocessing as a constant background process, rather than one ran every event
    
    # Finally, run the game.
    app.run()