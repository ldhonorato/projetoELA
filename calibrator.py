from gui import UserInterface
from direcao import Direction
from eyeTracker import EyeTrack
import cv2
import time


class Calibrator:
    def __init__(self, gui : UserInterface, eyeTracker : EyeTrack ):
        self.gui = gui
        self.eyeTracker = eyeTracker
            
    def calibrar(self):
        self.gui.showTexto('Calibrando!')
        cv2.waitKey(10)
        # time.sleep(1)
        
        #verificando se a face aparece
        self.gui.falar("Ajuste iluminação e posicionamento do rosto")
        consecutiveImages = 0
        while consecutiveImages < 25:
            coords, frame = self.eyeTracker.capturarCoordenadas(numFrames=1, debug=True)
            if coords:
                consecutiveImages += 1
            else:
                consecutiveImages = 0
            print(consecutiveImages)
            cv2.imshow("image", frame) #Display the frame for debug
            cv2.waitKey(1)


        #==================================================================
        #------------------------COORDENADAS CENTRO------------------------
        #==================================================================
        self.gui.showQuadradoCalibracao(Direction.CENTRO)
        cv2.waitKey(50)
        self.gui.falar("Olhe para o centro")
        
        
        coordenadasCentro = {}
        while not coordenadasCentro:
            coordenadasCentro, _ = self.eyeTracker.capturarCoordenadas()
            # print(coordenadasCentro)
        blinkRatio_open = coordenadasCentro['blink']
        coordenadasCentro = self.eyeTracker.calculateDistancesLR(coordenadasCentro)
            # print(coordenadasCentro)

        #==================================================================
        #------------------------COORDENADAS DIREITA-----------------------
        #==================================================================
        self.gui.showQuadradoCalibracao(Direction.DIREITA)
        cv2.waitKey(50)
        self.gui.falar("Olhe para a direita")
        

        coordenadasDireita = {}
        while not coordenadasDireita:
            coordenadasDireita, _ = self.eyeTracker.capturarCoordenadas()
        coordenadasDireita = self.eyeTracker.calculateDistancesLR(coordenadasDireita)
            # print(coordenadasDireita)
        
        #==================================================================
        #-----------------------COORDENADAS ESQUERDA-----------------------
        #==================================================================
        self.gui.showQuadradoCalibracao(Direction.ESQUERDA)
        cv2.waitKey(50)
        self.gui.falar("Olhe para a esquerda")
        
        coordenadasEsquerda = {}
        while not coordenadasEsquerda:
            coordenadasEsquerda, _ = self.eyeTracker.capturarCoordenadas()
        coordenadasEsquerda = self.eyeTracker.calculateDistancesLR(coordenadasEsquerda)
        # print(coordenadasDireita)

        #==================================================================
        #-----------------------COORDENADAS CIMA---------------------------
        #==================================================================
        self.gui.showQuadradoCalibracao(Direction.CIMA)
        cv2.waitKey(50)
        self.gui.falar("Olhe para cima")
        
        coordenadasCima = {}
        while not coordenadasCima:
            coordenadasCima, _ = self.eyeTracker.capturarCoordenadas()
        coordenadasCima = self.eyeTracker.calculateDistancesUD(coordenadasCima)

        #==================================================================
        #-----------------------COORDENADAS BAIXO--------------------------
        #==================================================================
        self.gui.showQuadradoCalibracao(Direction.BAIXO)
        cv2.waitKey(50)
        self.gui.falar("Feche os olhos")
        
        coordenadasBaixo = {}
        while not coordenadasBaixo:
            coordenadasBaixo, _ = self.eyeTracker.capturarCoordenadas()
        blinkRatio_close = coordenadasBaixo['blink']
        coordenadasBaixo = self.eyeTracker.calculateDistancesUD(coordenadasBaixo)
        
        # print(coordenadasDireita)


        # self.gui.showQuadradoCalibracao(Direction.BAIXO)
        # time.sleep(1)
        # coordenadasBaixo = self.eyeTracker.capturarCoordenadas()
        self.gui.falar("Calibração Concluída")

        calibracao = { "centro": coordenadasCentro,
                       "direita": coordenadasDireita,
                       "esquerda": coordenadasEsquerda,
                       "cima": coordenadasCima,
                       "baixo": coordenadasBaixo,
                       "aberto": blinkRatio_open,
                       "fechado": blinkRatio_close
                       }
        print("Calibracao: ", calibracao)
        self.eyeTracker.updateCalibracao(calibracao)

if __name__ == '__main__':
    gui = UserInterface()
    eyeTrack = EyeTrack(None)
    calibrator = Calibrator(gui, eyeTrack)
    calibrator.calibrar()
    while True:
        coords, frame = eyeTrack.capturarCoordenadas(numFrames=2, debug=True)

        if coords:
            direcao = eyeTrack.getEyeDirection(coords)
            print(direcao)
            if direcao == Direction.DIREITA:
                gui.falar("Direita")
            elif direcao == Direction.ESQUERDA:
                gui.falar("Esquerda")
            elif direcao == Direction.CIMA:
                gui.falar("Cima")
            elif direcao == Direction.FECHADO:
                gui.falar("Fechado")
        # print(coords)
        # if len(coords['center_l']) != 0:
        #     direcao = eyeTrack.getEyeDirection(coords)
        cv2.imshow("image", frame) #Display the frame for debug
        if cv2.waitKey(100) & 0xFF == ord('q'): #Exit program when the user presses 'q'
            break

