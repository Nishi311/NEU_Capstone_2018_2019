import os

from .quadrant_object import Quadrant


class JSQuadrantHandler(object):

    THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self.config_file_name = "quadrant_"
        self.config_path = os.path.join(self.THIS_FILE_PATH, "..", "configs", self.config_file_name)
        self.quadrant_list = []

    def run_module(self, raw_js_string):
        self.quadrant_list = self.parse_raw_input(raw_js_string)

    def parse_raw_input(self, raw_js_string):
        # Data comes in in a big string like this:
        #
        # <div class="grid-item examined-next" id="Quadrant 6" lat_limit_left="1" long_limit_left="1" lat_limit_right="1.665361236570813" long_limit_right="1.665361236570813" top_limit="2" bottom_limit="1"></div>
        # <div class="grid-item examined-next" id="Quadrant 5" lat_limit_left="1.665361236570813" long_limit_left="1.665361236570813" lat_limit_right="2.330722473141626" long_limit_right="2.330722473141626" top_limit="2" bottom_limit="1"></div>
        # <div class="grid-item examined-next" id="Quadrant 4" lat_limit_left="2.330722473141626" long_limit_left="2.330722473141626" lat_limit_right="2.996083709712439" long_limit_right="2.996083709712439" top_limit="2" bottom_limit="1"></div>
        # <div class="grid-item examined-next" id="Quadrant 3" lat_limit_left="2.996083709712439" long_limit_left="2.996083709712439" lat_limit_right="3.661444946283252" long_limit_right="3.661444946283252" top_limit="2" bottom_limit="1"></div>
        # <div class="grid-item examined-next" id="Quadrant 2" lat_limit_left="3.661444946283252" long_limit_left="3.661444946283252" lat_limit_right="4.326806182854066" long_limit_right="4.326806182854066" top_limit="2" bottom_limit="1"></div>
        # <div class="grid-item examined-next" id="Quadrant 1" lat_limit_left="4.326806182854066" long_limit_left="4.326806182854066" lat_limit_right="4.992167419424879" long_limit_right="4.992167419424879" top_limit="2" bottom_limit="1"></div>"
        # And it needs to be cut down to workable pieces.

        # Step one, create a list of strings corresponding to each grid. Chuck out the first bit of the list as it'll
        # only have "<div class="grid-item"" or some such.
        # Will look something like this:
        # "'"Quadrant 6" lat_limit_left="1" long_limit_left="1" lat_limit_right="1.665361236570813" long_limit_right="1.665361236570813" top_limit="2" bottom_limit="1"></div><div class="grid-item examined-next"
        raw_quad_list = raw_js_string.split("id=")
        raw_quad_list.pop(0)

        # Cut off any extraneous bits at the end to look like this:
        # '"Quadrant 4" lat_limit_left="2.330722473141626" long_limit_left="2.330722473141626" lat_limit_right="2.996083709712439" long_limit_right="2.996083709712439" top_limit="2" bottom_limit="1"></div><div class="grid-item examined-next" '
        refined_quad_strings = []
        for raw_quad_string in raw_quad_list:
            refined_quad_strings.append(raw_quad_string.split("></div>")[0])

        # Create a list of quadrant objects for easy use.
        quadrant_objects = []
        for refined_quad_string in refined_quad_strings:
            new_quad_object = Quadrant()
            new_quad_object.parse_js_string(refined_quad_string)
            quadrant_objects.append(new_quad_object)

        return quadrant_objects

    def write_quadrants_to_config(self):
        with open(self.config_path, "w") as config_file:
            for quadrant in self.quadrant_list:
                config_file.print(quadrant.generate_string())


