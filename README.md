# MorphFun
### Overview
Playing an instrument is a lot of fun, but what if you could have... MORPHFUN!

MorphFun is a Timbre Transfer application, that relies on a Pose Estimation approach to let the user choose the instrument.
The core libraries used are:
- [magenta/ddsp](https://github.com/magenta/ddsp) and its [Timbre Transfer](https://colab.research.google.com/github/magenta/ddsp/blob/master/ddsp/colab/demos/timbre_transfer.ipynb) demo module.
- [Mediapipe](https://google.github.io/mediapipe/), for the Pose Estimation part.
- [PyQT5](https://pypi.org/project/PyQt5/) for the Graphical User Interface.

The entire project is developed in Python and Jupyter Notebook.

### Project Versions
[Here](https://github.com/PaoloSani/MorphFun/blob/main/prototype_MORPHUN%20PRESENTATION.pptx), you can find the presentation of the prototype, developed between Python and [Processing](https://processing.org/).
If you want to take a look at the code see this [branch](https://github.com/PaoloSani/MorphFun/tree/Prototype).

Here, instead in the [main branch](https://github.com/PaoloSani/MorphFun) you can take a look to the final code of the application.

### Repo Structure
Apart from the main and the [Prototype](https://github.com/PaoloSani/MorphFun/tree/Prototype) branches, already introduced, this Repo has two more branches: [Develop](https://github.com/PaoloSani/MorphFun/tree/Develop) and [gui-develop](https://github.com/PaoloSani/MorphFun/tree/gui-develop). Both are dedicated to the project development.

### Main branch overview
The code is in the [Source folder](https://github.com/PaoloSani/MorphFun/tree/main/Source).
The main modules are:
- [main.py](https://github.com/PaoloSani/MorphFun/blob/main/Source/main.py), which creates the application, as well as the main thread and data queues.
- [controller.py](https://github.com/PaoloSani/MorphFun/blob/main/Source/controller.py), which orchestrate the behaviour of all the modules and the interaction between the GUI and the backend.
- [gui.py](https://github.com/PaoloSani/MorphFun/blob/main/Source/gui.py) contains the structure of the application GUI.
- [audio_utilities](https://github.com/PaoloSani/MorphFun/tree/main/Source/audio_utilities), which manage the audio acquisition and the reproduction of the morphed audios.
- [ddsp_functions](https://github.com/PaoloSani/MorphFun/tree/main/Source/ddsp_functions), which contains the functions used to morph the recorded audio with [magenta/ddsp](https://github.com/magenta/ddsp).
- [pose_estimation](https://github.com/PaoloSani/MorphFun/tree/main/Source/pose_estimation), which contains all the necessary modules for the pose_estimation part.
- [CONFIG](https://github.com/PaoloSani/MorphFun/tree/main/Source/CONFIG), [images](https://github.com/PaoloSani/MorphFun/tree/main/Source/images), [utils.py](https://github.com/PaoloSani/MorphFun/blob/main/Source/utils.py) and [models](https://github.com/PaoloSani/MorphFun/tree/main/Source/models) allow to build the application and the pipeline with all the correct configurations.

### Installation
To test this project, clone the Repo and install the libraries listed in [requirements.txt](https://github.com/PaoloSani/MorphFun/blob/main/requirements.txt) in a virtual environment of your choice.

### Contact the authors
| Name              | Contact                          |
|-------------------|----------------------------------|
| Armando Boemio    | armando.boemio@mail.polimi.it    |
| Lorenzo Brugioni  | lorenzo.brugioni@mail.polimi.it  |
| Gabriele Maucione | gabriele.maucione@mail.polimi.it |
| Paolo Sani        | paolo1.sani@mail.polimi.it       |
