"""
Fill this
"""
import sys
sys.path.append("..")
import settings
from properties.value import gen_properties_value
from misc import get_angle, Count, change_axis
from properties.multiDimensionalKeyframed import gen_properties_multi_dimensional_keyframed
from properties.valueKeyframed import gen_value_Keyframed

def gen_shapes_star(lottie, layer, idx):
    """
    Generates the dictionary corresponding to shapes/star.json
    """
    index = Count()
    lottie["ty"] = "sr"     # Type: star
    lottie["pt"] = {}       # Number of points on the star
    lottie["p"] = {}        # Position of star
    lottie["r"] = {}        # Angle / Star's rotation
    lottie["ir"] = {}       # Inner radius
    lottie["or"] = {}       # Outer radius
    lottie["is"] = {}       # Inner roundness of the star
    lottie["os"] = {}       # Outer roundness of the star
    regular_polygon = "false"
    for child in layer:
        if child.tag == "param":
            if child.attrib["name"] == "regular_polygon":
                regular_polygon = child[0].attrib["value"]
            elif child.attrib["name"] == "points":
                if child[0].tag == "animated":

                    # To uniquely identify the points, attribute type is changed
                    child[0].attrib['type'] = 'points'
                    gen_value_Keyframed(lottie["pt"], child[0], index.inc())
                else:
                    gen_properties_value(lottie["pt"],
                                         int(child[0].attrib["value"]),
                                         index.inc(),
                                         settings.DEFAULT_ANIMATED,
                                         settings.NO_INFO)
            elif child.attrib["name"] == "angle":
                if child[0].tag == "animated":
                    gen_value_Keyframed(lottie["r"], child[0], index.inc())
                else:
                    theta = get_angle(float(child[0].attrib["value"]))
                    gen_properties_value(
                        lottie["r"], theta, index.inc(), settings.DEFAULT_ANIMATED,
                        settings.NO_INFO)
            elif child.attrib["name"] == "radius1":
                if child[0].tag == "animated":
                    gen_value_Keyframed(lottie["or"], child[0], index.inc())
                else:
                    r_outer = float(child[0].attrib["value"])
                    gen_properties_value(
                        lottie["or"], int(
                            settings.PIX_PER_UNIT * r_outer), index.inc(),
                        settings.DEFAULT_ANIMATED, settings.NO_INFO)
            elif child.attrib["name"] == "radius2":
                if child[0].tag == "animated":
                    gen_value_Keyframed(lottie["ir"], child[0], index.inc())
                else:
                    r_inner = float(child[0].attrib["value"])
                    gen_properties_value(
                        lottie["ir"], int(
                            settings.PIX_PER_UNIT * r_inner), index.inc(),
                        settings.DEFAULT_ANIMATED, settings.NO_INFO)
            elif child.attrib["name"] == "origin":
                if child[0].tag == "animated":
                    gen_properties_multi_dimensional_keyframed(lottie["p"],
                                                             child[0], index.inc())
                else:
                    x_val = float(child[0][0].text) * settings.PIX_PER_UNIT
                    y_val = float(child[0][0].text) * settings.PIX_PER_UNIT
                    gen_properties_value(lottie["p"], change_axis(x_val, y_val),
                                         index.inc(), settings.DEFAULT_ANIMATED,
                                         settings.NO_INFO)

    if regular_polygon == "false":
        lottie["sy"] = 1    # Star Type

        # inner property is only needed if type is star
        gen_properties_value(lottie["is"], 0, index.inc(),
                settings.DEFAULT_ANIMATED, settings.NO_INFO)
    else:
        lottie["sy"] = 2    # Polygon Type

        # for polygon type, "ir" and "is" must not be present
        del lottie["ir"]

    gen_properties_value(lottie["os"], 0, index.inc(),
            settings.DEFAULT_ANIMATED, settings.NO_INFO)
    lottie["ix"] = idx