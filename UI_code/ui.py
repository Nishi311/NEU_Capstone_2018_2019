from flask import Flask, render_template, request, jsonify


from Interfaces.detection_thread_wrapper import RecognitionThreadWrapper
from Interfaces.quadrant_handling.quadrant_handler import QuadrantHandler
import webbrowser
import time
import os


app = Flask(__name__)
THIS_FILE_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIRECTORY = os.path.join(THIS_FILE_DIR_PATH, "static", "generalIO", "output")
quadrant = "quadrant_2"

# Main menu
@app.route('/')
def ui():
    return render_template('ui.html')

# Terminates the program
@app.route('/exit', methods=['GET', 'POST'])
def close_ui():
    exit()

# Gets the Initial GEO coordinates from the Drone
# These coordinates are used for later pathplanning
@app.route('/building_sweep', methods=['GET', 'POST'])
def initialize_drone():
    print("initializing drone")
    return jsonify("success")

# Brings up the drone control pannel
@app.route('/open_drone_manual', methods=['GET', 'POST'])
def open_drone_control_panel():
    print("opening drone control menu")
    return render_template('drone_control_ui.html')

# Gets the manual directions selected by user
@app.route('/drone_manual', methods=['GET', 'POST'])
def drone_manual_control():
    if request.method == 'POST':
        direction = request.form['direction']
        print(direction)
    return jsonify("success")

# Brings up the camera control pannel
@app.route('/open_camera_manual', methods=['GET', 'POST'])
def open_camera_control_panel():
    print("opening camera control menu")
    return render_template('Camera_control_ui.html')

# Gets the manual directions selected by the user and returns an image
# if the user takes one
@app.route('/camera_manual', methods=['GET', 'POST'])
def camera_manual_control():
    if request.method == 'POST':
        direction = request.form['direction']
        if direction == "PIC":
            print("taking picture")
        elif direction == "UP":
            print(direction)
            return jsonify("UP success")
        elif direction == "DOWN":
            print(direction)
            return jsonify("DOWN success")
        else:
            return jsonify("failure")
    else:
        new = "https://www.boma.org/images/homePage/windyPoint.png"
        old = "test"
        if new != old:
            return jsonify(new)
        else:
            time.sleep(5);
            new = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a8/Industrial_Trust_Building_Providence_RI.jpg/240px-Industrial_Trust_Building_Providence_RI.jpg"

            if new != old:
                return jsonify(new)
            else:
                return jsonify("failure")
    return jsonify("failure")


@app.route('/count_quadrants', methods=['GET', 'POST'])
def retrieve_available_quadrants():
    path = os.path.join(OUTPUT_DIRECTORY, "finished_reports")
    try:
        for root, dirs, files in os.walk(path):
            print(dirs)
            return jsonify(dirs)

            break
    except Exception as e:
        print(e)


@app.route('/select_new_quadrant', methods=['GET', 'POST'])
def select_new_quadrant():
    global quadrant

    if request.method == 'POST':
        quadrant = request.form['quadrant']
        print(quadrant)
        return jsonify("success")

    return jsonify("nothing changed")

# Gets all images stored for a give quadrant
# TODO: Grab image results, make new JSON {image_name, crack / no crack}
@app.route('/get_images', methods=['GET', 'POST'])
def get_images():
    global quadrant

    path = os.path.join(OUTPUT_DIRECTORY, "finished_photos", quadrant)
    print(path)
    image_list = []
    try:
        for throw_away_root, throw_away_dirs, image_list in os.walk(path):
            print(image_list)
            break
        if image_list:
            return_list = []
            for image_name in image_list:
                image_path_quadrant_rel = os.path.join(quadrant, image_name)
                file_name_no_ext = os.path.splitext(image_name)[0]

                report_name = file_name_no_ext + "_final_report.txt"
                full_report_path = os.path.join(OUTPUT_DIRECTORY, "finished_reports", quadrant, report_name)

                with open(full_report_path) as report:
                    throw_away_name_line = report.readline()
                    success_line = report.readline()
                    success_value = success_line.split("Crack Detected: ")[1].replace('\n', '')

                final_file_return_string = image_path_quadrant_rel + ": {0},{1}".format(quadrant, success_value)
                return_list.append(final_file_return_string)
            # file_list = [f for f in file_list if not f[0] == '.']
            # file_list = ['/' + quadrant + '/' + f for f in file_list]
            return jsonify(return_list)
        return jsonify("No Images")
    except Exception as e:
        print(e)

@app.route('/update_quadrant_config', methods=['POST'])
def update_quadrant_config():
    js_data = request.form['grid_data']
    quad_handler = QuadrantHandler()
    quad_handler.write_quadrants_to_config(js_data)

    return "And Hello to you too"

@app.route('/get_all_image_results', methods=['POST'])
def get_all_image_results():
    test = request
    partial_image_paths = request.form['partial_image_paths']
    # partial_image_paths = request.args.get('partial_image_paths')
    # TODO: parse partial image paths properly.
    results = []
    for image_path in partial_image_paths:
        quadrant_name, image_name = os.path.split(image_path)

        quadrant_name = quadrant_name.replace('/', '')
        image_name_no_ext = os.path.splitext(image_name)[0]
        report_name = image_name_no_ext + "_final_report.txt"

        full_image_path = os.path.join(OUTPUT_DIRECTORY, "finished_photos", image_path)

        full_report_path = os.path.join(OUTPUT_DIRECTORY, "finished_reports", quadrant_name, report_name)
        with open(full_report_path) as report:
            name_line = report.readline()
            success_line = report.readline()

        success_value = success_line.split("Crack Detected: ")[1].replace('\n', '')


        results += [image_path, quadrant_name, success_value]
    return jsonify(results)

# Opens the program to the main menu.
def main():
    # TODO: add try catch-block to prevent script from running if error.
    recognition_wrapper = RecognitionThreadWrapper()
    recognition_wrapper.run_module()

    webbrowser.get('windows-default').open("http://127.0.0.1:5000/")
    app.run(host='127.0.0.1')

class basic(object):
    
    @staticmethod
    def run_module():
        # TODO: add try catch-block to prevent script from running if error.
        recognition_wrapper = RecognitionThreadWrapper()
        recognition_wrapper.run_module()

        webbrowser.get('windows-default').open("http://127.0.0.1:5000/")
        app.run(host='127.0.0.1')

#if __name__ == "__main__":
#    main()
