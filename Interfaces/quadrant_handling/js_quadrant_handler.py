import os
import shutil

from .quadrant_object import Quadrant

class JSQuadrantHandler(object):

    THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self.config_file_name = "quadrant_"
        self.config_path = os.path.join(self.THIS_FILE_PATH, "..", "configs", self.config_file_name)


    def run_module(self, raw_js_string):
        self.parse_raw_input(raw_js_string)

    def parse_raw_input(self, raw_js_string):
        # Data comes in in a big string like this:
        # "<div class="grid-item" id="Quadrant 4" data-left="12" data-right="6" data-top="12" data-bottom="6">Quadrant 4</div>
        # <div class="grid-item" id="Quadrant 3" data-left="6" data-right="0" data-top="12" data-bottom="6">Quadrant 3</div>
        # <div class="grid-item" id="Quadrant 2" data-left="12" data-right="6" data-top="6" data-bottom="0">Quadrant 2</div>
        # <div class="grid-item examined-next" id="Quadrant 1" data-left="6" data-right="0" data-top="6" data-bottom="0">Quadrant 1</div>"
        # And it needs to be cut down to workable pieces.

        # Step one, create a list of strings corresponding to each grid. Chuck out the first bit of the list as it'll
        # only have "<div class="grid-item"" or some such.
        # Will look something like this:
        # "Quadrant 4" data-left="12" data-right="6" data-top="12" data-bottom="6">Quadrant 4</div><div class="grid-item"
        raw_quad_list = raw_js_string.split("id=")
        raw_quad_list.pop(0)

        # Cut off any extraneous bits at the end to look like this:
        # "Quadrant 4" data-left="12" data-right="6" data-top="12" data-bottom="6"
        refined_quad_strings = []
        for raw_quad_string in raw_quad_list:
            refined_quad_strings.append(raw_quad_string.split(">Quadrant")[0])

        # Create a list of quadrant objects for easy use.
        quadrant_objects = []
        for refined_quad_string in refined_quad_strings:
            new_quad_object = Quadrant()
            new_quad_object.parse_js_string(refined_quad_string)
            quadrant_objects.append(new_quad_object)


