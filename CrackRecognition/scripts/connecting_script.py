import os
import argparse

from .image_breakdown import ImageBreakdownModule
from .recognition_script import RecognitionModule


class UnifiedRecognition(object):
    # Default width of an image sub-component as measured in pixels
    DEFAULT_WIDTH = 227

    # Default height of an image sub-component as measured in pixels
    DEFAULT_HEIGHT = 227

    # Default graph that will be used to detect cracks.
    DEFAULT_GRAPH_FILENAME = "crack_detection_graph.pb"

    # Default labl set that will be used to label detection results.
    DEFAULT_LABEL_FILENAME = "crack_detection_labels.txt"

    def __init__(self):

        # Variables related to image breakdown
        self.full_image_filepath = ""
        self.cropped_subcomponent_dir_filepath = ""
        self.cropped_px_width = self.DEFAULT_WIDTH
        self.cropped_px_height = self.DEFAULT_HEIGHT
        self.ignoreLeftoverPixels = False
        self.skip_breakdown = False

        # Variables related to image recognition
        self.graph_name = self.DEFAULT_GRAPH_FILENAME
        self.graph_labels = self.DEFAULT_LABEL_FILENAME
        self.cropped_image_filepath = ""

    def run_module(self):
        args = self.set_args()
        self.parse_args(args)

        if

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
                                       help='[REQUIRED] The absolute path to the image that will be broken down. '
                                             'Or a relative path to the image from where this script is called from')
        connection_parser.add_argument('-o', '--outputDir', type=str, required=True,
                                       help='[REQUIRED] The absolute path to the directory where the smaller '
                                            'images will be stored. Or a relative path from where this script is '
                                            'called from. If the directory already exists, it will be overwritten. '
                                            'If it does not exist, it will be made.')
        connection_parser.add_argument('-w', '--SubImageWidth', type=int, help='How many pixels wide each sub-image '
                                                                               'should be. Defaults to 227px')
        connection_parser.add_argument('-t', '--SubImageHeight', type=int,  help='How many pixels tall each sub-image '
                                                                                 'should be. Defaults to 227px')

        connection_parser.add_argument("--SkipBreakdown",store=True, help="Skip the breakdown process and attempt to"
                                                                          "run recognition on an exiting image. WILL"
                                                                          "ASSUME THAT THE IMAGE IS OF EITHER DEFAULT"
                                                                          "DIMENSIONS OR OF SPECIFIED SUB-IMAGE "
                                                                          "WIDTH/HEIGHT.")

        connection_parser.add_argument('-p', '--ignoreLeftoverPixels', action='store_true',
                                       help='If the image width or height is not cleanly divisible by the '
                                            'given sub-image width / height values, there will be leftover '
                                            'pixels. This flag will prevent those leftovers from being made '
                                            'into their own non-regulation-sized sub-images.')

        connection_parser.add_argument('-g', '--recognitionGraph', type=str, help="An absolute path to the non-default"
                                                                                  "graph to be used for crack "
                                                                                  "recognition. Can also be relative"
                                                                                  "path from where script is executed.")
        connection_parser.add_argument('-l', '--recognitionLabels', type=str, help="An absolute path to the non-default"
                                                                                   "labels to be used for crack "
                                                                                   "recognition. Can also be relative"
                                                                                   "path from where script is executed.")
        connection_parser.add_argument("--use")
        return connection_parser.parse_args()

    def parse_args(self, args):
        """
        Parses the given arguments and sets class parameters accordingly
        :param args: the args to parse.
        """

        if args:
            if args.inputPath:
                self.full_image_filepath = args.inputPath
            if args.outputDir:
                self.cropped_subcomponent_dir_filepath = args.outputDir
            if args.SubImageWidth:
                self.cropped_px_width = args.subImageWidth
            if args.SubImageHeight:
                self.cropped_px_height = args.subImageHeight
            if args.ignoreLeftoverPixels:
                self.ignoreLeftoverPixels = True
            if args.SkipBreakdown:
                self.skip_breakdown = True
            if args.recognitionGraph:
                self.graph_name = args.recognitionGraph
            if args.recognitionLabels:
                self.graph_labels = args.recognitionLabels
        else:
            self.exit_with_error_msg("No arguments given!")

    def call_image_breakdown(self):
        pass

    @staticmethod
    def exit_with_error_msg(error_message):
        """
        exit the program with code 1 (failure) and print out the given message.
        :param error_message: The error message to print out
        """
        print(error_message)
        exit(1)
