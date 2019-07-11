# pylint: disable=line-too-long
"""
misc.py
Some miscellaneous functions and classes will be provided here
"""

import math
import settings


class Count:
    """
    Class to keep count of variable
    """
    def __init__(self):
        """
        Args:
            (None)

        Returns:
            (None)
        """
        self.idx = -1

    def inc(self):
        """
        This method increases the count by 1 and returns the new count

        Args:
            (None)

        Returns:
            (int) : The updated count is returned
        """
        self.idx += 1
        return self.idx


class Hermite:
    """
    To keep the hermite curve stored inside this
    """
    def __init__(self, p1, p2, t1, t2):
        """
        Args:
            p1 (float)  : First control point of bezier curve
            p2 (float)  : Fourth control point
            t1 (float)  : Second control point
            t2 (float)  : Third control point

        Returns:
            (None)
        """
        self.p1 = p1
        self.p2 = p2
        self.t1 = t1
        self.t2 = t2
        self.sync()

    def sync(self):
        """
        Calculates the coefficients and variables required in calculation of
        derivative and value of the curve at time t.
        Here p1, p2, t1, t2 are control points of bezier curve and a, b, c, d
        are control points of hermite
        """
        self.a = self.p1
        self.b = self.p1 + self.t1/3
        self.c = self.p2 - self.t2/3
        self.d = self.p2

        self.coeff0 = self.a
        self.coeff1 = self.b*3- self.a*3
        self.coeff2 = self.c*3 - self.b*6 + self.a*3
        self.coeff3 = self.d - self.c*3 + self.b*3 - self.a

    def derivative(self, x):
        """
        Calculates the derivative of the curve at x

        Args:
            x (float) : Time at which the derivative is needed

        Returns:
            (float) : The value of the derivative at time x
        """
        y = 1 - x
        ret = ((self.b - self.a) * y * y + (self.c - self.b) * x * y * 2 + (self.d - self.c) * x * x) * 3
        return ret

    def value(self, t):
        """
        Calculates the value of the curve at time t

        Args:
            t (float) : Time at which the value is needed

        Returns:
            (float) : Value of the curve at time t
        """
        ret = self.coeff0 + (self.coeff1 + (self.coeff2 + (self.coeff3)*t)*t)*t
        return ret


class Matrix2:
    """
    Will store a Matrix 2X2
    """
    def __init__(self, m00=1.0, m01=0.0, m10=0.0, m11=1.0):
        self.m00 = m00
        self.m01 = m01
        self.m10 = m10
        self.m11 = m11

    def set_rotate(self, angle):
        """
        This will serve as a rotation matrix with angle `angle`
        """
        c = math.cos(angle)
        s = math.sin(angle)
        self.m00, self.m01 = c, s
        self.m10, self.m11 = -s, c

    def get_transformed(self, v):
        """
        Rotate or transform a vector using this Matrix
        """
        ret = Vector()
        x, y = v[0], v[1]
        ret[0] = x*self.m00 + y*self.m10
        ret[1] = x*self.m01 + y*self.m11
        return ret


class Vector:
    """
    To store the position of layers
    val1 represents the x-axis value
    val2 represents the y-axis value

    For other parameters
    val1 represents the value of the parameter
    val2 represents the time parameter

    type represents what this vector is representing
    """

    def __init__(self, val1=0, val2=0, _type=None):
        """
        Args:
            val1  (float) : First value of the vector
            val2  (float) : Second value of the vector
            _type (:obj: `str`, optional)  : Type of vector

        Returns:
            (None)
        """
        self.val1 = val1
        self.val2 = val2
        self.type = _type

    def __str__(self):
        return "({0},{1}, {2})".format(self.val1, self.val2, self.type)

    def __add__(self, other):
        val1 = self.val1 + other.val1
        val2 = self.val2 + other.val2
        return Vector(val1, val2, self.type)

    def __sub__(self, other):
        val1 = self.val1 - other.val1
        val2 = self.val2 - other.val2
        return Vector(val1, val2, self.type)

    def __neg__(self):
        return -1 * self

    def __getitem__(self, key):
        if key:
            return self.val2
        return self.val1

    def __setitem__(self, key, value):
        if key:
            self.val2 = value
        else:
            self.val1 = value

    def mag(self):
        """
        Returns the magnitude of the vector

        Args:
            (None)
        Returns:
            (float) : The magnitude of the vector
        """
        return math.sqrt(self.mag_squared())

    def inv_mag(self):
        """
        Returns the inverse of the magnitude of the vector

        Args:
            (None)
        Returns:
            (float) : Magnitude inversed
        """
        return 1.0 / self.mag()

    def perp(self):
        """
        Returns a perpendicular version of the vector

        Args:
            (None)
        Returns:
            (misc.Vector) : Perpendicular vector with same magnitude
        """
        return Vector(self.val2, -self.val1)

    def is_equal_to(self, other):
        """
        Tells if the current vector is equal to `other` vector

        Args:
            other (misc.Vector) : The vector to be compared with

        Returns:
            (bool) : True if the vectors are equal
                   : False otherwise
        """
        return approximate_equal((self - other).mag_squared(), 0)

    def mag_squared(self):
        """
        Returns the squared magnitude of the vector

        Args:
            (None)
        Returns:
            (float) : squared magnitude
        """
        ret = self.val1 * self.val1 + self.val2 * self.val2
        return ret

    def norm(self):
        """
        Returns a normalised version of the vector

        Args:
            (None)
        Returns:
            (misc.Vector) : itselves whose magnitude is 1
        """
        obj = self * self.inv_mag()
        self.__dict__.update(obj.__dict__)
        return self

    # other can only be of type real
    def __mul__(self, other):
        if not isinstance(other, self.__class__):
            val1 = self.val1 * other
            val2 = self.val2 * other
            return Vector(val1, val2, self.type)
        elif isinstance(other, self.__class__):
            return self.val1*other.val1 + self.val2*other.val2
        raise Exception('Multiplication with {} not defined'.format(type(other)))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, self.__class__):
            val1 = self.val1 / other
            val2 = self.val2 / other
            return Vector(val1, val2, self.type)
        raise Exception('Division with {} not defined'.format(type(other)))

    def get_list(self):
        """
        Get val1 and val2 values in the format required by lottie

        Args:
            (None)

        Returns:
            (list) : Contains the Vector in list format
        """
        return [self.val1, self.val2]

    def get_val(self):
        """
        Get value in the format required by lottie

        Args:
            (None)

        Returns:
            (list) : Depending upon _type a list is returned
        """
        if self.type == "origin":
            return [self.val1, self.val2]
        elif self.type == "circle_radius":
            return [self.val1, self.val1]
        elif self.type in {"rectangle_size", "image_scale", "scale_layer_zoom", "group_layer_scale"}:
            return [self.val1, self.val3]
        else:
            return [self.val1]

    def add_new_val(self, val3):
        """
        This function store an additional value in the vector.
        This is currently required by the rectangle layer

        Args:
            val3 (float) : Some Vectors need additional value to be used later

        Returns:
            (None)
        """
        self.val3 = val3

    def set_type(self, _type):
        """
        This set's the type of the Vector

        Args:
            _type (str) : Type of Vector to be set

        Returns:
            (None)
        """
        self.type = _type


class Color:
    """
    To store the colors in Synfig and operations on them
    """

    def __init__(self, red=1, green=1, blue=1, alpha=1):
        """
        Args:
            red (:obj: `float`, optional) : Red value of color
            green (:obj: `float`, optional) : Green value of color
            blue (:obj: `float`, optional) : Blue value of color
            alpha (:obj: `float`, optional) : Alpha value of color

        Returns:
            (None)
        """
        self.red = red
        self.green = green
        self.blue = blue
        self.alpha = alpha

    def __str__(self):
        return "({0}, {1}, {2}, {3})".format(self.red, self.green, self.blue,
                                             self.alpha)

    def __add__(self, other):
        red = self.red + other.red
        green = self.green + other.green
        blue = self.blue + other.blue
        return Color(red, green, blue, self.alpha)

    def __sub__(self, other):
        red = self.red - other.red
        green = self.green - other.green
        blue = self.blue - other.blue
        return Color(red, green, blue, self.alpha)

    def __mul__(self, other):
        if not isinstance(other, self.__class__):
            red = self.red * other
            green = self.green * other
            blue = self.blue * other
            return Color(red, green, blue, self.alpha)
        raise Exception('Multiplication with {} not defined'.format(type(other)))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if not isinstance(other, self.__class__):
            red = self.red / other
            green = self.green / other
            blue = self.blue / other
            return Color(red, green, blue, self.alpha)
        raise Exception('Division with {} not defined'.format(type(other)))

    def get_val(self):
        """
        Get the color in the format required by lottie

        Args:
            (None)

        Returns:
            (list) : Stores color in list format
        """
        return [self.red, self.green, self.blue, self.alpha]


def approximate_equal(a, b):
    """
    Need to define this function somewhere else, a and b are of type "float"

    Args:
        a (float) : First number to be compared
        b (float) : Second number to be compared

    Returns:
        (bool) : True if the numbers are approximately equal under precision
               : False otherwise
    """
    precision = 1e-8
    if a < b:
        return b - a < precision
    return a - b < precision


def calculate_pixels_per_unit():
    """
    Gives the value of 1 unit in terms of pixels according to the canvas defined

    Args:
        (None)

    Returns:
        (float) : Pixels per unit
    """
    image_width = float(settings.lottie_format["w"])
    image_area_width = settings.view_box_canvas["val"][2] - settings.view_box_canvas["val"][0]
    settings.PIX_PER_UNIT = image_width / image_area_width
    return settings.PIX_PER_UNIT


def change_axis(x_val, y_val, is_transform=False):
    """
    Convert synfig axis coordinates into lottie format

    Args:
        x_val (float | str) : x axis value in pixels
        y_val (float | str) : y axis value in pixels
        is_transform (`obj`: bool, optional) : Is this value used in transform module?

    Returns:
        (list)  : x and y axis value in Lottie format
    """
    x_val, y_val = float(x_val), float(y_val)
    if is_transform:
        x_val, y_val = x_val, -y_val
    else:
        x_val, y_val = x_val + settings.lottie_format["w"]/2, -y_val + settings.lottie_format["h"]/2
    return [x_val, y_val]


def parse_position(animated, i):
    """
    To convert the synfig coordinates from units(initially a string) to pixels
    Depends on whether a vector is provided to it or a real value
    If real value is provided, then time is also taken into consideration

    Args:
        animated (lxml.etree._Element) : Stores animation which contains waypoints
        i        (int)                 : Iterator over animation

    Returns:
        (misc.Vector) If the animated type is not color
        (misc.Color)  Else if the animated type is color
    """
    if animated.attrib["type"] == "vector":
        pos = [float(animated[i][0][0].text),
               float(animated[i][0][1].text)]
        pos = [settings.PIX_PER_UNIT*x for x in pos]

    elif animated.attrib["type"] == "real":
        pos = parse_value(animated, i)

    elif animated.attrib["type"] == "circle_radius":
        pos = parse_value(animated, i)
        pos[0] *= 2 # Diameter

    elif animated.attrib["type"] == "angle":
        pos = [get_angle(float(animated[i][0].attrib["value"])),
               get_frame(animated[i])]

    elif animated.attrib["type"] in {"region_angle", "star_angle_new"}:
        pos = [float(animated[i][0].attrib["value"]),
               get_frame(animated[i])]

    elif animated.attrib["type"] == "rotate_layer_angle":
        # Angle needs to made neg of what they are
        pos = [-float(animated[i][0].attrib["value"]),
               get_frame(animated[i])]

    elif animated.attrib["type"] == "opacity":
        pos = [float(animated[i][0].attrib["value"]) * settings.OPACITY_CONSTANT,
               get_frame(animated[i])]

    elif animated.attrib["type"] == "effects_opacity":
        pos = [float(animated[i][0].attrib["value"]),
               get_frame(animated[i])]

    elif animated.attrib["type"] == "points":
        pos = [int(animated[i][0].attrib["value"]),
               get_frame(animated[i])]

    elif animated.attrib["type"] == "rectangle_size":
        pos = parse_value(animated, i)
        vec = Vector(pos[0], pos[1], animated.attrib["type"])
        vec.add_new_val(float(animated[i][0].attrib["value2"]) * settings.PIX_PER_UNIT)
        return vec

    elif animated.attrib["type"] == "image_scale":
        val = float(animated[i][0].attrib["value"])
        val2 = get_frame(animated[i])
        vec = Vector(val, val2, animated.attrib["type"])
        vec.add_new_val(float(animated[i][0].attrib["value2"]))
        return vec

    elif animated.attrib["type"] == "scale_layer_zoom":
        val = (math.e ** float(animated[i][0].attrib["value"])) * 100
        val2 = get_frame(animated[i])
        vec = Vector(val, val2, animated.attrib["type"])
        vec.add_new_val(val)
        return vec

    elif animated.attrib["type"] == "group_layer_scale":
        val1 = float(animated[i][0][0].text) * 100
        val3 = float(animated[i][0][1].text) * 100
        vec = Vector(val1, get_frame(animated[i]), animated.attrib["type"])
        vec.add_new_val(val3)
        return vec

    elif animated.attrib["type"] == "time":
        val = parse_time(animated[i][0].attrib["value"])    # Needed in seconds
        val2 = get_frame(animated[i])   # Needed in frames
        return Vector(val, val2, animated.attrib["type"])

    elif animated.attrib["type"] == "color":
        red = float(animated[i][0][0].text)
        green = float(animated[i][0][1].text)
        blue = float(animated[i][0][2].text)
        alpha = float(animated[i][0][3].text)
        red = red ** (1/settings.GAMMA)
        green = green ** (1/settings.GAMMA)
        blue = blue ** (1/settings.GAMMA)
        return Color(red, green, blue, alpha)

    return Vector(pos[0], pos[1], animated.attrib["type"])


def parse_value(animated, i):
    """
    To convert the synfig value parameter from units to pixels
    and also take into consideration the time parameter

    Args:
        animated (lxml.etree._Element) : Stores animation which holds waypoints
        i        (int)                 : Iterator for animation

    Returns:
        (list)  : [value, time] is returned
    """
    pos = [float(animated[i][0].attrib["value"]) * settings.PIX_PER_UNIT,
           get_frame(animated[i])]
    return pos


def get_angle(theta):
    """
    Converts the .sif angle into lottie angle
    .sif uses positive x-axis as the start point and goes anticlockwise
    lottie uses positive y-axis as the start point and goes clockwise

    Args:
        theta (float) : Stores Synfig format angle

    Returns:
        (int)   : Lottie format angle
    """
    theta = int(theta)
    shift = -int(theta / 360)
    theta = theta % 360
    theta = (90 - theta) % 360

    theta = theta + shift * 360
    return theta


def is_animated(node):
    """
    Tells whether a parater is animated or not

    Args:
        node (lxml.etree._Element) : Animation which stores waypoints

    Returns:
        (int) : Depending upon whether the parameter is animated, following
                values are returned
                0: If not animated
                1: If only single waypoint is present
                2: If more than one waypoint is present
    """
    case = 0
    if node.tag == "animated":
        if len(node) == 1:
            case = 1
        else:
            case = 2
    else:
        case = 0
    return case


def clamp_col(color):
    """
    This function converts the colors into int and takes them to the range of
    0-255

    Args:
        color (float) : Synfig format color value

    Returns:
        (int) : Color value between 0-255
    """
    color = color ** (1/settings.GAMMA)
    color *= 255
    color = int(color)
    return max(0, min(color, 255))


def get_color_hex(node):
    """
    Convert the <color></color> from rgba to hex format

    Args:
        node (lxml.etree._Element) : Synfig format color parameter

    Returns:
        (str) : hex format of color
    """
    red, green, blue = 1, 0, 0
    for col in node:
        if col.tag == "r":
            red = float(col.text)
        elif col.tag == "g":
            green = float(col.text)
        elif col.tag == "b":
            blue = float(col.text)
    # Convert to 0-255 range
    red, green, blue = clamp_col(red), clamp_col(green), clamp_col(blue)

    # https://stackoverflow.com/questions/3380726/converting-a-rgb-color-tuple-to-a-six-digit-code-in-python/3380739#3380739
    ret = "#{0:02x}{1:02x}{2:02x}".format(red, green, blue)
    return ret

def get_frame(waypoint):
    """
    Given a waypoint, it parses the time to frames

    Args:
        waypoint (lxml.etree._Element) : Synfig format waypoint

    Returns:
        (int) : the frame at which waypoint is present
    """
    time = get_time(waypoint)
    frame = time * settings.lottie_format["fr"]
    frame = round(frame)
    return frame


def get_time(waypoint):
    """
    Given a waypoint, it parses the string time to float time

    Args:
        waypoint (lxml.etree._Element) : Synfig format waypoint

    Returns:
        (float) : the time in seconds at which the waypoint is present
    """
    return parse_time(waypoint.attrib["time"])


def parse_time(time_in_str):
    """
    Given a string, it parses time to float time

    Args:
        time_in_str (str) : Time in string format

    Returns:
        (float) : the time in seconds at represented by the string
    """
    time = time_in_str.split(" ")
    final = 0
    for frame in time:
        if frame[-1] == "h":
            final += float(frame[:-1]) * 60 * 60
        elif frame[-1] == "m":
            final += float(frame[:-1]) * 60
        elif frame[-1] == "s":
            final += float(frame[:-1])
        elif frame[-1] == "f":  # This should never happen according to my code
            raise ValueError("In waypoint, time is never expected in frames.")
    return final


def get_vector(waypoint):
    """
    Given a waypoint, it parses the string vector into Vector class defined in
    this convertor

    Args:
        waypoint (lxml.etree._Element) : Synfig format waypoint

    Returns:
        (misc.Vector) : x and y axis values stores in Vector format
    """
    # converting radius and angle to a vector
    if waypoint.tag == "radial_composite":
        for child in waypoint:
            if child.tag == "radius":
                radius = float(child[0].attrib["value"])
                radius *= settings.PIX_PER_UNIT
            elif child.tag == "theta":
                angle = float(child[0].attrib["value"])
        x, y = radial_to_tangent(radius, angle)
    else:
        x = float(waypoint[0][0].text)
        y = float(waypoint[0][1].text)
    return Vector(x, y)

def radial_to_tangent(radius, angle):
    """
    Converts a tangent from radius and angle format to x, y axis co-ordinate
    system
    """
    angle = math.radians(angle)
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    return x, y

def set_vector(waypoint, pos):
    """
    Given a waypoint and pos(Vector), it set's the waypoint's vectors

    Args:
        waypoint (lxml.etree._Element) : Synfig format waypoint

    Returns:
        (None)
    """
    waypoint[0][0].text = str(pos.val1)
    waypoint[0][1].text = str(pos.val2)
