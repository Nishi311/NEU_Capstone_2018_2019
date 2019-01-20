import os
import argparse
import glob
import shutil

from types import SimpleNamespace

from image_breakdown import ImageBreakdownModule
from recognition_script import RecognitionModule


class UnifiedRecognitionModule(object):
    # Default width of an image sub-component as measured in pixels
    DEFAULT_WIDTH = 227

    # Default height of an image sub-component as measured in pixels
    DEFAULT_HEIGHT = 227

    # Default graph that will be used to detect cracks.
    DEFAULT_GRAPH_FILEPATH = os.path.join("..", "retrained_model", "crack_detection_graph.pb")

    # Default label set that will be used to label detection results.
    DEFAULT_LABEL_FILEPATH = os.path.join("..", "retrained_model", "crack_detection_labels.txt")

    # location of the output directory relative to this script
    OUTPUT_PATH = os.path.join("..", "output")

    # Default output location for the final recognition report.
    DEFAULT_FINAL_REPORT_FILEPATH = os.path.join(OUTPUT_PATH, "recognition_report.txt")

    # Default short path for intermediary reports
    DEFAULT_INTER_REPORT_FILEPATH = os.path.join(OUTPUT_PATH, "individual_reports")

    # Default parameter for recognition input mean (dunno exactly what that is)
    DEFAULT_INPUT_MEAN = 0

    # Default parameter for recognition input standard of deviation (dunno exactly what that is)
    DEFAULT_INPUT_STD = 255

    def __init__(self):
        # Very important control variable governing whether or an entire directory or a single file is being analysed.
        self.is_input_dir = True

        # Variables related to image breakdown
        self.input_filepath = ""
        self.cropped_subcomponent_dir_filepath = ""
        self.cropped_px_width = self.DEFAULT_WIDTH
        self.cropped_px_height = self.DEFAULT_HEIGHT
        self.ignore_leftover_pixels = True
        # self.skip_breakdown = False

        # Variables related to image recognition
        self.graph_filepath = self.DEFAULT_GRAPH_FILEPATH
        self.graph_labels_filepath = self.DEFAULT_LABEL_FILEPATH
        self.cropped_image_filepath = ""
        self.report_path = ""

        # self-contained modules for use in breaking down then recognizing images.
        self.image_breakdown_module = ImageBreakdownModule()
        self.recognition_module = RecognitionModule()

    def run_module(self):
        """
        Primary function that runs everything. Sets up directories, calls for image breakdown
        and recognition.
        """
        args = self.set_args()
        self.parse_args(args)

        # Remove previous output (if it exists)
        if os.listdir(self.OUTPUT_PATH):
            self.wipe_directory(self.OUTPUT_PATH)

        if not os.path.exists(self.DEFAULT_INTER_REPORT_FILEPATH):
            os.mkdir(self.DEFAULT_INTER_REPORT_FILEPATH)

        # Recognition module will only use one graph throughout its lifecycle.
        # set those parameters here. Will update individual files as needed.
        recognition_args = self.setup_recognition_arguments()
        self.recognition_module.setup_module(recognition_args)

        if self.is_input_dir:
            input_photos = glob.glob(self.input_filepath)
            # Go over all photos that must be checked
            for photo_path in input_photos:
                # Breakdown module needs to be run for every photo with different parameters.
                # Update args with every photo.
                breakdown_args = self.setup_image_breakdown_arguments(photo_path)
                self.image_breakdown_module.setup_module(breakdown_args)

                # Break down the image into sub-images for recognition
                self.image_breakdown_module.run_module()

                # Get a list of the sub-images.
                broken_down_images = glob.glob(os.path.join(self.cropped_subcomponent_dir_filepath, "*"))

                # Set up the report output directory for this photo.
                individual_photo_report_filepath = os.path.join(self.DEFAULT_INTER_REPORT_FILEPATH,
                                                                os.path.split(photo_path)[1].split(".")[0])
                if os.path.exists(individual_photo_report_filepath):
                    self.wipe_directory(individual_photo_report_filepath)
                else:
                    os.mkdir(individual_photo_report_filepath)
                self.recognition_module.report_location = individual_photo_report_filepath

                # run recognition on all sub-images
                for sub_photo_path in broken_down_images:
                    self.recognition_module.input_filepath = sub_photo_path
                    self.recognition_module.run_module()
                # parse the resulting sub-reports into one single report for the image.
                self.sub_report_parser(individual_photo_report_filepath)
                # wipe the sub-image directory to make room for the next set.
                self.wipe_directory(self.cropped_subcomponent_dir_filepath)

    def set_args(self):
        """
        Sets the command line arguments necessary to operate the ImageBreakdown class.
        :return the interpreted arguments.
        """
        #TODO : Clean up options. Need to be clear delineations between functions.
        connection_parser = argparse.ArgumentParser(description='Breaks down the given image into smaller chunks '
                                                                     'of the given size and stores them in the given '
                                                                     'directory')
        connection_parser.add_argument('-i', '--inputPath', type=str, required=True,
                                       help='[REQUIRED] The absolute path to the dir/image that will be broken down. '
                                            'Or a relative path to the dir/image from where this script is called from. '
                                            'IF PAIRED WITH THE -f FLAG, WILL ASSUME THE PATH IS A SINGLE FILE AND WILL '
                                            'ATTEMPT TO WORK ON THAT SOLE IMAGE.')
        connection_parser.add_argument('-f', '--singleFileRecognition', action="store_true",
                                       help="If this flag is set, then the --inputPath given is assumed to be a "
                                            "single image and will attempt to analyse only that image.")
        connection_parser.add_argument('-o', '--outputDir', type=str, required=True,
                                       help='[REQUIRED] The absolute path to the directory where the smaller '
                                            'images will be stored. Or a relative path from where this script is '
                                            'called from. If the directory already exists, it will be overwritten. '
                                            'If it does not exist, it will be made.')
        connection_parser.add_argument('-w', '--SubImageWidth', type=int, help='How many pixels wide each sub-image '
                                                                               'should be. Defaults to 227px')
        connection_parser.add_argument('-t', '--SubImageHeight', type=int,  help='How many pixels tall each sub-image '
                                                                                 'should be. Defaults to 227px')

        # connection_parser.add_argument('-s', "--SkipBreakdown", action="store_true",
        #                                 help="Skip the breakdown process and attempt to run recognition on an exiting " \
        #                                      "image. WILL ASSUME THAT THE IMAGE IS OF EITHER DEFAULT DIMENSIONS OR OF " \
        #                                      "SPECIFIED SUB-IMAGE WIDTH/HEIGHT.")

        connection_parser.add_argument('-p', '--ignoreLeftoverPixels', action='store_true',
                                       help='If the image width or height is not cleanly divisible by the '
                                            'given sub-image width / height values, there will be leftover '
                                            'pixels. This flag will prevent those leftovers from being made '
                                            'into their own non-regulation-sized sub-images.')

        connection_parser.add_argument('-g', '--recognitionGraphPath', type=str,
                                       help="An absolute path to the non-default graph to be used for crack recognition. "
                                            "Can also be relative path from where script is executed.")
        connection_parser.add_argument('-l', '--recognitionLabelsPath', type=str,
                                       help="An absolute path to the non-default labels to be used for crack recognition. "
                                            "Can also be relative path from where script is executed.")
        connection_parser.add_argument('-r', '--reportLocation', type=str,
                                       help="An absolute path to location where the summary report shall be output. "
                                            "Can also be relative path from where script is executed.")

        return connection_parser.parse_args()

    def parse_args(self, args):
        """
        Parses the given arguments and sets class parameters accordingly
        :param args: the args to parse.
        """

        if args:
            if args.inputPath:
                if args.singleFileRecognition:
                    self.is_input_dir = False
                    self.input_filepath = args.inputPath
                else:
                    self.input_filepath = os.path.join(args.inputPath, "*")
            if args.outputDir:
                self.cropped_subcomponent_dir_filepath = args.outputDir
            if args.SubImageWidth:
                self.cropped_px_width = args.subImageWidth
            if args.SubImageHeight:
                self.cropped_px_height = args.subImageHeight
            if args.ignoreLeftoverPixels:
                self.ignore_leftover_pixels = True
            # if args.SkipBreakdown:
            #     self.skip_breakdown = True
            if args.recognitionGraphPath:
                self.graph_filepath = args.recognitionGraph
            if args.recognitionLabelsPath:
                self.graph_labels_filepath = args.recognitionLabels
        else:
            self.exit_with_error_msg("No arguments given!")

    def setup_image_breakdown_arguments(self, input_filepath):
        """
        Creates the namespace that can be given to the image breakdown module to use as arguments.
        :param input_filepath: The filepath to the image that will be broken down.
        :return: a namespace that can be fed into the image breakdown module
        """
        breakdown_arg_namespace = SimpleNamespace()

        # Specific checks for required fields.
        if input_filepath:
            breakdown_arg_namespace.inputPath = input_filepath
        else:
            self.exit_with_error_msg("connecting_script.py, call_image_breakdown(): MUST have an "
                                     "input image path\n")
        if self.cropped_subcomponent_dir_filepath:
            breakdown_arg_namespace.outputDir = self.cropped_subcomponent_dir_filepath
        else:
            self.exit_with_error_msg("connecting_script.py, call_image_breakdown(): MUST have an "
                                     "output cropped image dir path\n")

        # Otherwise, set parameters to either default or specified values without fuss.
        breakdown_arg_namespace.subImageWidth = self.cropped_px_width
        breakdown_arg_namespace.subImageHeight = self.cropped_px_height
        # breakdown_arg_namespace.subImageWidth = 299
        # breakdown_arg_namespace.subImageHeight = 299
        breakdown_arg_namespace.ignoreLeftoverPixels = True if self.ignore_leftover_pixels else False

        return breakdown_arg_namespace

    def setup_recognition_arguments(self):
        """
        Creates the namespace that can be given to the recognition module to use as arguments. NOTE:
        DOES NOT SET THE IMAGE THAT WILL BE ANALYSED. That must be be done on a case-by-case basis outside
        of this function.
        :return: a namespace that can be fed into the recognition module
        """
        recog_arg_namespace = SimpleNamespace()

        # Name will need to be updated on an image-by-image basis. Leave blank for now
        recog_arg_namespace.input_filepath = ""

        recog_arg_namespace.graph = self.graph_filepath
        recog_arg_namespace.labels = self.graph_labels_filepath
        # recog_arg_namespace.input_width = self.cropped_px_width
        # recog_arg_namespace.input_height = self.cropped_px_height
        recog_arg_namespace.input_width = 299
        recog_arg_namespace.input_height = 299
        recog_arg_namespace.input_layer = "Placeholder"
        recog_arg_namespace.output_layer = "final_result"

        recog_arg_namespace.input_mean = self.DEFAULT_INPUT_MEAN
        recog_arg_namespace.input_std = self.DEFAULT_INPUT_STD

        return recog_arg_namespace

    def sub_report_parser(self, sub_report_dir):
        """
        Parses all the sub-reports found in the given directory into a single, fairly high level
        overview of what the image is like in terms of positive and negative detection. Final report
        will be output to the same directory.
        :param sub_report_dir: The directory that needs to be parsed.
        """
        if os.path.exists(sub_report_dir):
            list_of_reports = glob.glob(os.path.join(sub_report_dir, "*"))

            positive_report_list = []
            negative_report_list = []
            report_name = os.path.split(sub_report_dir)[1]
            # Go through all image sub reports
            for report_path in list_of_reports:
                with open(report_path) as r:
                    report_lines = r.readlines()
                # Go through all lines in that report and get values
                for line in report_lines:
                    if "Negative:" in line:
                        neg_value = float(line.split("Negative:")[1])
                    if "Positive:" in line:
                        pos_value = float(line.split("Positive:")[1])
                    if "Name:" in line:
                        sub_report_name = line.split("Name:")[1]

                if neg_value > pos_value:
                    negative_report_list.append(sub_report_name)
                else:
                    positive_report_list.append(sub_report_name)
                # Create the final report for the image, listing the number of neg > pos sub-images
                # and pos > neg sub-images.
                final_report_file = open(os.path.join(sub_report_dir,
                                                      os.path.split(report_name+"_final_report.txt"), "w+"))
                final_report_file.write("Name: {0}\n".format(report_name))
                final_report_file.write("Neg > Pos Image count: {0}\n".format(len(negative_report_list)))
                final_report_file.write("Neg > Pos Image reports: \n")
                for report in negative_report_list:
                    final_report_file.write("{0}\n".format(report))

                final_report_file.write("Pos > Neg Image count: {0}\n".format(len(positive_report_list)))
                final_report_file.write("Pos > Neg Image reports: \n")
                for report in positive_report_list:
                    final_report_file.write("{0}\n".format(report))

                final_report_file.close()
        else:
            self.exit_with_error_msg("connecting_script, sub_report_parser(): sub_report_dir {0} does not "
                                     "exist! Exiting".format(sub_report_dir))

    @staticmethod
    def wipe_directory(directory_path):
        """
        Small helper function that will remove the given path then remake it.
        :param directory_path: the path to wipe.
        """
        if os.path.exists(directory_path):
            shutil.rmtree(directory_path)
            os.mkdir(directory_path)

    @staticmethod
    def exit_with_error_msg(error_message):
        """
        exit the program with code 1 (failure) and print out the given message.
        :param error_message: The error message to print out
        """
        print(error_message)
        exit(1)


if __name__ == "__main__":
    connecting_module = UnifiedRecognitionModule()
    connecting_module.run_module()
