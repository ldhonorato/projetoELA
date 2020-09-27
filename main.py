from eyeTracker import EyeTrack
from direcao import Direction
from videocaptureasync import VideoCaptureAsync 
import pyautogui
import pyttsx3
from gui import Interface

if __name__ == '__main__':   
    
    eyeTrack = EyeTrack()
    int2Text = ['zero', 'um', 'dois', 'tres', 'quatro', 'cinco']
    contadorOlhosFechados = 0
    
    gui = Interface()
    gui.speech_assistant('Olá estou aqui para ajudar você a expressar algumas necessidades.  Por favor, olhe em direção ao cartão que expressa a sua necessidade')
    video = VideoCaptureAsync(0) 
    video.start()

    pyautogui.press('tab')

    while True:
        (grabed, frame) = video.read() 
        if not grabed:
            break
        
        coords,frame = eyeTrack.getCoordenada(frame,debug=False)
                    
        if coords:
            direcao = eyeTrack.getEyeDirection(coords)
    
            if direcao == Direction.DIREITA:    
                gui.speech_assistant('direita')
                pyautogui.press('tab')
                
            elif direcao == Direction.ESQUERDA:
                gui.speech_assistant('esquerda')
                pyautogui.hotkey('shift', 'tab')
                
            elif direcao == Direction.CIMA:
                gui.speech_assistant('cima')
                if gui.activateYT:
                    pyautogui.press('enter')                    
                else:
                    pyautogui.press('space')                    
                
            elif direcao == Direction.FECHADO:
                if contadorOlhosFechados == 0:
                    gui.speech_assistant("Olhos fechados")
                else:
                    gui.speech_assistant(int2Text[contadorOlhosFechados])
                    
                if contadorOlhosFechados == 3:
                    gui.speech_assistant('Saindo do programa')  
                    gui.root.destroy()
                    break
                     
                contadorOlhosFechados += 1              
                
    video.stop()
