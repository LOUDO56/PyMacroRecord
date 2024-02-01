from tkinter import messagebox


def confirm_save():
    """Just popup a window to say 'Do you want to save your record?'
    So the user don't lost his last record accidentally"""
    return messagebox.askyesnocancel("Confirm", "Do you want to save your record?")
