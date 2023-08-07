import tkinter as tk
from PIL import Image, ImageTk
import subprocess

host_width = 50
host_height = 30
server_width = 30
server_height = 50

# Global GUI variables
canvas = None
image = None
""" bandwidth_text1 = None
bandwidth_text2 = None
bandwidth_result = None """
# Sliders for slice bandwidth
slider1 = None
slider2 = None
slider3 = None
# Labels
label1 = None
label2 = None
label3 = None
label_server = None

# Variables for the slices
slice1_active = False
slice2_active = False
slice3_active = False

rectangles = [None for _ in range(9)]
server_rectangle = None

slice1_hosts = [2, 3, 4]
slice2_hosts = [6, 7, 8, 9]
slice3_hosts = [1, 5]
server_slices = [0, 1, 2]  # Slice number 0 means no slice active
server_slice_index = 0  # The index of the active slice

slice1_color = "#CC0000"
slice2_color = "#00CC00"
slice3_color = "#0000CC"

host_coordinates = [
    (65, 8),
    (65, 100),
    (65, 135),
    (65, 181),
    (390, 8),
    (390, 65),
    (390, 100),
    (390, 135),
    (390, 181),
]

server_coordinates = (230, 190)

# Mininet object
net = None


def draw_rec(x, width, y, height, color):
    r = canvas.create_rectangle(
        x, y, x+width, y+height, fill=color, )
    canvas.tag_lower(r, image)
    return r


# Button handlers

def toggle_slice(active, hosts, color, script):
    if active:
        subprocess.run([script, "start"])
        for h in hosts:
            i = h-1
            rectangles[i] = draw_rec(
                host_coordinates[i][0], host_width, host_coordinates[i][1], host_height, color)
    else:
        subprocess.run([script, "stop"])
        for h in hosts:
            i = h-1
            canvas.delete(rectangles[i])
            rectangles[i] = None


def slice1_handler():
    global slice1_active
    slice1_active = not slice1_active
    toggle_slice(slice1_active, slice1_hosts, slice1_color, "./slice1.sh")
    if slice1_active:
        label1.configure(text="Slice 1: active")
    else:
        label1.configure(text="Slice 1: not active")


def slice2_handler():
    global slice2_active
    slice2_active = not slice2_active
    toggle_slice(slice2_active, slice2_hosts, slice2_color, "./slice2.sh")
    if slice2_active:
        label2.configure(text="Slice 2: active")
    else:
        label2.configure(text="Slice 2: not active")


def slice3_handler():
    global slice3_active
    slice3_active = not slice3_active
    toggle_slice(slice3_active, slice3_hosts, slice3_color, "./slice3.sh")
    if slice3_active:
        label3.configure(text="Slice 3: active")
    else:
        label3.configure(text="Slice 3: not active")


def clear_server_rec():
    global server_rectangle
    if server_rectangle != None:
        canvas.delete(server_rectangle)
        server_rectangle = None


def server_handler():
    global server_slice_index, server_rectangle
    server_slice_index = (server_slice_index + 1) % len(server_slices)
    clear_server_rec()
    if server_slice_index == 0:
        subprocess.run(["./server_slice.sh", "remove1"])
        subprocess.run(["./server_slice.sh", "remove2"])
        label_server.configure(text="No slice")
    elif server_slice_index == 1:
        subprocess.run(["./server_slice.sh", "add1"])
        server_rectangle = draw_rec(
            server_coordinates[0], server_width, server_coordinates[1], server_height, slice1_color)
        label_server.configure(text="Slice 1")
    elif server_slice_index == 2:
        subprocess.run(["./server_slice.sh", "add2"])
        server_rectangle = draw_rec(
            server_coordinates[0], server_width, server_coordinates[1], server_height, slice2_color)
        label_server.configure(text="Slice 2")


def change_bandwidth():
    b1 = slider1.get()
    b2 = slider2.get()
    b3 = slider3.get()
    subprocess.run(["./queues.sh", str(b1), str(b2), str(b3)])


""" def show_bandwidth():
    host1 = bandwidth_text1.get("1.0", "end")[:-1]
    host2 = bandwidth_text2.get("1.0", "end")[:-1]
    slice1 = -1
    slice2 = -1
    if len(host1) == 2 and host1[:1] == "h" and host1[1:].isnumeric():
        host1_number = int(host1[1:])
        if host1_number in slice1_hosts and slice1_active:
            slice1 = 1
        elif host1_number in slice2_hosts and slice2_active:
            slice1 = 2
        elif host1_number in slice3_hosts and slice3_active:
            slice1 = 3
    elif host1 == "server":
        host1_number = 10
        slice1 = server_slices[server_slice_index]
    else:
        bandwidth_result.configure(text="Error with host 1")
        return

    if len(host2) == 2 and host2[:1] == "h" and host2[1:].isnumeric():
        host2_number = int(host2[1:])
        if host2_number in slice1_hosts and slice1_active:
            slice2 = 1
        elif host2_number in slice2_hosts and slice2_active:
            slice2 = 2
        elif host2_number in slice3_hosts and slice3_active:
            slice2 = 3
    elif host2 == "server":
        host2_number = 10
        slice2 = server_slices[server_slice_index]
    else:
        bandwidth_result.configure(text="Error with host 2")
        return

    if slice1 != slice2 or slice1 == -1:
        bandwidth_result.configure(text="Hosts not on the same slice")

    bandwidth_result.configure(text="OK")
    res = net.iperf(hosts=[host1, host2])
    print(res) """


def setup_gui(mininet=None):
    global canvas, image, slider1, slider2, slider3, label1, label2, label3, label_server, net
    net = mininet
    # Create the window
    window = tk.Tk()
    window.title("Networking 2 project")
    window.geometry("1100x600")
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
    server_frame = tk.Frame(slices_frame)
    server_frame.pack(side=tk.TOP)
    """ bandwidth_frame = tk.Frame(slices_frame)
    bandwidth_frame.pack(side=tk.TOP)
    result_frame = tk.Frame(slices_frame)
    result_frame.pack(side=tk.TOP) """

    # First slice
    button1 = tk.Button(frame1, text="TOGGLE 1", command=slice1_handler)
    button1.pack(side=tk.LEFT, padx=10, pady=5)
    label1 = tk.Label(frame1, text="Slice 1: not active")
    label1.pack(side=tk.LEFT, padx=10, pady=5)

    slider1 = tk.Scale(frame1, from_=1, to=4000,
                       label="Bandwidth (Kb/s)", orient=tk.HORIZONTAL)
    slider1.pack(side=tk.RIGHT, padx=10, pady=5)
    set_bandwidth1 = tk.Button(frame1, text="SET", command=change_bandwidth)
    set_bandwidth1.pack(side=tk.RIGHT, padx=10, pady=5)

    # Second slice
    button2 = tk.Button(frame2, text="TOGGLE 2", command=slice2_handler)
    button2.pack(side=tk.LEFT, padx=10, pady=5)

    label2 = tk.Label(frame2, text="Slice 2: not active")
    label2.pack(side=tk.LEFT, padx=10, pady=5)

    slider2 = tk.Scale(frame2, from_=1, to=5000,
                       label="Bandwidth (Kb/s)", orient=tk.HORIZONTAL)
    slider2.pack(side=tk.RIGHT, padx=10, pady=5)
    set_bandwidth2 = tk.Button(frame2, text="SET", command=change_bandwidth)
    set_bandwidth2.pack(side=tk.RIGHT, padx=10, pady=5)

    # Third slice
    button3 = tk.Button(frame3, text="TOGGLE 3", command=slice3_handler)
    button3.pack(side=tk.LEFT, padx=10, pady=5)

    label3 = tk.Label(frame3, text="Slice 3: not active")
    label3.pack(side=tk.LEFT, padx=10, pady=5)

    slider3 = tk.Scale(frame3, from_=1, to=2000,
                       label="Bandwidth (Kb/s)", orient=tk.HORIZONTAL)
    slider3.pack(side=tk.RIGHT, padx=10, pady=5)
    set_bandwidth3 = tk.Button(frame3, text="SET", command=change_bandwidth)
    set_bandwidth3.pack(side=tk.RIGHT, padx=10, pady=5)

    # Server slice
    server_button = tk.Button(
        server_frame, text="TOGGLE SERVER", command=server_handler)
    server_button.pack(side=tk.LEFT, padx=10, pady=5)

    label_server = tk.Label(server_frame, text="No slice")
    label_server.pack(side=tk.LEFT, padx=10, pady=5)

    """ # Bandwidth frame
    label1 = tk.Label(bandwidth_frame, text="First host")
    label1.pack(side=tk.LEFT)
    bandwidth_text1 = tk.Text(bandwidth_frame, height=1, width=6)
    bandwidth_text1.pack(side=tk.LEFT)
    label2 = tk.Label(bandwidth_frame, text="Second host")
    label2.pack(side=tk.LEFT)
    bandwidth_text2 = tk.Text(bandwidth_frame, height=1, width=6)
    bandwidth_text2.pack(side=tk.LEFT)

    bandwidth_button = tk.Button(
        bandwidth_frame, text="SHOW BANDWIDTH", command=show_bandwidth)
    bandwidth_button.pack(side=tk.LEFT)

    bandwidth_result = tk.Label(result_frame, text="Result")
    bandwidth_result.pack(side=tk.LEFT) """

    window.mainloop()


# setup_gui()
