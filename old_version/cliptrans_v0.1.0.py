from googletrans import Translator
from pyperclip import paste
from threading import Thread
from time import sleep
from tkinter import (Tk, StringVar, Menu, Frame, Scrollbar, Text,
    END, INSERT, VERTICAL, RIGHT, Y)

__author__ = 'Jayden'
__version__ = '0.1.0'

def display(content):
    text.config(state='normal')
    text.delete(1.0, END)
    text.insert(INSERT, content)
    text.config(state='disabled')

def translate():
    global lang
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

if __name__ == '__main__':

    root = Tk()
    root.title('cliptrans')
    root.geometry('300x130')
    root.resizable(0, 0)
    root.iconbitmap(r'.\icon.ico')
    root.attributes('-topmost', True)

    lang = [
        ('English', 'en'),
        ('Chinese(中文)', 'zh-cn'),
        ('Japanese(日本語)', 'ja')
    ]
    lang_choice = StringVar()
    lang_choice.set('zh-cn')

    menubar = Menu(root)
    language = Menu(menubar, tearoff=0)
    option = Menu(menubar, tearoff=0)
    menubar.add_cascade(label='Language', menu=language)
    menubar.add_cascade(label='Option', menu=option)
    for label, value in lang:
        language.add_radiobutton(label=label, variable=lang_choice, value=value)
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
