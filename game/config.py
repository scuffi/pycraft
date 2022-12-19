import yaml

# Load the settings.yml file as that holds all our settings
with open('settings.yml', 'r') as file:
    settings_file = yaml.safe_load(file)

class WorldSettings:
    """WorldSettings relate to settings about the World and generation"""
    CHUNK_SIZE = settings_file['chunk-size']
    RENDER_DISTANCE = settings_file['render-distance']
    
class Settings:
    """Settings relate to general-purpose features that don't need a specific category"""
    REACH = settings_file['reach']
    HOVER_COLOUR = settings_file['hover-colour']
    
class DebugSettings:
    """DebugSettings relate to debug settings that alter gameplay, but allow for visualisations of processes"""
    CHUNK_COLOURS = settings_file['chunk-colours']
    TRAIL = settings_file['colour-derendered']
    BOUNDING_BOX = settings_file['bounding-box']