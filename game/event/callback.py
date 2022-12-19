import types

from multiprocessing import Process

from dataclasses import dataclass

@dataclass
class Callback:
    function: types.FunctionType
    asynchronous: bool
    
    def execute(self, **kwargs):
        if self.asynchronous:
            print("Operating in new thread")
            p = Process(target=self.function, kwargs=kwargs)
            p.start()
        else:
            self.function(kwargs)