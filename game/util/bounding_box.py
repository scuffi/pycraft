import itertools
from numpy import floor

class BoundingBox:
    
    @classmethod
    def from_centre(self, pos, radius: int):
        x1 = pos.x - (radius / 2)
        z1 = pos.z - (radius / 2)
        x2 = pos.x + (radius / 2)
        z2 = pos.z + (radius / 2)
        
        return self(x1, z1, x2, z2)
    
    @classmethod
    def from_centre_chunk(self, pos: tuple, radius: int):
        x1 = pos[0] - (radius / 2)
        z1 = pos[1] - (radius / 2)
        x2 = pos[0] + (radius / 2)
        z2 = pos[1] + (radius / 2)
        
        return self(x1, z1, x2, z2)
    
    def __init__(self, x1, z1, x2, z2) -> None:
        self._x1 = int(floor(x1))
        self._z1 = int(floor(z1))
        self._x2 = int(floor(x2))
        self._z2 = int(floor(z2))
    
    def get_product(self):
        range_x = range(self._x1, self._x2 + 1)
        range_z = range(self._z1, self._z2 + 1)
        
        return list(itertools.product(range_x, range_z))
    
class BoundingBox3D:
    
    @classmethod
    def from_centre(self, pos, radius: int):
        x1 = pos.x - (radius / 2)
        y1 = pos.y - (radius / 2)
        z1 = pos.z - (radius / 2)
        
        x2 = pos.x + (radius / 2)
        y2 = pos.y + (radius / 2)
        z2 = pos.z + (radius / 2)
        
        return self(x1, y1, z1, x2, y2, z2)
    
    def __init__(self, x1, y1, z1, x2, y2, z2) -> None:
        self._x1 = int(floor(x1))
        self._y1 = int(floor(y1))
        self._z1 = int(floor(z1))
        
        self._x2 = int(floor(x2))
        self._y2 = int(floor(y2))
        self._z2 = int(floor(z2))
    
    def get_product(self):
        range_x = range(self._x1, self._x2 + 1)
        range_z = range(self._z1, self._z2 + 1)
        range_y = range(self._y1, self._y2 + 1)
        
        return list(itertools.product(range_x, range_y, range_z))
    