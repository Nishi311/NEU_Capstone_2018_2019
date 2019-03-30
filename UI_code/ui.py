from flask import Flask, render_template, request, jsonify

from UI_code.website_wrapper.detection_thread_wrapper import RecognitionThreadWrapper

import threading
import webbrowser
import time
import os

app = Flask(__name__)

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
    path = "./static/images"
    for root, dirs, files in os.walk(path):
        print(dirs)
        break

    return jsonify(dirs)

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

    path = "./static/images/" + quadrant
    print(path)
    for root, dirs, files in os.walk(path):
        print(files)
        break

    files = [f for f in files if not f[0] == '.']
    files = ['/'+quadrant+'/'+f for f in files]
    return jsonify(files)


# Opens the program to the main menu.
def main():
    recognition_wrapper = RecognitionThreadWrapper()
    recognition_wrapper.run_module()

    webbrowser.get('windows-default').open("http://127.0.0.1:5000/")
    app.run(host='127.0.0.1')

if __name__ == "__main__":
    main()
