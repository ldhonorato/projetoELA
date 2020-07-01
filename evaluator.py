import cv2
import numpy as np
from eyeTracker import EyeTrack
from gui import UserInterface
from direcao import Direction
#--------------------------------------------
import skimage
from skimage.util import random_noise
import sys
    
def dirEnum2Str(direcao):
    dirstr = ""
    if direcao == Direction.DIREITA:
        dirstr = "Direita"
    elif direcao == Direction.ESQUERDA:
        dirstr = "Esquerda"
    elif direcao == Direction.FECHADO:
        dirstr = "Fechado"
    elif direcao == Direction.CIMA:
        dirstr = "Cima"
    elif direcao == Direction.CENTRO:
        dirstr = "Centro"
    elif direcao == Direction.NENHUMA:
        dirstr = "Nenhuma"
    
    return dirstr                 

def noise_sp(frame, amount_x):
    #https://theailearner.com/2019/05/07/add-different-noise-to-an-image/
    noise_img = random_noise(frame, mode='s&p',amount= amount_x)
    noise_img = np.array(255*noise_img, dtype = 'uint8') 
    return noise_img

def noise_gauss(frame, mean_x):
    #https://theailearner.com/2019/05/07/add-different-noise-to-an-image/
    noise_img = random_noise(frame, mode='gaussian',mean = mean_x)
    noise_img = np.array(255*noise_img, dtype = 'uint8') 
    return noise_img
    
def blur(frame, name_blur, kernel_size):
    #https://www.geeksforgeeks.org/opencv-python-program-to-blur-an-image/
   
    # make sure that you have saved it in the same folder 
    # Averaging -> You can change the kernel size as you want 
    if name_blur == 'avging':
        avging = cv2.blur(frame,(kernel_size,kernel_size)) #10x10
        return avging
    
    elif name_blur == 'gaussian':
        # Gaussian Blurring -> Again, you can change the kernel size 
        gausBlur = cv2.GaussianBlur(frame, (kernel_size,kernel_size),0) #5x5
        return gausBlur

def adjust_gamma(frame, gamma=1.0):
    #O gama é o valor relativo de claro e escuro da imagem.
    #adjusted = adjust_gamma(frame, gamma=2.0)#0.3
    #https://stackoverflow.com/questions/33322488/how-to-change-image-illumination-in-opencv-python
    #gamma maior clareia 
    #gamma menor escurece 
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(frame, table)

def rotacao(frame, graus):
    #http://www.galirows.com.br/meublog/opencv-python/opencv2-python27/capitulo1-basico/translacao-rotacao/
    altura, largura = frame.shape[:2]
    ponto = (largura / 2, altura / 2) #ponto no centro da figura
    rotacao = cv2.getRotationMatrix2D(ponto, graus, 1.0)
    rotacionado = cv2.warpAffine(frame, rotacao, (largura, altura))
    return rotacionado
    
def run(pessoa_id):
    ACTION_THRESHOLD = 2
    
    gui = UserInterface(ACTION_THRESHOLD+1)
    eyeTrack = EyeTrack(gui)
    
    pathCalibracao = "Base\\Videos\\"
    video = cv2.VideoCapture(pathCalibracao + "Teste" + str(pessoa_id) + ".mp4")

    writer_vid = cv2.VideoWriter("output" + str(pessoa_id) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"),10, (640, 480), True)
    
    f_csv_tabela = open("output" + str(pessoa_id) + ".csv", 'w')
    f_csv_tabela.write('Vídeo;Frame;Class\n')
    
    frameNumber = 1
    while True:
        print("frame: "+ str(frameNumber))
        
        (grabed, frame) = video.read()
        if not grabed:
            break  
        
        noise = noise_gauss(frame,0.01)
        coords, frame = eyeTrack.getCoordenada(noise, debug=True)
        
        if coords:
            direcao = eyeTrack.getEyeDirection(coords)
            direcaoStr = dirEnum2Str(direcao)

            cv2.putText(frame, str(frameNumber) + " " + direcaoStr, (35, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.25, 
                        (100, 50, 100), 5)
            
            writer_vid.write(frame)
            f_csv_tabela.write(str(pessoa_id) + ';' + str(frameNumber) + ';' + direcaoStr + '\n') 
            
            cv2.imshow("Output", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        
            frameNumber += 1
    
    writer_vid.release()
    video.release()
    f_csv_tabela.close()
            
if __name__ == '__main__':
    for pessoa_id in range(11,12):
        print(pessoa_id)
        run(pessoa_id)


    
    