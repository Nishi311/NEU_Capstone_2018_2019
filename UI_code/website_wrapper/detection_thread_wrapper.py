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

        self.unified_module.cropped_subcomponent_dir_filepath = self.image_breakdown_dir
        self.unified_module.final_reports_dir = self.final_report_output_dir
        self.unified_module.final_reports_dir = self.final_report_output_dir

        if not os.path.exists(self.unified_module.cropped_subcomponent_dir_filepath):
            os.makedirs(self.unified_module.cropped_subcomponent_dir_filepath)

        # Sets up the module to run single-file recognition
        self.unified_module.is_input_dir = False
        self.unified_module.skip_parse_args = True
        self.unified_module.pre_wipe_output_dir = False

        self.unified_module.cropped_px_height = 1000
        self.unified_module.cropped_px_width = 1000

    def run_module(self):

        if not os.path.exists(self.photo_queue_dir):
            os.makedirs(self.photo_queue_dir)

        if not os.path.exists(self.photo_output_dir):
            os.makedirs(self.photo_output_dir)

        if not os.path.exists(self.final_report_output_dir):
            os.makedirs(self.final_report_output_dir)

        thread = threading.Thread(target=self.continous_detection(), args=())
        thread.daemon = True
        thread.start()

    def continous_detection(self):

        while True:
            self.queue_of_photos += self.check_for_new_photos()

            if self.queue_of_photos:
                current_photo = os.path.join(self.THIS_FILE_PATH, self.queue_of_photos.pop(0))
                # current_photo = os.path.join(self.GENERAL_IO_RELATIVE_DIR, "queued_photos")

                self.unified_module.input_filepath = current_photo
                self.unified_module.run_module()
                shutil.move(current_photo, self.photo_output_dir)
            else:
                print("Photo Queue Empty: Standing by for additional images\n")
                time.sleep(1)

    def check_for_new_photos(self):

        queue_dir_snapshot = glob.glob(os.path.join(self.photo_queue_dir, "*.jpg"))
        new_entries = list(set(queue_dir_snapshot) - set(self.queue_of_photos))

        return new_entries


if __name__ == "__main__":
    testModule = RecognitionThreadWrapper()
    testModule.run_module()
