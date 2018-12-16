from PIL import Image
import argparse
import os
import shutil

class ImageBreakdown(object):

    # Default width of an image sub-component as measured in pixels
    DEFAULT_WIDTH = 227

    # Default height of an image sub-component as measured in pixels
    DEFAULT_HEIGHT = 227

    def __init__(self):
        # Absolute path to the image that will be broken down
        self._full_image_filepath = ""
        # Image object retrieved from "_image_filepath"
        self._full_image_object = None
        # The extension-less name of the image file
        self._full_image_name = ""
        # The extension that goes with the image name
        self._full_image_extension = ""

        # The number of pixels wide the FULL image is.
        self._full_px_width = 0
        # The number of pixels tall the FULL image is.
        self._full_px_height = 0

        # The number of pixels wide a final image sub-component should be
        self._cropped_px_width = self.DEFAULT_WIDTH
        # The number of pixels tall the cropped image sub-component should be
        self._cropped_px_height = self.DEFAULT_HEIGHT
        # Absolute path to the cropped directory where the broken down images will be kept.
        self._cropped_subcomponent_dir = ""

        # Control flag that will let the breakdown function ignore any left over pixels.
        self._ignore_leftover_pixels = False

    # Begin ALL properties

    # Begin original image properties
    @property
    def full_image_object(self):
        return self._full_image_object

    @full_image_object.setter
    def full_image_object(self, new_full_image_object):
        self._full_image_object = new_full_image_object

    @property
    def full_image_name(self):
        return self._full_image_name

    @full_image_name.setter
    def full_image_name(self, new_full_image_name):
        self._full_image_name = new_full_image_name

    @property
    def full_image_extension(self):
        return self._full_image_extension

    @full_image_extension.setter
    def full_image_extension(self, new_full_image_extension):
        self._full_image_extension = new_full_image_extension

    @property
    def full_px_width(self):
        return self._full_px_width

    @full_px_width.setter
    def full_px_width(self, new_full_px_width):
        if not new_full_px_width <= 0:
            self._full_px_width = new_full_px_width
        else:
            self.exit_with_error_msg("ImageBreakdown, full_px_width setter(): Cannot have pixel width <= 0. Exiting")

    @property
    def full_px_height(self):
        return self._full_px_height

    @full_px_height.setter
    def full_px_height(self, new_full_px_height):
        if not new_full_px_height <= 0:
            self._full_px_height = new_full_px_height
        else:
            self.exit_with_error_msg("ImageBreakdown, full_px_height setter(): Cannot have pixel height <= 0. Exiting")

    @property
    def full_image_filepath(self):
        return self._full_image_filepath

    @full_image_filepath.setter
    def full_image_filepath(self, new_full_image_filepath):
        # If the given file path exists, attempt to open the image at that path. Sets the full width / height values
        # based on the image data. Sets the full image name and extension based on the final entry in the filepath.
        if os.path.exists(new_full_image_filepath):
            self._full_image_filepath = new_full_image_filepath
            try:
                self.full_image_object = Image.open(self.full_image_filepath)

                self.full_px_width, self.full_px_height = self.full_image_object.size

                complete_file_name = os.path.split(self.full_image_filepath)[1]

                self.full_image_name = os.path.splitext(complete_file_name)[0]
                self.full_image_extension = os.path.splitext(complete_file_name)[1]

            except IOError:
                self.exit_with_error_msg("ImageBreakdown, image_filepath setter(): new_full_image_path {0} could not "
                                         "be opened as an image! Exiting".format(new_full_image_filepath))

        else:
            self.exit_with_error_msg("ImageBreakdown, image_filepath setter(): new_full_image_path {0} does not exist! "
                  "Exiting".format(new_full_image_filepath))

    # End original image properties

    # Begin sub-image properties
    @property
    def cropped_px_width(self):
        return self._cropped_px_width

    @cropped_px_width.setter
    def cropped_px_width(self, new_cropped_px_width):
        # Basic sanity check
        if not new_cropped_px_width <= 0:
            if not new_cropped_px_width > self.full_px_width:
                self._cropped_px_width = new_cropped_px_width
            else:
                self.exit_with_error_msg("ImageBreakdown, cropped_px_width setter(): cropped width CANNOT be > original"
                                         "image width. Exiting")
        else:
            self.exit_with_error_msg("ImageBreakdown, cropped_px_width setter(): cropped width CANNOT be <= 0. Exiting")

    @property
    def cropped_px_height(self):
        return self._cropped_px_height

    @cropped_px_height.setter
    def cropped_px_height(self, new_cropped_px_height):
        if not new_cropped_px_height <= 0:
            if not new_cropped_px_height > self.full_px_height:
                self._cropped_px_height = new_cropped_px_height
            else:
                self.exit_with_error_msg("ImageBreakdown, cropped_px_height setter(): cropped width CANNOT be > "
                                         "original image width. Exiting")
        else:
            self.exit_with_error_msg("ImageBreakdown, cropped_px_height setter(): cropped width CANNOT be <= 0. "
                                     "Exiting")

    @property
    def cropped_subcomponent_dir(self):
        return self._cropped_subcomponent_dir

    @cropped_subcomponent_dir.setter
    def cropped_subcomponent_dir(self, new_cropped_subcomponent_dir):
        self._cropped_subcomponent_dir = new_cropped_subcomponent_dir

    # End sub-image properties

    # Begin control properties

    @property
    def ignore_leftover_pixels(self):
        return self._ignore_leftover_pixels

    @ignore_leftover_pixels.setter
    def ignore_leftover_pixels(self, will_ignore_leftover_pixels):
        self._ignore_leftover_pixels = will_ignore_leftover_pixels

    # End control properties

    # End ALL Properties

    # Begin non-static functions

    def run_module(self):
        """
        Small function that controls the overall workflow of the class. Sets and parses the arguments, handles the
        creation of new output directories as necessary, runs the breakdown then, finally, cleans up.
        :return:
        """

        # Set and parse arguments
        args = self.set_args()
        self.parse_args(args)

        # Remove previous version of the output directory, if it exists.
        if os.path.exists(self.cropped_subcomponent_dir):
            shutil.rmtree(self.cropped_subcomponent_dir)
        # Make a new output dir.
        os.makedirs(self.cropped_subcomponent_dir)

        # Run breakdown
        self.image_breakdown()

        self.full_image_object.close()

    def set_args(self):
        """
        Sets the command line arguments necessary to operate the ImageBreakdown class.
        :return the interpreted arguments.
        """
        image_breakdown_parser = argparse.ArgumentParser(description='Breaks down the given image into smaller chunks '
                                                                     'of the given size and stores them in the given '
                                                                     'directory')
        image_breakdown_parser.add_argument('--input_path', type=str, required=True,
                                            help='[REQUIRED] The absolute path to the image that will be broken down. '
                                                 'Or a relative path to the image from where this script is called from')
        image_breakdown_parser.add_argument('--output_dir', type=str, required=True,
                                            help='[REQUIRED] The absolute path to the directory where the smaller '
                                                 'images will be stored. Or a relative path from where this script is '
                                                 'called from. If the directory already exists, it will be overwritten. '
                                                 'If it does not exist, it will be made.')
        image_breakdown_parser.add_argument('--sub_image_width', type=int, help='How many pixels wide each sub-image '
                                                                                'should be. Defaults to 227px')

        image_breakdown_parser.add_argument('--sub_image_height', type=int,  help='How many pixels tall each sub-image '
                                                                                  'should be. Defaults to 227px')
        image_breakdown_parser.add_argument('--ignore_leftover_pixels', action='store_true',
                                            help='If the image width or height is not cleanly divisible by the '
                                                 'given sub-image width / height values, there will be leftover '
                                                 'pixels. This flag will prevent those leftovers from being made '
                                                 'into their own non-regulation-sized sub-images.')
        return image_breakdown_parser.parse_args()

    def parse_args(self, args):
        """
        Parses the given arguments and sets class parameters accordingly
        :param args: the args to parse.
        """

        if args:
            if args.input_path:
                self.full_image_filepath = args.input_path
            if args.output_dir:
                self.cropped_subcomponent_dir = args.output_dir
            if args.sub_image_width:
                self.cropped_px_width = args.sub_image_width
            if args.sub_image_height:
                self.cropped_px_height = args.sub_image_height
            if args.ignore_leftover_pixels:
                self.ignore_leftover_pixels = True
        else:
            self.exit_with_error_msg("No arguments given!")

    def image_breakdown(self):
        """
        The function that does the actual breaking down of the image. Terminology used in function:

        row: one strip of the image that is cropped_px_height tall and extends horizontally across the full image.
        column: one strip of the image that is cropped_px_width wide and extends vertically down the full image.

        This function goes row by row and column by column to save sub-images of size cropped_px_width x cropped_px_height.
        If either cropped_px_width or cropped_px_height do not divide cleanly into the full image dimensions, it will
        still save those oddly-sized sub-images unless explicitly told not to by the ImageBreakdown parameter
        'ignore_leftover_pixels'.
        """

        if not self.ignore_leftover_pixels:
            leftover_width_pixels = int(self.full_px_width % self.cropped_px_width)
            leftover_height_pixels = int(self.full_px_height % self.cropped_px_height)
        else:
            leftover_width_pixels = 0
            leftover_height_pixels = 0

        num_full_width_crops = int(self.full_px_width / self.cropped_px_width)
        num_full_height_crops = int(self.full_px_height / self.cropped_px_height)

        # this tuple represents the boundaries of the cropped image in this order:
        #
        # {width start px, height start px, width end px, height end px}
        #
        # (width start px, height start px) ._______
        #             ^    |                |cropped|
        #     height- |    V height+        |area   |
        #                                   |_______|.(width start px + (width), height start px + (height))
        #                                     -> width+
        #                                     <- width-
        current_crop_area = (0, 0, self.cropped_px_width, self.cropped_px_height)

        # Go top to bottom by rows to crop image
        for row_count in range(num_full_height_crops):
            # On each row, go column by column cropping full-sized sub-images
            for col_count in range(num_full_width_crops):
                self.save_crop_area(current_crop_area, row_count, col_count)
                # Only update crop area is next column is guaranteed to be full width.
                if col_count+1 != num_full_width_crops:
                    current_crop_area = self.get_new_horizontal_crop_area(current_crop_area, self.cropped_px_width)

            # If the row has leftover pixels after cropping the full-sized columns, make a smaller sub-image.
            if leftover_width_pixels:
                current_crop_area = self.get_new_horizontal_crop_area(current_crop_area, leftover_width_pixels)
                self.save_crop_area(current_crop_area, row_count, num_full_width_crops)

            # Only update crop area if the next row is guaranteed to be full height.
            if row_count+1 != num_full_height_crops:
                # Reset cropped area to first column, one row down.
                current_crop_area = self.get_new_vertical_crop_area(current_crop_area, self.cropped_px_width,
                                                                    self.cropped_px_height)

        # If the columns all still have a bit of left over, do one more pass to make smaller sub-images out of that.
        if leftover_height_pixels:
            current_crop_area = self.get_new_vertical_crop_area(current_crop_area, self.cropped_px_width,
                                                                leftover_height_pixels)
            for col_count in range(num_full_width_crops):
                self.save_crop_area(current_crop_area, num_full_height_crops, col_count)
                current_crop_area = self.get_new_horizontal_crop_area(current_crop_area, self.cropped_px_width)

        # If there is both leftover width AND height, we will have missed one little sub-image at the very bottom
        # right-hand corner. Pick that up.
        if leftover_width_pixels and leftover_height_pixels:
            top_left = (self.full_px_width-leftover_width_pixels, self.full_px_height-leftover_height_pixels)
            bottom_right = (self.full_px_width, self.full_px_height)
            current_crop_area = top_left[0], top_left[1], bottom_right[0], bottom_right[1]

            self.save_crop_area(current_crop_area, num_full_height_crops, num_full_width_crops)

    def save_crop_area(self, crop_area, col_num, row_num):
        """
        Crops the full-sized image stored by the ImageBreakdown class and saves it as a new image with a row (r)
        and column (c) sub-tag on the image name for easy recognition. Results saved to cropped_subcomponent_dir
        outlined by ImageBreakdown class.
        :param crop_area: (tuple) the area of the full image to crop.
        :param col_num: The column number of the cropped image (e.g: 3rd sub-image on height row 1)
        :param row_num: The row number of the cropped image (e.g: currently cropping images from row 0, px 0-227)
        """
        cropped_image_name = "{0}_r{1}_c{2}{3}".format(self.full_image_name, col_num, row_num,
                                                       self.full_image_extension)
        cropped_image_path = os.path.join(self.cropped_subcomponent_dir, cropped_image_name)

        cropped_image = self.full_image_object.crop(crop_area)
        cropped_image.save(cropped_image_path)

    # End non-static functions

    # Begin static functions
    @staticmethod
    def get_new_horizontal_crop_area(current_crop_area, px_width_of_new_area):
        """
        Moves the cropped area one length over.
        :param current_crop_area: (tuple) The cropped area to adjust.
        :param px_width_of_new_area: (int) The width to adjust the cropped area by.
        :return: (tuple) cropped area adjusted by one width.
        """
        new_top_left = (current_crop_area[2], current_crop_area[1])
        new_bottom_right = (current_crop_area[2] + px_width_of_new_area, current_crop_area[3])

        return new_top_left[0], new_top_left[1], new_bottom_right[0], new_bottom_right[1]

    @staticmethod
    def get_new_vertical_crop_area(current_crop_area, px_width_of_new_area, px_height_of_new_area):
        """
        Drops the crop area down a row. Resets column to origin position and brings the row down one notch
        from its current position.
        :param current_crop_area: (tuple) The current crop area to be dropped a row.
        :param px_width_of_new_area: (int) The width of one cropped area
        :param px_height_of_new_area: (int) The height of one cropped area
        :return: (tuple) cropped area that has been reset to column origin and dropped one row.
        """
        new_top_left = (0, current_crop_area[3])
        new_bottom_right = (px_width_of_new_area, current_crop_area[3] + px_height_of_new_area)

        return new_top_left[0], new_top_left[1], new_bottom_right[0], new_bottom_right[1]

    @staticmethod
    def exit_with_error_msg(error_message):
        """
        exit the program with code 1 (failure) and print out the given message.
        :param error_message: The error message to print out
        """
        print(error_message)
        exit(1)

    # End static functions

if __name__ == '__main__':
    image_breakdown = ImageBreakdown()
    image_breakdown.run_module()
