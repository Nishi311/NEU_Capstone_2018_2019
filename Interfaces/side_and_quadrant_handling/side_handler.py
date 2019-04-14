import os

from .side_object import SideObject
from .quadrant_object import Quadrant

class SideHandler(object):

    THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    SIDE_CONFIGS_DIR = os.path.join(THIS_FILE_PATH, "..", "configs", "side_configs")

    def __init__(self):
        self.side_dict = {}

    @property
    def num_sides(self):
        return len(self.side_dict)

    def read_sides_from_configs(self):
        list_of_dirs = []
        if os.path.exists(self.SIDE_CONFIGS_DIR):

            for root, dirs, files in os.walk(self.SIDE_CONFIGS_DIR):
                list_of_dirs = dirs
                break

            for dir_name in list_of_dirs:
                side_object = SideObject(dir_name)
                side_object.read_quadrants_from_config()
                self.side_dict[side_object.side_name] = side_object

            self.create_all_side_dirs()

    def determine_side_and_quadrant(self, photo_lat, photo_long, photo_alt):

        for side_name, side_object in self.side_dict.items():
            if isinstance(side_object, SideObject):
                potential_side = side_object.side_name
                potential_quadrant = side_object.determine_quadrant_from_coords(photo_lat, photo_long, photo_alt)
                if potential_quadrant:
                    return [potential_side, potential_quadrant]

        return ["Unknown Side", "Unknown Quadrant"]

    def get_side_object(self, side_name):
        return self.side_dict[side_name]

    def update_quadrant_results(self, side_name, quad_name, crack_detected):

        if side_name != "Unknown Side":
            if not self.side_dict[side_name].quadrant_dict[quad_name].cracks_detected:
                self.side_dict[side_name].quadrant_dict[quad_name].cracks_detected = crack_detected
                self.side_dict[side_name].write_quadrants_to_config_from_internal()
        else:
            pass

    def check_for_new_sides(self):
        try:
            found_num_sides = 0
            for root, dirs, file in os.walk(self.SIDE_CONFIGS_DIR):
                found_num_sides = len(dirs)
                break
            if self.num_sides != found_num_sides:
                self.side_dict = {}
                self.read_sides_from_configs()
                self.create_all_side_dirs()
        except OSError:
            pass

    def create_all_side_dirs(self):
        for side_name, side_object in self.side_dict.items():
            if isinstance(side_object, SideObject):
                side_object.create_side_dirs()
