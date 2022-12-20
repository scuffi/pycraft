from ursina import Text

from .game_types import BlockType
class Inventory:
    """Disclaimer before this class:
        As a managed Inventory would've taken too long to implement, you can image this
        as a class that holds all the blocks, and allows a player to build with any of them.
        This class just allows for the management of blocks, rather than a complex inventory.
    """
    
    def __init__(self, all_blocks: list[BlockType]) -> None:
        self.current_index = 0
        self.all_blocks = all_blocks
        
        self.overlay_text = Text(text=self.all_blocks[self.current_index].name, scale=2, x=-.05, y=-.3)
        
    def is_scrolling(self, key):
        if key == 'scroll up':
            self.current_index = self.current_index + 1 if self.current_index < len(self.all_blocks)-1 else 0
        elif key == 'scroll down':
            self.current_index = self.current_index - 1 if self.current_index > 0 else len(self.all_blocks)-1
            
        self.overlay_text.text = self.all_blocks[self.current_index].name
        
    @property
    def current_block(self) -> BlockType:
        return self.all_blocks[self.current_index]