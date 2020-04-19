from enum import IntEnum
import copy

DEFAULT_FONT = "arial"
DEFAULT_FONT_SIZE = 0.05


class Pos(IntEnum):
    """
    TODO
    """
    NW = 0
    N = 1
    NE = 2
    W = 3
    CENTER = 4
    E = 5
    SW = 6
    S = 7
    SE = 8


class Meme:
    """
    TODO
    """

    def __init__(self, meme_id):
        self.id = meme_id
        self.aliases = []
        self.abstract = None
        self.info = None
        self.template = None
        self.text_base = Text()
        self.texts = None

    def clone(self):
        return copy.deepcopy(self)


class Text:
    """
    TODO
    """
    base_properties = ["font", "font_size", "fill", "stroke_width",
                       "stroke_fill", "align", "position"]

    def __init__(self, text=None):
        self.text = text
        self.text_ref = None

        self.style_ref = None

        self.x_range = (0, 1)
        self.y_range = (0, 1)
        self.angle = None

        self.font = None
        self.font_size = None

        self.fill = None
        self.stroke_width = None
        self.stroke_fill = None

        self.align = None
        self.position = None

    def update(self, base):
        """
        TODO

        :param (Text) base:
        """
        for prop in Text.base_properties:
            if getattr(self, prop) is None:
                setattr(self, prop, getattr(base, prop))

    def init(self):
        """
        TODO
        """
        if self.x_range is None:
            self.x_range = (0, 1)
        if self.y_range is None:
            self.y_range = (0, 1)
        if self.angle is None:
            self.angle = 0
        if self.font is None:
            self.font = DEFAULT_FONT
        if self.font_size is None:
            self.font_size = DEFAULT_FONT_SIZE
        if self.align is None:
            self.align = "center"
        if self.fill is None:
            self.fill = (0, 0, 0)
        else:
            self.fill = tuple(self.fill)
        if self.stroke_fill is None:
            self.stroke_fill = (0, 0, 0)
        else:
            self.stroke_fill = tuple(self.stroke_fill)
        if self.stroke_width is None:
            self.stroke_width = 0
        if self.position is None:
            self.position = Pos.CENTER
