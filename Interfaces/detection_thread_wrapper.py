import os
import threading
import time
import glob
import shutil

from CrackRecognition.scripts.connecting_script import UnifiedRecognitionModule

from Interfaces.side_and_quadrant_handling.gps_handler import GPSHandler
from Interfaces.side_and_quadrant_handling.side_handler import SideHandler


class RecognitionThreadWrapper(object):

    GENERAL_IO_RELATIVE_DIR = os.path.join("..", "UI_code", "static", "generalIO")

    THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))
    GENERAL_IO_ABS_PATH = os.path.join(THIS_FILE_PATH, GENERAL_IO_RELATIVE_DIR)

    CONFIG_FILE_NAME = "quadrant_config.txt"
    CONFIG_DIR = os.path.join(THIS_FILE_PATH, "configs")
    RECOGNITION_CONFIG_DIR = os.path.join(CONFIG_DIR, "recognition_config")

    def __init__(self):
        self.photo_queue_dir = os.path.join(self.GENERAL_IO_ABS_PATH, "queued_photos")
        self.intermediary_dir = os.path.join(self.GENERAL_IO_ABS_PATH, "intermediary")
        self.image_breakdown_dir = os.path.join(self.intermediary_dir, "image_breakdown")
        self.breakdown_report_dir = os.path.join(self.intermediary_dir, "breakdown_reports")

        self.output_dir = os.path.join(self.GENERAL_IO_ABS_PATH, "output")
        self.photo_output_dir = os.path.join(self.output_dir, "finished_photos")
        self.final_report_output_dir = os.path.join(self.output_dir, "finished_reports")

        self.side_handler = SideHandler()

        # List of photos that currently need to be processed
        self.queue_of_photos = []

        # List of photos that have already been processed and can be ignored
        self.finished_photos = []

        # list of all photos (in
        self.photo_list_snapshot = glob.glob(self.photo_queue_dir)

        self.unified_module = UnifiedRecognitionModule()

        self.recognition_state_file_path = os.path.join(self.RECOGNITION_CONFIG_DIR, "state.txt")

        self.running_recognition = False

    def run_module(self):
        """
        Governing function for the entire class. Will start a new thread dedicated to checking queue directory for new
        images and running recognition on them and spitting out results. Will poll for new images once a second.
        """
        self.wipe_previous_directories()

        self.setup_recognition_config()
        self.unified_module_setup()

        # Read in existing configurations, if available.
        if os.path.exists(self.CONFIG_DIR):
            if os.listdir(self.CONFIG_DIR):
                self.side_handler.read_sides_from_configs()
        else:
            os.makedirs(self.CONFIG_DIR)

        self.create_general_directories()
        self.check_and_update_queue()
        # Begin the main loop of check, recognize, report.
        thread = threading.Thread(target=self.continous_detection, name="recognition_thread", args=())
        thread.daemon = True
        thread.start()

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

    def setup_recognition_config(self):
        """
        Set recognition to not run as a default option
        :return:
        """
        if not os.path.exists(self.RECOGNITION_CONFIG_DIR):
            os.makedirs(self.RECOGNITION_CONFIG_DIR)

        with open(self.recognition_state_file_path, "w") as state_file:
            state_file.write("INACTIVE")

    def continous_detection(self):
        """
        Never ending function that will constantly poll for new images, run recognition, and spit out results.
        """
        # Run ALL THE TIME!!!!
        # Begin initialization of quadrant list
        while True:

            # Run continual checks for new states or sides.
            self.check_and_update_recognition_state()
            self.side_handler.check_for_new_sides()
            self.check_and_update_queue()

            if self.running_recognition:
                # Add any new photos in the directory to the queue
                # If the queue is populated, run recognition workflow on top of the queue
                if self.queue_of_photos:
                    # Pop top of the queue off for recognition
                    current_photo = os.path.join(self.THIS_FILE_PATH, self.queue_of_photos[0])
                    current_photo_name = os.path.split(current_photo)[1]
                    side_name, quad_name = self.determine_photo_side_and_quad(current_photo)
                    side_quad_path = os.path.join(side_name, quad_name)

                    # Run recognition workflow
                    self.unified_module.input_filepath = current_photo
                    self.unified_module.final_reports_sub_dir = os.path.join(self.unified_module.final_reports_dir,
                                                                             side_quad_path)
                    self.unified_module.run_module()

                    # Move finished photo out of the queue directory and into the finished directory
                    quadrant_photo_output_dir = os.path.join(self.photo_output_dir, side_quad_path)
                    if not os.path.exists(quadrant_photo_output_dir):
                        os.makedirs(quadrant_photo_output_dir)

                    output_photo_path = os.path.join(quadrant_photo_output_dir, current_photo_name)
                    if os.path.exists(output_photo_path):
                        os.remove(output_photo_path)

                    shutil.move(current_photo, quadrant_photo_output_dir)
                    self.queue_of_photos.pop(0)
                # Otherwise, wait a second and see if anything new comes up.
                else:
                    time.sleep(1)

    def check_and_update_recognition_state(self):
        with open(self.recognition_state_file_path) as state_file:
            state_line = state_file.readline()
        if state_line == "ACTIVE":
            self.running_recognition = True
        else:
            self.running_recognition = False

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

    def determine_photo_side_and_quad(self, photo_path):
        photo_lat_dd, photo_long_dd, photo_alt_m = GPSHandler().run_module(photo_path)

        side_name, quad_name = self.side_handler.determine_side_and_quadrant(photo_lat_dd, photo_long_dd, photo_alt_m)

        return [side_name, quad_name]

    def create_general_directories(self):
        # Setup all input / output directories. Intermediary directories will be created by the
        # unified module as needed.
        if not os.path.exists(self.photo_queue_dir):
            os.makedirs(self.photo_queue_dir)

        if not os.path.exists(self.photo_output_dir):
            os.makedirs(self.photo_output_dir)

        if not os.path.exists(self.final_report_output_dir):
            os.makedirs(self.final_report_output_dir)
        
        if self.side_handler.side_list:
            self.side_handler.create_all_side_dirs()

    # Thanks to https://www.pythoncentral.io/hashing-files-with-python/

    def wipe_previous_directories(self):
        if os.path.exists(self.CONFIG_DIR):
            shutil.rmtree(self.CONFIG_DIR)

        inter_output_directory = os.path.join(self.GENERAL_IO_ABS_PATH, "intermediary")
        final_output_directory = os.path.join(self.GENERAL_IO_ABS_PATH, "output")

        if os.path.exists(inter_output_directory):
            shutil.rmtree(inter_output_directory)

        if os.path.exists(final_output_directory):
            shutil.rmtree(final_output_directory)


if __name__ == "__main__":
    testModule = RecognitionThreadWrapper()
    testModule.run_module()
