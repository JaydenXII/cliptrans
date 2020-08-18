from googletrans import Translator
from pyperclip import paste
from threading import Thread
from time import sleep
from tkinter import Tk, Frame, Text, Scrollbar, END, INSERT, RIGHT, VERTICAL, Y, PhotoImage

def display(content):
    text.config(state='normal')
    text.delete(1.0, END)
    text.insert(INSERT, content)
    text.config(state='disabled')

def translate():
    translator = Translator(service_urls=['translate.google.cn'])
    data_old = paste()
    while True:
        data = paste()
        if data != data_old:
            try:
                result = translator.translate(data, src='en', dest='zh-CN').text
                display(result)
                data_old = data
            except Exception as error:
                display(error)
        sleep(0.5)

if __name__ == '__main__':

    root = Tk()
    root.title('cliptrans')
    root.geometry('300x100')
    root.resizable(0, 0)
    root.iconbitmap('.\\icon.ico')
    root.attributes('-topmost', True)
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

    thread = Thread(target=translate)
    thread.daemon = True
    thread.start()

    root.mainloop()
