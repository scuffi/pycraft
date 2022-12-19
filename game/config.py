import yaml
with open('settings.yml', 'r') as file:
    settings_file = yaml.safe_load(file)

class WorldSettings:
    CHUNK_SIZE = settings_file['chunk-size']
    PRE_GENERATION_SIZE = settings_file['pregen-size']
    
class Settings:
    REACH = settings_file['reach']
    
class DebugSettings:
    CHUNK_COLOURS = settings_file['chunk-colours']
    TRAIL = settings_file['colour-derendered']
    BOUNDING_BOX = settings_file['bounding-box']