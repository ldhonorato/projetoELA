import cv2
import numpy as np
from eyeTracker import EyeTrack
from calibrator import Calibrator
from gui import UserInterface
import threading

if __name__ == '__main__':
    gui = UserInterface()
    eyeTrack = EyeTrack(gui)
    calibrator = Calibrator(gui, eyeTrack)

    calibrator.calibrar()

    t = threading.Thread(target=eyeTrack.run, args=(1,))
    while True:
        t.start()

        if cv2.waitKey(50)  & 0xFF == ord('q'): #Exit program when the user presses 'q'
            break

    cv2.destroyAllWindows()
