from ursina import Text

from .game_types import BlockType
class Inventory:
    """Disclaimer before this class:
        As a managed Inventory would've taken too long to implement, you can image this
        as a class that holds all the blocks, and allows a player to build with any of them.
        This class just allows for the management of blocks, rather than a complex inventory.
    """
    
    def __init__(self, all_blocks: list[BlockType]) -> None:
        """
        Create an inventory.
        
        Args:
          all_blocks (list[BlockType]): list[BlockType]
        """
        self.current_index = 0
        self.all_blocks = all_blocks
        
        self.overlay_text = Text(text=self._get_overlay_text(), scale=2, x=-.85, y=.5)
        
    def is_scrolling(self, key: str):
        """
        If the user is scrolling up, increment the current index by 1, unless the current index is already
        at the end of the list, in which case set it to 0. If the user is scrolling down, decrement the
        current index by 1, unless the current index is already at the beginning of the list, in which case
        set it to the end of the list
        
        Args:
          key (str): The key that was pressed
        """
        if key == 'scroll up':
            self.current_index = self.current_index + 1 if self.current_index < len(self.all_blocks)-1 else 0
        elif key == 'scroll down':
            self.current_index = self.current_index - 1 if self.current_index > 0 else len(self.all_blocks)-1
            
        self.overlay_text.text = self._get_overlay_text()
        
    def _get_overlay_text(self) -> str:
        """
        It returns a string that contains the name of the block that the player is currently holding
        
        Returns:
          The name of the block that is currently being held.
        """
        return f"Holding: {self.all_blocks[self.current_index].name}"
        
    @property
    def current_block(self) -> BlockType:
        """
        The current block being held.
        """
        return self.all_blocks[self.current_index]