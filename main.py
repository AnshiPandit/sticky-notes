import tkinter as tk
import uuid
import json

notes = {}
json_file = "./database.json"

def create_note():
    # Generate a unique ID for the note
    note_id = str(uuid.uuid4())

    note = tk.Toplevel()
    note.title("Sticky Note")
    note.geometry("300x300")

    # Frame for control buttons
    controls = tk.Frame(note)
    controls.pack(side="top", fill="x", pady=4)

    text = tk.Text(note, wrap='word', bg='pink', fg='black', padx=5, pady=5)
    text.pack(expand=True, fill='both') # expand to fill the window and fill text both directions
    
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

    notes[note_id] = {
        "window": note,
        "text": text,
        "color": "pink"
    }

    text.bind("<KeyRelease>",lambda e:save_all_notes())
    note.bind("<Configure>", lambda e:save_all_notes())


def change_color(note_id):
    colors = ['yellow', 'lightblue', 'lightgreen', 'pink', 'white']
    note_data = notes[note_id]

    text = note_data['text']
    current_color = note_data['color']

    next_color = colors[(colors.index(current_color) + 1) % len(colors)]

    text.configure(bg=next_color)
    note_data['color'] = next_color

    save_all_notes()

def save_all_notes():
    data = {}
    for note_id, note_data in notes.items():
        note = note_data['window']
        text = note_data['text']

        data[note_id] = {
            "x": note.winfo_x(),
            "y": note.winfo_y(),
            "width": note.winfo_width(),
            "height": note.winfo_height(),
            "text": text.get("1.0", "end-1c"),
            "color": note_data['color']
        }

    with open(json_file, "w") as f:
        json.dump(data, f, indent=4)

    print("Saved all notes.")

root = tk.Tk()
root.title("Sticky Notes App")
root.geometry("200x200")
# root.withdraw()  # Hide the main window
tk.Button(root, text="New Note", command=create_note).pack()

# frm = ttk.Frame(root, padding=10)
# frm.grid()
# ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)


root.mainloop()

