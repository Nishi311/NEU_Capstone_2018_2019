# from ..CrackRecognition.scripts.connecting_script import UnifiedRecognitionModule

from CrackRecognition.scripts.connecting_script import UnifiedRecognitionModule

import threading
import time
import os
import glob
import shutil
# TODO: Sort out report paths between detection thread / connecting script / recognition script


class RecognitionThreadWrapper(object):

    GENERAL_IO_RELATIVE_DIR = os.path.join("..", "static", "generalIO")

    THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    GENERAL_IO_ABS_PATH = os.path.join(THIS_FILE_PATH, GENERAL_IO_RELATIVE_DIR)

    def __init__(self):
        self.photo_queue_dir = os.path.join(self.GENERAL_IO_ABS_PATH, "queued_photos")
        self.intermediary_dir = os.path.join(self.GENERAL_IO_ABS_PATH, "intermediary")
        self.image_breakdown_dir = os.path.join(self.intermediary_dir, "image_breakdown")
        self.breakdown_report_dir = os.path.join(self.intermediary_dir, "breakdown_reports")

        self.output_dir = os.path.join(self.GENERAL_IO_ABS_PATH, "output")
        self.photo_output_dir = os.path.join(self.output_dir, "finished_photos")
        self.final_report_output_dir = os.path.join(self.output_dir, "finished_reports")

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

        # Setup all input / output directories. Intermediary directories will be created by the
        # unified module as needed.
        if not os.path.exists(self.photo_queue_dir):
            os.makedirs(self.photo_queue_dir)

        if not os.path.exists(self.photo_output_dir):
            os.makedirs(self.photo_output_dir)

        if not os.path.exists(self.final_report_output_dir):
            os.makedirs(self.final_report_output_dir)

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
                current_photo = os.path.join(self.THIS_FILE_PATH, self.queue_of_photos.pop(0))

                # Run recognition workflow
                self.unified_module.input_filepath = current_photo
                self.unified_module.run_module()

                # Move finished photo out of the queue directory and into the finished directory
                shutil.move(current_photo, self.photo_output_dir)

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


if __name__ == "__main__":
    testModule = RecognitionThreadWrapper()
    testModule.run_module()
