from tkinter import *

class message(Frame):
    #globals args
    id = 0
    anchor = ''
    message_text = ''
    message_wiget = None
    text_message = None
    container = None

    def __init__(self, container,id:int, athor:str,message_text:str,input_string_var:StringVar):
        super().__init__(container)

        #initialize args
        self.container = container
        self.id = id
        self.anchor = athor
        self.message_text = message_text
        self.input_string_var = input_string_var

        self.create_wiget()

    def create_wiget(self):
        # create author_label
        author_label = Label(self,text=f"[{self.anchor}]:",width=10)
        author_label.bind("<Button-1>", self.author_label_cliked)
        author_label.bind("<Enter>", self.red_text)
        author_label.bind("<Leave>", self.black_text)
        author_label.grid(row=0, column=0)

        # create text_string_var and label to it
        text_string_var = StringVar()
        text_string_var.set('\n'.join([self.message_text[x:x+85] for x in range (0, len(self.message_text), 85)])) #cut message_text into pieces by size 85
        Label(self, textvariable=text_string_var, width=72, justify=LEFT, anchor=W).grid(row=0, column=1)

        # create edit button
        Button(self, text='edit', command=self.button_clicked).grid(row=0, column=5, sticky=W)

        # assignment
        self.text_string_var = text_string_var
        self.author_label = author_label

    def edit_text(self,new_text:str):
        self.text_string_var.set(new_text);

    def button_clicked(self):
        self.container.edit_message(self.id)
        self.input_string_var.set(self.text_string_var.get())
        print('Information '+self.text_string_var.get())

    def author_label_cliked(self):
        print(self.anchor)

    def red_text(self,event=None):
        self.author_label.config(fg="red")

    def black_text(self,event=None):
        self.author_label.config(fg="black")