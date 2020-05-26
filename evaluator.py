import cv2
import time
import numpy as np
from eyeTracker import EyeTrack
from gui import UserInterface
from direcao import Direction
import threading

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
    
    pathCalibracao = "Base\\Videos\\"
    video = cv2.VideoCapture(pathCalibracao + "Teste" + str(pessoa_id) + ".mp4")

    #writer = cv2.VideoWriter("output" + str(pessoa_id) + ".avi", cv2.VideoWriter_fourcc(*"MJPG"), 30, (640, 480), True)
    
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
		                1.25, (100, 50, 100), 5)
            
            #writer.write(frame)
            f_csv.write(str(frameNumber) + ';' + direcaoStr + '\n') 
            
            cv2.imshow("Output", frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        
            frameNumber += 1
    
    #writer.release()
    video.release()
    #f_csv.close()
            
if __name__ == '__main__':
    for pessoa_id in range(1,17):
        print(pessoa_id)
        run(pessoa_id)


    
    