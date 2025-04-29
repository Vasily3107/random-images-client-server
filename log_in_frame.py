from socket import socket
from jsonpickle import encode

from tkinter     import Label, Button, Entry
from tkinter.ttk import Notebook, Frame

from collections.abc import Callable

def init_log_in_frame(conn:socket, tab_switch:Notebook, trigger:Callable[[], None]) -> None:
    log_in_frame = Frame(tab_switch, name='log_in_frame')

    login_subframe = Frame(log_in_frame, padding=10)
    Label(login_subframe, text='Login:', width=10).grid(row=0, column=0)
    login_entry = Entry(login_subframe)
    login_entry.grid(row=0, column=1)
    login_subframe.pack(pady=(70, 0))

    password_subframe = Frame(log_in_frame, padding=10)
    Label(password_subframe, text='Password:', width=10).grid(row=0, column=0)
    password_entry = Entry(password_subframe, show='*')
    password_entry.grid(row=0, column=1)
    password_subframe.pack()

    def send_log_in_req() -> None:
        info_label.config(text='', fg='black')

        login = str(login_entry.get())
        password = str(password_entry.get())

        if not len(login)   : info_label.config(text='Error: login cannot be empty'   , fg='red'); return
        if not len(password): info_label.config(text='Error: password cannot be empty', fg='red'); return

        conn.send(b'log_in')
        conn.send(encode(
            {'login'   : login,
             'password': password}
        ).encode())
        res = int(conn.recv(1024).decode())

        if not res:
            info_label.config(text='Error: invalid login or password', fg='red')
            return

        if 'img_frame' not in ''.join(tab_switch.tabs()):
            trigger()

        info_label.config(text=f'Logged in as: {login}', fg='green')

    Button(log_in_frame, text='Log in', command=send_log_in_req, width=30).pack()

    info_label = Label(log_in_frame, height=2)
    info_label.pack()

    if 'log_in_frame' not in ''.join(tab_switch.tabs()):
        tab_switch.add(log_in_frame, text='Log in')