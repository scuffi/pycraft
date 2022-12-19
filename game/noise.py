from perlin_noise import PerlinNoise
from numpy import floor

class Noise:
    
    def __init__(self, seed, amp: int, freq: int, octaves: int) -> None:
        """
        Noise is a class that holds and implements data relating to PerlinNoise, which is how we generate the chunks.
        
        Args:
          seed: The seed for the noise.
          amp (int): The amplitude of the noise. This is the maximum value that the noise will return.
          freq (int): The frequency of the noise. This is how many times the noise repeats in a given space.
          octaves (int): The number of octaves to use.
        """
        self._seed = seed
        self._amp = amp
        self._freq = freq
        self._octaves = octaves
        
        self._noise = PerlinNoise(octaves=octaves, seed=seed)
    
    @property
    def noise(self):
        return self._noise
    
    @property
    def seed(self):
        return self._seed

    @property
    def amplitude(self):
        return self._amp
    
    @property
    def frequency(self):
        return self._freq
    
    @property
    def octaves(self):
        return self._octaves
    
    def get_y(self, x, z):
        """
        Return a noisy y coordinate based off of the x,z plane.
        
        Args:
          x: The x coordinate of the block
          z: The z coordinate of the block.
        
        Returns:
          The y value of the terrain at the given x and z coordinates.
        """
        return floor(self.noise([x/self.frequency, z/self.frequency]) * self.amplitude)