from tkinter     import Tk
from tkinter.ttk import Notebook

from log_in_frame   import init_log_in_frame
from log_edit_frame import init_log_edit_frame

root = Tk()
tab_switch = Notebook(root)

def trigger() -> None:
    init_log_edit_frame(tab_switch)

init_log_in_frame(tab_switch, trigger)

tab_switch.pack(expand=1, fill='both')

root.title('Admin panel')
root.geometry('800x400')
root.minsize(800, 400)
root.resizable(True, False)
root.mainloop()