from .player import Player
from .world import World

def register_listeners(player: Player, world: World):
    """
    Register any listeners to start listening to events
    
    Args:
      player (Player): The player entity
      world (World): The world object
    """
    
    @player.event.listen("chunk_changed", background=False)
    def chunk_change(args: dict):
        """
        When a chunk is changed, generate the terrain for that chunk
        
        Args:
          args (dict): dict -> Any parameters
        """
        chunk_location = args['chunk']
        
        # Generate the terrain from the new chunk location
        world.generate_terrain(chunk_location)
    
        
    @player.event.listen("position_changed")
    def position_change(args: dict):
        """
        It generates the players interactive area.
        
        Args:
          args (dict): dict -> Any parameters
        """
        # Generate the players bounding area
        player.generate_bounding_area(world)