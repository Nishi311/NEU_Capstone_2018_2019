import os

from .quadrant_object import Quadrant


class QuadrantHandler(object):

    THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE_NAME = "quadrant_config.txt"
    CONFIG_DIR = os.path.join(THIS_FILE_PATH, "..", "configs")
    CONFIG_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE_NAME)

    def __init__(self):
        self.quadrant_list = []

    def write_quadrants_to_config(self, raw_js_string):
        if not os.path.exists(self.CONFIG_DIR):
            os.makedirs(self.CONFIG_DIR)

        self.quadrant_list = self.parse_raw_js_input(raw_js_string)

        with open(self.CONFIG_PATH, "w") as config_file:
            for quadrant in self.quadrant_list:
                config_file.write(quadrant.generate_string())

    def read_quadrants_from_config(self):
        if not os.path.exists(self.CONFIG_PATH):
            print("quadrant_handler, read_quadrants_from_config(): ERROR. Could not find quadrant config file "
                  "{0}".format(self.CONFIG_PATH))
            return False

        try:
            with open(self.CONFIG_PATH, "r") as config_file:
                raw_config_string = config_file.readlines()
        except IOError as e:
            print("Quadrant_handler, read_quadrants_from_config(): Could not read from config file {0}. Returned "
                  "Error {1}".format(self.CONFIG_PATH, e))
            return False

        return self.parse_raw_config_input(raw_config_string)

    def parse_raw_js_input(self, raw_js_string):
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

    def parse_raw_config_input(self, raw_config_input):

        super_string = ""
        for line in raw_config_input:
            super_string += line.replace('\n', ' ')

        refined_quad_strings = super_string.split("Quadrant Name: ")
        refined_quad_strings.pop(0)
        quadrant_objects = []
        for refined_quad_string in refined_quad_strings:
            new_quad_object = Quadrant()
            new_quad_object.parse_config_string(refined_quad_string)
            quadrant_objects.append(new_quad_object)

        self.quadrant_list = quadrant_objects

    def determine_quadrant_from_coords(self, lat, long, alt):
        unknown_quad_name = "Unknown Quadrant"

        for quadrant in self.quadrant_list:
            if quadrant.check_coordinates(lat, long, alt):
                return quadrant.quadrant_name

        return unknown_quad_name
