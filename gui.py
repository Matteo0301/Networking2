import tkinter as tk
from PIL import Image, ImageTk
import subprocess


class GUI:
    def __init__(self, mininet):
        self.net = mininet

        self.host_width = 40
        self.host_height = 32
        self.server_width = 25
        self.server_height = 40

        # Variables for the slices
        self.slice1_active = False
        self.slice2_active = False
        self.slice3_active = False

        self.rectangles = [None for _ in range(9)]
        self.server_rectangle = None

        self.slice1_hosts = [2, 3, 4]
        self.slice2_hosts = [6, 7, 8, 9]
        self.slice3_hosts = [1, 5]
        self.server_slices = [0, 1, 2]  # Slice number 0 means no slice active
        self.server_slice_index = 0  # The index of the active slice

        self.slice1_color = "#FF0000"
        self.slice2_color = "#00FF00"
        self.slice3_color = "#0000FF"

        self.host_coordinates = [
            (78, 12),
            (83, 115),
            (83, 167),
            (83, 224),
            (383, 12),
            (383, 63),
            (383, 115),
            (383, 167),
            (383, 224),
        ]
        self.server_coordinates = (233, 218)

        self.setup_gui()
        """ self.gui_thread = threading.Thread(target=self.setup_gui)
        self.gui_thread.start() """

    def toggle_slice(self, active, hosts, color, script):
        if active:
            subprocess.run([script, "start"])
            for h in hosts:
                i = h-1
                self.rectangles[i] = self.draw_rec(
                    self.host_coordinates[i][0], self.host_width, self.host_coordinates[i][1], self.host_height, color)
        else:
            subprocess.run([script, "stop"])
            for h in hosts:
                i = h-1
                self.canvas.delete(self.rectangles[i])
                self.rectangles[i] = None

    def draw_rec(self, x, width, y, height, color):
        r = self.canvas.create_rectangle(
            x, y, x+width, y+height, fill=color, )
        self.canvas.tag_lower(r, self.image)
        return r

    # Handlers for slice buttons
    def slice1_handler(self):
        self.slice1_active = not self.slice1_active
        self.toggle_slice(self.slice1_active, self.slice1_hosts,
                          self.slice1_color, "./slice1.sh")
        if self.slice1_active:
            self.label1.configure(text="Slice 1: active")
        else:
            self.label1.configure(text="Slice 1: not active")

    def slice2_handler(self):
        self.slice2_active = not self.slice2_active
        self.toggle_slice(self.slice2_active, self.slice2_hosts,
                          self.slice2_color, "./slice2.sh")
        if self.slice2_active:
            self.label2.configure(text="Slice 2: active")
        else:
            self.label2.configure(text="Slice 2: not active")

    def slice3_handler(self):
        self.slice3_active = not self.slice3_active
        self.toggle_slice(self.slice3_active, self.slice3_hosts,
                          self.slice3_color, "./slice3.sh")
        if self.slice3_active:
            self.label3.configure(text="Slice 3: active")
        else:
            self.label3.configure(text="Slice 3: not active")

    def clear_server_rec(self):
        if self.server_rectangle != None:
            self.canvas.delete(self.server_rectangle)
            self.server_rectangle = None

    def server_handler(self):
        self.server_slice_index = (
            self.server_slice_index + 1) % len(self.server_slices)
        self.clear_server_rec()
        if self.server_slice_index == 0:
            subprocess.run(["./server_slice.sh", "remove1"])
            subprocess.run(["./server_slice.sh", "remove2"])
            self.label_server.configure(text="No slice")
        elif self.server_slice_index == 1:
            subprocess.run(["./server_slice.sh", "add1"])
            self.server_rectangle = self.draw_rec(
                self.server_coordinates[0], self.server_width, self.server_coordinates[1], self.server_height, self.slice1_color)
            self.label_server.configure(text="Slice 1")
        elif self.server_slice_index == 2:
            subprocess.run(["./server_slice.sh", "add2"])
            self.server_rectangle = self.draw_rec(
                self.server_coordinates[0], self.server_width, self.server_coordinates[1], self.server_height, self.slice2_color)
            self.label_server.configure(text="Slice 2")

    def change_bandwidth(self):
        b1 = self.slider1.get()
        b2 = self.slider2.get()
        b3 = self.slider3.get()
        subprocess.run(["./queues.sh", str(b1), str(b2), str(b3)])

    def show_bandwidth(self):
        host1 = self.bandwidth_text1.get("1.0", "end")[:-1]
        host2 = self.bandwidth_text2.get("1.0", "end")[:-1]
        slice1 = -1
        slice2 = -1
        if len(host1) == 2 and host1[:1] == "h" and host1[1:].isnumeric():
            host1_number = int(host1[1:])
            if host1_number in self.slice1_hosts and self.slice1_active:
                slice1 = 1
            elif host1_number in self.slice2_hosts and self.slice2_active:
                slice1 = 2
            elif host1_number in self.slice3_hosts and self.slice3_active:
                slice1 = 3
        elif host1 == "server":
            host1_number = 10
            slice1 = self.server_slices[self.server_slice_index]
        else:
            self.bandwidth_result.configure(text="Invalid host 1")
            return

        if len(host2) == 2 and host2[:1] == "h" and host2[1:].isnumeric():
            host2_number = int(host2[1:])
            if host2_number in self.slice1_hosts and self.slice1_active:
                slice2 = 1
            elif host2_number in self.slice2_hosts and self.slice2_active:
                slice2 = 2
            elif host2_number in self.slice3_hosts and self.slice3_active:
                slice2 = 3
        elif host2 == "server":
            host2_number = 10
            slice2 = self.server_slices[self.server_slice_index]
        else:
            self.bandwidth_result.configure(text="Invalid host 2")
            return

        if slice1 != slice2 or slice1 == -1:
            self.bandwidth_result.configure(text="Hosts not on the same slice")
            return

        res = self.net.iperf(hosts=[self.net.getNodeByName(
            host1), self.net.getNodeByName(host2)])
        self.bandwidth_result.configure(
            text=("Transfer: " + str(res[0]) + "  Bandwidth: " + str(res[1])))

    def setup_gui(self):
        # Create the window
        self.window = tk.Tk()
        self.window.title("Networking 2 project")
        self.window.geometry("1100x600")
        # Load the image
        self.image = Image.open("topology.png")
        self.photo = ImageTk.PhotoImage(self.image)
        self.canvas = tk.Canvas(
            self.window, width=self.image.size[0], height=self.image.size[1])
        self.canvas.pack(side=tk.LEFT)
        self.image = self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.photo)

        self.slices_frame = tk.Frame(self.window)
        self.slices_frame.pack(side=tk.RIGHT)

        # Frames for the slices
        self.frame1 = tk.Frame(self.slices_frame)
        self.frame1.pack(side=tk.TOP)
        self.frame2 = tk.Frame(self.slices_frame)
        self.frame2.pack(side=tk.TOP)
        self.frame3 = tk.Frame(self.slices_frame)
        self.frame3.pack(side=tk.TOP)
        self.server_frame = tk.Frame(self.slices_frame)
        self.server_frame.pack(side=tk.TOP)
        self.bandwidth_frame = tk.Frame(self.slices_frame)
        self.bandwidth_frame.pack(side=tk.TOP)
        self.result_frame = tk.Frame(self.slices_frame)
        self.result_frame.pack(side=tk.TOP)

        # First slice
        self.button1 = tk.Button(
            self.frame1, text="TOGGLE 1", command=self.slice1_handler)
        self.button1.pack(side=tk.LEFT, padx=10, pady=5)
        self.label1 = tk.Label(self.frame1, text="Slice 1: not active")
        self.label1.pack(side=tk.LEFT, padx=10, pady=5)

        self.slider1 = tk.Scale(self.frame1, from_=1, to=4000,
                                label="Bandwidth (Kb/s)", orient=tk.HORIZONTAL)
        self.slider1.pack(side=tk.RIGHT, padx=10, pady=5)
        self.set_bandwidth1 = tk.Button(
            self.frame1, text="SET", command=self.change_bandwidth)
        self.set_bandwidth1.pack(side=tk.RIGHT, padx=10, pady=5)

        # Second slice
        self.button2 = tk.Button(
            self.frame2, text="TOGGLE 2", command=self.slice2_handler)
        self.button2.pack(side=tk.LEFT, padx=10, pady=5)

        self.label2 = tk.Label(self.frame2, text="Slice 2: not active")
        self.label2.pack(side=tk.LEFT, padx=10, pady=5)

        self.slider2 = tk.Scale(self.frame2, from_=1, to=5000,
                                label="Bandwidth (Kb/s)", orient=tk.HORIZONTAL)
        self.slider2.pack(side=tk.RIGHT, padx=10, pady=5)
        self.set_bandwidth2 = tk.Button(
            self.frame2, text="SET", command=self.change_bandwidth)
        self.set_bandwidth2.pack(side=tk.RIGHT, padx=10, pady=5)

        # Third slice
        self.button3 = tk.Button(
            self.frame3, text="TOGGLE 3", command=self.slice3_handler)
        self.button3.pack(side=tk.LEFT, padx=10, pady=5)

        self.label3 = tk.Label(self.frame3, text="Slice 3: not active")
        self.label3.pack(side=tk.LEFT, padx=10, pady=5)

        self.slider3 = tk.Scale(self.frame3, from_=1, to=2000,
                                label="Bandwidth (Kb/s)", orient=tk.HORIZONTAL)
        self.slider3.pack(side=tk.RIGHT, padx=10, pady=5)
        self.set_bandwidth3 = tk.Button(
            self.frame3, text="SET", command=self.change_bandwidth)
        self.set_bandwidth3.pack(side=tk.RIGHT, padx=10, pady=5)

        # Server slice
        self.server_button = tk.Button(
            self.server_frame, text="TOGGLE SERVER", command=self.server_handler)
        self.server_button.pack(side=tk.LEFT, padx=10, pady=5)

        self.label_server = tk.Label(self.server_frame, text="No slice")
        self.label_server.pack(side=tk.LEFT, padx=10, pady=5)

        # Bandwidth frame
        self.blabel1 = tk.Label(self.bandwidth_frame, text="First host")
        self.blabel1.pack(side=tk.LEFT)
        self.bandwidth_text1 = tk.Text(self.bandwidth_frame, height=1, width=6)
        self.bandwidth_text1.pack(side=tk.LEFT)
        self.blabel2 = tk.Label(self.bandwidth_frame, text="Second host")
        self.blabel2.pack(side=tk.LEFT)
        self.bandwidth_text2 = tk.Text(self.bandwidth_frame, height=1, width=6)
        self.bandwidth_text2.pack(side=tk.LEFT)

        self.bandwidth_button = tk.Button(
            self.bandwidth_frame, text="SHOW BANDWIDTH", command=self.show_bandwidth)
        self.bandwidth_button.pack(side=tk.LEFT)

        self.bandwidth_result = tk.Label(self.result_frame, text="Result")
        self.bandwidth_result.pack(side=tk.LEFT)

        self.window.mainloop()


if __name__ == "__main__":
    gui = GUI(None)
