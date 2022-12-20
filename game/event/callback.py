import types

from multiprocessing import Process

from dataclasses import dataclass

@dataclass
class Callback:
    """Callback holds needed information for an Event callback to execute"""
    function: types.FunctionType
    asynchronous: bool
    
    def execute(self, **kwargs):
        """
        Execute the stored function.
        
        Passes any arguments given to the function
        """
        if self.asynchronous:
            # TODO: Ursina fails with this, grr
            p = Process(target=self.function, kwargs=kwargs)
            p.start()
        else:
            self.function(kwargs)