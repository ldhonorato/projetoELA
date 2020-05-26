import cv2
import numpy as np
from eyeTracker import EyeTrack
from gui import UserInterface
from direcao import Direction

if __name__ == '__main__':
    int2Text = ['zero', 'um', 'dois', 'tres', 'quatro', 'cinco']
    ACTION_THRESHOLD = 2
    gui = UserInterface(ACTION_THRESHOLD+1)
    eyeTrack = EyeTrack(gui)
    contadorOlhosFechados = 0

    gui.show()
    video = cv2.VideoCapture(0) # Start capturing the WebCam

    while True:
        
        grabed, frame = video.read()
        if not grabed:
            break
        
        coords,_ = eyeTrack.getCoordenada(frame, debug=True)
                    
        if coords:
            direcao = eyeTrack.getEyeDirection(coords)
        
            if direcao == Direction.DIREITA or direcao == Direction.ESQUERDA:
                gui.moverSelecao(direcao)

            if direcao == Direction.FECHADO:
                if contadorOlhosFechados == 0:
                    gui.falar("Olhos fechados")
                else:
                    gui.falar(int2Text[contadorOlhosFechados])
                
                if contadorOlhosFechados == 3:
                    gui.falar('Saindo do programa')
                    break
                contadorOlhosFechados += 1
                
            else:
                contadorOlhosFechados = 0
                if direcao == Direction.DIREITA:
                    gui.falar("Direita")
                elif direcao == Direction.ESQUERDA:
                    gui.falar("Esquerda")
                elif direcao == Direction.CIMA:
                    gui.falarSelecao()
        
        if cv2.waitKey(5)  & 0xFF == ord('q'): #Exit program when the user presses 'q'
            break

    cv2.destroyAllWindows()
