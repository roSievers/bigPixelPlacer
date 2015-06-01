import pygame
import color

class Window(object):
    """bigPixelPlacer.Window(..) can be created once and is used to interact with the game Window"""
    def __init__(self, pixelSize, width, height,
                 caption="Big Pixel Placer - Unnamed Project",
                 fps=30):
        pygame.init()

        self.pixelSize = pixelSize
        self.width = width
        self.height = height

        self.content = DataContainer(width, height, color.white, self.updatePixel)

        self.refresh_display_size()
        self.caption = caption
        self.dirty = []
        self.display.fill(color.white)
        pygame.display.flip()

        self.fps = fps
        self.clock = pygame.time.Clock()

    def refresh_display_size(self):
        self.display = pygame.display.set_mode((self.width * self.pixelSize, self.height * self.pixelSize))

    @property
    def caption(self):
        return pygame.display.get_caption()
    @caption.setter
    def caption(self, title):
        pygame.display.set_caption(title)

    def frame(self):
        """Start rendering and displaying the current content.
        The function may wait to fulfill fps requirement"""
        self.clock.tick(self.fps)

        # make sure that our changes are transmitted to the screen
        pygame.display.update(self.dirty)
        self.dirty = []

    def updatePixel(self, position, value):
        rect = pygame.Rect(self.pixelSize * position.x,
                           self.pixelSize * position.y,
                           self.pixelSize, self.pixelSize)
        self.display.fill(value, rect)
        self.dirty.append(rect)
        return value

    def events(self):
        for e in pygame.event.get():
            yield e


class DataContainer(object):
    """This class embodies a 2-dimensional array which contains arbitrary data"""
    def __init__(self, width, height, initialValue=None, hook=None):
        self.raw = [[initialValue for y in xrange(height)] for x in xrange(width)]
        self.size = Vector(width, height)
        self.hook = hook # the hook can modify input or react to it.

    def allPositions(self):
        """Returns an iterator over all positions, first by row, then by column."""
        for x in xrange(self.width):
            for y in xrange(self.height):
                yield Vector(x, y)

    def __len__(self):
        return self.size
    def __getitem__(self, key):
        return self.raw[key.x][key.y]
    def __setitem__(self, key, value):
        if self.hook is not None:
            value = self.hook(key, value)
        self.raw[key.x][key.y] = value

class Vector(object):
    """A 2-dimensional vector class."""
    def __init__(self, x, y):
        self.x = x
        self.y = y
    # Here a lot of "magic members" are defined:
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)
    def __ne__(self, other):
        return (self.x != other.x) or (self.y != other.y)
    def __neg__(self):
        return Vector(-self.x, -self.y)
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def __mod__(self, other):
        return Vector(self.x % other.x, self.y % other.y)
    def __str__(self):
        return "(%s, %s)" % (self.x, self.y)

class Matrix(object):
    """A 2x2-dimensional matrix, data input in row form.
    Matrix([[0,-1],[1,0]]) rotates a vector counterclockwise"""
    def __init__(self, data):
        self.data = data
    def __call__(self, input):
        return Vector(self.data[0][0] * input.x + self.data[1][0] * input.y,
                      self.data[0][1] * input.x + self.data[1][1] * input.y)
