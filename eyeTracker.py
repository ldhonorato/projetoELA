import cv2
import numpy as np
import dlib
from gui import UserInterface
from direcao import Direction
from scipy.spatial import distance as dist

class EyeTrack:
        
    def __init__(self, gui : UserInterface):
        self.detector = dlib.get_frontal_face_detector() #Face detector
        self.predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat") #Landmark identifier. Set the filename to whatever you named the downloaded file
        self.gui = gui

    #Esta função calcula a distância euclidiana entre os pontos verticais e horizontais definidos ao redor dos olhos. 
    #Dessa forma calculamos a área de abertura dos olhos do indivíduo.
    def eye_aspect_ratio(self, eye):
        #compute the euclidean distances between the two sets vertical eye landmarks (x, y)-coordinates
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        # compute the euclidean distance between the horizontal eye landmark (x, y)-coordinates
        C = dist.euclidean(eye[0], eye[3])
        # compute the eye aspect ratio
        ear = (A + B) / (2.0 * C)
        #return the eye aspect ratio
        return ear

    def getCoordenada(self, frame, debug=False):
        #Eyes points
        RIGHT_EYE_POINTS = list(range(36, 42))
        LEFT_EYE_POINTS = list(range(42, 48))
        
        coords = {}
        center_r = []
        center_l = []
        lelc_coord = []
        lerc_coord = []
        relc_coord = []
        rerc_coord = []
        ledn_coord = []
        redn_coord = []
        leup_coord = []
        reup_coord = []
        
        ear_left = 0.0
        ear_right = 0.0
        
        lelc=36 #left eye left cornea
        lerc=39 #left eye rigth cornea
        leup=38 #left eye up cornea
        ledn=40 #left eye down cornea
        
        rerc=45 #rigth eye right cornea
        relc=42 #rigth eye left cornea
        reup=43 #rigth eye up cornea
        redn=47 #rigth eye down cornea
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#a imagem é passada para a escala de cinza 

        faces = self.detector(gray, 1) #Detect the faces in the image
        
        for f in faces:
            
            print("Number of faces detected: {}".format(len(faces))) 
            if len(faces) != 1:
                return coords, frame
                
            print("Detection: Left: {} Top: {} Right: {} Bottom: {}".format(f.left(), f.top(), f.right(), f.bottom()))
                
            x = f.left()
            y = f.top() 
            w = f.right() 
            h = f.bottom() 
            
            #A partir daqui a imagem é recortada no tamanho do retangulo 
            cv2.rectangle(frame, (x, y), (w, h), 255, 2)
            gray = gray[y:h,x:w]
            newf = frame[y:h,x:w]            
            
            # aplicando o clahe na imagem -> Equalização do histograma adaptativo com contraste limitado 
            # CLAHE(Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))#COLOCAR NAS PROPRIEDADES
            clahe_image = clahe.apply(gray)
    
            # detectando a face com o contraste melhorado -> usa a Dlib
            detections = self.detector(clahe_image, 1) #Detect the faces in the image
            
            for d in detections: #For each detected face
                                
                # localizando os landmarks
                shape = self.predictor(clahe_image, d) #Get coordinates

                # o EAR é usando para identificar se o olho está aberto ou fechado
                landmarks = np.matrix([[p.x, p.y] for p in shape.parts()])
                ear_left = self.eye_aspect_ratio(landmarks[LEFT_EYE_POINTS])#left_eye = landmarks[LEFT_EYE_POINTS]
                ear_right = self.eye_aspect_ratio(landmarks[RIGHT_EYE_POINTS])#right_eye = landmarks[RIGHT_EYE_POINTS]
                                
                # essas coordenadas estão no tamanho para a imagem original(sem corte)                
                lelc_coord = [shape.part(lelc).x+x, shape.part(lelc).y+y]# +x/+y is done for absolute value on screen
                lerc_coord = [shape.part(lerc).x+x, shape.part(lerc).y+y]
                
                relc_coord = [shape.part(relc).x+x, shape.part(relc).y+y]
                rerc_coord = [shape.part(rerc).x+x, shape.part(rerc).y+y]
                
                ledn_coord = [shape.part(ledn).x+x, shape.part(ledn).y+y]
                redn_coord = [shape.part(redn).x+x, shape.part(redn).y+y]
                
                leup_coord = [shape.part(leup).x+x, shape.part(leup).y+y]
                reup_coord = [shape.part(reup).x+x, shape.part(reup).y+y]

                if debug:
                    #For each point, draw a red circle with thickness on the original frame
                    #aqui a imagem usada está recortada por isso não se soma +x e +y
                    cv2.circle(newf, (shape.part(lelc).x, shape.part(lelc).y), 1, (0,0,255), thickness=1)
                    cv2.circle(newf, (shape.part(lerc).x, shape.part(lerc).y), 1, (0,0,255), thickness=1)
                
                    cv2.circle(newf, (shape.part(rerc).x, shape.part(rerc).y), 1, (0,0,255), thickness=1) 
                    cv2.circle(newf, (shape.part(relc).x, shape.part(relc).y), 1, (0,0,255), thickness=1)
                
                    cv2.circle(newf, (shape.part(redn).x, shape.part(redn).y), 1, (100,255,0), thickness=1)
                    cv2.circle(newf, (shape.part(ledn).x, shape.part(ledn).y), 1, (255,255,0), thickness=1)
        
                    cv2.circle(newf, (shape.part(reup).x, shape.part(reup).y), 1, (100,255,0), thickness=1)
                    cv2.circle(newf, (shape.part(leup).x, shape.part(leup).y), 1, (255,255,0), thickness=1)

                # extraindo o olho esquerdo
                left_y_coord = shape.part(leup).y+y
                left_x_coord = lelc_coord[0] 
                lefteye = newf[shape.part(leup).y-3:shape.part(ledn).y+3,shape.part(lelc).x+2:shape.part(lerc).x-2]
                
                # extraindo o olho direito               
                right_y_coord = shape.part(reup).y+y
                right_x_coord = relc_coord[0]
                # Região de Interesse (ROI-"Region Of Interest")
                roi = newf[shape.part(reup).y-3:shape.part(redn).y+3,shape.part(relc).x+2:shape.part(rerc).x-2]

                # passando o "lefteye" e "roi" pra escala de cinza
                g_resize = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)                
                left_g_resize = cv2.cvtColor(lefteye,cv2.COLOR_BGR2GRAY)
      
                # mudando o contraste dos olhos -> Melhora o contraste, a distribuição da cor é em todo o range da luminância  
                # cv2.equalizeHist() -> Equalize the histogram of a grayscale image.          
                equ_t = cv2.equalizeHist(g_resize)
                left_equ_t = cv2.equalizeHist(left_g_resize)
                
                equ = cv2.equalizeHist(cv2.add(equ_t, np.array([-70.0])))
                left_equ = cv2.equalizeHist(cv2.add(left_equ_t, np.array([-70.0])))
                
                # extraindo a bola do olho com base na faixa de cores
                # inRange(src, lowerb, upperb, dst)-> keep only the pixels defined by lower and upper bound range
                # Para uma img gray que tem o shape (M,N) em np e tamanho MxN com um único canal no OpenCV, cv2.inRange assume limites escalares.
                thres = cv2.inRange(equ,0,15)
                left_thres = cv2.inRange(left_equ,0,15)
                
                # creating a elliptical Kernel 5x5 and 3x3
                kernel_5x5 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
                kernel_3x3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
                
                #-------------------------------------------------------------------------#
                # dilate() -> removing small noise inside the white image
                # erode() -> decreasing the size of the white region 
                #-------------------------------------------------------------------------#
                
                # appling morphology close / Dilation followed by Erosion -> erosion(dilation())
                closing = cv2.morphologyEx(thres, cv2.MORPH_CLOSE, kernel_5x5, iterations = 1)        
                left_closing = cv2.morphologyEx(left_thres, cv2.MORPH_CLOSE, kernel_5x5, iterations = 1)
                
                # appling morphology open / Erosion followed by Dilation -> dilation(erosion())
                opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel_5x5, iterations = 2)        
                left_opening = cv2.morphologyEx(left_closing, cv2.MORPH_OPEN,kernel_5x5, iterations = 2)

                #appling morphology close / Dilation followed by Erosion -> erosion(dilation())
                closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel_3x3, iterations = 1)        
                left_closing = cv2.morphologyEx(left_opening, cv2.MORPH_CLOSE, kernel_3x3, iterations = 1)
                
                # creating the countor around the eyeball
                # contours é uma lista de todos os contornos da img. Cada contorno individual é uma matriz np de (x,y) coord dos pontos de contorno do obj.
                _, contours, _ = cv2.findContours(closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
                _, lcontours, _ = cv2.findContours(left_closing,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
                
                cx = 0
                cy = 0
                lcx = 0
                lcy = 0
                
                # Momento da imagem é uma média ponderada específica das intensidades de pixel da imagem, 
                # com a ajuda da qual podemos encontrar algumas propriedades específicas de uma imagem, como raio, área, 
                # centróide etc. 
                
        #---------------------calculando o centro do olho direito ------------------------------------------#
                if len(contours)>0:
                    #Find the index of the largest contour
                    areas = [cv2.contourArea(c) for c in contours]
                    max_index = np.argmax(areas)
                    
                    M = cv2.moments(contours[max_index])
                    
                    if M['m00'] != 0: #Se M ["m00"] for diferente de zero, ou seja, quando a segmentação ocorreu perfeitamente.
                        cx = int(M['m10']/M['m00'])
                        cy = int(M['m01']/M['m00'])
                        if debug:
                            #cv2.line(roi,(cx,cy),(cx,cy),(0,0,255),3)
                            cv2.line(roi, (cx - 3,cy), (cx + 3, cy), (0,0,255))
                            cv2.line(roi, (cx,cy - 3), (cx, cy + 3), (0,0,255))
                            
        #---------------------calculando o centro do olho esquerdo ------------------------------------------#
                if len(lcontours)>0:
                    #Find the index of the largest contour
                    areas = [cv2.contourArea(c) for c in lcontours]
                    max_index = np.argmax(areas)
                    
                    M = cv2.moments(lcontours[max_index])
                    
                    if M['m00'] != 0: #Se M ["m00"] for diferente de zero, ou seja, quando a segmentação ocorreu perfeitamente.
                        lcx = int(M['m10']/M['m00'])
                        lcy = int(M['m01']/M['m00'])
                        if debug:
                            #cv2.line(lefteye,(lcx,lcy),(lcx,lcy),(0,0,255),3)
                            cv2.line(lefteye, (lcx - 3, lcy), (lcx + 3, lcy), (0,0,255))
                            cv2.line(lefteye, (lcx, lcy - 3), (lcx, lcy + 3), (0,0,255))

                center_l = [lcx + left_x_coord,lcy + left_y_coord]
                center_r = [cx + right_x_coord,cy + right_y_coord]
            
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
            coords['leup'] = leup_coord
            coords['reup'] = reup_coord
            coords['ear_left'] = ear_left
            coords['ear_right'] = ear_right
            
            return coords, frame

    def distancia_maior_porc(self, dist_1, dist_2, porcento):
        #indica se a dist_1 é tantos porcentos maior que a dist_2 -> return true or false 
        x = (dist_1*100)/dist_2
        return (x-100) >= porcento
        
    def calculateEyeDirection(self, coords): 
        
        #----------------------coordenadas---------------------------------#
        lelc_coord = np.array(coords['lelc'])
        lerc_coord = np.array(coords['lerc'])
        
        relc_coord = np.array(coords['relc'])
        rerc_coord = np.array(coords['rerc'])
        
        center_l = np.array(coords['center_l'])
        center_r = np.array(coords['center_r'])
        
        ledn_coord = np.array(coords['ledn'])
        redn_coord = np.array(coords['redn'])
        
        leup_coord = np.array(coords['leup'])
        reup_coord = np.array(coords['reup'])
        #--------------------------------------------------------------------#
        
        dist_re_rc = ((center_r[0]-rerc_coord[0])**2 + (center_r[1]-rerc_coord[1])**2)**0.5
        dist_re_lc = ((center_r[0]-relc_coord[0])**2 + (center_r[1]-relc_coord[1])**2)**0.5
        dist_re_dn = center_r[1] - redn_coord[1]
        dist_re_up = reup_coord[1] - center_r[1]
        
        
        dist_le_rc = ((center_l[0]-lerc_coord[0])**2 + (center_r[1]-lerc_coord[1])**2)**0.5
        dist_le_lc = ((center_l[0]-lelc_coord[0])**2 + (center_r[1]-lelc_coord[1])**2)**0.5
        dist_le_dn = center_l[1] - ledn_coord[1]
        dist_le_up = leup_coord[1] - center_l[1] 


        direcaoOlho = -1
        if self.distancia_maior_porc(dist_re_lc, dist_re_rc, 50) and self.distancia_maior_porc(dist_le_lc, dist_le_rc, 50):
            direcaoOlho = Direction.DIREITA
        elif self.distancia_maior_porc(dist_re_rc, dist_re_lc, 50) and self.distancia_maior_porc(dist_le_rc, dist_le_lc, 50):
            direcaoOlho = Direction.ESQUERDA 
        elif self.distancia_maior_porc(dist_re_dn, dist_re_up, 50) and self.distancia_maior_porc(dist_le_dn, dist_le_up, 50):
            direcaoOlho = Direction.CIMA
        else:
            direcaoOlho = Direction.CENTRO
            
        return direcaoOlho
    
    def olhoFechado(self, coords):
        threshold = 0.17
        return coords['ear_left'] < threshold and coords['ear_right'] < threshold

    def getEyeDirection(self, coords):
        if self.olhoFechado(coords):
            return Direction.FECHADO
        else:  
            return self.calculateEyeDirection(coords)
            
    def run(self):
        pass
    