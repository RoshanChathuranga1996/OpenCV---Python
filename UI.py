import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
import os

ad_paths = []


def close_window():
    root.destroy()
    # destroying the main window


def adHash():
    os.system('AdHash.py')


def streamHash():
    os.system('StreamHash.py')


def onClick():
    checkValue = check.get()
    if checkValue == 1:
        adHash()
    else:
        streamHash()


def fileChooser():
    root.filename = filedialog.askopenfilename(initialdir="E:\\Opencv_project\\Videos", title="Select a file",
                                    filetypes=(("Mp4 files", "*.mp4"), ("Mov files", "*.mov"), ("All files", "*.*")))
    fPath = root.filename
    ad_paths.append(fPath)

    if len(ad_paths) == 1:
        entSt0.insert(0, ad_paths[0])
    if len(ad_paths) == 2:
        entSt0.insert(0, ad_paths[0])
        entSt1.insert(0, ad_paths[1])
    if len(ad_paths) == 3:
        entSt0.insert(0, ad_paths[0])
        entSt1.insert(0, ad_paths[1])
        entSt2.insert(0, ad_paths[2])
    if len(ad_paths) == 4:
        entSt0.insert(0, ad_paths[0])
        entSt1.insert(0, ad_paths[1])
        entSt2.insert(0, ad_paths[2])
        entSt3.insert(0, ad_paths[3])
    if len(ad_paths) == 5:
        entSt0.insert(0, ad_paths[0])
        entSt1.insert(0, ad_paths[1])
        entSt2.insert(0, ad_paths[2])
        entSt3.insert(0, ad_paths[3])
        entSt4.insert(0, ad_paths[4])
    if len(ad_paths) == 6:
        entSt0.insert(0, ad_paths[0])
        entSt1.insert(0, ad_paths[1])
        entSt2.insert(0, ad_paths[2])
        entSt3.insert(0, ad_paths[3])
        entSt4.insert(0, ad_paths[4])
        entSt5.insert(0, ad_paths[5])


root = tk.Tk()
root.geometry('600x350')
root.title("Ad Detection")

# Canvas
canvas = tk.Canvas(root, height=600, width=800)
canvas.grid()
# Image
myImg = ImageTk.PhotoImage(Image.open("C:\\Users\\rosha\\Pictures\\Saved Pictures\\dd1.jpg"))
bckLbl = tk.Label(root, image=myImg)
bckLbl.place(relheight=1, relwidth=1)

# Channel stream lbl
lblSt = tk.Label(bckLbl, text="Channel Stream :", bg="light gray", fg="black", width=20, height=1)
lblSt.grid(row=0, column=0, padx=5)
# Text filed for stream
entSt0 = tk.Entry(bckLbl, width=50, bg="white", fg="black")
entSt0.grid(row=0, column=2, padx=5)
#  Stream btn
btnOK = tk.Button(bckLbl, text="[Click Me]", command=fileChooser)
btnOK.grid(row=0, column=3, pady=20)

# Ad1 stream lbl
lblSt = tk.Label(bckLbl, text="Advertisement 1 :", bg="gray", fg="white", width=20, height=1)
lblSt.grid(row=1, column=0)
# Text filed for Ad 1
entSt1 = tk.Entry(bckLbl, width=50, bg="white", fg="black")
entSt1.grid(row=1, column=2)
#  Ad1 btn btn
btnOK = tk.Button(bckLbl, text="[Click Me]", command=fileChooser)
btnOK.grid(row=1, column=3, pady=3)

# Ad2 stream lbl
lblSt = tk.Label(bckLbl, text="Advertisement 2 :", bg="gray", fg="white", width=20, height=1)
lblSt.grid(row=2, column=0)
# Text filed for Ad 2
entSt2 = tk.Entry(bckLbl, width=50, bg="white", fg="black")
entSt2.grid(row=2, column=2)
#  Ad2 btn btn
btnOK = tk.Button(bckLbl, text="[Click Me]", command=fileChooser)
btnOK.grid(row=2, column=3, pady=3)

# Ad3 stream lbl
lblSt = tk.Label(bckLbl, text="Advertisement 3 :", bg="gray", fg="white", width=20, height=1)
lblSt.grid(row=3, column=0)
# Text filed for Ad 3
entSt3 = tk.Entry(bckLbl, width=50, bg="white", fg="black")
entSt3.grid(row=3, column=2)
#  Ad3 btn btn
btnOK = tk.Button(bckLbl, text="[Click Me]", command=fileChooser)
btnOK.grid(row=3, column=3, pady=3)

# Ad4 stream lbl
lblSt = tk.Label(bckLbl, text="Advertisement 4 :", bg="gray", fg="white", width=20, height=1)
lblSt.grid(row=4, column=0)
# Text filed for Ad 4
entSt4 = tk.Entry(bckLbl, width=50, bg="white", fg="black")
entSt4.grid(row=4, column=2)
#  Ad4 btn btn
btnOK = tk.Button(bckLbl, text="[Click Me]", command=fileChooser)
btnOK.grid(row=4, column=3, pady=3)

# Ad5 stream lbl
lblSt = tk.Label(bckLbl, text="Advertisement 5 :", bg="gray", fg="white", width=20, height=1)
lblSt.grid(row=5, column=0)
# Text filed for Ad 5
entSt5 = tk.Entry(bckLbl, width=50, bg="white", fg="black")
entSt5.grid(row=5, column=2)
#  Ad5 btn btn
btnOK = tk.Button(bckLbl, text="[Click Me]", command=fileChooser)
btnOK.grid(row=5, column=3, pady=3)

# checkBtn
check = tk.IntVar()
checkBtn = tk.Checkbutton(bckLbl, text=" Create Ad hashes ", variable=check, fg="black", bg="gray")
checkBtn.place(x=5, y=250)

# Start btn
btnStart = tk.Button(bckLbl, text="START", fg="black", bg="gray", font=("Helvetica", 10), width=8,
                     activebackground="light blue", command=onClick)
btnStart.place(x=200, y=250)

# Quit btn
btnQuit = tk.Button(bckLbl, text="QUIT", fg="black", bg="gray", font=("Helvetica", 10), width=8,
                    activebackground="light blue", command=close_window)
btnQuit.place(x=300, y=250)

root.mainloop()
