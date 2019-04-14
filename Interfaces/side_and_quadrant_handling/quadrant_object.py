import os
from .status_values import StatusValues

class Quadrant(object):
    THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    RELATIVE_FINISHED_PHOTO_DIR = os.path.join(THIS_FILE_PATH, "..", "..", "UI_code", "static", "generalIO",
                                               "output", "finished_photos")
    RELATIVE_FINISHED_REPORT_DIR = os.path.join(THIS_FILE_PATH, "..", "..", "UI_code", "static", "generalIO",
                                                "output", "finished_reports")
    def __init__(self):
        self._quadrant_name = ""
        self._side_name = ""

        self.current_status = StatusValues.NOT_STARTED

        self.cracks_detected = False

        self.num_photos_per_quad = 0

        self.coord_dict = {"left_latitude_DD": 0,
                           "left_longitude_DD": 0,

                           "right_latitude_DD": 0,
                           "right_longitude_DD": 0,

                           "top_altitude_Meters": 0,
                           "bottom_altitude_Meters": 0}

        self.photo_output_dir = os.path.join(self.RELATIVE_FINISHED_PHOTO_DIR, self.side_name, self.quadrant_name)

        self.report_output_dir = os.path.join(self.RELATIVE_FINISHED_REPORT_DIR, self.side_name, self.quadrant_name)

    @property
    def quadrant_name(self):
        return self._quadrant_name

    @quadrant_name.setter
    def quadrant_name(self, new_quadrant_name):
        self._quadrant_name = new_quadrant_name

        self.photo_output_dir = os.path.join(self.RELATIVE_FINISHED_PHOTO_DIR, self.side_name, self._quadrant_name)

        self.report_output_dir = os.path.join(self.RELATIVE_FINISHED_REPORT_DIR, self.side_name, self._quadrant_name)

    @property
    def side_name(self):
        return self._side_name

    @side_name.setter
    def side_name(self, new_side_name):
        self._side_name = new_side_name

        self.photo_output_dir = os.path.join(self.RELATIVE_FINISHED_PHOTO_DIR, self._side_name, self.quadrant_name)

        self.report_output_dir = os.path.join(self.RELATIVE_FINISHED_REPORT_DIR, self._side_name, self.quadrant_name)

    def set_quadrant_detected(self, crack_detected_bool):
        self.cracks_detected = crack_detected_bool

    def parse_js_string(self, js_string, num_photos_per_quad):
        """
        Parses the given refined JS string and sets the parameters of the object.
        :param js_string: (string) -> MUST be in the format:
                           "Quadrant 56" lat_limit_left="1" long_limit_left="1" lat_limit_right="1.07"
                           long_limit_right="1.07" top_limit="5" bottom_limit="1"
       :param num_photos_per_quad: (int) -> The number of photos each quadrants should have before being considered "complete"

        """
        name_string, left_lat_limit_on = js_string.split("lat_limit_left=")
        left_lat_limit, left_long_limit_on = left_lat_limit_on.split("long_limit_left=")
        left_long_limit, right_lat_limit_on = left_long_limit_on.split("lat_limit_right=")
        right_lat_limit, right_long_limit_on = right_lat_limit_on.split("long_limit_right=")
        right_long_limit, top_limit_on = right_long_limit_on.split("top_limit=")
        top_limit, bottom_limit = top_limit_on.split("bottom_limit=")

        self.quadrant_name = name_string.replace('\"', '')
        self.num_photos_per_quad = num_photos_per_quad
        self.coord_dict["left_latitude_DD"] = left_lat_limit.replace('\"', '').replace(' ', '')
        self.coord_dict["left_longitude_DD"] = left_long_limit.replace('\"', '').replace(' ', '')
        self.coord_dict["right_latitude_DD"] = right_lat_limit.replace('\"', '').replace(' ', '')
        self.coord_dict["right_longitude_DD"] = right_long_limit.replace('\"', '').replace(' ', '')
        self.coord_dict["top_altitude_Meters"] = top_limit.replace('\"', '').replace(' ', '')
        self.coord_dict["bottom_altitude_Meters"] = bottom_limit.replace('\"', '').replace(' ', '')

    def parse_config_string(self, config_string):
        """
        Parses the given refined config string and sets the parameters of the object.
        :param js_string: (string) -> MUST be in the format:
                           "Quadrant 56" lat_limit_left="1" long_limit_left="1" lat_limit_right="1.07"
                           long_limit_right="1.07" top_limit="5" bottom_limit="1"
        """
        name_string, detected_on = config_string.split("Cracks Detected: ")
        detected_string, num_photos_on = detected_on.split("Num_Photos: ")
        num_photos, left_limit_on = num_photos_on.split("Left_Limit (DD): ")
        left_limit, right_limit_on = left_limit_on.split("Right_Limit (DD):")
        right_limit, top_limit_on = right_limit_on.split("Top_Limit (m): ")
        top_limit, bottom_limit = top_limit_on.split("Bottom_Limit (m): ")

        self.quadrant_name = name_string.rstrip(' ')
        self.cracks_detected = True if detected_string.rstrip(' ') == "TRUE" else False
        self.num_photos_per_quad = int(num_photos)
        self.coord_dict["left_latitude_DD"] = float(left_limit.replace('(', '').replace(')', '').replace(' ', '').split(",")[0])
        self.coord_dict["left_longitude_DD"] = float(left_limit.replace('(', '').replace(')', '').replace(' ', '').split(",")[1])
        self.coord_dict["right_latitude_DD"] = float(right_limit.replace('(', '').replace(')', '').replace(' ', '').split(",")[0])
        self.coord_dict["right_longitude_DD"] = float(right_limit.replace('(', '').replace(')', '').replace(' ', '').split(",")[1])
        self.coord_dict["top_altitude_Meters"] = float(top_limit.replace(' ', ''))
        self.coord_dict["bottom_altitude_Meters"] = float(bottom_limit.replace(' ', ''))

    def generate_string(self):
        """
        Generates a string that contains the quadrant name, number of photos, left / right lat & long limits
        (in Decimal Degree) and top and bottom altitude limits (in meters)
        :return: (String): Result string.
        """
        detected_string = "TRUE" if self.cracks_detected else "FALSE"
        output_string = "Quadrant Name: {0}\nCracks Detected: {1}\nNum_Photos: {2}\nLeft_Limit (DD): ({3}, {4})\n" \
                        "Right_Limit (DD): ({5}, {6})\nTop_Limit (m): {7}\nBottom_Limit (m): {8}\n" \
                        "\n".format(self.quadrant_name, detected_string, self.num_photos_per_quad,
                                    self.coord_dict["left_latitude_DD"], self.coord_dict["left_longitude_DD"],
                                    self.coord_dict["right_latitude_DD"], self.coord_dict["right_longitude_DD"],
                                    self.coord_dict["top_altitude_Meters"], self.coord_dict["bottom_altitude_Meters"])
        return output_string

    def check_coordinates(self, lat, long, alt):
        """
        Checks to see if a given coordinate string is within the bounds of this quadrant.
        :param lat: The latitude of the coordinate to check in Decimal Degree format.
        :param long: The longitude of the coordinate to check in Decimal Degree format.
        :param alt: The altitude of the coordinate to check in meters.
        :return: (bool) -> True: The coordinate string IS within the bounds of this quadrant
                           False: The coordinate string is NOT within the bounds of this quadrant
        """

        if not self.range_check(self.coord_dict["left_latitude_DD"], self.coord_dict["right_latitude_DD"], lat):
            return False
        if not self.range_check(self.coord_dict["left_longitude_DD"], self.coord_dict["right_longitude_DD"], long):
            return False
        if not self.range_check(self.coord_dict["top_altitude_Meters"], self.coord_dict["bottom_altitude_Meters"], alt):
            return False
        return True

    def create_output_directories(self):
        """
        Creates the output directories needed to store quadrant results in the UI/static/generalIO directory
        """
        if not os.path.exists(self.photo_output_dir):
            os.makedirs(self.photo_output_dir)

        if not os.path.exists(self.report_output_dir):
            os.makedirs(self.report_output_dir)

    def check_and_return_status(self):
        """
        Returns a value corresponding to the status of the quadrant. If no images are in the quadrant report directory,
        the quadrant has not been started. If there are photos in the directory but not enough to match the designated
        end number, it is in progress. If there are sufficient photos to meet the requirement, it has been completed.
        :return: (StatusValue): StatusValue corresponding to the quadrant's state.
        """
        try:
            completed_report_names = os.listdir(self.report_output_dir)
            completed_report_paths = []

            for name in completed_report_names:
                completed_report_paths.append(os.path.join(self.report_output_dir, name))

            contains_crack_string = "FALSE"
            if len(completed_report_paths) == self.num_photos_per_quad:
                for report in completed_report_paths:
                    success_line = ""
                    with open(report, "r") as report_file:
                        throw_away_name_line = report_file.readline()
                        throw_away_coord_line = report_file.readline()
                        success_line = report_file.readline()

                    if "Positive" in success_line:
                        contains_crack_string = "TRUE"
                        break

                return StatusValues.COMPLETE, contains_crack_string
            elif len(completed_report_paths) > 0:
                return StatusValues.IN_PROGRESS, contains_crack_string
            else:
                return StatusValues.NOT_STARTED, contains_crack_string
        except Exception:
            return StatusValues.NOT_STARTED, contains_crack_string

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
