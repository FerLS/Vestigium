class SceneManager:
    def __init__(self, director):
        self.director = director
        self.scenes = {}

    def register_scene(self, name, scene_class):
        self.scenes[name] = scene_class

    def change_scene(self, name):
        if name in self.scenes:
            self.director.change_scene(self.scenes[name](self.director))
    
    def stack_scene(self, name):
        if name in self.scenes:
            scene_instance = self.scenes[name](self.director)
            self.director.stack_scene(scene_instance)

