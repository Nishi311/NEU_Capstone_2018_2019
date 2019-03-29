# from ..CrackRecognition.scripts.connecting_script import UnifiedRecognitionModule

from CrackRecognition.scripts.connecting_script import UnifiedRecognitionModule

import threading
import time
import os
import glob
import shutil


class RecognitionThreadWrapper(object):

    GENERAL_IO_RELATIVE_DIR = os.path.join("..", "static", "generalIO")

    THIS_FILE_PATH = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        self.output_dir = os.path.join(self.GENERAL_IO_RELATIVE_DIR, "output")
        self.photo_queue_dir = os.path.join(self.GENERAL_IO_RELATIVE_DIR, "queued_photos")
        self.photo_output_dir = os.path.join(self.output_dir, "finished_photos")
        self.result_output_dir = os.path.join(self.output_dir, "finished_reports")

        # List of photos that currently need to be processed
        self.queue_of_photos = glob.glob(os.path.join(self.photo_queue_dir, "*.jpg"))

        # List of photos that have already been processed and can be ignored
        self.finished_photos = []

        # list of all photos (in
        self.photo_list_snapshot = glob.glob(self.photo_queue_dir)

        self.unified_module = UnifiedRecognitionModule()
        self.unified_module_setup()

    def unified_module_setup(self):

        self.unified_module.cropped_subcomponent_dir_filepath = os.path.join(self.THIS_FILE_PATH,
                                                                                 self.GENERAL_IO_RELATIVE_DIR,
                                                                                 "image_breakdown")
        self.unified_module.output_dir = self.output_dir
        self.unified_module.final_reports_dir = self.result_output_dir

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

        if not os.path.exists(self.result_output_dir):
            os.makedirs(self.result_output_dir)

        thread = threading.Thread(target=self.continous_detection(), args=())
        thread.daemon = True
        thread.start()

    def continous_detection(self):

        while True:
            time.sleep(1)
            self.queue_of_photos += self.check_for_new_photos()

            if self.queue_of_photos:
                current_photo = os.path.join(self.THIS_FILE_PATH, self.queue_of_photos.pop(0))
                # current_photo = os.path.join(self.GENERAL_IO_RELATIVE_DIR, "queued_photos")

                self.unified_module.input_filepath = current_photo
                self.unified_module.run_module()
                shutil.move(current_photo, self.photo_output_dir)

    def check_for_new_photos(self):

        queue_dir_snapshot = glob.glob(os.path.join(self.photo_queue_dir, "*.jpg"))
        new_entries = list(set(queue_dir_snapshot) - set(self.queue_of_photos))

        return new_entries


if __name__ == "__main__":
    testModule = RecognitionThreadWrapper()
    testModule.run_module()
