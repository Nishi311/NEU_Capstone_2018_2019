Going to need Anaconda to run this thing.

Follow this guide to install Anaconda:
https://www.youtube.com/watch?v=83vR1Nz3dHA

Install the Anaconda Navigator for easy UI management of Conda environments:
https://anaconda.org/anaconda/anaconda-navigator

MUST USE PYTHON 3.6 FOR THIS. TENSORFLOW DOES NOT. REPEAT NOT. WORK ON PYTHON 3.7

Install the following libraries:
    NOTE: For libraries that don't show up in the "not installed" tab of the env package list (listed here with a
          "(terminal)" designator, you can just run the env with the terminal and then use
          "python -m pip install [package name]" to do it manually.

# Website
flask

# Image manipulation / GPS Coordinate grabbing
pillow
exifread (terminal)

# Crack Detection
tensorboard (terminal)
tensorflow
numpy
scipy

If you have a NVIDIA GPU that supports CUDA drivers, can use "tensorflow-gpu" instead of "tensorflow" during package
installation. HOWEVER, you must also install the appropriate CUDA drivers:

https://developer.nvidia.com/cuda-downloads