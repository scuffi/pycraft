import itertools

class BoundingBox:
    """BoundingBox is a 2-dimensional bounding box utility class
    """
    
    @classmethod
    def from_centre(self, pos, width: int):
        """
        `from_centre` takes a position and a width, and returns a rectangle with the position at the centre
        and the width as the length of the sides
        
        Args:
          pos: The position of the centre of the square
          width (int): The width of the rectangle.
        """
        x1 = pos.x - (width / 2)
        z1 = pos.z - (width / 2)
        x2 = pos.x + (width / 2)
        z2 = pos.z + (width / 2)
        
        return self(x1, z1, x2, z2)
    
    @classmethod
    def from_centre_chunk(self, pos: tuple, width: int):
        """
        It takes a position and a width, and returns a new Area object that is centered on the position and
        has the given width. This bounding box method is specifically for chunk's, not world coordinates.
        
        Args:
          pos (tuple): The position of the centre of the chunk.
          width (int): The width of the chunk.
        """
        x1 = pos[0] - (width / 2)
        z1 = pos[1] - (width / 2)
        x2 = pos[0] + (width / 2)
        z2 = pos[1] + (width / 2)
        
        return self(x1, z1, x2, z2)
    
    def __init__(self, x1, z1, x2, z2) -> None:
        """
        Create a bounding box from 2 corners.
        
        Where x1,z1 is the bottom left, and x2,z2 is the top right corner.
        
        Args:
          x1: The x coordinate of the first point.
          z1: The z coordinate of the first point.
          x2: The x coordinate of the second point.
          z2: The z-coordinate of the second point.
        """
        self._x1 = int(round(x1))
        self._z1 = int(round(z1))
        self._x2 = int(round(x2))
        self._z2 = int(round(z2))
    
    def get_product(self):
        """
        It returns a list of tuples, where each tuple is a pair of coordinates (x, z) that are within the
        bounds of the rectangle
        
        Returns:
          A list of tuples.
        """
        range_x = range(self._x1, self._x2 + 1)
        range_z = range(self._z1, self._z2 + 1)
        
        return list(itertools.product(range_x, range_z))
    
class BoundingBox3D:
    """BoundingBox3D is a 3-dimensional bounding box utility class
    """
    
    @classmethod
    def from_centre(self, pos, width: int):
        """
        It takes a position and a width, and returns a box with the position at the centre and the width as
        the size
        
        Args:
          pos: The position of the centre of the cube.
          width (int): The width of the cuboid.
        
        Returns:
          A new instance of the class.
        """
        x1 = pos.x - (width / 2)
        y1 = pos.y - (width / 2)
        z1 = pos.z - (width / 2)
        
        x2 = pos.x + (width / 2)
        y2 = pos.y + (width / 2)
        z2 = pos.z + (width / 2)
        
        return self(x1, y1, z1, x2, y2, z2)
    
    def __init__(self, x1, y1, z1, x2, y2, z2) -> None:
        """
        Creates a 3D bounding box from two points.
        
        Where x1,y1,z1 is the bottom left and x2,y2,z2 are the top right corners.
        
        Args:
          x1: The x coordinate of the first point.
          y1: The y-coordinate of the first point.
          z1: The z-coordinate of the first point.
          x2: The x-coordinate of the second point.
          y2: The y coordinate of the second point.
          z2: The z-coordinate of the end point of the line segment.
        """
        self._x1 = int(round(x1))
        self._y1 = int(round(y1))
        self._z1 = int(round(z1))
        
        self._x2 = int(round(x2))
        self._y2 = int(round(y2))
        self._z2 = int(round(z2))
    
    def get_product(self):
        """
        It takes the coordinates of the bounding box and returns a list of all the coordinates within the
        bounding box
        
        Returns:
          A list of tuples.
        """
        range_x = range(self._x1, self._x2 + 1)
        range_z = range(self._z1, self._z2 + 1)
        range_y = range(self._y1, self._y2 + 1)
        
        return list(itertools.product(range_x, range_y, range_z))
    