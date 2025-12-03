import tkinter as tk

root = tk.Tk()
# root.withdraw()   # Hide main window for now, optional

note = tk.Toplevel()
note.title("Sticky Note")
note.geometry("200x200")

text = tk.Text(note, wrap="word")
text.pack(expand=True, fill="both")

def get_window_data():
    return {
        "x": note.winfo_x(),
        "y": note.winfo_y(),
        "width": note.winfo_width(),
        "height": note.winfo_height(),
        "text": text.get("1.0", "end-1c")
    }

