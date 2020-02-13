import cv2
import numpy as np
from direcao import Direction
from win32api import GetSystemMetrics
import pyttsx3
from PIL import Image, ImageDraw, ImageFont

class UserInterface:
    def __init__(self, trackbarSize=3):
        self.font                   = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (100,500)
        self.fontScale              = 1
        self.fontColor              = (255,255,255)
        self.lineType               = 2

        #imagem de água
        agua = cv2.resize(cv2.imread('imgs/agua.jpg'), (256, 226))
        frameTexto = np.zeros([30,256,3],dtype=np.uint8)
        cv2.putText(frameTexto,"Estou com sede",(10,20),self.font,0.8,self.fontColor,self.lineType)
        agua = np.concatenate((agua, frameTexto), axis=0)

        #imagem de comida
        comida = cv2.resize(cv2.imread('imgs/comida.jpg'), (256, 226))
        frameTextoComida = np.zeros([30,256,3],dtype=np.uint8)
        cv2.putText(frameTextoComida,"Estou com fome",(10,20),self.font,0.8,self.fontColor,self.lineType)
        comida = np.concatenate((comida, frameTextoComida), axis=0)

        #imagem de saliva
        saliva = cv2.resize(cv2.imread('imgs/limpar_saliva.jpg'), (256, 226))
        frameTextoSaliva = np.zeros([30,256,3],dtype=np.uint8)
        cv2.putText(frameTextoSaliva,"Limpar saliva",(10,20),self.font,0.8,self.fontColor,self.lineType)
        saliva = np.concatenate((saliva, frameTextoSaliva), axis=0)

        #imagem de pescoco
        pescoco = cv2.resize(cv2.imread('imgs/pescoco.jpg'), (256, 226))
        frameTextoPescoco = np.zeros([30,256,3],dtype=np.uint8)
        cv2.putText(frameTextoPescoco,"Dor no pescoco",(10,20),self.font,0.8,self.fontColor,self.lineType)
        pescoco = np.concatenate((pescoco, frameTextoPescoco), axis=0)

        #imagem de tv
        youtube = cv2.resize(cv2.imread('imgs/youtube.jpg'), (256, 226))
        frameTextoYoutube = np.zeros([30,256,3],dtype=np.uint8)
        cv2.putText(frameTextoYoutube,"Ver Tv",(10,20),self.font,0.8,self.fontColor,self.lineType)
        youtube = np.concatenate((youtube, frameTextoYoutube), axis=0)

        #imagem de coceira
        coceira = cv2.resize(cv2.imread('imgs/coceira.jpg'), (256, 226))
        frameTextoCoceira = np.zeros([30,256,3],dtype=np.uint8)
        cv2.putText(frameTextoCoceira,"Estou com coceira",(10,20),self.font,0.8,self.fontColor,self.lineType)
        coceira = np.concatenate((coceira, frameTextoCoceira), axis=0)

        #imagem dor geral
        dor = cv2.resize(cv2.imread('imgs/dor.jpg'), (256, 226))
        frameTextoDor = np.zeros([30,256,3],dtype=np.uint8)
        cv2.putText(frameTextoDor,"Estou com dor",(10,20),self.font,0.8,self.fontColor,self.lineType)
        dor = np.concatenate((dor, frameTextoDor), axis=0)

        #imagem de mudar de posiçao
        mudar_posicao = cv2.resize(cv2.imread('imgs/mudar_posicao.jpg'), (256, 226))
        frameTextoPosicao = np.zeros([30,256,3],dtype=np.uint8)
        cv2.putText(frameTextoPosicao,"Mudar de posicao",(10,20),self.font,0.8,self.fontColor,self.lineType)
        mudar_posicao = np.concatenate((mudar_posicao, frameTextoPosicao), axis=0)

        #imagem de falta de ar
        falta_ar = cv2.resize(cv2.imread('imgs/falta_de_ar.jpg'), (256, 226))
        frameTextoFaltaDeAr = np.zeros([30,256,3],dtype=np.uint8)
        cv2.putText(frameTextoFaltaDeAr,"Falta de ar",(10,20),self.font,0.8,self.fontColor,self.lineType)
        falta_ar = np.concatenate((falta_ar, frameTextoFaltaDeAr), axis=0)

        #imagem de bpap
        bpap = cv2.resize(cv2.imread('imgs/bpap.jpg'), (256, 226))
        frameTextoBPAP = np.zeros([30,256,3],dtype=np.uint8)
        cv2.putText(frameTextoBPAP,"bpap",(10,20),self.font,0.8,self.fontColor,self.lineType)
        bpap = np.concatenate((bpap, frameTextoBPAP), axis=0)

        image_linha1 = np.concatenate((agua, comida, saliva, pescoco, youtube), axis=1)
        image_linha2 = np.concatenate((coceira, dor, mudar_posicao, falta_ar, bpap), axis=1)

        self.frases = ["água, por favor", "estou com fome", "limpe minha saliva", "meu pescoço doi", "quero ver tv", "Estou com coceira", "estou com dor", "quero mudar de posição", "estou com falta de ar", "ligue o bi pap"]

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
        self.engine = pyttsx3.init()
        self.trackbarSize = trackbarSize
    
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
    
    def showQuadradoCalibracao(self, direcao):
        frame = np.zeros([int(self.height*self.proporcao_tela),int(self.width*self.proporcao_tela),3],dtype=np.uint8)           
        
        if direcao == Direction.CENTRO:
            frame = cv2.imread('imgs/alvo.png')
        elif direcao == Direction.DIREITA:
            frame = cv2.imread('imgs/telaSetaDireita.png')
        elif direcao ==  Direction.ESQUERDA:
            frame = cv2.imread('imgs/telaSetaEsquerda.png')
        elif direcao == Direction.CIMA:
            frame = cv2.imread('imgs/telaSetaCima.png')

        winname = "image"
        cv2.namedWindow(winname)
        cv2.moveWindow(winname, 120,0)
        cv2.imshow(winname, frame)
    
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
        # gui.showQuadradoCalibracao(Direction.DIREITA)
       
        if cv2.waitKey(50)  & 0xFF == ord('q'): #Exit program when the user presses 'q'
            break

    cv2.destroyAllWindows()

