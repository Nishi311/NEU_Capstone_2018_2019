
class Quadrant(object):
    def __init__(self):
        self.quadrant_name = ""
        self.coord_dict = {"left_latitude": 0,
                           "left_longitude": 0,

                           "right_latitude": 0,
                           "right_longitude": 0,

                           "top_altitude": 0,
                           "bottom_altitude": 0}

    def parse_js_string(self, js_string):
        """
        Parses the given refined JS string and sets the parameters of the object.
        :param js_string: (string) -> MUST be in the format:
                           "Quadrant 4" data-left="12" data-right="6" data-top="12" data-bottom="6"
        """
        name_string, data_left_on = js_string.split("data-left=")
        data_left, data_right_on = data_left_on.split("data-right=")
        data_right, data_top_on = data_right_on.split("data-top=")
        data_top, data_bottom = data_top_on.split("data-bottom=")

        self.quadrant_name = name_string.replace('\"', '')
        data_left = data_left.replace('\"', '')
        data_right = data_right.replace('\"', '')
        data_top = data_top.replace('\"', '')
        data_bottom = data_bottom.replace('\"', '')

        self.coord_dict["left_latitude"] = data_top.replace('\"', '')
        self.coord_dict["left_longitude"] = 0

        self.coord_dict["right_latitude"] = data_bottom.replace('\"', '')
        self.coord_dict["right_longitude"] = 0

        self.coord_dict["top_altitude"] = 0
        self.coord_dict["bottom_altitude"] = 0


    def parse_config_string(self,config_string):
        pass

    def print_string(self):
        pass

    def check_coordinates(self, coordinate_list):
        pass
