from surface import SURFACE_HEIGHT, SURFACE_WIDTH
from load_image import pond

POND_RECT = pond.get_rect()
POND_WIDTH = POND_RECT.width
POND_HEIGHT = POND_RECT.height
POND_COOR = (SURFACE_WIDTH / 2 - (POND_WIDTH / 2),
             SURFACE_HEIGHT / 2 - (POND_HEIGHT / 2))
