import types

from multiprocessing import Process

from dataclasses import dataclass

# A decorator that creates a class with the given attributes.
@dataclass
class Callback:
    function: types.FunctionType
    asynchronous: bool
    
    def execute(self, **kwargs):
        """
        Execute the stored function.
        
        Passes any arguments given to the function
        """
        if self.asynchronous:
            print("Operating in new thread")
            p = Process(target=self.function, kwargs=kwargs)
            p.start()
        else:
            self.function(kwargs)