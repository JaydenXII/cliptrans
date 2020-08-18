from googletrans import Translator
from pyperclip import paste, copy
from threading import Thread
from time import sleep
from tkinter import (Tk, Menu, Frame, Scrollbar, Text, Entry, Button,
    StringVar, BooleanVar, END, INSERT, VERTICAL, RIGHT, Y, TOP, LEFT)

__author__ = 'Jayden'
__version__ = '0.1.1'

lang = [
        ('English', 'en'),
        ('Chinese(中文)', 'zh-cn'),
        ('Japanese(日本語)', 'ja')
    ]

def display(content):
    text.config(state='normal')
    text.delete(0, END)
    text.insert(INSERT, content)
    text.config(state='disabled')

def translate():
    translator = Translator(service_urls=['translate.google.cn'])
    data_old = paste()
    while True:
        data = paste()
        if data != data_old:
            try:
                result = translator.translate(data, src='auto', dest=lang_choice.get()).text
                display(result)
                data_old = data
            except Exception as error:
                display(error)
        sleep(0.5)

def on_top():
    root.attributes('-topmost', top_stat.get())
    

if __name__ == '__main__':

    root = Tk()
    root.title('cliptrans')
    root.geometry('300x130')
    root.resizable(0, 0)
    root.iconbitmap(r'.\icon.ico')
    root.attributes('-topmost', True)

    lang_choice = StringVar()
    lang_choice.set('zh-cn')

    top_stat = BooleanVar()
    top_stat.set(True)

    menubar = Menu(root)
    language = Menu(menubar, tearoff=0)
    option = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Language', menu=language)
    menubar.add_cascade(label='Option', menu=option)
    for label, value in lang:
        language.add_radiobutton(label=label, variable=lang_choice, value=value)
    option.add_checkbutton(label='On top', variable=top_stat, command=on_top)
    option.add_command(label='Exit', command=root.quit)

    frame = Frame(root)
    scrollbar = Scrollbar(frame, orient=VERTICAL)
    text = Text(
        frame,
        state='disable',
        font=('宋体', 12,),
        yscrollcommand=scrollbar.set
    )
    scrollbar.pack(side=RIGHT, fill=Y)
    scrollbar.config(command=text.yview)
    text.pack()
    frame.pack(expand=True, fill='both')
    root.config(menu=menubar)

    thread = Thread(target=translate)
    thread.daemon = True
    thread.start()

    root.mainloop()
