import cv2
import numpy as np
from eyeTracker import EyeTrack
from calibrator import Calibrator
from gui import UserInterface
from direcao import Direction
import threading

if __name__ == '__main__':
    ACTION_THRESHOLD = 2

    gui = UserInterface(ACTION_THRESHOLD+1)
    eyeTrack = EyeTrack(gui)
    calibrator = Calibrator(gui, eyeTrack)

    calibrator.calibrar()

    # t = threading.Thread(target=eyeTrack.run, args=(1,))
    # t.start()
    gui.show()
    direcaoAnterior = Direction.NENHUMA
    contadorDirecao = 0
    while True:
        coords, _ = eyeTrack.capturarCoordenadas(numFrames=1, debug=False)
        # print(coords)
        if coords:
             direcao = eyeTrack.getEyeDirection(coords)
        
        if direcao != Direction.NENHUMA:
            if direcaoAnterior == direcao:
                contadorDirecao += 1
            else:
                contadorDirecao = 0
        
        direcaoAnterior = direcao
        gui.updateTrackbar(contadorDirecao)

        if contadorDirecao > ACTION_THRESHOLD:
            contadorDirecao = 0
            gui.moverSelecao(direcao)
            if direcao == Direction.DIREITA:
                gui.falar("Direita")
            elif direcao == Direction.ESQUERDA:
                gui.falar("Esquerda")

        if cv2.waitKey(5)  & 0xFF == ord('q'): #Exit program when the user presses 'q'
            break

    cv2.destroyAllWindows()
