import os

from .quadrant_object import Quadrant


class SideObject(object):

    THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    CONFIG_FILE_NAME = "quadrant_config.txt"

    def __init__(self, side_name=None):
        if side_name:
            self.side_name = side_name
        else:
            self.side_name = None

        self.num_columns = 0
        self.num_rows = 0

        self.side_dir = os.path.join(self.THIS_FILE_PATH, "..", "configs", "side_configs", side_name)
        self.side_config_path = os.path.join(self.side_dir, self.CONFIG_FILE_NAME)
        self.quadrant_list = []

    def write_quadrants_to_config(self, raw_js_string, num_photos_per_quad, num_rows, num_columns):
        """
        Takes a raw JS string and writes the values to a configuration file in the Interfaces/config directory
        :param raw_js_string: (string) -> Raw Javascript string from the UI
        :param num_photos_per_quad: (int) -> The number of photos each quadrants should have before being considered "complete"
        :param num_rows: (int) -> The number of rows the side should be split into (one quadrant = one cell)
        :param num_columns: (int) -> The number of the side should be split into (one quadrant = one cell)
        """
        if not os.path.exists(self.side_dir):
            os.makedirs(self.side_dir)

        self.num_rows = num_rows
        self.num_columns = num_columns

        self.parse_raw_js_input(raw_js_string, num_photos_per_quad)

        with open(self.side_config_path, "w") as config_file:
            config_file.write("Rows: {0}\nColumns: {1}\n\n".format(num_rows, num_columns))
            for quadrant in self.quadrant_list:
                config_file.write(quadrant.generate_string())

    def read_quadrants_from_config(self):
        """
        Reads a config file from the pre-determined config location for the side and creates the directories necessary
        for outputting results in the UI/static/generalIO directory if they do not already exist.
        """
        if not os.path.exists(self.side_config_path):
            print("quadrant_handler, read_quadrants_from_config(): ERROR. Could not find quadrant config file "
                  "{0}".format(self.side_config_path))
            return False

        try:
            with open(self.side_config_path, "r") as config_file:
                raw_config_string = config_file.readlines()
        except IOError as e:
            print("Quadrant_handler, read_quadrants_from_config(): Could not read from config file {0}. Returned "
                  "Error {1}".format(self.side_config_path, e))
            return False

        self.parse_raw_config_input(raw_config_string)

    def parse_raw_js_input(self, raw_js_string, num_photos_per_quad):
        """
        Parsing helper function that generates the internal list of quadrants based on the raw Javascript string.
        :param raw_js_string: (string) -> The raw Javascript string to parse.
        :param num_photos_per_quad: (int) -> The number of photos each quadrants should have before being considered "complete"
        """

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
            new_quad_object.side_name = self.side_name
            new_quad_object.parse_js_string(refined_quad_string, num_photos_per_quad)
            quadrant_objects.append(new_quad_object)

        self.quadrant_list = quadrant_objects

    def parse_raw_config_input(self, raw_config_input):
        """
        Parsing helper function that generates the internal list of quadrants based on the raw config string.
        :param raw_config_input: (string) -> The raw config string to parse.
        """

        row_line = raw_config_input.pop(0)
        column_line = raw_config_input.pop(0)

        num_rows = int(row_line.split("Rows: ")[1].rstrip("\n"))
        num_columns = int(column_line.split("Columns: ")[1].rstrip("\n"))

        self.num_rows = num_rows
        self.num_columns = num_columns

        super_string = ""
        for line in raw_config_input:
            super_string += line.replace('\n', ' ')

        refined_quad_strings = super_string.split("Quadrant Name: ")
        refined_quad_strings.pop(0)
        quadrant_objects = []
        for refined_quad_string in refined_quad_strings:
            new_quad_object = Quadrant()
            new_quad_object.parse_config_string(refined_quad_string)
            new_quad_object.side_name = self.side_name

            quadrant_objects.append(new_quad_object)

        self.quadrant_list = quadrant_objects

    def determine_quadrant_from_coords(self, lat, long, alt):
        """
        Based on the latitude, longitude (both Decminal Degree) and altitude (Meters) given, determines what quadrant
        on this side (if any) the coordinates belong to.
        :param lat: Latitude to check (Decimal Degree)
        :param long: Longitude to check (Decimal Degree)
        :param alt: Altitude to check (Meters)
        :return: (String) -> The name of the quadrant (if found). Otherwise returns False.
        """
        for quadrant in self.quadrant_list:
            if isinstance(quadrant, Quadrant):
                if quadrant.check_coordinates(lat, long, alt):
                    return quadrant.quadrant_name

        return False

    def create_side_dirs(self):
        """
        Creates all the output directories necessary for the side.
        """
        for quadrant in self.quadrant_list:
            if isinstance(quadrant, Quadrant):
                quadrant.create_output_directories()

    def check_and_return_all_quadrant_statuses_string(self):
        """
        Queries all child quadrants for their status and returns it as a string.
        :return: (string) -> A string of the quadrant statuses, in format "[quadrant name]: [quadrant status], ..."
        """
        quadrant_status_string = ""

        for quadrant in self.quadrant_list:
            quadrant_status = quadrant.check_and_return_status()
            quadrant_status_string += "?{0},{1},{2},{3},{4},{5},{6},{7}" .format(quadrant.quadrant_name, quadrant_status,
                                                                                 quadrant.coord_dict["left_latitude_DD"],
                                                                                 quadrant.coord_dict["left_longitude_DD"],
                                                                                 quadrant.coord_dict["right_latitude_DD"],
                                                                                 quadrant.coord_dict["right_longitude_DD"],
                                                                                 quadrant.coord_dict["top_altitude_Meters"],
                                                                                 quadrant.coord_dict["bottom_altitude_Meters"])

        return quadrant_status_string