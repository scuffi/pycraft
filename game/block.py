from ursina import Entity

class Block(Entity):
    
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
    
    def update(self):
        # print("Updated")
        pass