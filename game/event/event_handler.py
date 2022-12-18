import inspect
from multiprocessing import Pool
import asyncio

class EventHandler:
    def __init__(self) -> None:
        self.callbacks = {}
        
    def listen(self, event: str):
        # Define a decorator differently as we want parameters
        def decorator(func):
            # Add function to callbacks
            self._add_callback(event, func)
            # Empty wrapper as we don't want to execute any code
            def wrapper():
                ...
                
            return wrapper
        return decorator
    
    def _add_callback(self, event: str, function):
        # Either add the callback to the preexisting list of callbacks...
        if event in self.callbacks:
            self.callbacks[event].append(function)
        else:
            # ...or create a new list with the callback inside
            self.callbacks[event] = [ function ]
        
    def trigger(self, event: str, **kwargs):
        if event in self.callbacks:
            for callback in self.callbacks[event]:
                if inspect.iscoroutinefunction(callback):
                    asyncio.get_event_loop().create_task(callback(**kwargs))
                else:
                    callback(**kwargs)