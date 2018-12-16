In order to run the ML stuff, you'll need to install Anaconda from :

https://www.anaconda.com/download/

Once it's installed, run the command:

conda create -n [whatever you want the env to be called] --file [path to the conda_env_requirement.txt file]

This will set up the conda environment complete with tensorflow, PIL and other dependencies of this program. Be sure to
actually set the program to use this env though!
1.) If using Pycharm, go to "File->Settings->Project->Project Interpreter"
2.) Open the "Project Interpreter" dropdown menu at the top and click "Show all"
3.) Click the "+" button
4.) Select "Conda Env"
5.) Select "Existing Env"
6.) Navigate to your conda install folder
7.) Find the "envs" folder in the conda directory and select the environment you just set up.