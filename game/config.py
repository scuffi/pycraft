import yaml
with open('settings.yml', 'r') as file:
    settings_file = yaml.safe_load(file)

class WorldSettings:
    CHUNK_SIZE = settings_file['chunk-size']
    PRE_GENERATION_SIZE = settings_file['pregen-size']
    
class Settings:
    REACH = settings_file['reach']