import os
import threading
import time
import glob
import shutil

from CrackRecognition.scripts.connecting_script import UnifiedRecognitionModule

from Interfaces.quadrant_handling.quadrant_object import Quadrant
from Interfaces.quadrant_handling.quadrant_handler import QuadrantHandler
from Interfaces.quadrant_handling.gps_handler import GPSHandler

import hashlib

class RecognitionThreadWrapper(object):

    GENERAL_IO_RELATIVE_DIR = os.path.join("..", "UI_code", "static", "generalIO")

    THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    GENERAL_IO_ABS_PATH = os.path.join(THIS_FILE_PATH, GENERAL_IO_RELATIVE_DIR)

    CONFIG_FILE_NAME = "quadrant_config.txt"
    CONFIG_DIR = os.path.join(THIS_FILE_PATH, "configs")
    CONFIG_PATH = os.path.join(CONFIG_DIR, CONFIG_FILE_NAME)

    def __init__(self):
        self.photo_queue_dir = os.path.join(self.GENERAL_IO_ABS_PATH, "queued_photos")
        self.intermediary_dir = os.path.join(self.GENERAL_IO_ABS_PATH, "intermediary")
        self.image_breakdown_dir = os.path.join(self.intermediary_dir, "image_breakdown")
        self.breakdown_report_dir = os.path.join(self.intermediary_dir, "breakdown_reports")

        self.output_dir = os.path.join(self.GENERAL_IO_ABS_PATH, "output")
        self.photo_output_dir = os.path.join(self.output_dir, "finished_photos")
        self.final_report_output_dir = os.path.join(self.output_dir, "finished_reports")

        self.config_hash = self.hash_file(self.CONFIG_PATH)
        self.quadrant_handler = QuadrantHandler()

        # List of photos that currently need to be processed
        self.queue_of_photos = glob.glob(os.path.join(self.photo_queue_dir, "*.jpg"))

        # List of photos that have already been processed and can be ignored
        self.finished_photos = []

        # list of all photos (in
        self.photo_list_snapshot = glob.glob(self.photo_queue_dir)

        self.unified_module = UnifiedRecognitionModule()
        self.unified_module_setup()

    def unified_module_setup(self):
        """
        Sets up the Unified Module to run single-file crack recognition.
        """
        # Assign breakdown photo / report paths as well as final report path
        self.unified_module.cropped_subcomponent_dir_filepath = self.image_breakdown_dir
        self.unified_module.breakdown_reports_dir = self.breakdown_report_dir
        self.unified_module.final_reports_dir = self.final_report_output_dir

        # Sets up the module to run single-file recognition
        self.unified_module.is_input_dir = False
        self.unified_module.skip_parse_args = True

        self.unified_module.cropped_px_height = 1000
        self.unified_module.cropped_px_width = 1000

    def run_module(self):
        """
        Governing function for the entire class. Will start a new thread dedicated to checking queue directory for new
        images and running recognition on them and spitting out results. Will poll for new images once a second.
        """
        self.quadrant_handler.read_quadrants_from_config()
        self.create_general_directories()

        # Begin the main loop of check, recognize, report.
        thread = threading.Thread(target=self.continous_detection, name="recognition_thread", args=())
        thread.daemon = True
        thread.start()

    def continous_detection(self):
        """
        Never ending function that will constantly poll for new images, run recognition, and spit out results.
        """
        # Run ALL THE TIME!!!!
        while True:
            # Add any new photos in the directory to the queue
            self.check_and_update_queue()

            # If the queue is populated, run recognition workflow on top of the queue
            if self.queue_of_photos:
                # Pop top of the queue off for recognition
                self.check_and_update_quadrants()
                current_photo = os.path.join(self.THIS_FILE_PATH, self.queue_of_photos.pop(0))

                photo_quadrant = self.determine_photo_quadrant(current_photo)

                # Run recognition workflow
                self.unified_module.input_filepath = current_photo
                self.unified_module.final_reports_sub_dir = os.path.join(self.unified_module.final_reports_dir,
                                                                         photo_quadrant)
                self.unified_module.run_module()

                # Move finished photo out of the queue directory and into the finished directory
                quadrant_photo_output_dir = os.path.join(self.photo_output_dir, photo_quadrant)
                if not os.path.exists(quadrant_photo_output_dir):
                    os.makedirs(quadrant_photo_output_dir)

                shutil.move(current_photo, quadrant_photo_output_dir)

            # Otherwise, wait a second and see if anything new comes up.
            else:
                print("Photo Queue Empty: Standing by for additional images\n")
                time.sleep(1)

    def check_and_update_queue(self):
        """
        Quick function that checks to see if there are any new photos in the queue directory that are NOT ALREADY
        in the queue list. If so, add them.
        """
        # Get the list of all photos in the directory
        queue_dir_snapshot = glob.glob(os.path.join(self.photo_queue_dir, "*.jpg"))
        # Get a list of photos that are not already in the queue
        new_entries = list(set(queue_dir_snapshot) - set(self.queue_of_photos))
        # Update the queue
        self.queue_of_photos += new_entries

    def check_and_update_quadrants(self):
        new_hash = self.hash_file(self.CONFIG_PATH)

        if not new_hash == self.config_hash:
            self.quadrant_handler.read_quadrants_from_config()
            self.create_quadrant_directories()

            self.config_hash = new_hash

    def determine_photo_quadrant(self, photo_path):
        photo_lat_dd, photo_long_dd, photo_alt_m = GPSHandler().run_module(photo_path)

        photo_quadrant_name = self.quadrant_handler.determine_quadrant_from_coords(photo_lat_dd, photo_long_dd,
                                                                                   photo_alt_m)

        return photo_quadrant_name

    def create_general_directories(self):
        # Setup all input / output directories. Intermediary directories will be created by the
        # unified module as needed.
        if not os.path.exists(self.photo_queue_dir):
            os.makedirs(self.photo_queue_dir)

        if not os.path.exists(self.photo_output_dir):
            os.makedirs(self.photo_output_dir)

        if not os.path.exists(self.final_report_output_dir):
            os.makedirs(self.final_report_output_dir)

        if self.quadrant_handler.quadrant_list:
            self.create_quadrant_directories()

    def create_quadrant_directories(self):

        for quadrant in self.quadrant_handler.quadrant_list:
            quadrant_report_path = os.path.join(self.final_report_output_dir, quadrant.quadrant_name)
            quadrant_photo_path = os.path.join(self.photo_output_dir, quadrant.quadrant_name)

            if not os.path.exists(quadrant_report_path):
                os.makedirs(quadrant_report_path)
            if not os.path.exists(quadrant_photo_path):
                os.makedirs(quadrant_photo_path)

        unknown_quadrant_report_path = os.path.join(self.final_report_output_dir, "Unknown Quadrant")
        unknown_quadrant_photo_path = os.path.join(self.photo_output_dir, "Unknown Quadrant")

        if not os.path.exists(unknown_quadrant_report_path):
            os.makedirs(unknown_quadrant_report_path)
        if not os.path.exists(unknown_quadrant_photo_path):
            os.makedirs(unknown_quadrant_photo_path)

    # Thanks to https://www.pythoncentral.io/hashing-files-with-python/
    @staticmethod
    def hash_file(file_path):
        hasher = hashlib.md5()
        with open(file_path, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        return hasher.hexdigest()


if __name__ == "__main__":
    testModule = RecognitionThreadWrapper()
    testModule.run_module()
