from flask import Flask, render_template, request, jsonify


from Interfaces.detection_thread_wrapper import RecognitionThreadWrapper
from Interfaces.side_and_quadrant_handling.side_object import SideObject
import webbrowser
import time
import os


app = Flask(__name__)
THIS_FILE_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIRECTORY = os.path.join(THIS_FILE_DIR_PATH, "static", "generalIO", "output")

result_side = "NO SIDE CHOSEN"
result_quadrant = "NO QUADRANT CHOSEN"

status_side = "NO SIDE CHOSEN"

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


@app.route('/get_sides_list', methods=['GET', 'POST'])
def get_sides_list():
    path = os.path.join(OUTPUT_DIRECTORY, "finished_reports")

    if os.path.exists(path):
        try:
            for root, dirs, files in os.walk(path):
                if dirs:
                    return jsonify(dirs)
                else:
                    return jsonify("No sides found")
        except Exception as e:
            return jsonify("No sides found")
    else:
        return jsonify("No sides found")


@app.route('/get_quadrants_list', methods=['GET', 'POST'])
def get_quadrants_list():
    global result_side

    path = os.path.join(OUTPUT_DIRECTORY, "finished_reports", result_side)

    if os.path.exists(path):
        try:
            for root, dirs, files in os.walk(path):
                if dirs:
                    return jsonify(dirs)
                else:
                    return jsonify("No quadrants found")
        except Exception as e:
            return jsonify("No quadrants found")
    else:
        return jsonify("No quadrants found")


@app.route('/select_new_result_quadrant', methods=['GET', 'POST'])
def select_new_result_quadrant():
    global result_quadrant

    if request.method == 'POST':
        if request.form['quadrant'] != "No Quadrants Found":
            result_quadrant = request.form['quadrant']
        return jsonify("success")

    return jsonify("nothing changed")


@app.route('/select_new_result_side', methods=['GET', 'POST'])
def select_new_result_side():
    global result_side
    global result_quadrant

    if request.method == 'POST':
        if request.form['side'] != "No Sides Found":
            result_side = request.form['side']
            result_quadrant = "No Quadrant Chosen"
        return jsonify("success")

    return jsonify("nothing changed")

@app.route('/select_new_status_side', methods=['GET', 'POST'])
def select_new_status_side():
    global status_side

    if request.method == 'POST':
        if request.form['side'] != "No Sides Found":
            result_side = request.form['side']
        return jsonify("success")

    return jsonify("nothing changed")


# Gets all images stored for a give quadrant
@app.route('/get_all_image_data', methods=['GET', 'POST'])
def get_all_image_data():
    global result_quadrant
    global result_side

    path = os.path.join(OUTPUT_DIRECTORY, "finished_photos", result_side, result_quadrant)
    image_list = []
    try:
        for throw_away_root, throw_away_dirs, image_list in os.walk(path):
            print(image_list)
            break
        if image_list:
            return_list = []
            for image_name in image_list:
                image_path_quadrant_rel = os.path.join(result_side, result_quadrant, image_name)
                file_name_no_ext = os.path.splitext(image_name)[0]

                report_name = file_name_no_ext + "_final_report.txt"
                full_report_path = os.path.join(OUTPUT_DIRECTORY, "finished_reports", result_side, result_quadrant, report_name)

                with open(full_report_path) as report:
                    throw_away_name_line = report.readline()
                    coord_line = report.readline()
                    success_line = report.readline()
                coord_string = coord_line.split("Coordinates(Lat, Long, Alt): ")[1].replace('\n', '')
                success_value = success_line.split("Crack Detected: ")[1].replace('\n', '')

                final_file_return_string = "{0}|{1}|{2}|{3}".format(image_path_quadrant_rel, coord_string, result_quadrant,
                                                                    success_value)
                return_list.append(final_file_return_string)
            return jsonify(return_list)

        return jsonify("No Images")
    except Exception as e:
        print(e)

@app.route('/add_new_side', methods=['POST'])
def add_new_side():
    grid_data = request.form['grid_data']
    num_photos_per_quad = request.form['num_photos_per_quad']
    new_side_name = "Side {0}".format(get_num_sides()+1)
    side_object = SideObject(new_side_name)
    side_object.write_quadrants_to_config(grid_data, num_photos_per_quad)
    side_object.create_side_dirs()

    return "And Hello to you too"

def get_num_sides():
    path = os.path.join(OUTPUT_DIRECTORY, "finished_reports")

    if os.path.exists(path):
        try:
            for root, dirs, files in os.walk(path):
                if "Unknown Side" in dirs:
                    return len(dirs)-1
                else:
                    return len(dirs)
        except Exception as e:
            return -1
    else:
        return -1

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

        try:
            webbrowser.get('windows-default').open("http://127.0.0.1:5000/")
        except:
            webbrowser.get('chrome').open("http://127.0.0.1:5000/")
        
        app.run(host='127.0.0.1')

#if __name__ == "__main__":
#    main()
