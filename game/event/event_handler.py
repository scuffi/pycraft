import inspect
import asyncio
from threading import Thread
import multiprocessing
from multiprocess import Pool

class EventHandler:
    def __init__(self) -> None:
        self.callbacks = {}
        self.background = []
        
    def listen(self, event: str, background: bool = False):
        # Define a decorator differently as we want parameters
        def decorator(func):
            # Add function to callbacks
            self._add_callback(event, func)
            
            # Add to background tasks if specified
            if background:
                self.background.append(func)
                
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
                if callback in self.background:
                    # task = asyncio.get_event_loop().create_task(callback(**kwargs))
                    # task = Thread(target=callback, args=(kwargs,))
                    # task.start()
                    # x = multiprocessing.Process(target = callback, daemon=True)
                    # x.start()
                    # with multiprocessing.Pool() as pool:
                    #     pool.apply(callback, args=kwargs)
                        
                    p = Pool(4)
                    p.map(callback, kwargs)
                else:
                    callback(kwargs)
                    # task = asyncio.get_event_loop().create_task(callback(**kwargs))