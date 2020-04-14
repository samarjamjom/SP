import codecs
from tkinter import messagebox
import tkinter.filedialog as filedialog
import tkinter as tk
import os
source_code = ""
def gui_fun():
    master = tk.Tk()
    intermid_file = "intermid"
    def input():
        global source_code
        input_path = tk.filedialog.askopenfilename()
        input_entry.delete(1, tk.END)  # Remove current text in entry
        input_entry.insert(0, input_path)  # Insert the 'path'
        source_code = os.path.basename(input_path)
        print(input_path)
    def output():
        path = tk.filedialog.askopenfilename()
        input_entry.delete(1, tk.END)  # Remove current text in entry
        input_entry.insert(0, path)  # Insert the 'path'

    top_frame = tk.Frame(master)
    bottom_frame = tk.Frame(master)
    master.title("SIC Assembler")
    line = tk.Frame(master, height=1, width=400, bg="grey80", relief='groove')


    input_path = tk.Label(top_frame, text="This field must contain the path of the file \n \n please browse to get a full path of .asm file as input file path:\n \n ")
    input_entry = tk.Entry(top_frame, text="", width=40)
    browse1 = tk.Button(top_frame, text="Browse", command=input)

    # outputfile = tk.StringVar()
    # output_path = tk.Label(bottom_frame,textvariable=outputfile, text="Output File Name:")
    # output_entry = tk.Entry(bottom_frame, text="", width=40)
    # print(output_entry.get())
    # global intermidfile 
    # intermidfile = output_entry.get()
    # print(intermid_file)
    # browse2 = tk.Button(bottom_frame, text="Browse", command=output)

    begin_button = tk.Button(bottom_frame, text='Begin!', command= master.destroy)

    top_frame.pack(side=tk.TOP)
    line.pack(pady=10)
    bottom_frame.pack(side=tk.BOTTOM)

    input_path.pack(pady=5)
    input_entry.pack(pady=5)
    browse1.pack(pady=5)

    # output_path.pack(pady=5)
    # output_entry.pack(pady=5)
    # browse2.pack(pady=5)

    begin_button.pack(pady=20, fill=tk.X)

    master.mainloop()
    # intermidfile = output_entry.get()
    # print(intermid_file)
    return (source_code,intermid_file)