from tkinter import BOTTOM, LEFT, TOP, Spinbox, messagebox
from tkinter.ttk import Button, Frame, Label
from sys import maxsize as INT_BOUND
from windows.others.distribution import DistributionDrawer
from windows.popup import Popup

class RandomizedDelay(Popup):
    def __init__(self, parent, main_app):
        super().__init__(main_app.text_content["options_menu"]["playback_menu"]["randomized_delay_settings"]["title"], 350, 180, parent)
        main_app.prevent_record = True
        self.main_app = main_app
        self.settings = main_app.settings
        text = main_app.text_content["options_menu"]["playback_menu"]["randomized_delay_settings"]
        Label(self, text=text["sub_text"], font=("Segoe UI", 10)).pack(side=TOP, pady=10)
        user_settings = main_app.settings.settings_dict
        randomized_delay = user_settings["Playback"].get("Randomized_Delay",
            {
                "Enabled": False,
                "Lower": 0,
                "Upper": 0,
                "Distribution": None
            }
        )
        # Keep the currently saved distribution while this popup is open.
        self.distribution = randomized_delay.get("Distribution")
        input_area = Frame(self)
        Label(input_area, text=text["lower_text"]).pack(side=LEFT, padx=5)
        self.lowerInput = Spinbox(input_area, from_=-1 * INT_BOUND, to=INT_BOUND, width=9, validate="key", validatecommand=(main_app.validate_cmd_float, "%d", "%P"))
        self.lowerInput.delete(0, "end")
        self.lowerInput.insert(0, str(randomized_delay.get("Lower", 0)))
        self.lowerInput.pack(side=LEFT, padx=5)
        Label(input_area, text=text["upper_text"]).pack(side=LEFT, padx=5)
        self.upperInput = Spinbox(input_area, from_=-1 * INT_BOUND, to=INT_BOUND, width=9, validate="key", validatecommand=(main_app.validate_cmd_float, "%d", "%P"))
        self.upperInput.delete(0, "end")
        self.upperInput.insert(0, str(randomized_delay.get("Upper", 0)))
        self.upperInput.pack(side=LEFT, padx=5)
        input_area.pack(pady=10)
        distribution_area = Frame(self)
        Button(distribution_area, text=text.get("distribution_button", "Customize distribution"), command=self.open_distribution_editor).pack(side=LEFT, padx=5)
        distribution_area.pack(pady=5)
        button_area = Frame(self)
        Button(button_area, text=main_app.text_content["global"]["confirm_button"], command=lambda: self.setNewValues(self.lowerInput.get(), self.upperInput.get(), main_app)).pack(side=LEFT, padx=10)
        Button(button_area, text=main_app.text_content["global"]["cancel_button"], command=self.destroy).pack(side=LEFT, padx=10)
        button_area.pack(side=BOTTOM, pady=10)
        self.update_idletasks()
        popup_width = min(max(350, self.winfo_reqwidth() + 10), 800)
        popup_height = min(max(180, self.winfo_reqheight() + 10), 600)
        self.geometry(f"{popup_width}x{popup_height}")
        self.wait_window()
        main_app.prevent_record = False

    def open_distribution_editor(self):
        """Open the distribution drawer as a child of this popup."""

        try:
            lower_bound = float(self.lowerInput.get())
            upper_bound = float(self.upperInput.get())
        except ValueError:
            messagebox.showerror(self.main_app.text_content["global"]["error"], self.main_app.text_content["options_menu"]["playback_menu"]["randomized_delay_settings"]["error_new_value"])
            return

        if lower_bound > upper_bound:
            lower_bound, upper_bound = upper_bound, lower_bound

        DistributionDrawer(self, self.main_app, lower_bound, upper_bound, self.distribution)

    def setNewValues(self, lower_bound, upper_bound, main_app):
        """Set the new Randomized Delay values."""
        try:
            lower_bound = float(lower_bound)
            upper_bound = float(upper_bound)
        except ValueError:
            messagebox.showerror(main_app.text_content["global"]["error"], main_app.text_content["options_menu"]["playback_menu"]["randomized_delay_settings"]["error_new_value"])
            return
        if lower_bound > upper_bound:
            lower_bound, upper_bound = upper_bound, lower_bound
        enabled = lower_bound != 0 or upper_bound != 0
        self.settings.change_settings("Playback", "Randomized_Delay", None, {
                "Enabled": enabled,
                "Lower": lower_bound,
                "Upper": upper_bound,
                "Distribution": self.distribution
            }
        )
        self.destroy()
