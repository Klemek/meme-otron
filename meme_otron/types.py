from enum import IntEnum
import copy


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
        
        self.font = None
        self.font_size = None
        
        self.fill = (0, 0, 0)
        self.stroke_width = 0
        self.stroke_fill = (0, 0, 0)
        
        self.align = "center"
        self.position = Pos.CENTER

    def update(self, base):
        for prop in ["font", "font_size", "fill", "stroke_width",
                     "stroke_fill", "align", "position"]:
            if getattr(self, prop) is None:
                setattr(self,prop, getattr(base, prop))
