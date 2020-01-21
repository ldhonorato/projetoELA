import cv2
import numpy as np
from direcao import Direction
from win32api import GetSystemMetrics

class UserInterface:
    def __init__(self):
        agua = cv2.resize(cv2.imread('imgs/agua.jpg'), (256, 256))
        comida = cv2.resize(cv2.imread('imgs/comida.jpg'), (256, 256))
        saliva = cv2.resize(cv2.imread('imgs/limpar_saliva.jpg'), (256, 256))
        pescoco = cv2.resize(cv2.imread('imgs/pescoco.jpg'), (256, 256))
        youtube = cv2.resize(cv2.imread('imgs/youtube.jpg'), (256, 256))

        coceira = cv2.resize(cv2.imread('imgs/coceira.jpg'), (256, 256))
        dor = cv2.resize(cv2.imread('imgs/dor.jpg'), (256, 256))
        mudar_posicao = cv2.resize(cv2.imread('imgs/mudar_posicao.jpg'), (256, 256))
        falta_ar = cv2.resize(cv2.imread('imgs/falta_de_ar.jpg'), (256, 256))
        bpap = cv2.resize(cv2.imread('imgs/bpap.jpg'), (256, 256))
        image_linha1 = np.concatenate((agua, comida, saliva, pescoco, youtube), axis=1)
        image_linha2 = np.concatenate((coceira, dor, mudar_posicao, falta_ar, bpap), axis=1)
        self.guiPainel = np.concatenate((image_linha1, image_linha2), axis=0)
        self.guiPainelContorno = np.copy(self.guiPainel)
        self.proporcao_tela = 1.1
        self.font                   = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (100,500)
        self.fontScale              = 1
        self.fontColor              = (255,255,255)
        self.lineType               = 2
        self.width = GetSystemMetrics(0)
        self.height = GetSystemMetrics(1)
        self.indice_selecao = 0

        self.mean_y = int(self.width*self.proporcao_tela/2)
        self.mean_x = int(self.height*self.proporcao_tela/2)

        self.contornaImagem(self.indice_selecao)
    
    def show(self):
        cv2.imshow("image", self.guiPainelContorno)
    
    def contornaImagem(self, indice):
        self.guiPainelContorno = np.copy(self.guiPainel)
        iniX = int(indice/5)*255
        fimX = (int(indice/5)+1)*255
        iniY = int(indice%5)*255
        fimY = (int(indice%5)+1)*255
        self.guiPainelContorno[iniX:iniX+10,iniY:fimY,:]=0
        self.guiPainelContorno[fimX-10:fimX,iniY:fimY,:]=0
        self.guiPainelContorno[iniX:fimX,iniY:iniY+10,:]=0
        self.guiPainelContorno[iniX:fimX,fimY-10:fimY,:]=0
        #return self.guiPainelContorno
    
    def moverSelecao(self, eyeDirection):
        if eyeDirection == Direction.DIREITA:
            if self.indice_selecao < 9:
                self.indice_selecao += 1
            else:
                self.indice_selecao = 0
        elif eyeDirection == Direction.ESQUERDA:
            if self.indice_selecao > 0:
                self.indice_selecao -= 1
            else:
                self.indice_selecao = 9
    
    def showQuadradoCalibracao(self, direcao):
        frame = np.zeros([int(self.height*self.proporcao_tela),int(self.width*self.proporcao_tela),3],dtype=np.uint8)
        #frame.fill(0)
        if direcao == Direction.CENTRO:
            frame[self.mean_x-20:self.mean_x+20,self.mean_y-20:self.mean_y+20]=255
        elif direcao == Direction.DIREITA:
            frame[self.mean_x-20:self.mean_x+20,int(self.width*self.proporcao_tela)-40:]=255
        elif direcao ==  Direction.ESQUERDA:
            frame[self.mean_x-20:self.mean_x+20,:40]=255
        #elif direcao == EyeDirection.BAIXO:
        cv2.imshow("image", frame)
    
    def showTexto(self, texto):
        frame = np.zeros([int(self.height*self.proporcao_tela),int(self.width*self.proporcao_tela),3],dtype=np.uint8)
        cv2.putText(frame,texto,self.bottomLeftCornerOfText,self.font,self.fontScale,self.fontColor,self.lineType)
        cv2.imshow("image", frame)


            
if __name__ == '__main__':
    gui = UserInterface()
    while True:
        #gui.show()
        gui.showQuadradoCalibracao(Direction.DIREITA)

        if cv2.waitKey(50)  & 0xFF == ord('q'): #Exit program when the user presses 'q'
            break

    cv2.destroyAllWindows()

