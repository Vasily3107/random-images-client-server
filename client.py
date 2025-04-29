from socket     import socket, AF_INET, SOCK_STREAM

from tkinter     import Tk, Label
from tkinter.ttk import Notebook, Frame

from log_in_frame  import init_log_in_frame
from sign_up_frame import init_sign_up_frame
from img_frame     import init_img_frame

IP = "127.0.0.1"
PORT = 12345

root = Tk()
tab_switch = Notebook(root)

client = socket(AF_INET, SOCK_STREAM)
connected = True

try:
    client.connect((IP, PORT))
except:
    connected = False
    connect_error_frame = Frame(tab_switch)

    Label(connect_error_frame,
          text='Sorry we couldn\'t connect you to the server\n\nPlease try again later',
          fg='red', font=20).pack(pady=(133, 0))

    tab_switch.add(connect_error_frame, text='Connection error')


def trigger() -> None:
    init_img_frame(client, tab_switch)

if connected:
    init_log_in_frame(client, tab_switch, trigger)
    init_sign_up_frame(client, tab_switch, trigger)

def on_window_close():
    try: client.send(b'end')
    except: ...

    client.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_window_close)

tab_switch.pack(expand=1, fill='both')

root.title('Client side')
root.geometry('800x400')
root.resizable(False, False)
root.mainloop()