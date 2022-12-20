import sys
import yaml

from ..game_types import BlockType

def load_blocks(config_file: str) -> dict[str, BlockType]:
    """
    Load the block configuration file into BlockType objects
    
    Args:
      config_file (str): The path to the config file.
    
    Returns:
      A dictionary of BlockType objects.
    """
    try:
        with open(config_file, 'r') as file:
            block_config = yaml.safe_load(file)
    except:
        # Fail if we can't open the file
        print("Failed to load block config, please check it exists and/or is readable.")
        sys.exit(1)
        
    # Return a dictionary mapping the values. If a value is malformed, we skip it
    block_types = {}
    
    # Iterate over the settings file
    for key, item in block_config.items():
        # Try to load the block
        try:
            block = BlockType(name=key,
                        texture=item['texture'],
                        break_sound=item['break_sound'] if 'break_sound' in item else None,
                        place_sound=item['place_sound'] if 'place_sound' in item else None
                    )
            
            block_types[key] = block
        except KeyError:
            # If loading of the block fails, skip this iteration
            print(f"Skipping {key} as the configuration was malformed")

    return block_types