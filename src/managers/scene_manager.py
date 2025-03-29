from scenes.scene import Scene
class SceneManager:
    """
    Manages scene registration and transitions. Interfaces with the Director
    to change or stack scenes dynamically during runtime.
    """

    def __init__(self, director):
        """
        Initializes the scene manager with a reference to the Director.
        Stores a mapping of scene names to their corresponding classes.
        
        :param director: The Director instance that manages the game loop and events.
        """
        self.director = director
        self.scenes: dict[str, Scene] = {}

    def register_scene(self, 
                       name: str, 
                       scene_class: Scene):
        """
        Registers a scene class under a given name.
        This allows dynamic instantiation later by name.

        :param name: Unique identifier for the scene (e.g., "MainMenu").
        :param scene_class: The class of the scene to be registered.
        """
        self.scenes[name] = scene_class

    def change_scene(self, name: str):
        """
        Replaces the current scene with a new instance of the specified scene.

        :param name: The name of the scene to switch to (e.g., "GameOver").
        """
        if name in self.scenes:
            self.director.change_scene(self.scenes[name](self.director))

    def stack_scene(self, name: str):
        """
        Adds a new scene instance on top of the current one.
        Useful for overlays like pause menus or dialogs.

        :param name: The name of the scene to stack (e.g., "PauseMenu").
        """
        if name in self.scenes:
            scene_instance = self.scenes[name](self.director)
            self.director.stack_scene(scene_instance)
