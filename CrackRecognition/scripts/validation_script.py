import os
import glob
import datetime
import argparse


class ValidationModule(object):

    POSITIVE_STRING = "Positive"
    NEGATIVE_STRING = "Negative"

    CLASS_REPORT_DESIGNATION_STRING = "final_report"
    CLASS_REPORT_NEG_STRING = "Neg > Pos Image count:"
    CLASS_REPORT_POS_STRING = "Pos > Neg Image count:"
    CLASS_REPORT_NAME_STRING = "Name:"

    FINAL_REPORT_LOCATION = os.path.join("..", "output", "classification_stats")
    FINAL_REPORT_NAME = "training_report.txt"

    def __init__(self):
        self.baseline_location = ""
        self.base_true_pos_list = set()
        self.base_true_neg_list = set()

        self.reports_location = ""
        self.classified_pos_list = set()
        self.classified_neg_list = set()

        self.image_type = ".jpg"

        self.num_true_pos = 0
        self.num_true_neg = 0
        self.num_false_pos = 0
        self.num_false_neg = 0
        self.num_total_reports = 0
        self.sub_image_detection_threshold = 0.5

        self.recall_percentage = 0
        self.precision_percentage = 0
        self.accuracy_percentage = 0

    def run_module(self):

        args = self.set_args()
        self.parse_args(args)

        self.gather_base_list()
        self.gather_classified_list()
        self.calculate_stats()
        self.generate_report()

    def set_args(self):
        validation_parser = argparse.ArgumentParser(description='Runs reports analysis, generating metrics on recognition'
                                                            'success and failure.')
        validation_parser.add_argument('-b', '--baselinePath', type=str, required=True,
                                       help='[REQUIRED] The absolute / relative path to where the baseline photos'
                                            'are stored')
        validation_parser.add_argument('-r', '--reportsPath', type=str, required=True,
                                       help='[REQUIRED] the absolute / relative path to where the reports are stored.')
        validation_parser.add_argument('-t', '--posThreshold', type=float,
                                       help='the ratio of pos to neg sub-images that will determine if an entire image '
                                            'is crack-positive. By default the ratio is 0.5 for pos classification')
        validation_parser.add_argument('-e', '--extensionType', type=str,
                                       help='The extension type of the photos. By default is ".jpg"')
        return validation_parser.parse_args()

    def parse_args(self, args):
        if args:
            if args.baselinePath:
                self.baseline_location = args.baselinePath
            else:
                self.exit_with_error_msg("MUST provide baseline path")
            if args.reportsPath:
                self.reports_location = args.reportsPath
            else:
                self.exit_with_error_msg("MUST provide report path")
            if args.posThreshold:
                self.sub_image_detection_threshold = args.posThreshold
            if args.extensionType:
                self.image_type = args.extensionType

    def gather_base_list(self):
        # Need to go one level down for actual list of file paths.
        baseline_dir_path_list = glob.glob(os.path.join(self.baseline_location, "**",
                                                        "*{0}".format(self.image_type)), recursive=True)
        temp_neg_list = set()
        temp_pos_list = set()

        for dir in baseline_dir_path_list:
            if self.POSITIVE_STRING in dir:
                temp_pos_list = set(glob.glob(dir))
            elif self.NEGATIVE_STRING in dir:
                temp_neg_list = set(glob.glob(dir))

        # Strip away all paths and extension types and leave bare file name for pos / neg list.
        for photo_name in temp_pos_list:
            self.base_true_pos_list.add(os.path.split(os.path.splitext(photo_name)[0])[1])
        for photo_name in temp_neg_list:
            self.base_true_neg_list.add(os.path.split(os.path.splitext(photo_name)[0])[1])

    def gather_classified_list(self):
        # Go one level down from the given directory to find actual reports.
        list_of_report_paths = glob.glob(os.path.join(self.reports_location, "**", "*.txt"), recursive=True)
        final_report_path_list = set()

        # Generate a list of all final reports (one for each photo)
        for report_path in list_of_report_paths:
            if self.REPORT_STRING in report_path:
                final_report_path_list.add(report_path)
        # Go through the report and find out how many sub-images were flagged
        # as positive versus negative.
        for report_path in final_report_path_list:
            report_name = ""
            num_neg_sub_image = 0
            num_pos_sub_image = 0

            report_lines = open(report_path).readlines()
            for line in report_lines:
                if self.CLASS_REPORT_NAME_STRING in line:
                    report_name = line.split(self.CLASS_REPORT_NAME_STRING)[1]
                if self.CLASS_REPORT_NEG_STRING in line:
                    num_neg_sub_image = int(line.split(self.CLASS_REPORT_NEG_STRING)[1])
                if self.CLASS_REPORT_POS_STRING in line:
                    num_pos_sub_image = int(line.split(self.CLASS_REPORT_POS_STRING)[1])

            if (num_pos_sub_image / (num_pos_sub_image+num_neg_sub_image)) >= self.sub_image_detection_threshold:
                self.classified_pos_list.add(report_name)
            else:
                self.classified_neg_list.add(report_name)

    def calculate_stats(self):
        for report in self.base_true_pos_list:
            if report in self.classified_pos_list:
                self.num_true_pos += 1
            if report in self.classified_neg_list:
                self.num_false_neg += 1
        
        for report in self.base_true_neg_list:
            if report in self.classified_pos_list:
                self.num_false_pos += 1
            if report in self.classified_neg_list:
                self.num_true_neg += 1 
        
        self.num_total_reports = self.num_true_pos + self.num_true_neg + self.num_false_pos + self.num_false_neg
        
        self.accuracy_percentage = float((self.num_true_pos + self.num_true_neg) / self.num_total_reports)
        self.recall_percentage = float(self.num_true_pos / (self.num_true_pos + self.num_false_neg))
        self.precision_percentage = float(self.num_true_pos / (self.num_true_pos + self.num_false_pos))
        
    def generate_report(self):
        if not os.path.exist(self.FINAL_REPORT_LOCATION):
            os.makedirs(self.FINAL_REPORT_LOCATION)
        os.chdir(self.FINAL_REPORT_LOCATION)

        final_report = open(self.FINAL_REPORT_NAME, "w+")
        final_report.write("Report Time: {0}\n".format(datetime.datetime.now()))
        final_report.write("Accuracy Rating: {0}\n".format(self.accuracy_percentage))
        final_report.write("Recall Rating: {0}\n".format(self.recall_percentage))
        final_report.write("Precision Rating {0}\n".format(self.precision_percentage))

        final_report.close()

    @staticmethod
    def exit_with_error_msg(error_message):
        """
        exit the program with code 1 (failure) and print out the given message.
        :param error_message: The error message to print out
        """
        print(error_message)
        exit(1)


if __name__ == "__main__":
    validation_module = ValidationModule()
    validation_module.run_module()




