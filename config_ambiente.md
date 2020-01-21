# How to create [Anaconda](https://www.anaconda.com/distribution/) Environment for this project

To create environment from the 'projeto_ela_env.yml' file:
* conda env create -f projeto_ela_env.yml

To create evirnment from scrach, run the following lines:
1. conda create -n projeto_ela python=3.6
2. conda install -c conda-forge opencv=3.4.3
3. conda install -c conda-forge pywin32
4. conda install -c conda-forge dlib
5. pip install pyttsx3
6. conda install -c conda-forge scipy
7. conda install -c conda-forge pyautogui
8. pip install keyboard
9. conda install -c conda-forge rope

In both cases, you also need to download the following files:
* [shape_predictor_68_face_landmarks.dat]( https://github.com/AKSHAYUBHAT/TensorFace/blob/master/openface/models/dlib/shape_predictor_68_face_landmarks.dat)
* [haarcascade_frontalface_alt.xml](https://github.com/opencv/opencv/blob/master/data/haarcascades/haarcascade_frontalface_alt.xml)

