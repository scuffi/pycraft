import inspect
from multiprocess import Pool

from .callback import Callback

class EventHandler:
    def __init__(self) -> None:
        self.callbacks: dict[str, list[Callback]] = {}
        
    def listen(self, event: str, background: bool = False):
        # Define a decorator differently as we want parameters
        def decorator(func):
            # Create the callback object
            callback = Callback(func, background)
            
            # Add function to callbacks
            self._add_callback(event, callback)
            
            # Empty wrapper as we don't want to execute any code
            def wrapper():
                ...
                
            return wrapper
        return decorator
    
    def _add_callback(self, event: str, callback: Callback):
        # Either add the callback to the preexisting list of callbacks...
        if event in self.callbacks:
            self.callbacks[event].append(callback)
        else:
            # ...or create a new list with the callback inside
            self.callbacks[event] = [ callback ]
        
    def trigger(self, event: str, **kwargs):
        if event in self.callbacks:
            for callback in self.callbacks[event]:
                callback.execute(**kwargs)