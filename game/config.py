import yaml

# Load the settings.yml file as that holds all our settings
with open('settings.yml', 'r') as file:
    settings_file = yaml.safe_load(file)

class WorldSettings:
    """WorldSettings relate to settings about the World and generation"""
    CHUNK_SIZE = settings_file['chunk-size']
    RENDER_DISTANCE = settings_file['render-distance']
    DEFAULT_BLOCK = settings_file['default-block']
    
    
class NoiseSettings:
    """NoiseSettings relate to Noise specific configuration, as the world is based off of noise, editing these will change the world generation"""
    SEED = settings_file['seed']
    AMPLITUDE = settings_file['amplitude']
    FREQUENCY = settings_file['frequency']
    OCTAVES = settings_file['octaves']
    
class Settings:
    """Settings relate to general-purpose features that don't need a specific category"""
    REACH = settings_file['reach']
    HOVER_COLOUR = settings_file['hover-colour']
    BLOCK_CONFIG = settings_file['block-config']
    
class DebugSettings:
    """DebugSettings relate to debug settings that alter gameplay, but allow for visualisations of processes"""
    CHUNK_COLOURS = settings_file['chunk-colours']
    TRAIL = settings_file['colour-derendered']
    BOUNDING_BOX = settings_file['bounding-box']