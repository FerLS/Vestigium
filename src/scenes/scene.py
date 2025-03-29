from abc import ABC

NOT_IMPLEMENTED_MSG = "Subclasses must implement this method"

class Scene(ABC):
    """
    Abstract base class for all game scenes. Defines the core interface
    for lifecycle methods that each scene must implement.
    """
    def __init__(self, director):
        """
        Initializes the scene with a reference to the Director.
        """
        self.director = director

    def update(self, *args):
        """
        Updates game logic for the scene. Must be implemented by subclasses.
        """
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)
    
    def events(self, *args):
        """
        Handles input events (e.g., keyboard, mouse). Must be implemented by subclasses.
        """
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)
    
    def draw(self):
        """
        Renders the scene to the screen. Must be implemented by subclasses.
        """
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)
    
    def continue_procedure(self):
        """
        Called when the scene is resumed after being paused or stacked.
        Must be implemented by subclasses.
        """
        raise NotImplementedError(NOT_IMPLEMENTED_MSG)
