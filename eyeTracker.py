import cv2
import numpy as np
import dlib
import timeit
import math
from gui import UserInterface
from direcao import Direction
from math import hypot
# from videocaptureasync import VideoCaptureAsync

class EyeTrack:
    def __init__(self, gui : UserInterface):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
        self.detector = dlib.get_frontal_face_detector() #Face detector
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") #Landmark identifier. Set the filename to whatever you named the downloaded file

        # self.threshold_esquerda = 0.4
        self.threshold = 2
        # self.vid = VideoCaptureAsync(0)
        self.vid = cv2.VideoCapture(0)

        self.gui = gui

        self.calibracao = {}
        
    def startVideoCapture(self):
        self.vid.start()
    
    def stopVideoCapture(self):
        self.vid.stop()
    
    def getFrame(self):
        return self.vid.read()
    
    def updateCalibracao(self, calibracao):
        self.calibracao = calibracao

    def midpoint(self, p1 ,p2):
        return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

    def get_blinking_ratio(self, eye_points, facial_landmarks):
        left_point = (facial_landmarks.part(eye_points[0]).x, facial_landmarks.part(eye_points[0]).y)
        right_point = (facial_landmarks.part(eye_points[3]).x, facial_landmarks.part(eye_points[3]).y)
        center_top = self.midpoint(facial_landmarks.part(eye_points[1]), facial_landmarks.part(eye_points[2]))
        center_bottom = self.midpoint(facial_landmarks.part(eye_points[5]), facial_landmarks.part(eye_points[4]))

        # hor_line = cv2.line(frame, left_point, right_point, (0, 255, 0), 2)
        # ver_line = cv2.line(frame, center_top, center_bottom, (0, 255, 0), 2)

        hor_line_lenght = hypot((left_point[0] - right_point[0]), (left_point[1] - right_point[1]))
        ver_line_lenght = hypot((center_top[0] - center_bottom[0]), (center_top[1] - center_bottom[1]))

        ratio = hor_line_lenght / (ver_line_lenght + 0.000001)
        return ratio

    def capturarCoordenadas(self, numFrames=10, delay_ms=100, debug=False):
        """
        Encontra as coordenadas do centro do olho esquerdo

        Parameters:
        numFrames (int): número de iterações da função, i.e. quantidade de coordenadas x,y a serem retornadas
        delay_ms (int): delay em ms entre as interações

        Return:
        list: retorna a média das coordenadas [x,y] do centro do olho esquerdo
        """
        coords = {}
        center_r = []
        center_l = []
        lelc_coord = []
        lerc_coord = []
        relc_coord = []
        rerc_coord = []
        ledn_coord = []
        redn_coord = []
        blink_ratio = []
        
        start = timeit.default_timer()

        lelc=36
        leup=38
        ledn=41
        lerc=39
        rerc=45
        reup=44
        redn=47
        relc=42

        # landmarksDetected = False

        for _ in range(numFrames):
            _, frame = self.vid.read()
            
            frame = cv2.flip(frame,1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) != 1:
                return coords, frame
            
            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
                gray=gray[y:y+h,x:x+w]
                newf=frame[y:y+h,x:x+w]
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                clahe_image = clahe.apply(gray)
        
                detections = self.detector(clahe_image, 1) #Detect the faces in the image
                
                for d in detections: #For each detected face
                    
                    shape = self.predictor(clahe_image, d) #Get coordinates
                    left_eye_ratio = self.get_blinking_ratio([36, 37, 38, 39, 40, 41], shape)
                    right_eye_ratio = self.get_blinking_ratio([42, 43, 44, 45, 46, 47], shape)
                    
                    blink_ratio.append([left_eye_ratio, right_eye_ratio])
                    lelc_coord.append([shape.part(lelc).x+x, shape.part(lelc).y+y])
                    lerc_coord.append([shape.part(lerc).x+x, shape.part(lerc).y+y])
                    relc_coord.append([shape.part(relc).x+x, shape.part(relc).y+y])
                    rerc_coord.append([shape.part(rerc).x+x, shape.part(rerc).y+y])
                    ledn_coord.append([shape.part(ledn).x+x, shape.part(ledn).y+y])
                    redn_coord.append([shape.part(redn).x+x, shape.part(redn).y+y])

                    if debug:
                        # left eye corners
                        cv2.circle(newf, (shape.part(lelc).x, shape.part(lelc).y), 1, (0,0,255), thickness=1)
                        cv2.circle(newf, (shape.part(lerc).x, shape.part(lerc).y), 1, (0,0,255), thickness=1)
                        cv2.circle(newf, (shape.part(rerc).x, shape.part(rerc).y), 1, (255,0,255), thickness=1) #For each point, draw a red circle with thickness2 on the original frame
                        cv2.circle(newf, (shape.part(relc).x, shape.part(relc).y), 1, (0,255,0), thickness=1)
                        # cv2.circle(newf, (shape.part(reup).x, shape.part(reup).y), 1, (100,255,0), thickness=1)
                        cv2.circle(newf, (shape.part(redn).x, shape.part(redn).y), 1, (100,255,0), thickness=1)
                        # cv2.circle(newf, (shape.part(leup).x, shape.part(leup).y), 1, (255,255,0), thickness=1)
                        cv2.circle(newf, (shape.part(ledn).x, shape.part(ledn).y), 1, (255,255,0), thickness=1)


                    #-------- making left eye configuration --------------------------#
                    lefleftcorn_x_axis=shape.part(lelc).x+x # +x is done for absolute value on screen
                    lefrigtcorn_x_axis=shape.part(lerc).x+x # +x is done for absolute value on screen
                    leftup_y_axis=shape.part(leup).y+y
                    leftdn_y_axis=shape.part(ledn).y+y
                    
                    # extracting the right eye
                    right_y_coord = shape.part(reup).y + y
                    right_x_coord = shape.part(relc).x + x
                    roi = newf[shape.part(reup).y-3:shape.part(redn).y+3,shape.part(relc).x+2:shape.part(rerc).x-2]
                    # resize = cv2.resize(roi, (0,0), fx=1, fy=1)

                    # extracting the left eye
                    left_y_coord = leftup_y_axis
                    left_x_coord = lefleftcorn_x_axis
                    lefteye = frame[leftup_y_axis:leftdn_y_axis,lefleftcorn_x_axis:lefrigtcorn_x_axis]
                    # converting to gray scale image
                    g_resize=cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
                    left_g_resize=cv2.cvtColor(lefteye,cv2.COLOR_BGR2GRAY)
                    # changing the contrast of the right eye 
                    equ = cv2.equalizeHist(g_resize)
                    left_equ=cv2.equalizeHist(left_g_resize)
                    # extracting the eye ball based on color range
                    thres=cv2.inRange(equ,0,15)
                    left_thres=cv2.inRange(left_equ,0,15)
                    # creating a kernel of 3x3
                    kernel = np.ones((5,5),np.uint8)
                    #/------- removing small noise inside the white image ---------/#
                    dilation = cv2.dilate(thres,kernel,iterations = 4)
                    left_dilation = cv2.dilate(left_thres,kernel,iterations = 4)
                    #/------- decreasing the size of the white region -------------/#
                    erosion = cv2.erode(dilation,kernel,iterations = 2)            
                    left_erosion = cv2.erode(left_dilation,kernel,iterations = 2) 
                    # creating the countor around the eyeball
                    _, contours, _ = cv2.findContours(erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
                    _, lcontours, _ = cv2.findContours(left_erosion,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
                    cx = 0
                    cy = 0
                    lcx = 0
                    lcy = 0
                    if len(contours)==2 or len(contours)==1:
                        M = cv2.moments(contours[0])
                        if M['m00']!=0:
                            cx = int(M['m10']/M['m00'])
                            cy = int(M['m01']/M['m00'])
                            if debug:
                                cv2.line(roi,(cx,cy),(cx,cy),(0,0,255),3)
                    #--------countor for left eye ------------------------------------------#
                    if len(lcontours)==2 or len(lcontours)==1:
                        M = cv2.moments(lcontours[0])
                        if M['m00']!=0:
                            lcx = int(M['m10']/M['m00'])
                            lcy = int(M['m01']/M['m00'])
                            if debug:
                                cv2.line(lefteye,(lcx,lcy),(lcx,lcy),(0,0,255),3)

                    center_l.append([lcx + left_x_coord,lcy + left_y_coord])
                    center_r.append([cx + right_x_coord,cy + right_y_coord])
            
            if timeit.default_timer()-start>2:
                break
            cv2.waitKey(delay_ms)
        
        center_l = np.mean(center_l,axis=0)
        center_r = np.mean(center_r,axis=0)

        lelc_coord = np.mean(lelc_coord,axis=0)
        lerc_coord = np.mean(lerc_coord,axis=0)
        relc_coord = np.mean(relc_coord,axis=0)
        rerc_coord = np.mean(rerc_coord,axis=0)
        ledn_coord = np.mean(ledn_coord,axis=0)
        redn_coord = np.mean(redn_coord,axis=0)
        blink_ratio = np.mean(blink_ratio, axis=0)

        if not debug:
            frame = 0
        
        coords['center_l'] = center_l
        coords['center_r'] = center_r
        coords['lelc'] = lelc_coord
        coords['lerc'] = lerc_coord
        coords['relc'] = relc_coord
        coords['rerc'] = rerc_coord
        coords['ledn'] = ledn_coord
        coords['redn'] = redn_coord
        coords['blink'] = blink_ratio
        
        # coord_ret = coords
        for k in coords:
            if (not isinstance(coords[k], np.ndarray)) or (len(coords[k]) != 2):
                coords = {} #nao sei pq mas algumas vezes náo pega as duas coordenadas
                break

        return coords, frame
        # return coords, cv2.flip(frame,1)

    def calculateDistancesLR(self, coords):
        lelc_coord = np.array(coords['lelc'])
        lerc_coord = np.array(coords['lerc'])
        center_l = np.array(coords['center_l'])
        relc_coord = np.array(coords['relc'])
        rerc_coord = np.array(coords['rerc'])
        center_r = np.array(coords['center_r'])

        dist_re_rc = ((center_r[0]-rerc_coord[0])**2 + (center_r[1]-rerc_coord[1])**2)**0.5
        dist_re_lc = ((center_r[0]-relc_coord[0])**2 + (center_r[1]-relc_coord[1])**2)**0.5
        
        dist_le_rc = ((center_l[0]-lerc_coord[0])**2 + (center_r[1]-lerc_coord[1])**2)**0.5
        dist_le_lc = ((center_l[0]-lelc_coord[0])**2 + (center_r[1]-lelc_coord[1])**2)**0.5

        dist_r = dist_re_rc - dist_re_lc
        dist_l = dist_le_rc - dist_le_lc

        return dist_r, dist_l

    def calculateDistancesUD(self, coords):
        center_l = np.array(coords['center_l'])
        center_r = np.array(coords['center_r'])

        ledn_coord = np.array(coords['ledn'])
        redn_coord = np.array(coords['redn'])
        
        dist_l_dn = ledn_coord[1] - center_l[1] 
        dist_r_dn = redn_coord[1] - center_r[1]
        
        return dist_l_dn, dist_r_dn
    
    def calculateEyeDirectionLR(self, currentDistance, eye=0):
        ############ Calibracoes ############
        if not self.calibracao:
            return -1 #empty calibration

        calibracaoCentro = self.calibracao["centro"]
        calibracaoDireita = self.calibracao["direita"]
        calibracaoEsquerda = self.calibracao["esquerda"]

        cal_centro_eye = calibracaoCentro[eye]
        cal_esquerda_eye = calibracaoDireita[eye]
        cal_direita_eye = calibracaoEsquerda[eye]

        cal_maior = max([cal_centro_eye, cal_esquerda_eye, cal_direita_eye])
        cal_menor = min([cal_centro_eye, cal_esquerda_eye, cal_direita_eye])

        cal_size = cal_maior - cal_menor
        limite_direita = cal_menor + 0.2*cal_size
        limite_esquerda = cal_menor + 0.8*cal_size

        direcaoOlho = -1
        if currentDistance < limite_direita:
            direcaoOlho = Direction.DIREITA
        elif currentDistance > limite_esquerda:
            direcaoOlho = Direction.ESQUERDA
        else:
            direcaoOlho = Direction.CENTRO
        
        # print("==========================================================")
        # print("Eye = ", eye)
        # print("Calibracao = %f | %f | %f" % (cal_centro_eye, cal_esquerda_eye, cal_direita_eye))
        # print("limites = %f | %f " % (limite_direita, limite_esquerda))
        # print("distanciaAtual = ", currentDistance)
        # print("Direcao = ", direcaoOlho)

        return direcaoOlho
    
    def calculateEyeDirectionUD(self, currentDistance, eye=0):
        ############ Calibracoes ############
        if not self.calibracao:
            return -1 #empty calibration

        coordenadasCima = self.calibracao["cima"]
        coordenadasBaixo = self.calibracao["baixo"]
        
        cal_cima_eye = coordenadasCima[eye]
        cal_baixo_eye = coordenadasBaixo[eye]
        
        cal_size = cal_baixo_eye - cal_cima_eye
        limite_cima = cal_cima_eye + 0.2*cal_size
        limite_baixo = cal_cima_eye + 0.8*cal_size

        direcaoOlho = -1
        if currentDistance < limite_baixo:
            direcaoOlho = Direction.BAIXO
        elif currentDistance > limite_cima:
            direcaoOlho = Direction.CIMA
        else:
            direcaoOlho = Direction.CENTRO
        
        # print("==========================================================")
        # print("Eye = ", eye)
        # print("Calibracao = %f | %f | %f" % (cal_centro_eye, cal_esquerda_eye, cal_direita_eye))
        # print("limites = %f | %f " % (limite_direita, limite_esquerda))
        # print("distanciaAtual = ", currentDistance)
        # print("Direcao = ", direcaoOlho)

        return direcaoOlho

    def olhoFechado(self, coords):
        limitesFechado = np.array(self.calibracao['fechado'])
        aberturaOlho = np.array(coords['blink'])
        
        aberturaOlho = aberturaOlho > (0.8*limitesFechado)

        return np.all(aberturaOlho)

        

    def getEyeDirection(self, coords):
        
        if self.olhoFechado(coords):
            return Direction.FECHADO
            
        dist_r, dist_l = self.calculateDistancesLR(coords)

        direcaoOlhoDireito = self.calculateEyeDirectionLR(dist_r, 0)
        direcaoOlhoEsquerdo = self.calculateEyeDirectionLR(dist_l, 1)

        if direcaoOlhoDireito == direcaoOlhoEsquerdo:
            if direcaoOlhoDireito == Direction.ESQUERDA or direcaoOlhoDireito == Direction.DIREITA:
                return direcaoOlhoDireito
            
            dist_l_dn, _ = self.calculateDistancesUD(coords)
            direcaoUDolhoDireito = self.calculateEyeDirectionUD(dist_l_dn, eye=1)

            return direcaoUDolhoDireito
        else:
            return Direction.NENHUMA

    def run(self):
        pass

if __name__ == '__main__':
    eyeTrack = EyeTrack(None)
    while True:
        coords, frame = eyeTrack.capturarCoordenadas(numFrames=1, debug=True)

        if coords:
            #print(coords)
            dist_l_dn, dist_r_dn = eyeTrack.calculateDistancesUD(coords)
            print(dist_r_dn)
            print(eyeTrack.getEyeDirection(coords))
            # print(coords)
            # y_le = coords['center_l'][1] - (coords['lelc'][1]+coords['lerc'][1])/2
            # y_re = coords['center_r'][1] - (coords['relc'][1]+coords['rerc'][1])/2
            # print(y_le, y_re)
        # print(coords)
        # if coords:
        #      direcao = eyeTrack.getEyeDirection(coords)
        cv2.imshow("image", frame) #Display the frame for debug
        if cv2.waitKey(10) & 0xFF == ord('q'): #Exit program when the user presses 'q'
            break
