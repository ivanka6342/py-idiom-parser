#!/usr/bin/env python3

import parser_controller
import platform, os
import tkinter as tk
from tkinter import filedialog as fd
from requests import exceptions as req_ex


# self inherits Tkinter()
class Project_X(tk.Tk):
    search_line = None
    search_btn = None
    res_lbl = None
    filename = None

    def __init__(self):
        super().__init__()
        self.initUI()
        self.config(menu=self.menuBar)

        self.title("Project-x")
        self['bg']='#5ec4cd'
        if platform.system() == "Linux":
            self.attributes('-zoomed', True)
        elif platform.system() == "Windows":
            self.state('zoomed')
        else:
            self.geometry('720x720')

    def initUI(self):
        # first widget - menu. at the top
        self.menuBar = tk.Menu(master=self)
        self.filemenu = tk.Menu(self.menuBar, tearoff=0)
        self.filemenu.add_command(label="Open", command=self.openfile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Save", command=self.savefile)
        self.menuBar.add_cascade(label="File", menu=self.filemenu)

        # create search stuff
        search_frame = tk.Frame(self)
        search_frame.pack(side=tk.TOP, fill=tk.X, expand=False)

        self.search_line = tk.Entry(search_frame, width=10)
        self.search_line.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=10, expand=True)
        self.search_line.bind("<Return>", lambda e: self.search_btn_clicked())
        self.search_line.focus()

        self.search_btn = tk.Button(search_frame, text="Search", bg="#39e639", command=self.search_btn_clicked)
        self.search_btn.pack(side=tk.RIGHT, fill=tk.NONE, padx=10, pady=10, expand=False)

        # create results view
        result_frame = tk.Frame(self)
        result_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.res_lbl = tk.Text(result_frame)
        self.res_lbl.bind("<Key>", lambda e: self.ctrlEvent(e))
        self.res_lbl.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10, ipadx=10, ipady=10, expand=True)


    def openfile(self):
        cwd = os.getcwd()
        self.filename = fd.askopenfilename(title='Open a file', initialdir=cwd, filetypes=(('text files', '.txt'),('all files', '*')))
        file_content = ''
        with open(self.filename, 'r') as f:
            file_content = f.read()
        self.res_lbl.delete('1.0', tk.END)
        self.res_lbl.insert(tk.END, file_content)


    def savefile(self):
        cwd = os.getcwd()
        savefile_name = fd.asksaveasfilename(title='Save file', initialdir=cwd, filetypes=(('text files', '.txt'),('all files', '*')))
        with open(savefile_name, 'w+') as f:
            f.write(self.res_lbl.get("1.0", tk.END))
        self.filename = savefile_name


    # forbid editings for result text field, except ctrl+c to copy
    def ctrlEvent(self, event):
        if (12 == event.state and event.keysym == 'c' ):
            return
        else:
            return "break"


    def search_btn_clicked(self):
        self.res_lbl.delete('1.0', tk.END)
        search_string = self.search_line.get()
        try:
            for parser in parser_controller.project_x_parsers:
                res = parser(search_string)
                self.res_lbl.insert(tk.END, 'site: ' + res['domain'] + '\n\n')
                for i,idiom in enumerate(res['idioms']):
                    self.res_lbl.insert(tk.END, str(i) + '. ' + idiom['title'] + '\n')
                    self.res_lbl.insert(tk.END, str(idiom['description']) + '\n')
                    self.res_lbl.insert(tk.END, idiom['example'] + '\n')
                    self.res_lbl.insert(tk.END, '--------------' + '\n')
        except req_ex as e:
            tk.messagebox.showinfo('Error occurred', e)
        except BaseException as b:
            tk.messagebox.showinfo('Error occurred', b)


def main():
    ui = Project_X()
    ui.mainloop()


if __name__ == '__main__':
    main()
