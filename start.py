from tkinter import *
from tkinter import filedialog, messagebox
import os
from Generator import Generator
import tkinter.font as font

root = Tk()
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()

positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2 - 200)
positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)

# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))
root['background'] = '#856ff8'
frame = Frame(root, bg='#856ff8')
padx = 5
pady = 5
frame.pack(pady=pady, padx=padx)

width = 52
bg = '#856ff8'

myFont = font.Font(size=20)


class GenerateFile:
    root.title("React file generator")

    def create_frame(self, list, text):
        _frame = 0
        label = 1
        entry = 2
        list[_frame] = Frame(frame, height=200, width=300,
                             highlightbackground="black", highlightthickness=1)
        list[_frame].pack(pady=padx, padx=pady)
        list[label] = Label(list[0], text=text)
        list[label].pack(side=TOP)
        list[entry] = Entry(list[0], width=width)
        list[entry].pack(side=BOTTOM, padx=padx, pady=pady)
        return list[entry]

    def __init__(self):
        self.file_path = ""
        pathFrame = Frame(frame, width=width, bg=bg)
        pathFrame.pack(pady=padx, padx=pady)
        buttonSearch = Button(pathFrame, text="Select Folder", command=self.selected_path, font=myFont, fg='red',
                              width=int(width / 3), )
        buttonSearch.pack(side=RIGHT, pady=padx, padx=pady)
        btnGenerate = Button(frame, text="Generate",
                             fg='red', command=self.generate_files, width=int(width / 3), font=myFont, )
        btnGenerate.pack(side=BOTTOM, padx=padx, pady=pady)
        self.actionEntry = self.create_frame(
            ['actionFrame', 'actionLabel', 'actionEntry'], 'Action Name')
        self.folderEntry = self.create_frame(
            ['folderFrame', 'folderLabel', 'folderEntry'], 'Folder Name')
        self.typeEntry = self.create_frame(
            ['typeFrame', 'typeLabel', 'typeEntry'], 'Type Name')
        self.apiEntry = self.create_frame(
            ['apiFrame', 'apiLabel', 'apiEntry'], 'Api Name')

    def selected_path(self):
        self.file_path = filedialog.askdirectory()

    def generate_files(self):
        try:
            path = self.file_path
            folder = path + '/src/'
            if not os.path.exists(folder):
                os.makedirs(folder)
            generate = Generator(folder, self.typeEntry.get(), self.folderEntry.get(), self.apiEntry.get(),
                                 self.actionEntry.get())
        except:
            messagebox.showerror('Failed', 'we have an error')


g = GenerateFile()
root.mainloop()
