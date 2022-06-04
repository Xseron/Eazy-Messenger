from tkinter import *
from tkinter.scrolledtext import ScrolledText
from message_frames import message
import client
import threading

from PIL import Image, ImageTk

class main_screen(Tk):
    #lol
    author_logo_label = None
    author_name_string_var = None
    input_string_var = None
    messages_box = None
    send_button = None
    edit_id = 0
    name = ''
    frame_array = []
    messages = []

    def __init__(self,name:str):
        super().__init__()
        self.name = name
        self.cl = client.Client(name,self)
        threading.Thread(self.cl.start()).start()
        # configure columns and rows
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=4)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=13)
        self.rowconfigure(3, weight=1)

        self.create_widgets()

        # not allowed to expand
        self.resizable(0, 0)

    def resize_logo_photo(self,logoPath:str,width=124,hight=124):
        # resize image to width and hight
        MAX_SIZE = (width, hight)
        image = Image.open(logoPath)
        image.thumbnail(MAX_SIZE)
        image.save('./res/logo_compl.png')
        return ImageTk.PhotoImage(image)

    def create_navigation_bar(self):
        # create author_logo_label
        author_logo_image = self.resize_logo_photo(r"./res/logo.jpg", 124, 124)
        author_logo_label = Label(image=author_logo_image)
        author_logo_label.image = author_logo_image
        author_logo_label.grid(row=0, column=0, columnspan=2, sticky=NW)

        # create author_name_label
        author_name_string_var = StringVar()
        author_name_string_var.set(self.name)
        author_name_label = Label(textvariable=author_name_string_var, font=("Arial", 12))
        author_name_label.grid(row=1, column=0, sticky=NW)

        # create edit profile button
        sendBtn = Button(self, text="Edit")
        sendBtn.grid(row=1, column=1, sticky=NE)

        # assignment
        self.author_logo_label = author_logo_label
        self.author_name_string_var = author_name_string_var

    def create_widgets(self):
        self.create_navigation_bar()

        # create messages_box
        messages_box = ScrolledText(self, width=77,state=DISABLED)
        messages_box.grid(row=0, column=2, columnspan=2,rowspan=3,sticky=NE)

        # create input_string_var
        input_string_var = StringVar()
        inp = Entry(textvariable=input_string_var, width=80)
        inp.grid(row=3, column=2)

        # create send button
        send_button = Button(self, text="send", command=self._send_btn_down, width=21)
        send_button.grid(row=3, column=3)

        # assignment
        self.send_button = send_button
        self.input_string_var = input_string_var
        self.messages_box = messages_box

    def edit_message(self,id:int):
        self.edit_id = id
        self.send_button.config(text='Edit',command=self._endit_btn_down)

    def _endit_btn_down(self):
        t = self.frame_array[self.edit_id]
        t.edit_text(self.input_string_var.get())
        self.send_button.config(text='Send', command=self._send_btn_down)
        self.input_string_var.set('')

    def _send_btn_down(self):
        text = self.input_string_var.get()
        self.input_string_var.set('')
        self.cl.client_send(text)

    def send_message(self,name:str,text_massage:str):
        text_massage = text_massage.strip()
        if text_massage!='':
            self.cl.client_send(text_massage)
            frame = message(self,len(self.frame_array),name,text_massage,self.input_string_var)
            self.frame_array.append(frame)
            self.messages_box.window_create(END, window=frame)
            self.messages_box.insert(END, '\n')
