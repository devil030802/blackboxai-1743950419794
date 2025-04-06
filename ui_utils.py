import tkinter as tk
from tkinter import ttk, messagebox

class UIUtils:
    @staticmethod
    def create_labeled_entry(parent, label_text, row):
        """Create a labeled entry widget."""
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky=tk.W)
        entry = ttk.Entry(parent)
        entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        return entry

    @staticmethod
    def create_labeled_combobox(parent, label_text, row, values=None):
        """Create a labeled combobox widget."""
        ttk.Label(parent, text=label_text).grid(row=row, column=0, sticky=tk.W)
        combobox = ttk.Combobox(parent)
        combobox.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=2)
        if values:
            combobox['values'] = values
        return combobox

    @staticmethod
    def create_button(parent, text, command, row, column=0, columnspan=1):
        """Create a button widget."""
        button = ttk.Button(parent, text=text, command=command)
        button.grid(row=row, column=column, columnspan=columnspan, pady=5)
        return button

    @staticmethod
    def create_treeview(parent, columns, show="headings"):
        """Create a treeview widget."""
        tree = ttk.Treeview(parent, columns=columns, show=show)
        for col in columns:
            tree.heading(col, text=col.capitalize())
        return tree

    @staticmethod
    def show_error(message):
        """Show an error messagebox."""
        messagebox.showerror("Error", message)

    @staticmethod
    def show_success(message):
        """Show a success messagebox."""
        messagebox.showinfo("Success", message)

    @staticmethod
    def confirm_action(message):
        """Show a confirmation dialog."""
        return messagebox.askyesno("Confirm", message)