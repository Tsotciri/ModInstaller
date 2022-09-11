from tkinter import filedialog as fd

def file_window(title,open_file = False):
    file_path = fd.askopenfilename(title=title)
    if open_file == True:
        file = open(file_path)
        return file
    else:
        return file_path