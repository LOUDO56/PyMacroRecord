import tkinter as tk

def validate_input(action, value_if_allowed):
    if action == "1":  # Insert
        try:
            float(value_if_allowed)
            return True
        except ValueError:
            return False
    return True

root = tk.Tk()
root.title("Entrée Nombres Seulement")

validate_cmd = root.register(validate_input)

entry = tk.Entry(root, validate="key", validatecommand=(validate_cmd, "%d", "%P"))
entry.pack(padx=20, pady=20)

root.mainloop()