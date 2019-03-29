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
    FINAL_REPORT_NAME = "baseline_report_verbose.txt"

    def __init__(self):
        self.baseline_location = ""
        self.base_true_pos_list = []
        self.base_true_neg_list = []

        self.reports_location = ""
        self.classified_pos_list = []
        self.classified_neg_list = []

        self.image_type = ".jpg"

        self.true_pos_list = []
        self.true_neg_list = []
        self.false_pos_list = []
        self.false_neg_list = []
        self.num_total_reports = 0
        self.sub_image_detection_threshold = 0.5

        self.recall_percentage = 0
        self.precision_percentage = 0
        self.accuracy_percentage = 0

        self.verbose_report = False

    def run_module(self):

        args = self.set_args()
        self.parse_args(args)

        self.gather_base_list()
        self.gather_classified_list()
        self.calculate_stats()
        self.generate_report()

    def set_args(self):
        validation_parser = argparse.ArgumentParser(description='Runs reports analysis, generating metrics on '
                                                                'recognition success and failure.')
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
        validation_parser.add_argument('-v', '--verbose', action='store_true',
                                       help='If set, will output the names of all photos classified under their '
                                            'respective tags (true pos, true neg, false pos, false neg')
        return validation_parser.parse_args()

    def parse_args(self, args):
        if args:
            if args.baselinePath:
                self.baseline_location = args.baselinePath
            else:
                self.exit_with_error_msg("MUST provide baseline path")
            if args.reportsPath :
                self.reports_location = args.reportsPath
            else:
                self.exit_with_error_msg("MUST provide report path")
            if float(args.posThreshold) >= 0:
                self.sub_image_detection_threshold = args.posThreshold
            if args.extensionType:
                self.image_type = args.extensionType
            if args.verbose:
                self.verbose_report = True

    def gather_base_list(self):
        # Need to go one level down for actual list of file paths.
        baseline_dir_path_list = glob.glob(os.path.join(self.baseline_location, "**",
                                                        "*{0}".format(self.image_type)), recursive=True)
        temp_neg_list = set()
        temp_pos_list = set()

        for photo_path in baseline_dir_path_list:
            if self.POSITIVE_STRING in photo_path:
                temp_pos_list.add(photo_path)
            elif self.NEGATIVE_STRING in photo_path:
                temp_neg_list.add(photo_path)

        # Strip away all paths and extension types and leave bare file name for pos / neg list.
        for photo_name in temp_pos_list:
            self.base_true_pos_list.append(os.path.split(os.path.splitext(photo_name)[0])[1])
        for photo_name in temp_neg_list:
            self.base_true_neg_list.append(os.path.split(os.path.splitext(photo_name)[0])[1])

    def gather_classified_list(self):
        # Go one level down from the given directory to find actual reports.
        list_of_report_paths = glob.glob(os.path.join(self.reports_location, "**", "*.txt"), recursive=True)
        final_report_path_list = set()

        # Generate a list of all final reports (one for each photo)
        for report_path in list_of_report_paths:
            if self.CLASS_REPORT_DESIGNATION_STRING in report_path:
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
                    # Get rid of trailing new line and leading space in report name.
                    report_name = line.split(self.CLASS_REPORT_NAME_STRING)[1].rstrip().lstrip()
                if self.CLASS_REPORT_NEG_STRING in line:
                    num_neg_sub_image = int(line.split(self.CLASS_REPORT_NEG_STRING)[1])
                if self.CLASS_REPORT_POS_STRING in line:
                    num_pos_sub_image = int(line.split(self.CLASS_REPORT_POS_STRING)[1])

            if (num_pos_sub_image / (num_pos_sub_image+num_neg_sub_image)) > self.sub_image_detection_threshold:
                self.classified_pos_list.append(report_name)
            else:
                self.classified_neg_list.append(report_name)

    def calculate_stats(self):
        for report in self.base_true_pos_list:
            if report in self.classified_pos_list:
                self.true_pos_list.append(report)
            if report in self.classified_neg_list:
                self.false_neg_list.append(report)
        
        for report in self.base_true_neg_list:
            if report in self.classified_pos_list:
                self.false_pos_list.append(report)
            if report in self.classified_neg_list:
                self.true_neg_list.append(report)
        
        self.num_total_reports = len(self.true_pos_list + self.true_neg_list + self.false_pos_list + self.false_neg_list)
        
        self.accuracy_percentage = float(len(self.true_pos_list + self.true_neg_list) / self.num_total_reports)
        self.recall_percentage = float(len(self.true_pos_list) / len(self.true_pos_list + self.false_neg_list))
        self.precision_percentage = float(len(self.true_pos_list) / len(self.true_pos_list + self.false_pos_list))
        
    def generate_report(self):
        if not os.path.exists(self.FINAL_REPORT_LOCATION):
            os.makedirs(self.FINAL_REPORT_LOCATION)
        os.chdir(self.FINAL_REPORT_LOCATION)
        final_report = open(self.FINAL_REPORT_NAME, "w+")

        calculation_results_string = "Report Time: {0}\nAccuracy Rating: {1}\nRecall Rating: {2}\n" \
                                     "Precision Rating {3}\n\n".format(datetime.datetime.now(), self.accuracy_percentage,
                                                                     self.recall_percentage, self.precision_percentage)
        final_report.write(calculation_results_string)

        if self.verbose_report:
            raw_results_string = "Num True Pos: {0}\nTrue Pos List:\n{1}\n\nNum True Neg: {2}\nTrue Neg List: \n{3}\n\n" \
                                 "Num False Pos: {4}\nFalse Pos List:\n{5}\n\nNum False Neg: {6}\nFalse Neg List:\n{7}\n\n"\
                                 .format(len(self.true_pos_list), self.true_pos_list,
                                         len(self.true_neg_list), self.true_neg_list,
                                         len(self.false_pos_list), self.false_pos_list,
                                         len(self.false_neg_list), self.false_neg_list)
            final_report.write(raw_results_string)
        else:
            raw_results_string = "Num True Pos: {0}\nNum True Neg: {1}\nNum False Pos: {2}\nNum False Neg: {3}\n" \
                .format(len(self.true_pos_list), len(self.true_neg_list), len(self.false_pos_list),
                        len(self.false_neg_list))
            final_report.write(raw_results_string)

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
