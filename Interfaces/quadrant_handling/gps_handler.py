import exifread

# NOTE: NOT MINE. Based HEAVILY on:  https://gist.github.com/snakeye/fdc372dbf11370fe29eb

class GPSHandler(object):

    def run_module(self, file_path):
        lat, long, altitude = self.get_exif_location(self.get_exif_data(file_path))

        return lat, long, altitude

    @staticmethod
    def get_exif_data(image_file):
        with open(image_file, 'rb') as f:
            exif_tags = exifread.process_file(f)
        return exif_tags

    @staticmethod
    def _get_if_exist(data, key):
        if key in data:
            return data[key]

        return None

    @staticmethod
    def _convert_to_degress(value):
        """
        Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
        :param value:
        :type value: exifread.utils.Ratio
        :rtype: float
        """
        d = float(value.values[0].num) / float(value.values[0].den)
        m = float(value.values[1].num) / float(value.values[1].den)
        s = float(value.values[2].num) / float(value.values[2].den)

        return d + (m / 60.0) + (s / 3600.0)

    def get_exif_location(self, exif_data):
        """
        Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)
        """
        lat = None
        lon = None
        altitude = None

        gps_latitude = self._get_if_exist(exif_data, 'GPS GPSLatitude')
        gps_latitude_ref = self._get_if_exist(exif_data, 'GPS GPSLatitudeRef')

        gps_longitude = self._get_if_exist(exif_data, 'GPS GPSLongitude')
        gps_longitude_ref = self._get_if_exist(exif_data, 'GPS GPSLongitudeRef')

        gps_altitude_ref = self._get_if_exist(exif_data, 'GPS GPSAltitudeRef')
        gps_altitude = self._get_if_exist(exif_data, 'GPS GPSAltitude')

        if gps_latitude and gps_latitude_ref:
            lat = self._convert_to_degress(gps_latitude)
            if gps_latitude_ref.values[0] != 'N':
                lat = 0 - lat

        if gps_longitude and gps_longitude_ref:
            lon = self._convert_to_degress(gps_longitude)
            if gps_longitude_ref.values[0] != 'E':
                lon = 0 - lon

        if gps_altitude and gps_altitude_ref:
            alt = gps_altitude.values[0]
            altitude = alt.num / alt.den
            if gps_altitude_ref.values[0] == 1: altitude *= -1

        return lat, lon, altitude


if __name__ == "__main__":
    gps_helper = GPSHelper()
    lat, long, altitude = gps_helper.run_module("A:\Capstone\Photos\drone_test_photos\\fake_wall_tests\\no_right_close_1.jpg")
    test = "helloWorld"
