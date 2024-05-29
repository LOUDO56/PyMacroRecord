from tkinter import messagebox


def confirm_save(main_app):
    """Just popup a window to say 'Do you want to save your record?'
    So the user don't lost his last record accidentally"""
    return messagebox.askyesnocancel(main_app.text_content["global"]["confirm"], main_app.text_content["global"]["confirm_save"])
