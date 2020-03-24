import cv2
import numpy as np
from eyeTracker import EyeTrack
from calibrator import Calibrator
from gui import UserInterface
from direcao import Direction
import threading


def calibrar(eyeTrack, path, id):
    #==================================================================
    #------------------------COORDENADAS CENTRO------------------------
    #==================================================================
    imgCentro = path + "Centro" + str(id) + ".jpg"
    img = cv2.imread(imgCentro)
    coordenadasCentro, img = eyeTrack.getCoordenada(img, debug=False)
    if not coordenadasCentro:
        print("Problema na coordenada centro")
        return -1
    blinkRatio_open = coordenadasCentro['blink']
    coordenadasCentro = eyeTrack.calculateDistancesLR(coordenadasCentro)

    #==================================================================
    #------------------------COORDENADAS DIREITA-----------------------
    #==================================================================
    imgDireita = path + "Direita" + str(id) + ".jpg"
    img = cv2.imread(imgDireita)
    coordenadasDireita, img = eyeTrack.getCoordenada(img, debug=False)
    if not coordenadasDireita:
        print("Problema na coordenada direita")
        return -1
    coordenadasDireita = eyeTrack.calculateDistancesLR(coordenadasDireita)
    
    #==================================================================
    #-----------------------COORDENADAS ESQUERDA-----------------------
    #==================================================================
    imgEsquerda = path + "Esquerda" + str(id) + ".jpg"
    img = cv2.imread(imgEsquerda)
    coordenadasEsquerda, img = eyeTrack.getCoordenada(img, debug=False)
    if not coordenadasEsquerda:
        print("Problema na coordenada esquerda")
        return -1
    coordenadasEsquerda = eyeTrack.calculateDistancesLR(coordenadasEsquerda)

    #==================================================================
    #-----------------------COORDENADAS CIMA---------------------------
    #==================================================================
    imgCima = path + "Cima" + str(id) + ".jpg"
    img = cv2.imread(imgCima)
    coordenadasCima, img = eyeTrack.getCoordenada(img, debug=False)
    if not coordenadasCima:
        print("Problema na coordenada cima")
        return -1
    coordenadasCima = eyeTrack.calculateDistancesUD(coordenadasCima)
    
    #==================================================================
    #-----------------------COORDENADAS BAIXO--------------------------
    #==================================================================
    imgBaixo = path + "Baixo" + str(id) + ".jpg"
    img = cv2.imread(imgBaixo)
    coordenadasBaixo, img = eyeTrack.getCoordenada(img, debug=False)
    if not coordenadasBaixo:
        print("Problema na coordenada baixo")
        return -1
    blinkRatio_close = coordenadasBaixo['blink']
    coordenadasBaixo = eyeTrack.calculateDistancesUD(coordenadasBaixo)
    
    
    calibracao = { "centro": coordenadasCentro,
                    "direita": coordenadasDireita,
                    "esquerda": coordenadasEsquerda,
                    "cima": coordenadasCima,
                    "baixo": coordenadasBaixo,
                    "aberto": blinkRatio_open,
                    "fechado": blinkRatio_close
                }
   
    return calibracao


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
                    

def run(pessoa_id):
    ACTION_THRESHOLD = 2
    
    gui = UserInterface(ACTION_THRESHOLD+1)
    eyeTrack = EyeTrack(gui)

    pathCalibracao = "Base\\Imagens\\"
    print(pathCalibracao)
    calibracao = calibrar(eyeTrack, pathCalibracao, pessoa_id)
    print("Calibracao: ", calibracao)
    eyeTrack.updateCalibracao(calibracao)

    
    pathCalibracao = "Base\\Videos\\"
    video = cv2.VideoCapture(pathCalibracao + "Teste" + str(pessoa_id) + ".mp4")

    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    writer = cv2.VideoWriter("output" + str(pessoa_id) + ".avi", fourcc, 30, (640, 480), True)
    f_csv = open("output" + str(pessoa_id) + ".csv", 'w')
    f_csv.write('Frame;Class\n')
    frameNumber = 1
    while True:
        (grabed, frame) = video.read()
        if not grabed:
            break

        coords, frame = eyeTrack.getCoordenada(frame, debug=True)
        if coords:
            direcao = eyeTrack.getEyeDirection(coords)
            direcaoStr = dirEnum2Str(direcao)

            cv2.putText(frame, str(frameNumber) + " " + direcaoStr, (35, 50), cv2.FONT_HERSHEY_SIMPLEX,
		                1.25, (0, 255, 0), 5)
            
            writer.write(frame)
            f_csv.write(str(frameNumber) + ';' + direcaoStr + '\n') 
            
            cv2.imshow("Output", frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
            frameNumber += 1
    
    writer.release()
    video.release()
    f_csv.close()
            

if __name__ == '__main__':
    for pessoa_id in range(7, 11):
        print(pessoa_id)
        run(pessoa_id)


    # coordenadasCentro, img = eyeTrack.getCoordenada(centro1, debug=True)
    # print(coordenadasCentro)
    
    
    # cv2.imshow('image',img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()