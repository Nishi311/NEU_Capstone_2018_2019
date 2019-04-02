
class Quadrant(object):
    def __init__(self):
        self.quadrant_name = ""
        self.coord_dict = {"left_latitude_DD": 0,
                           "left_longitude_DD": 0,

                           "right_latitude_DD": 0,
                           "right_longitude_DD": 0,

                           "top_altitude_Meters": 0,
                           "bottom_altitude_Meters": 0}

    def parse_js_string(self, js_string):
        """
        Parses the given refined JS string and sets the parameters of the object.
        :param js_string: (string) -> MUST be in the format:
                           "Quadrant 56" lat_limit_left="1" long_limit_left="1" lat_limit_right="1.07"
                           long_limit_right="1.07" top_limit="5" bottom_limit="1"
        """
        name_string, left_lat_limit_on = js_string.split("lat_limit_left=")
        left_lat_limit, left_long_limit_on = left_lat_limit_on.split("long_limit_left=")
        left_long_limit, right_lat_limit_on = left_long_limit_on.split("lat_limit_right=")
        right_lat_limit, right_long_limit_on = right_lat_limit_on.split("long_limit_right=")
        right_long_limit, top_limit_on = right_long_limit_on.split("top_limit=")
        top_limit, bottom_limit = top_limit_on.split("bottom_limit=")

        self.quadrant_name = name_string.replace('\"', '')
        self.coord_dict["left_latitude_DD"] = left_lat_limit.replace('\"', '').replace(' ', '')
        self.coord_dict["left_longitude_DD"] = left_long_limit.replace('\"', '').replace(' ', '')
        self.coord_dict["right_latitude_DD"] = right_lat_limit.replace('\"', '').replace(' ', '')
        self.coord_dict["right_longitude_DD"] = right_long_limit.replace('\"', '').replace(' ', '')
        self.coord_dict["top_altitude_Meters"] = top_limit.replace('\"', '').replace(' ', '')
        self.coord_dict["bottom_altitude_Meters"] = bottom_limit.replace('\"', '').replace(' ', '')

    def parse_config_string(self, config_string):
        name_string, left_limit_on = config_string.split("Left_Limit (DD): ")
        left_limit, right_limit_on = left_limit_on.split("Right_Limit (DD):")
        right_limit, top_limit_on = right_limit_on.split("Top_Limit (m): ")
        top_limit, bottom_limit = top_limit_on.split("Bottom_Limit (m): ")

        self.quadrant_name = name_string.replace(' ', '')

        self.coord_dict["left_latitude_DD"] = left_limit.replace('(', '').replace(')', '').replace(' ', '').split(",")[0]
        self.coord_dict["left_longitude_DD"] = left_limit.replace('(', '').replace(')', '').replace(' ', '').split(",")[1]
        self.coord_dict["right_latitude_DD"] = right_limit.replace('(', '').replace(')', '').replace(' ', '').split(",")[0]
        self.coord_dict["right_longitude_DD"] = right_limit.replace('(', '').replace(')', '').replace(' ', '').split(",")[1]
        self.coord_dict["top_altitude_Meters"] = top_limit.replace(' ', '')
        self.coord_dict["bottom_altitude_Meters"] = bottom_limit.replace(' ', '')

    def generate_string(self):
        output_string = "Quadrant Name: {0}\nLeft_Limit (DD): ({1}, {2})\nRight_Limit (DD): ({3}, {4})\nTop_Limit (m): " \
                        "{5}\nBottom_Limit (m): {6}\n\n".format(self.quadrant_name,
                                                                self.coord_dict["left_latitude_DD"],
                                                                self.coord_dict["left_longitude_DD"],
                                                                self.coord_dict["right_latitude_DD"],
                                                                self.coord_dict["right_longitude_DD"],
                                                                self.coord_dict["top_altitude_Meters"],
                                                                self.coord_dict["bottom_altitude_Meters"])
        return output_string

    def check_coordinates(self, coordinate_list):
        """
        Checks to see if a given coordinate string is within the bounds of this quadrant.
        :param coordinate_list: (list) -> MUST be in the format [[latitude (DD)], [longitude (DD)], [altitude (m)]]
        :return: (bool) -> True: The coordinate string IS within the bounds of this quadrant
                           False: The coordinate string is NOT within the bounds of this quadrant
        """
        if isinstance(coordinate_list, list):
            if len(coordinate_list) == 3:
                given_lat_coord_dd = coordinate_list[0]
                given_long_coord_dd = coordinate_list[1]
                given_alt_meters = coordinate_list[2]

                if not self.range_check(self.coord_dict["left_latitude_DD"], self.coord_dict["left_longitude_DD"],
                                        given_lat_coord_dd):
                    return False
                if not self.range_check(self.coord_dict["right_latitude_DD"], self.coord_dict["right_longitude_DD"],
                                        given_long_coord_dd):
                    return False
                if not self.range_check(self.coord_dict["top_altitude_Meters"], self.coord_dict["bottom_altitude_Meters"],
                                        given_alt_meters):
                    return True
                return True

    @staticmethod
    def range_check(left_coord, right_coord, checking_coord):
        """
        real quick function to check range. Because left and right sides of the quad might be swapped due to perspective,
        need to check ranges from both sides for a value in between.
        :param left_coord: left hand side of the range.
        :param right_coord: right hand side of the range.
        :param checking_coord: Value to check against
        :return: (bool) -> True: checking_coord in within the range of left and right.
                           False: checking_coord is NOT within the range of left and right.
        """
        if (left_coord < checking_coord < right_coord) or (left_coord > checking_coord > right_coord):
            return True
        else:
            return False
