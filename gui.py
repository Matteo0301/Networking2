import tkinter as tk
from PIL import Image, ImageTk
import subprocess


# Button handler

def handle_slice():
    pass


def change_bandwidth():
    pass


def setup_gui(mininet=None):
    # Create the window
    window = tk.Tk()
    window.title("Networking 2 project")
    window.geometry("900x600")
    # Load the image
    image = Image.open("topology.png")
    photo = ImageTk.PhotoImage(image)
    canvas = tk.Canvas(window, width=image.size[0], height=image.size[1])
    canvas.pack(side=tk.LEFT)
    image = canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    slices_frame = tk.Frame(window)
    slices_frame.pack(side=tk.RIGHT)

    # Frames for the slices
    frame1 = tk.Frame(slices_frame)
    frame1.pack(side=tk.TOP)
    frame2 = tk.Frame(slices_frame)
    frame2.pack(side=tk.TOP)
    frame3 = tk.Frame(slices_frame)
    frame3.pack(side=tk.TOP)

    # First slice
    button1 = tk.Button(frame1, text="ON 1", command=handle_slice)
    button1.pack(side=tk.LEFT, padx=10, pady=5)
    label1 = tk.Label(frame1, text="Slice 1: non attivo")
    label1.pack(side=tk.LEFT, padx=10, pady=5)

    slider1 = tk.Scale(frame1, from_=1000, to=3000,
                       label="Bandwidth", orient=tk.HORIZONTAL)
    slider1.pack(side=tk.RIGHT, padx=10, pady=5)
    set_bandwidth1 = tk.Button(frame1, text="SET", command=change_bandwidth)
    set_bandwidth1.pack(side=tk.RIGHT, padx=10, pady=5)

    # Second slice
    button2 = tk.Button(frame2, text="ON 2", command=handle_slice)
    button2.pack(side=tk.LEFT, padx=10, pady=5)

    label2 = tk.Label(frame2, text="Slice 2: non attivo")
    label2.pack(side=tk.LEFT, padx=10, pady=5)

    slider2 = tk.Scale(frame2, from_=1000, to=3000,
                       label="Bandwidth", orient=tk.HORIZONTAL)
    slider2.pack(side=tk.RIGHT, padx=10, pady=5)
    set_bandwidth2 = tk.Button(frame2, text="SET", command=change_bandwidth)
    set_bandwidth2.pack(side=tk.RIGHT, padx=10, pady=5)

    # Third slice
    button3 = tk.Button(frame3, text="ON 3", command=handle_slice)
    button3.pack(side=tk.LEFT, padx=10, pady=5)

    label3 = tk.Label(frame3, text="Slice 3: non attivo")
    label3.pack(side=tk.LEFT, padx=10, pady=5)

    slider3 = tk.Scale(frame3, from_=1000, to=4000,
                       label="Bandwidth", orient=tk.HORIZONTAL)
    slider3.pack(side=tk.RIGHT, padx=10, pady=5)
    set_bandwidth3 = tk.Button(frame3, text="SET", command=change_bandwidth)
    set_bandwidth3.pack(side=tk.RIGHT, padx=10, pady=5)
    window.mainloop()


# setup_gui()
