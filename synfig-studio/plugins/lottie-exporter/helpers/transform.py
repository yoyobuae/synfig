"""
Fill this
"""
import sys
sys.path.append("../")
import settings
from misc import Count, change_axis
from properties.value import gen_properties_value

def gen_helpers_transform(lottie, layer):
    """
    Generates the dictionary corresponding to helpers/transform.json
    """
    index = Count()
    lottie["o"] = {}    # opacity/Amount
    lottie["r"] = {}    # Rotation of the layer
    lottie["p"] = {}    # Position of the layer
    lottie["a"] = {}    # Anchor point of the layer
    lottie["s"] = {}    # Scale of the layer

    # setting the default location
    gen_properties_value(lottie["p"], [0, 0], index.inc(), settings.DEFAULT_ANIMATED, settings.NO_INFO)

    # setting the default opacity i.e. 100
    gen_properties_value(lottie["o"], settings.DEFAULT_OPACITY, index.inc(),
            settings.DEFAULT_ANIMATED, settings.NO_INFO)

    gen_properties_value(
        lottie["r"],
        settings.DEFAULT_ROTATION,
        index.inc(),
        settings.DEFAULT_ANIMATED,
        settings.NO_INFO)
    gen_properties_value(
        lottie["a"], [
            0, 0, 0], index.inc(), settings.DEFAULT_ANIMATED, settings.NO_INFO)
    gen_properties_value(
        lottie["s"], [
            100, 100, 100], index.inc(), settings.DEFAULT_ANIMATED, settings.NO_INFO)
