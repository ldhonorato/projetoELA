import cv2
import numpy as np
import dlib
import timeit
import math
from gui import UserInterface
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
        
    def startVideoCapture(self):
        self.vid.start()
    
    def stopVideoCapture(self):
        self.vid.stop()
    
    def getFrame(self):
        return self.vid.read()
    
    def updateCalibracao(self, calibracao):
        pass

    def capturarCoordenadas(self, numFrames=10, delay_ms=100, debug=False):
        """
        Encontra as coordenadas do centro do olho esquerdo

        Parameters:
        numFrames (int): número de iterações da função, i.e. quantidade de coordenadas x,y a serem retornadas
        delay_ms (int): delay em ms entre as interações

        Return:
        list: retorna a média das coordenadas [x,y] do centro do olho esquerdo
        """
        center_r = []
        center_l = []
        lelc_coord = []
        lerc_coord = []
        relc_coord = []
        rerc_coord = []
        
        start = timeit.default_timer()

        lelc=36
        leup=38
        ledn=41
        lerc=39
        rerc=45
        reup=44
        redn=47
        relc=42

        for _ in range(numFrames):
            _, frame = self.vid.read()
            
            frame = cv2.flip(frame,1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            if(len(faces) > 1):
                break
            
            for (x,y,w,h) in faces:
                #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),1)
                gray=gray[y:y+h,x:x+w]
                newf=frame[y:y+h,x:x+w]
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                clahe_image = clahe.apply(gray)
        
                detections = self.detector(clahe_image, 1) #Detect the faces in the image
        
                for _,d in enumerate(detections): #For each detected face
                    
                    shape = self.predictor(clahe_image, d) #Get coordinates
                    
                    lelc_coord.append([shape.part(lelc).x+x, shape.part(lelc).y+y])
                    lerc_coord.append([shape.part(lerc).x+x, shape.part(lerc).y+y])
                    relc_coord.append([shape.part(relc).x+x, shape.part(relc).y+y])
                    rerc_coord.append([shape.part(rerc).x+x, shape.part(rerc).y+y])
                    if debug:
                        # left eye corners
                        cv2.circle(newf, (shape.part(lelc).x, shape.part(lelc).y), 1, (0,0,255), thickness=1)
                        cv2.circle(newf, (shape.part(lerc).x, shape.part(lerc).y), 1, (0,0,255), thickness=1)
                        cv2.circle(newf, (shape.part(rerc).x, shape.part(rerc).y), 1, (0,0,255), thickness=1) #For each point, draw a red circle with thickness2 on the original frame
                        cv2.circle(newf, (shape.part(relc).x, shape.part(relc).y), 1, (0,0,255), thickness=1)

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

        if not debug:
            frame = 0
        
        coords = {}
        
        coords['center_l'] = center_l
        coords['center_r'] = center_r
        coords['lelc'] = lelc_coord
        coords['lerc'] = lerc_coord
        coords['relc'] = relc_coord
        coords['rerc'] = rerc_coord

        for k in coords:
            if math.isnan(coords[k]):
                coords[k] = 0

        return coords, frame
    
    def getEyeDirection(self, coords):
        
        #----------------Verifica direcao olho esquerdo------------------#
        direcao_esquerda = -1
        
        lelc_coord = np.array(coords['lelc'])
        lerc_coord = np.array(coords['lerc'])
        center_l = np.array(coords['center_l'])
        relc_coord = np.array(coords['relc'])
        rerc_coord = np.array(coords['rerc'])
        center_r = np.array(coords['center_r'])

        le_size = lerc_coord[0] - lelc_coord[0]
        le_pos = center_l[0] - lelc_coord[0]
        le = le_pos/le_size

        re_size = rerc_coord[0] - relc_coord[0]
        re_pos = center_r[0] - relc_coord[0]
        re = re_pos/re_size

        print('re =',re)
        print('le =',le)

        le_size = lerc_coord[0] - lelc_coord[0]
        le_pos = lerc_coord[0] - center_l[0]
        le = le_pos/le_size

        re_size = rerc_coord[0] - relc_coord[0]
        re_pos = rerc_coord[0] -  center_r[0]
        re = re_pos/re_size

        print('re2 =',re)
        print('le2 =',le)

        #dist1 = np.linalg.norm(lelc_coord, center_l)
        # dist1 = ((lelc_coord[0][0]-center_l[0][0])**2 + (lelc_coord[0][1]-center_l[0][1])**2)**0.5
        #dist2 = np.linalg.norm(lerc_coord, center_l)
        # dist2 = ((lerc_coord[0][0]-center_l[0][0])**2 + (lerc_coord[0][1]-center_l[0][1])**2)**0.5
        # dist_div = dist1/dist2
        
        # print('dist1=', dist1)
        # print('dist2=', dist2)

        # print('dist1/dist2=', dist_div)
        # diferenca_y1 = lelc_coord[0][1] - center_l[0][1]
        # diferenca_y2 = lerc_coord[0][1] - center_l[0][1]
        # # if diferenca_y1 > 10 or diferenca_y2 > 10:
        # #     # print('Baixo')
        # #     direcao = EyeDirection.BAIXO
        # if dist_div > self.threshold:
        #     print('DIREITA')
        #     direcao_esquerda = EyeDirection.DIREITA
        # else:
        #     if dist_div < 1:
        #         dist_div = dist2/dist1
        #         print('dist2/dist1=', dist_div)
        #     if dist_div > self.threshold:
        #         print('ESQUERDA')
        #         direcao_esquerda = EyeDirection.ESQUERDA
        #     else:
        #         print('CENTRO')
        #         direcao_esquerda = EyeDirection.CENTRO
            
        return direcao_esquerda

    def run(self):
        pass

if __name__ == '__main__':
    eyeTrack = EyeTrack(None)
    while True:
        coords, frame = eyeTrack.capturarCoordenadas(numFrames=2, debug=True)
        print(coords)
        # if len(coords['center_l']) != 0:
        #     direcao = eyeTrack.getEyeDirection(coords)
        cv2.imshow("image", frame) #Display the frame for debug
        if cv2.waitKey(100) & 0xFF == ord('q'): #Exit program when the user presses 'q'
            break
