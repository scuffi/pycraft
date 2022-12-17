from perlin_noise import PerlinNoise
from numpy import floor

class Noise:
    
    def __init__(self, seed, amp: int, freq: int, octaves: int) -> None:
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
        return floor(self.noise([x/self.frequency, z/self.frequency]) * self.amplitude)