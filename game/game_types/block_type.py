from dataclasses import dataclass

from ursina import Audio

@dataclass
class BlockType:
    name: str
    texture: str
    break_sound: Audio | None
    place_sound: Audio | None
    
    def __init__(self, name: str, texture: str, break_sound: Audio | None, place_sound: Audio | None) -> None:
        """
        It creates a new BlockType object
        
        Args:
          name (str): The name of the block.
          texture (str): The texture of the block.
          break_sound (Audio | None): The sound that plays when the block is broken.
          place_sound (Audio | None): The sound that plays when the block is placed.
        """
        self.name = name
        self.texture = texture
        
        self.break_sound = None
        self.place_sound = None
        
        if break_sound:
            self.break_sound = Audio(break_sound, autoplay=False)
            
        if place_sound:
            self.place_sound = Audio(place_sound, autoplay=False)

    