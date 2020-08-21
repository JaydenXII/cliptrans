from googletrans import Translator
from pyperclip import paste, copy
from threading import Thread
from time import sleep
from tkinter import (BooleanVar, Button, END, Entry, Frame, INSERT, LEFT,
    Menu, RIGHT, Scrollbar, StringVar, Text, Tk, TOP, VERTICAL, Y)

__author__ = "JaydenXII"
__version__ = "0.2.2"

class MainFrame(Tk):

    all_language = [
        ("English", "en"),
        ("Chinese(中文)", "zh-cn"),
        ("Dutch(Duitse)", "nl"),
        ("Japanese(日本語)", "ja")
    ]

    def __init__(self):
        Tk.__init__(self)
        self.title("cliptrans")
        self.geometry("300x150")
        self.resizable(0, 0)
        self.iconbitmap(r".\icon.ico")
        self.attributes("-topmost", True)
        #self.bind("<Return>", self.enterCommand)

        self.createMenu()
        self.createInputFrame()
        self.createOutputFrame()

        thread = Thread(target=self.translate)
        thread.daemon = True
        thread.start()

    def createMenu(self):
        self.status_top = BooleanVar()
        self.status_top.set(True)

        self.language_choice = StringVar()
        self.language_choice.set("zh-cn")

        menubar = Menu(self)
        language = Menu(menubar, tearoff=0)
        option = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Language", menu=language)
        menubar.add_cascade(label="Option", menu=option)
        for label, value in self.all_language:
            language.add_radiobutton(
                label=label,
                variable=self.language_choice,
                value=value
            )
        option.add_checkbutton(
            label="Always on Top",
            variable=self.status_top,
            command=lambda : self.attributes("-topmost", self.status_top.get())
        )
        option.add_command(label="Exit", command=self.quit)
        self.config(menu=menubar)

    def createInputFrame(self):
        self.text_input = StringVar()

        frame_input = Frame(self, bd=1)
        self.entry = Entry(
            master=frame_input,
            font=("宋体", 12),
            width=140,
            textvariable=self.text_input
        )
        button = Button(
            master=frame_input,
            text=" Translate ",
            command=lambda : [copy(self.text_input.get()) ,self.entry.select_range(0, END)]
        )
        button.pack(side=RIGHT)
        self.entry.pack(side=LEFT, fill="y")
        frame_input.pack(side=TOP)
        self.entry.bind(
            "<Return>",
            lambda event: [copy(self.text_input.get()), self.entry.select_range(0, END)]
        )
        self.entry.bind(
            "<Button-1>",
            lambda event: self.entry.delete(0, END)
        )
    
    def createOutputFrame(self):
        frame_output = Frame(self, bd=1)
        scrollbar = Scrollbar(frame_output, orient=VERTICAL)
        self.text = Text(
            master=frame_output,
            state="disable",
            font=("宋体", 12),
            yscrollcommand=scrollbar.set
        )
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=self.text.yview)
        self.text.pack()
        frame_output.pack(expand=True, fill="both")

    def translate(self):
        translator = Translator(service_urls=["translate.google.cn"])
        data_old = paste()
        while True:
            data = paste()
            if data != data_old:
                try:
                    content = translator.translate(data, dest=self.language_choice.get()).text
                    data_old = data
                except Exception as error:
                    result = error
                self.text.config(state="normal")
                self.text.delete(1.0, END)
                self.text.insert(INSERT, content)
                self.text.config(state="disabled")
            sleep(0.1)
            
if __name__ == "__main__":
    root = MainFrame()
    root.mainloop()
