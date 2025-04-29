from tkinter     import Tk, Label, Button, Entry, Listbox
from tkinter.ttk import Notebook, Frame

from idlelib.tooltip    import Hovertip
from tkinter.messagebox import showinfo, showerror
from datetime           import datetime

from db_handler  import DBHandler

def init_log_edit_frame(tab_switch:Notebook) -> None:
    log_edit_frame = Frame(tab_switch, name='log_edit_frame')

    # - - - USERS - - - - - - - - - - - - - - - - - - - - - - - - - - -
    users_lb = Listbox(log_edit_frame, height=4, selectmode='single', exportselection=False, justify='center')
    users = []

    def update_users_lb():
        logs_lb.delete(0, 'end')
        users_lb.delete(0, 'end')

        nonlocal users
        users = DBHandler.get_users()
        for _, name in users:
            users_lb.insert('end', name)

    Button(log_edit_frame, text='Refresh list of users', command=update_users_lb).pack(fill='x')
    users_lb.pack(fill='x')

    users_lb.bind('<<ListboxSelect>>', lambda _: update_logs_lb())

    # - - - LOGS - - - - - - - - - - - - - - - - - - - - - - - - - - -
    logs_lb = Listbox(log_edit_frame, height=15, selectmode='single', exportselection=False, font=('consolas', 9))
    logs = []

    def update_logs_lb():
        nonlocal users, logs
        if not users_lb.curselection(): return

        user_uuid = next(i[0] for i in users if i[1] == users_lb.get(users_lb.curselection()[0]))

        logs = DBHandler.get_user_logs(user_uuid)

        index_len = len(str(len(logs)))
        msg_len = len(max(logs, key=lambda i: len(i[2]))[2])

        logs_lb.delete(0, 'end')
        for i, (_, date, msg, url) in enumerate(logs, 1):
            logs_lb.insert('end', (f'{i:{index_len}}: '
                                   f'{str(date).split(".")[0]} | '
                                   f'{msg:{msg_len}} | {url}'))

    logs_lb.pack(fill='x')

    # - - - EDIT TOOLS - - - - - - - - - - - - - - - - - - - - - - - - - - -
    edit_subframe = Frame(log_edit_frame)
    edit_entry_width = 30
    edit_button_width = int(edit_entry_width * 0.8)


    # - - - HELPER FUNCTIONS - - -
    def clear_placeholder(entry:Entry, placeholder_text:str):
        if entry.get() == placeholder_text:
            entry.delete(0, 'end')
            entry.config(fg='black')

    def restore_placeholder(entry:Entry, placeholder_text:str):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg='grey')

    def entry_bind_placeholder(entry:Entry, placeholder_text:str):
        entry.config(exportselection=True)
        entry.bind("<FocusIn>",  lambda _: clear_placeholder(entry, placeholder_text))
        entry.bind("<FocusOut>", lambda _: restore_placeholder(entry, placeholder_text))
        restore_placeholder(entry, placeholder_text)

    def get_user_uuid():
        nonlocal users
        return next(i[0] for i in users if i[1] == users_lb.get(users_lb.curselection()[0]))

    def get_log_uuid():
        nonlocal logs
        return logs[int(logs_lb.get(logs_lb.curselection()[0]).split(':')[0]) - 1][0]


    # - - - DATE - - -
    date_entry = Entry(edit_subframe, width=edit_entry_width)
    date_entry.grid(row=0, column=0)
    entry_bind_placeholder(date_entry, 'Enter new datetime here...')
    Hovertip(date_entry, ('Enter datetime following this format: YYYY-MM-DD hh:mm:ss\n'
                          'Enter "now" to insert current server time'), 0)

    def update_date():
        if not logs_lb.curselection():
            showerror('Date change error', 'Please select log to change its date')
            return

        new_date = date_entry.get().strip()

        if new_date != 'now':
            try:
                datetime.strptime(new_date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                showerror('Date change error', ('Invalid datetime detected!\n\n'
                                                'Please enter datetime following this format:\nYYYY-MM-DD hh:mm:ss\n\n'
                                                'Example: "1987-7-31 2:3:4"\n\n'
                                                'Enter "now" to insert current server time'))
                return
        else:
            new_date = datetime.now()

        DBHandler.update_log(get_log_uuid(), '[date]', new_date)
        update_logs_lb()

    Button(edit_subframe, text='Change date', command=update_date, width=edit_button_width).grid(row=1, column=0)


    # - - - MESSAGE - - -
    msg_entry = Entry(edit_subframe, width=edit_entry_width)
    msg_entry.grid(row=0, column=1)
    entry_bind_placeholder(msg_entry, 'Enter new message here...')

    def update_msg():
        if not logs_lb.curselection():
            showerror('Message change error', 'Please select log to change its message')
            return

        new_msg = msg_entry.get().strip()

        if not new_msg or new_msg == 'Enter new message here...':
            showerror('Message change error', 'Message can\'t be empty')
            return

        DBHandler.update_log(get_log_uuid(), '[message]', new_msg)
        update_logs_lb()

    Button(edit_subframe, text='Change message', command=update_msg, width=edit_button_width).grid(row=1, column=1)


    # - - - URL - - -
    url_entry = Entry(edit_subframe, width=edit_entry_width)
    url_entry.grid(row=0, column=2)
    entry_bind_placeholder(url_entry, 'Enter new URL here...')

    def update_url():
        if not logs_lb.curselection():
            showerror('URL change error', 'Please select log to change its URL')
            return

        new_url = url_entry.get().strip()

        if not new_url or new_url == 'Enter new URL here...':
            showerror('URL change error', 'URL can\'t be empty')
            return

        DBHandler.update_log(get_log_uuid(), '[url]', new_url)
        update_logs_lb()

    Button(edit_subframe, text='Change URL', command=update_url, width=edit_button_width).grid(row=1, column=2)


    # - - - COPY URL - - -
    def copy_url():
        nonlocal logs
        if not logs_lb.curselection():
            showerror('URL Copy error', 'Please select log to copy its URL section')
            return

        log_index = int(logs_lb.get(logs_lb.curselection()[0]).split(':')[0]) - 1

        tmp_tk = Tk()
        tmp_tk.clipboard_append(logs[log_index][3])
        tmp_tk.update()
        tmp_tk.destroy()

        showinfo('URL Copy info', 'Image URL has been coppied to the clipboard')

    Button(edit_subframe, text='Copy URL to the clipboard', command=copy_url, width=33).grid(row=1, column=3, columnspan=2)


    # - - - ADD LOG - - -
    def add_log():
        if not users_lb.curselection():
            showerror('Log addition error', 'Please select user to add new log to his account')
            return

        new_date = date_entry.get().strip()
        if new_date != 'now':
            try:
                datetime.strptime(new_date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                showerror('Log addition error | Date', ('Invalid datetime detected!\n\n'
                                                        'Please enter datetime following this format:\nYYYY-MM-DD hh:mm:ss\n\n'
                                                        'Example: "1987-7-31 2:3:4"\n\n'
                                                        'Enter "now" to insert current server time'))
                return
        else:
            new_date = datetime.now()

        new_msg = msg_entry.get().strip()
        if not new_msg or new_msg == 'Enter new message here...':
            showerror('Log addition error | Message', 'Message can\'t be empty')
            return

        new_url = url_entry.get().strip()
        if not new_url or new_url == 'Enter new URL here...':
            showerror('Log addition error | URL', 'URL can\'t be empty')
            return

        DBHandler.add_log(get_user_uuid(), new_msg, new_url, new_date)
        update_logs_lb()

    Button(edit_subframe, text='Add log', command=add_log, width=16, fg='green').grid(row=0, column=3)


    # - - - DEL LOG - - -
    def del_log():
        if not logs_lb.curselection():
            showerror('Log deletion error', 'Please select log to delete it')
            return

        DBHandler.del_log(get_log_uuid())
        update_logs_lb()

    Button(edit_subframe, text='Delete log', command=del_log, width=16, fg='red').grid(row=0, column=4)


    edit_subframe.pack(fill='x')

    update_users_lb()

    if 'log_edit_frame' not in ''.join(tab_switch.tabs()):
        tab_switch.add(log_edit_frame, text='Edit logs')