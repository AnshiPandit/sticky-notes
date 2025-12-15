import tkinter as tk
# from tkinter import ttk

def create_note():
    note = tk.Toplevel()
    note.title("Sticky Note")
    note.geometry("300x300")

    text = tk.Text(note, wrap='word', bg='yellow', fg='black')
    text.pack(expand=True, fill='both') # expand to fill the window and fill text both directions

    note.attributes('-topmost', not note.attributes('-topmost'))
    tk.Button(note, text="Always on Top", command=lambda: note.attributes('-topmost', not note.attributes('-topmost'))).pack()

def get_window_data(note, text):
    return {
        "x": note.winfo_x(),
        "y": note.winfo_y(),
        "width": note.winfo_width(),
        "height": note.winfo_height(),
        "text": text.get("1.0", "end-1c")
    }

root = tk.Tk()
root.geometry("200x200")
# root.withdraw()  # Hide the main window
tk.Button(root, text="New Note", command=create_note).pack()

# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)


root.mainloop()

