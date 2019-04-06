import os
from .side_object import SideObject


class SideHandler(object):

    THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    CONFIGS_DIR = os.path.join(THIS_FILE_PATH, "..", "configs")

    def __init__(self):
        self.side_list = []

    def read_sides_from_configs(self):
        list_of_dirs = []
        if os.path.exists(self.CONFIGS_DIR):

            for root, dirs, files in os.walk(self.CONFIGS_DIR):
                list_of_dirs = dirs
                break

            for dir_name in list_of_dirs:
                side_object = SideObject(dir_name)
                side_object.read_quadrants_from_config()
                self.side_list.append(side_object)

    def determine_side_and_quadrant(self, photo_lat, photo_long, photo_alt):

        for side in self.side_list:
            if isinstance(side, SideObject):
                potential_side = side.side_name
                potential_quadrant = side.determine_quadrant_from_coords(photo_lat, photo_long, photo_alt)
                if potential_quadrant:
                    return os.path.join(potential_side, potential_quadrant)

        return os.path.join("Unknown Side", "Unknown Quadrant")

    def create_all_side_dirs(self):
        for side in self.side_list:
            if isinstance(side, SideObject):
                side.create_side_dirs()
