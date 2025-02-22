from enviorement.tilemap import Tilemap
from levels.scene import Scene
from utils.constants import SCALE_FACTOR, TILE_SIZE

# Mapa de prueba, Dibuja desde abajo a la izquierda para mas comodidad
map_data = [
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 1, 1, 1, 1, 1, 2],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, 7, 7, 7, 7, 7, 8],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, 7, 7, 7, 7, 7, 8],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 6, 7, 7, 7, 7, 7, 8],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 23, 7, 7, 7, 7, 7, 8],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8],
    [6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8],
]
ground_tileset = Tilemap.load_tileset(
    "assets/images/Ground_Tileset.png", TILE_SIZE, 5, 5, TILE_SIZE
)
tilemap = Tilemap(TILE_SIZE, map_data, ground_tileset, SCALE_FACTOR)


class TestLevel(Scene):
    def __init__(self, screen):
        super().__init__(tilemap, screen)
