from gui import UserInterface
from direcao import Direction
from eyeTracker import EyeTrack
import cv2

class Calibrator:
    def __init__(self, gui : UserInterface, eyeTracker : EyeTrack ):
        self.gui = gui
        self.eyeTracker = eyeTracker
    
    def calibrar(self):
        self.gui.showTexto('Calibrando!')
        cv2.waitKey(1000)

        self.gui.showQuadradoCalibracao(Direction.CENTRO)
        cv2.waitKey(500)
        coordenadasCentro = self.eyeTracker.capturarCoordenadas()

        self.gui.showQuadradoCalibracao(Direction.DIREITA)
        cv2.waitKey(500)
        coordenadasDireita = self.eyeTracker.capturarCoordenadas()
        
        self.gui.showQuadradoCalibracao(Direction.ESQUERDA)
        cv2.waitKey(500)
        coordenadasEsquerda = self.eyeTracker.capturarCoordenadas()

        self.gui.showQuadradoCalibracao(Direction.BAIXO)
        cv2.waitKey(500)
        coordenadasBaixo = self.eyeTracker.capturarCoordenadas()

        #TODO: Calcular e atualizar calibracao em EyeTracker
        calibracao = None
        self.eyeTracker.updateCalibracao(calibracao)



