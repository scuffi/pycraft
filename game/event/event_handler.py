from .callback import Callback

class EventHandler:
    """EventHandler will control, handle and execute events and their respectively registered functions."""
    
    def __init__(self) -> None:
        self.callbacks: dict[str, list[Callback]] = {}
        
    def listen(self, event: str, background: bool = False):
        """
        Add the decorated function to an event that will be executed when the event is triggered.
        
        Args:
          event (str): The event to listen to
          background (bool): If the callback should be executed in the background or not. Defaults to False
        """
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
        """
        If the event is already in the dictionary, add the callback to the list of callbacks for that event.
        Otherwise, create a new list with the callback inside
        
        Args:
          event (str): The name of the event to listen for.
          callback (Callback): The callback function to be called when the event is triggered.
        """
        # Either add the callback to the preexisting list of callbacks...
        if event in self.callbacks:
            self.callbacks[event].append(callback)
        else:
            # ...or create a new list with the callback inside
            self.callbacks[event] = [ callback ]
        
    def trigger(self, event: str, **kwargs):
        """
        Trigger all the callbacks associated with passed event.
        
        Also passes any keyword arguments to the function
        
        Args:
          event (str): The event to trigger.
        """
        if event in self.callbacks:
            for callback in self.callbacks[event]:
                callback.execute(**kwargs)