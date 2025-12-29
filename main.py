import tkinter as tk
import os
import uuid
import json

notes = {}
json_file = "./database.json"

def create_note(
        note_id=None,
        title="Untitled",
        content="",
        geometry="300x300",
        topmost=False,
        color="pink"
    ):

    # Generate a unique ID for the note
    if not note_id:
        note_id = str(uuid.uuid4())

    note = tk.Toplevel()
    note.geometry(geometry)
    note.attributes("-topmost", topmost)

    # Frame for control buttons
    controls = tk.Frame(note)
    controls.pack(side="top", fill="x", pady=4)
    
    # Text area for note content
    title_var = tk.StringVar(value=title)
    title_entry = tk.Entry(
        controls,
        textvariable=title_var,
        font=("Arial", 11, "bold"),
        bd=0
    )
    title_entry.pack(fill="x", padx=6, pady=4)

    text = tk.Text(note, wrap='word', bg=color, fg='black', padx=5, pady=5)
    text.pack(expand=True, fill='both')
    text.insert("1.0", content)

    # Buttons for controls
    tk.Button(
        controls,
        text="Always on Top📌",
        padx=8,
        pady=3,
        command=lambda: note.attributes("-topmost", not note.attributes("-topmost"))
    ).pack(side="left", padx=4)
    tk.Button(
        controls, 
        text="Change Color", 
        command=lambda: change_color(note_id)
    ).pack(side="left", padx=4)
    tk.Button(
        controls,
        text="🗑 Delete",
        command=lambda: delete_note(note_id)
    ).pack(side="right", padx=4)


    notes[note_id] = {
        "window": note,
        "text": text,
        "color": "pink",
        "title_var": title_var
    }

    title_entry.bind("<KeyRelease>", lambda e: (save_all_notes(), refresh_note_list()))
    text.bind("<KeyRelease>", lambda e: save_all_notes())
    
    note.bind("<Configure>", lambda e: save_all_notes())
    note.protocol("WM_DELETE_WINDOW",lambda nid=note_id, n=note: on_note_close(nid, n))

    refresh_note_list()


def change_color(note_id):
    colors = ['yellow', 'lightblue', 'lightgreen', 'pink', 'white']
    note_data = notes[note_id]

    text = note_data['text']
    current_color = note_data['color']

    next_color = colors[(colors.index(current_color) + 1) % len(colors)]

    text.configure(bg=next_color)
    note_data['color'] = next_color

    save_all_notes()

def refresh_note_list():
    listbox.delete(0, tk.END)
    for note_id, data in notes.items():
        listbox.insert(tk.END, data["title_var"].get())

def save_all_notes():
    data = {}
    for note_id, note_data in notes.items():
        note = note_data['window']
        text = note_data['text']

        data[note_id] = {
            "x": note.winfo_x(),
            "y": note.winfo_y(),
            "title": note.title(),
            "width": note.winfo_width(),
            "height": note.winfo_height(),
            "text": text.get("1.0", "end-1c"),
            "color": note_data['color'],
            "title": note_data['title_var'].get()
        }

    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)

    print("Saved all notes.")

def load_all_notes():
    if not os.path.exists(json_file):
        return

    with open(json_file, "r") as f:
        data = json.load(f)

    for note_id, note_data in data.items():
        create_note(
            note_id=note_id,
            title=note_data["title"],
            content=note_data["text"],
            geometry=f"{note_data['width']}x{note_data['height']}+{note_data['x']}+{note_data['y']}",
            color=note_data["color"],
            topmost=False,
        )

    refresh_note_list()
    print("Loaded all notes.")

def on_note_close(note_id, note):
    note.withdraw()
    save_all_notes()

def delete_note(note_id):
    note = notes[note_id]["window"]
    notes.pop(note_id)
    note.destroy()
    refresh_note_list()
    save_all_notes()

def focus_note(event):
    selection = listbox.curselection()
    if not selection:
        return

    note_id = list(notes.keys())[selection[0]]
    note = notes[note_id]["window"]

    note.deiconify()
    note.lift()
    note.focus_force()

root = tk.Tk()

root.title("Sticky Notes App")
root.geometry("200x200")
root.protocol("WM_DELETE_WINDOW", lambda: (save_all_notes(), root.destroy()))
# root.withdraw()  # Hide the main window

top_bar = tk.Frame(root)
top_bar.pack(fill="x", pady=5)
tk.Button(top_bar, text="New Note", command=create_note).pack(padx=10)

listbox = tk.Listbox(root, height=10)
listbox.pack(fill="both", expand=True)
listbox.bind("<Double-Button-1>", focus_note)



# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)


load_all_notes()
root.mainloop()

