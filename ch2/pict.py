# Picture language

# from subprocess import Popen

class Tag:
    "Write html tags easier"
    def __init__(self, name, attributes={}, values=[]):
        self.name = name
        self.attributes = attributes
        self.values = values

    def __str__(self):
        # Ordered dict or list might be a better choice
        # but I don't want that hassle.
        def attr_to_str(d):
            return " ".join("%s=\"%s\"" % (k, v) for k, v in d.items())

        if self.values:
            vals = ''.join(str(val) for val in self.values)
            return "<%s %s>%s</%s>" % (self.name, attr_to_str(self.attributes), vals, self.name)
        else:
            return "<%s %s />" % (self.name, attr_to_str(self.attributes))


class Vect:
    "2d vector"
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vect(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vect(self.x - other.x, self.y - other.y)

    def __rmul__(self, other):
        "scale only for now, other is a number"
        # rudimentary
        if isinstance(other, int) or isinstance(other, float):
            return Vect(other * self.x, other * self.y)
        else:
            raise Exception

    def to_int(self):
        self.x = int(round(self.x))
        self.y = int(round(self.y))
        return self

class Frame:
    ""
    def __init__(self, origin, edge1, edge2):
        self.origin = origin
        self.edge1 = edge1
        self.edge2 = edge2

    def coord_map(self):
        def apply_vect(v):
            return (self.origin + v.x * self.edge1 + v.y * self.edge2).to_int()
        return apply_vect


class Shape:
    pass


class Line(Shape):
    def __init__(self, start, end, stroke_width=1, stroke="black"):
        self.start = start
        self.end = end
        self.stroke_width = stroke_width
        self.stroke = stroke

    def apply_frame(self, frame):
        m = frame.coord_map()
        new_start = m(self.start)
        new_end = m(self.end)
        attrs = {'x1': new_start.x,
                 'y1': new_start.y,
                 'x2': new_end.x,
                 'y2': new_end.y,
                 'stroke-width': self.stroke_width,
                 'stroke': self.stroke}
        return Tag('line', attrs)

# svg circle or rectangles can't be directly used
# because they can't be fit in a twisted frame
# you need to implement them with lower level shapes.

def shapes2painter(shapes):
    def apply_frame(frame):
        tags = []
        for shape in shapes:
            tags.append(shape.apply_frame(frame))
        return tags
    return apply_frame


def transform_painter(painter, origin, corner1, corner2):
    def apply_frame(frame):
        m = frame.coord_map()
        new_origin = m(origin)
        return painter(Frame(new_origin,
                             m(corner1) - new_origin,
                             m(corner2) - new_origin))
    return apply_frame


def flip_vert(painter):
    return transform_painter(painter,
                             Vect(0, 1),
                             Vect(1, 1),
                             Vect(0, 0))

def flip_horiz(painter):
    return transform_painter(painter,
                             Vect(1, 0),
                             Vect(0, 0),
                             Vect(1, 1))


def beside(painter1, painter2):
    split_point = Vect(0.5, 0)
    paint_left = transform_painter(painter1,
                                   Vect(0, 0),
                                   split_point,
                                   Vect(0, 1))
    paint_right = transform_painter(painter2,
                                    split_point,
                                    Vect(1, 0),
                                    Vect(0.5, 1))
    def apply_frame(frame):
        # paint_left(frame) : a list of tags
        return paint_left(frame) + paint_right(frame)
    return apply_frame

def below(painter1, painter2):
    split_point = Vect(0, 0.5)
    paint_upper = transform_painter(painter2,
                                    split_point,
                                    Vect(1, 0.5),
                                    Vect(0, 1))
    paint_lower = transform_painter(painter1,
                                    Vect(0, 0),
                                    Vect(1, 0),
                                    Vect(0, 0.5))
    def apply_frame(frame):
        return paint_upper(frame) + paint_lower(frame)
    return apply_frame

def right_split(painter, n):
    if n == 0:
        return painter
    else:
        smaller = right_split(painter, n - 1)
        return beside(painter, below(smaller, smaller))

def up_split(painter, n):
    if n == 0:
        return painter
    else:
        smaller = up_split(painter, n - 1)
        return below(painter, beside(smaller, smaller))

def corner_split(painter, n):
    if n == 0:
        return painter
    else:
        up = up_split(painter, n - 1)
        right = right_split(painter, n - 1)
        top_left = beside(up, up)
        bottom_right = below(right, right)
        corner = corner_split(painter, n - 1)
        return beside(below(painter, top_left),
                      below(bottom_right, corner))

def square_limit(painter, n):
    quarter = corner_split(painter, n)
    half = beside(flip_horiz(quarter), quarter)
    return below(flip_vert(half), half)


def draw(painter, width=600, height=600):
    frame = Frame(Vect(0, height), Vect(width, 0), Vect(0, -height))
    tags = painter(frame)
    return str(Tag('svg', {'width': width, 'height': height}, tags))


if __name__ == '__main__':
    wave_lines = [
        Line(Vect(0.006, 0.840), Vect(0.155, 0.591)),
        Line(Vect(0.006, 0.635), Vect(0.155, 0.392)),
        Line(Vect(0.304, 0.646), Vect(0.155, 0.591)),
        Line(Vect(0.298, 0.591), Vect(0.155, 0.392)),
        Line(Vect(0.304, 0.646), Vect(0.403, 0.646)),
        Line(Vect(0.298, 0.591), Vect(0.354, 0.492)),
        Line(Vect(0.403, 0.646), Vect(0.348, 0.845)),
        Line(Vect(0.354, 0.492), Vect(0.249, 0.000)),
        Line(Vect(0.403, 0.000), Vect(0.502, 0.293)),
        Line(Vect(0.502, 0.293), Vect(0.602, 0.000)),
        Line(Vect(0.348, 0.845), Vect(0.403, 0.999)),
        Line(Vect(0.602, 0.999), Vect(0.652, 0.845)),
        Line(Vect(0.652, 0.845), Vect(0.602, 0.646)),
        Line(Vect(0.602, 0.646), Vect(0.751, 0.646)),
        Line(Vect(0.751, 0.646), Vect(0.999, 0.343)),
        Line(Vect(0.751, 0.000), Vect(0.597, 0.442)),
        Line(Vect(0.597, 0.442), Vect(0.999, 0.144)),
    ]

    wave_file = 'wave.html'

    with open(wave_file, 'w') as f:
        wave = shapes2painter(wave_lines)
        waves = square_limit(wave, 5)
        f.write(draw(waves))

    # Popen(['open', '-a', 'Google Chrome', wave_file])
