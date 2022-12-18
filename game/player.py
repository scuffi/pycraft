from ursina.prefabs.first_person_controller import FirstPersonController
from numpy import floor

from game.event import EventHandler

class Player:
    def __init__(self) -> None:
        self.controller = FirstPersonController()
        
        self.event = EventHandler()
        
        self.last_location = None
        self.last_chunk = None
        
    @property
    def position(self):
        return self.controller.position
    
    # ! Private functions
    def _position_changed(self, **kwargs):
        self.event.trigger("position_changed", **kwargs)
        
    def _chunk_changed(self, **kwargs):
        self.event.trigger("chunk_changed", **kwargs)
        
    def _update(self, chunk_size: int):
        if self.position != self.last_location:
            self._position_changed(position=self.position)
            self.last_location = self.position
            
            chunk = (chunk_x, chunk_z) = (floor(self.position.x / chunk_size), floor(self.position.z / chunk_size))
            if chunk != self.last_chunk:
                self._chunk_changed(chunk=chunk, last_chunk=self.last_chunk if self.last_chunk is not None else (0, 0))
                self.last_chunk = chunk
        