import tkinter as tk
import threading
from PIL import ImageTk, Image
import pyttsx3
import webbrowser
import pyautogui
import time


class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.bind("<FocusIn>", self.on_focus_in)
        self.bind("<FocusOut>", self.on_focus_out)

    def on_focus_in(self, e):
        self['background'] = 'blue'

    def on_focus_out(self, e):
        self['background'] = 'black'

class Interface(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        
    def callback(self):
        self.root.quit()

    def run(self):
        self.root = self.create_window("Smart Eye Communicator", "imgs_png/icone_olho.ico", 1350,600)
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        
        #tk.Label(self.root, text="Smart Eye Communicator", bg = "light green", fg = "dark green",font = "Helvetica 30 bold").grid(row=0,column=0, pady=10,columnspan= 3)    
        
        img_hunger,img_thrist,img_itching,img_breath,img_bipap,img_neck_pain,img_pain,img_change_position,img_saliva,img_youtube = self.upload_img()
            
        self.btn_thrist = self.btn_needs(self.root, img_thrist,"Thrist",1,1, lambda: self.speech_assistant("Estou com sede"))
        self.btn_hunger = self.btn_needs(self.root, img_hunger,"Hunger",1,2, lambda: self.speech_assistant("Estou com fome"))
        self.btn_itching = self.btn_needs(self.root, img_itching,"Itching",1,3, lambda: self.speech_assistant("Estou com coceira"))
        self.btn_itching = self.btn_needs(self.root, img_breath,"Shortness of Breath",1,4, lambda: self.speech_assistant("Estou com falta de ar"))
        self.btn_bipap = self.btn_needs(self.root, img_bipap,"Turning BiPAP",1,5, lambda: self.speech_assistant("Preciso do Bi papi"))
        self.btn_neck_pain = self.btn_needs(self.root, img_neck_pain,"Neck Pain",2,1, lambda: self.speech_assistant("Estou com dor no pescoço"))
        self.btn_pain = self.btn_needs(self.root, img_pain,"Pain",2,2, lambda: self.speech_assistant("Estou com dor"))
        self.btn_position = self.btn_needs(self.root, img_change_position,"Change Position",2,3, lambda: self.speech_assistant("Preciso mudar de posição"))
        self.btn_saliva = self.btn_needs(self.root, img_saliva,"Cleanring Saliva",2,4, lambda: self.speech_assistant("Por favor, limpe minha saliva"))
        self.btn_youtube = self.btn_needs(self.root, img_youtube,"Youtube",2,5, lambda: self.playYT())

        self.activateYT = False
        self.root.mainloop()

    def create_window(self, titulo, icone, largura, altura, bg="light green"):
        window = tk.Tk() 
        window.title(titulo)
        window.iconbitmap(icone)
        window.geometry("%dx%d" % (largura, altura))
        window.configure(bg = bg)
        self.center_window(window) 
        return window  
    
    def center_window(self, win):
        win.update_idletasks()
        size = tuple(int(_) for _ in win.geometry().split('+')[0].split('x'))
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = screen_width/2 - size[0]/2
        y = screen_height/2 - size[1]/2
        win.geometry("+%d+%d" % (x, y))
     
    def upload_img(self, width=170, height=170):
        hunger = ImageTk.PhotoImage(Image.open("imgs_png/comida.png").resize((width,height), Image.ANTIALIAS))
        thrist = ImageTk.PhotoImage(Image.open("imgs_png/agua.png").resize((width,height), Image.ANTIALIAS))
        itching = ImageTk.PhotoImage(Image.open("imgs_png/coceira.png").resize((width,height), Image.ANTIALIAS))
        breath = ImageTk.PhotoImage(Image.open("imgs_png/falta_ar.png").resize((width,height), Image.ANTIALIAS))
        bipap = ImageTk.PhotoImage(Image.open("imgs_png/bipap.png").resize((width,height), Image.ANTIALIAS))
        neck_pain = ImageTk.PhotoImage(Image.open("imgs_png/dor_pescoco.png").resize((width,height), Image.ANTIALIAS))
        pain = ImageTk.PhotoImage(Image.open("imgs_png/dor.png").resize((width,height), Image.ANTIALIAS))
        change_position = ImageTk.PhotoImage(Image.open("imgs_png/mudar_posicao.png").resize((width,height), Image.ANTIALIAS))
        saliva = ImageTk.PhotoImage(Image.open("imgs_png/saliva.png").resize((width,height), Image.ANTIALIAS))
        youtube = ImageTk.PhotoImage(Image.open("imgs_png/youtube.png").resize((width,height), Image.ANTIALIAS))
        
        return hunger,thrist,itching,breath,bipap,neck_pain,pain,change_position,saliva,youtube
        
    def btn_needs(self,root, photo, txt, line, column, function):
        return HoverButton(root, image= photo, compound=tk.TOP, text=txt, font = "Helvetica 11 bold",
                         fg="white", bg="black",takefocus=True, activebackground ="red",  
                         padx=5, pady=5, command = function).grid(row=line, column= column, padx=40, pady=40)
  
    def playYT(self, url="https://www.youtube.com"):
        self.speech_assistant("Indo para o iutube")
        try:
            client = webbrowser.get()
            client.open(url)
            self.activateYT = True
            time.sleep(5) 
            for i in range(3):
                pyautogui.press('tab')

            pyautogui.press('enter')

        except webbrowser.Error as e:
            print(e)
        
    def speech_assistant(self, text):
        try:
            engine = pyttsx3.init()
            #rate = engine.getProperty('rate')
            #engine.setProperty('rate', rate+20)
            engine.say(text)
            engine.runAndWait()  
        except RuntimeError:
            pass
    
if __name__ == "__main__":
    gui = Interface()
