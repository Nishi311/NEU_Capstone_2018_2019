from flask import Flask, render_template, request, jsonify


from Interfaces.detection_thread_wrapper import RecognitionThreadWrapper
from Interfaces.quadrant_handling.quadrant_handler import QuadrantHandler
import webbrowser
import time
import os


app = Flask(__name__)
THIS_FILE_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIRECTORY = os.path.join(THIS_FILE_DIR_PATH, "static", "generalIO", "output")
side = "Unknown Side"
quadrant = "Unknown Quadrant"

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


@app.route('/count_sides', methods=['GET', 'POST'])
def count_sides():
    path = os.path.join(OUTPUT_DIRECTORY, "finished_reports")

    if os.path.exists(path):
        try:
            for root, dirs, files in os.walk(path):
                if dirs:
                    print(dirs)
                    return jsonify(dirs)
                else:
                    return jsonify("No sides found")
        except Exception as e:
            return jsonify("No sides found")
    else:
        return jsonify("No sides found")


@app.route('/count_quadrants', methods=['GET', 'POST'])
def count_quadrants():
    global side

    path = os.path.join(OUTPUT_DIRECTORY, "finished_reports", side)

    if os.path.exists(path):
        try:
            for root, dirs, files in os.walk(path):
                if dirs:
                    print(dirs)
                    return jsonify(dirs)
                else:
                    return jsonify("No quadrants found")
        except Exception as e:
            return jsonify("No quadrants found")
    else:
        return jsonify("No quadrants found")

@app.route('/select_new_quadrant', methods=['GET', 'POST'])
def select_new_quadrant():
    global quadrant

    if request.method == 'POST':
        if request.form['quadrant'] != "No Quadrants Found":
            quadrant = request.form['quadrant']
            print(quadrant)
        return jsonify("success")

    return jsonify("nothing changed")

@app.route('/select_new_side', methods=['GET', 'POST'])
def select_new_side():
    global side

    if request.method == 'POST':
        if request.form['side'] != "No Sides Found":
            side = request.form['side']
            print(side)
        return jsonify("success")

    return jsonify("nothing changed")

# Gets all images stored for a give quadrant
@app.route('/get_all_image_data', methods=['GET', 'POST'])
def get_all_image_data():
    global quadrant
    global side

    path = os.path.join(OUTPUT_DIRECTORY, "finished_photos", side, quadrant)
    print(path)
    image_list = []
    try:
        for throw_away_root, throw_away_dirs, image_list in os.walk(path):
            print(image_list)
            break
        if image_list:
            return_list = []
            for image_name in image_list:
                image_path_quadrant_rel = os.path.join(side, quadrant, image_name)
                file_name_no_ext = os.path.splitext(image_name)[0]

                report_name = file_name_no_ext + "_final_report.txt"
                full_report_path = os.path.join(OUTPUT_DIRECTORY, "finished_reports", side, quadrant, report_name)

                with open(full_report_path) as report:
                    throw_away_name_line = report.readline()
                    coord_line = report.readline()
                    success_line = report.readline()
                coord_string = coord_line.split("Coordinates(Lat, Long, Alt): ")[1].replace('\n', '')
                success_value = success_line.split("Crack Detected: ")[1].replace('\n', '')

                final_file_return_string = "{0}|{1}|{2}|{3}".format(image_path_quadrant_rel, coord_string, quadrant,
                                                                    success_value)
                return_list.append(final_file_return_string)
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
