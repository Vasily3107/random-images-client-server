from socket import socket

from tkinter     import Label, Button, Checkbutton, BooleanVar
from tkinter.ttk import Notebook, Frame

from tkinter.messagebox   import showerror, showinfo
from tkinter.filedialog   import askdirectory
from tkinter.simpledialog import askstring

from PIL import Image, ImageTk
from io  import BytesIO

from random import choice

def init_img_frame(conn:socket, tab_switch:Notebook) -> None:
    img_frame = Frame(tab_switch, name='img_frame')

    # - - - FILTERS - - - - - - - - - - - - - - - - - - - - - - - - - - -
    filter_subframe = Frame(img_frame)
    Label(filter_subframe, text='Filters:').grid(row=0, column=0)
    is_cat = BooleanVar(value=True)
    is_dog = BooleanVar(value=True)
    is_bird= BooleanVar(value=True)
    is_cat_cb = Checkbutton(filter_subframe, variable=is_cat , text='Cats')
    is_dog_cb = Checkbutton(filter_subframe, variable=is_dog , text='Dogs')
    is_bird_cb= Checkbutton(filter_subframe, variable=is_bird, text='Birds')
    is_cat_cb .grid(row=0, column=1)
    is_dog_cb .grid(row=0, column=2)
    is_bird_cb.grid(row=0, column=3)
    filter_subframe.pack()

    # - - - IMAGE - - - - - - - - - - - - - - - - - - - - - - - - - - -
    cur_img_bin = None
    cur_img_ext = None

    def show_rand_img() -> None:
        include = []
        if is_cat .get(): include.append(b'cat')
        if is_dog .get(): include.append(b'dog')
        if is_bird.get(): include.append(b'bird')

        if not len(include):
            showerror('Filter error', 'Please set at least 1 filter')
            return

        conn.send(b'get_img')
        conn.send(choice(include))

        binary = b''
        conn.settimeout(10)
        while True:

            try:
                packet = conn.recv(1024)

            except TimeoutError:
                showerror('Image error', 'Sorry we couldn\'t get you an image\nPlease try again later')
                return

            if packet[-3:] == b'<!>':
                binary += packet[:-3]
                break

            binary += packet
        conn.settimeout(None)

        if binary == b'0' or not binary:
            showerror('Image error', 'Sorry we couldn\'t get you an image\nPlease try again later')
            return

        image_stream = BytesIO(binary)
        
        img = Image.open(image_stream)

        nonlocal cur_img_bin, cur_img_ext
        cur_img_bin = binary
        cur_img_ext = img.format.lower()

        resize_factor = max(img.size)/370
        new_x, new_y = int(img.size[0]/resize_factor), int(img.size[1]/resize_factor)
        img = img.resize((new_x, new_y))

        img = ImageTk.PhotoImage(img)
        img_label.config(image=img, text='')
        img_label.image = img

    img_label = Label(img_frame)

    Button(img_frame, text='Get random image', command=show_rand_img).pack(fill='x')

    img_label.pack()

    # - - - DOWNLOAD - - - - - - - - - - - - - - - - - - - - - - - - - - -
    def download_img():
        nonlocal cur_img_bin, cur_img_ext
        if not cur_img_ext: return

        path = askdirectory(title='Select install location:')
        if not path: showinfo('Downloading canceled', 'Download process has been cancelled'); return
        filename = askstring('', 'Image name:')
        if filename == None: showinfo('Downloading canceled', 'Download process has been cancelled'); return

        with open(f'{path}\\{filename}.{cur_img_ext}', 'wb') as f:
            f.write(cur_img_bin)

        conn.send(b'downloading')

    Button(img_frame, text='Download image', command=download_img).place(x=6, y=60)

    if 'img_frame' not in ''.join(tab_switch.tabs()):
        tab_switch.add(img_frame, text='Random images')