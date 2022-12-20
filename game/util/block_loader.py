import sys
import yaml

from ..game_types import BlockType

def load_blocks(config_file: str) -> dict[str, BlockType]:
    try:
        with open(config_file, 'r') as file:
            block_config = yaml.safe_load(file)
    except:
        print("Failed to load block config, please check it exists and/or is readable.")
        sys.exit(1)
        
    return {
        key: BlockType(name=key, texture=block_config[key]['texture'], break_sound=block_config[key]['break_sound']) for key in block_config.keys()
    }