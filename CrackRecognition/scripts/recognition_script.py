# Copyright 2017 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Base code from: https://github.com/tensorflow/tensorflow/raw/master/tensorflow/examples/label_image/label_image.py
# ==============================================================================

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import argparse

import numpy as np
import tensorflow as tf


class RecognitionModule(object):
    DEFAULT_INTER_REPORT_FILEPATH = os.path.join("..", "output", "individual_reports")

    def __init__(self):
        self.input_filepath = ""
        self.model_file = ""
        self.label_file = ""
        self.input_height = 299
        self.input_width = 299
        self.input_mean = 0
        self.input_std = 255
        self.input_layer = "input"
        self.output_layer = "InceptionV3/Predictions/Reshape_1"
        self.report_location = ""
        self.graph = None

    def setup_module(self, args=""):
        if not args:
            args = self.set_args()
        self.parse_args(args)

        self.graph = self.load_graph(self.model_file)

    def run_module(self):

        image_name = os.path.split(self.input_filepath)[1].split(".")[0]
        report_path = os.path.join(self.report_location, image_name + "_report.txt")
        inter_report_file = open(report_path, "w+")
        inter_report_file.write("name: {0}\n".format(image_name))

        if self.graph:
            t = self.read_tensor_from_image_file(
                self.input_filepath,
                input_height=self.input_height,
                input_width=self.input_width,
                input_mean=self.input_mean,
                input_std=self.input_std)

            input_name = "import/" + self.input_layer
            output_name = "import/" + self.output_layer
            input_operation = self.graph.get_operation_by_name(input_name)
            output_operation = self.graph.get_operation_by_name(output_name)

            with tf.Session(graph=self.graph) as sess:
                results = sess.run(output_operation.outputs[0], {
                    input_operation.outputs[0]: t})
            results = np.squeeze(results)

            top_k = results.argsort()[-5:][::-1]
            labels = self.load_labels(self.label_file)

            for i in top_k:
                print(labels[i], results[i])
                inter_report_file.write("{0}: {1}\n".format(labels[i], results[i]))

            inter_report_file.close()
        else:
            self.exit_with_error_msg("recognition_script, run_module(): No graph set. Was setup run? Exiting.")

    def set_args(self):
        recognition_parser = argparse.ArgumentParser()

        recognition_parser.add_argument("--input_filepath", help="image to be processed")
        recognition_parser.add_argument("--graph", help="graph/model to be executed")
        recognition_parser.add_argument("--labels", help="name of file containing labels")
        recognition_parser.add_argument("--input_height", type=int, help="input height")
        recognition_parser.add_argument("--input_width", type=int, help="input width")
        recognition_parser.add_argument("--input_mean", type=int, help="input mean")
        recognition_parser.add_argument("--input_std", type=int, help="input std")
        recognition_parser.add_argument("--input_layer", help="name of input layer")
        recognition_parser.add_argument("--output_layer", help="name of output layer")

        return recognition_parser.parse_args()

    def parse_args(self, args):
        if args.graph:
            self.model_file = args.graph
        if args.input_filepath:
            self.input_filepath = args.image
        if args.labels:
            self.label_file = args.labels
        if args.input_height:
            self.input_height = args.input_height
        if args.input_width:
            self.input_width = args.input_width
        if args.input_mean:
            self.input_mean = args.input_mean
        if args.input_std:
            self.input_std = args.input_std
        if args.input_layer:
            self.input_layer = args.input_layer
        if args.output_layer:
            self.output_layer = args.output_layer

    # Static functions
    @staticmethod
    def load_graph(model_file):
        graph = tf.Graph()
        graph_def = tf.GraphDef()

        with open(model_file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graph_def)

        return graph

    @staticmethod
    def read_tensor_from_image_file(input_filepath,
                                    input_height=299,
                                    input_width=299,
                                    input_mean=0,
                                    input_std=255):
        input_name = "file_reader"
        output_name = "normalized"
        file_reader = tf.read_file(input_filepath, input_name)
        if input_filepath.endswith(".png"):
            image_reader = tf.image.decode_png(
                file_reader, channels=3, name="png_reader")
        elif input_filepath.endswith(".gif"):
            image_reader = tf.squeeze(
                tf.image.decode_gif(file_reader, name="gif_reader"))
        elif input_filepath.endswith(".bmp"):
            image_reader = tf.image.decode_bmp(file_reader, name="bmp_reader")
        else:
            image_reader = tf.image.decode_jpeg(
                file_reader, channels=3, name="jpeg_reader")
        float_caster = tf.cast(image_reader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0)
        resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
        sess = tf.Session()
        result = sess.run(normalized)

        return result

    @staticmethod
    def load_labels(label_file):
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(label_file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
        return label

    @staticmethod
    def exit_with_error_msg(error_message):
        """
        exit the program with code 1 (failure) and print out the given message.
        :param error_message: The error message to print out
        """
        print(error_message)
        exit(1)

if __name__ == "__main__":
    recongition_module = RecognitionModule()
    recongition_module.setup_module()
    recongition_module.run_module()
