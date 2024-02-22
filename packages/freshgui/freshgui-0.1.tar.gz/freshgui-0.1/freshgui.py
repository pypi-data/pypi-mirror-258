import tkinter as tk

dict = {}

def create(name='FreshGUI Window', size='400x300'):
    global root

    root = tk.Tk()
    root.title(name)
    root.geometry(size)

def text(name='textVariable', text='Text'):
    dict[name] = tk.Label(root, text=text)
    dict[name].pack()

def textUpdate(name='textVariable', text='Text'):
    dict[name].config(text=text)

def button(name='buttonVariable', text='Text', command=''):
    dict[name] = tk.Button(root, text=text, command=command)
    dict[name].pack()

def run():
    root.mainloop()