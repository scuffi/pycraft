import types
from dataclasses import dataclass

@dataclass
class Callback:
    function: types.CoroutineType
    asynchronous: bool
    
    def execute(self, **kwargs):
        self.function(kwargs)