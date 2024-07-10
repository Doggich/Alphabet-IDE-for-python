import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import threading
from tkinter import ttk


class IDE:
    def __init__(self, root_):
        self.root = root_
        self.root.title("Alphabet IDE")
        self.root.geometry("800x600")

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)

        self.edit_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=self.cut)
        self.edit_menu.add_command(label="Copy", command=self.copy)
        self.edit_menu.add_command(label="Paste", command=self.paste)

        self.text_area = tk.Text(self.root)
        self.text_area.pack(fill="both", expand=True)

        self.run_button = tk.Button(self.root, text="Run", command=self.run_code)
        self.run_button.pack(fill="x")

        self.snipet_button = tk.Button(self.root, text="Snipet", command=self.run_snipet)
        self.snipet_button.pack(fill="x")

        themes = ["Default", "Dark", "Light", "Contrast", "Console Green", "Console Magenta"]
        self.theme_combobox = ttk.Combobox(self.root, values=themes)
        self.theme_combobox.bind("<<ComboboxSelected>>", self.change_theme)
        self.theme_combobox.pack()

    def new_file(self):
        self.text_area.delete(1.0, "end")

    def open_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.insert("end", file.read())

    def save_file(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, "end"))

    def cut(self):
        self.text_area.clipboard_clear()
        self.text_area.clipboard_append(self.text_area.selection_get())
        self.text_area.delete("sel.first", "sel.last")

    def copy(self):
        self.text_area.clipboard_clear()
        self.text_area.clipboard_append(self.text_area.selection_get())

    def paste(self):
        self.text_area.insert("insert", self.text_area.clipboard_get())

    def run_code(self):
        code = self.text_area.get(1.0, "end")
        try:
            with open("temp.py", "w") as file:
                file.write(code)

            def run_in_thread():
                process = subprocess.call("start cmd /k python temp.py", shell=True)

            threading.Thread(target=run_in_thread).start()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def run_snipet(self):
        try:
            subprocess.call("start cmd /k python", shell=True)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def change_theme(self, event):
        selected_theme = self.theme_combobox.get()
        if selected_theme == "Dark":
            self.text_area.config(bg="black", fg="white")
        elif selected_theme == "Light":
            self.text_area.config(bg="white", fg="black")
        elif selected_theme == "Contrast":
            self.text_area.config(bg="yellow", fg="blue")
        elif selected_theme == "Console Green":
            self.text_area.config(bg="black", fg="green")
        elif selected_theme == "Console Magenta":
            self.text_area.config(bg="black", fg="magenta")
        else:
            self.text_area.config(bg="white", fg="black")


if __name__ == "__main__":
    root = tk.Tk()
    ide = IDE(root)
    root.mainloop()
