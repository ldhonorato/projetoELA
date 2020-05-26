import cv2
import numpy as np
import pyttsx3
import win32api
from direcao import Direction
#from win32api import GetSystemMetrics 
from PIL import Image, ImageDraw, ImageFont

class UserInterface:
    def __init__(self, trackbarSize=3):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (100,500)
        self.fontScale = 1
        self.fontColor = (255,255,255)
        self.lineType = 2
        
        agua,comida,saliva,pescoco,youtube,coceira,dor,mudar_posicao,falta_ar,bpap = self.put_img_needs()
        image_linha1 = np.concatenate((agua, comida, saliva, pescoco, youtube), axis=1)
        image_linha2 = np.concatenate((coceira, dor, mudar_posicao, falta_ar, bpap), axis=1)

        self.frases = ["água, por favor", "estou com fome", "limpe minha saliva", "meu pescoço doi", "quero ver tv", 
                       "Estou com coceira", "estou com dor", "quero mudar de posição", "estou com falta de ar", "ligue o bi pap"]
        
        self.guiPainel = np.concatenate((image_linha1, image_linha2), axis=0)
        self.guiPainelContorno = np.copy(self.guiPainel)
        self.proporcao_tela = 1.1
        self.width = win32api.GetSystemMetrics(0)
        self.height = win32api.GetSystemMetrics(1)
        self.indice_selecao = 0

        self.mean_y = int(self.width*self.proporcao_tela/2)
        self.mean_x = int(self.height*self.proporcao_tela/2)

        self.contornaImagem(self.indice_selecao)
        self.engine = pyttsx3.init()
        self.trackbarSize = trackbarSize
        
    def upload_img(self, image, slogan):
        obj = cv2.resize(cv2.imread(image), (256, 226))
        frameTexto = np.zeros([30,256,3],dtype=np.uint8)
        cv2.putText(frameTexto,slogan,(10,20),self.font,0.8,self.fontColor,self.lineType)
        obj = np.concatenate((obj, frameTexto), axis=0)
        return obj

    def put_img_needs(self):
        agua = self.upload_img('imgs/agua.jpg','Estou com sede')
        comida = self.upload_img('imgs/comida.jpg', 'Estou com fome')
        saliva = self.upload_img('imgs/limpar_saliva.jpg', 'Limpar saliva')
        pescoco = self.upload_img('imgs/pescoco.jpg', 'Dor no pescoco')
        youtube = self.upload_img('imgs/youtube.jpg', 'Ver TV')
        coceira = self.upload_img('imgs/coceira.jpg', 'Estou com coceira')
        dor = self.upload_img('imgs/dor.jpg', 'Estou com dor')
        mudar_posicao = self.upload_img('imgs/mudar_posicao.jpg', 'Mudar de posicao')
        falta_ar = self.upload_img('imgs/falta_de_ar.jpg', 'Falta de ar')
        bpap = self.upload_img('imgs/bpap.jpg', 'Bpap')
        
        return agua,comida,saliva,pescoco,youtube,coceira,dor,mudar_posicao,falta_ar,bpap

    def nothing(self, x):
        pass

    def show(self):
        cv2.imshow("image", self.guiPainelContorno)
        # cv2.createTrackbar('Ativando','image',0,self.trackbarSize,self.nothing)
    
    def updateTrackbar(self, value):
        cv2.setTrackbarPos('Ativando','image',value)
    
    def falar(self, texto):
        self.engine.say(texto)
        self.engine.setProperty('rate',200)
        self.engine.runAndWait()
    
    def falarSelecao(self):
        self.falar(self.frases[self.indice_selecao])

    def contornaImagem(self, indice):
        self.guiPainelContorno = np.copy(self.guiPainel)
        iniX = int(indice/5)*255
        fimX = (int(indice/5)+1)*255
        iniY = int(indice%5)*255
        fimY = (int(indice%5)+1)*255
        cor = [0, 0, 255] #BGR
        self.guiPainelContorno[iniX:iniX+10,iniY:fimY]=cor
        self.guiPainelContorno[fimX-10:fimX,iniY:fimY]=cor
        self.guiPainelContorno[iniX:fimX,iniY:iniY+10]=cor
        self.guiPainelContorno[iniX:fimX,fimY-10:fimY]=cor
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
        self.contornaImagem(self.indice_selecao)
        self.show()
    
    def showTexto(self, texto):
        frame = np.zeros([int(self.height*self.proporcao_tela),int(self.width*self.proporcao_tela),3],dtype=np.uint8)
        cv2.putText(frame,texto,self.bottomLeftCornerOfText,self.font,self.fontScale,self.fontColor,self.lineType)

        winname = "image"
        cv2.namedWindow(winname)
        cv2.moveWindow(winname, 120,0)
        cv2.imshow(winname, frame)

            
if __name__ == '__main__':
    gui = UserInterface()
    while True:
        gui.show()
       
        if cv2.waitKey(50)  & 0xFF == ord('q'): #Exit program when the user presses 'q'
            break

    cv2.destroyAllWindows()

