from enum import Enum
import copy


class Pos(Enum):
    """
    TODO
    """
    NW = "NW"
    N = "NC"
    NE = "NE"
    W = "CW"
    CENTER = "CC"
    E = "CE"
    SW = "NW"
    S = "NC"
    SE = "NE"


class Meme:
    """
    TODO
    """

    def __init__(self, meme_id, aliases, abstract, template, font, font_size, texts):
        self.id = meme_id
        self.aliases = aliases
        self.abstract = abstract
        self.template = template
        self.font = font
        self.font_size = font_size
        self.texts = texts

    def clone_texts(self):
        return copy.deepcopy(self.texts)

    def clone(self):
        return Meme(self.id,
                    self.aliases,
                    self.abstract,
                    self.template,
                    self.font,
                    self.font_size,
                    self.clone_texts())


class Text:
    """
    TODO
    """

    def __init__(self, text=None):
        self.text = text
        self.x_range = (0, 1)
        self.y_range = (0, 1)
        self.position = Pos.CENTER
        self.font_size = None
        self.fill = (0, 0, 0)
        self.stroke_width = 0
        self.stroke_fill = (0, 0, 0)
        self.font = None
        self.align = "center"
