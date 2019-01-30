import os
import glob
import shutil


class ValidationModule(object):

    POSITIVE_STRING = "Positive"
    NEGATIVE_STRING = "Negative"
    REPORT_DESIGNATION_STRING = "final_report"

    REPORT_NEG_STRING = "Neg > Pos Image count:"
    REPORT_POS_STRING = "Pos > Neg Image count:"
    REPORT_NAME_STRING = "Name:"
    def __init__(self):
        self.baseline_location = ""
        self.base_true_pos_list = {}
        self.base_true_neg_list = {}

        self.reports_location = ""
        self.classified_pos_list = {}
        self.classified_neg_list = {}

        self.num_true_pos = 0
        self.num_true_neg = 0
        self.num_false_pos = 0
        self.num_false_neg = 0

        self.sub_image_detection_threshold = 0.5

        self.recall_percentage = 0
        self.precision_percentage = 0

    def gather_base_list(self):
        baseline_dir_path_list = glob.glob(self.baseline_location)

        for dir in baseline_dir_path_list:
            if self.POSITIVE_STRING in dir:
                self.base_true_pos_list = glob.glob(dir)
            elif self.NEGATIVE_STRING in dir:
                self.base_true_neg_list = glob.glob(dir)

    def gather_recognized_list(self):
        photo_path_list = glob.glob(self.reports_location)
        final_report_path_list = set()

        # Generate a list of all final reports (one for each photo)
        for photo_path in photo_path_list:
            list_of_report_paths = glob.glob(photo_path)
            for report_path in list_of_report_paths:
                if self.REPORT_STRING in report_path:
                    final_report_path_list.add(report_path)
        # Go through the report and find out how many sub-images were flagged
        # as positive versus negative.
        for report_path in final_report_path_list:
            report name = ""
            num_neg_sub_image = 0
            num_pos_sub_image = 0

            report_lines = open(report_path).readlines()
                for line in report_lines:
                    if self.REPORT_NAME_STRING in line:
                        report_name = line.split(self.REPORT_NAME_STRING)[1]
                    if self.REPORT_NEG_STRING in line:
                        num_neg_sub_image = int(line.split(self.REPORT_NEG_STRING)[1])
                    if self.REPORT_POS_STRING in line:
                        num_pos_sub_image = int(line.split(self.REPORT_POS_STRING)[1])

                if (num_pos_sub_image / (num_pos_sub_image+num_neg_sub_image)) > self.sub_image_detection_threshold:
                    self.classified_pos_list.




