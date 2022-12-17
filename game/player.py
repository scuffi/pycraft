from ursina.prefabs.first_person_controller import FirstPersonController

class Player:
    def __init__(self) -> None:
        self.controller = FirstPersonController()
        
    @property
    def position(self):
        return self.controller.position