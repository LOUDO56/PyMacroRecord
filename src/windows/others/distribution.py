import math
from tkinter import BOTTOM, LEFT, RIGHT, TOP, Canvas, IntVar, Scrollbar, Spinbox, StringVar
from tkinter.ttk import Button, Combobox, Frame, Label

from windows.popup import Popup


class DistributionDrawer(Popup):
    """
    Visual distribution editor.

    The curve is stored as normalized points:
        [x, y]

    X is the position between Lower and Upper.
    Y is how common / likely that value should be.

    Drawing is non-destructive: drawing over an existing curve only replaces
    the portion covered by the new stroke. Right-click dragging erases the
    covered portion. Green points are individually draggable vertically.
    """

    CANVAS_WIDTH = 560
    CANVAS_HEIGHT = 280
    CONTROL_WIDTH = 230
    EDIT_RADIUS_X = 0.012
    ERASE_RADIUS_X = 0.018
    POINT_HIT_RADIUS_PX = 9
    LINEAR_EDGE_OFFSET = 0.06
    PRESET_SAMPLE_COUNT = 256

    USER_POINT_COLOR = "#4a890b"
    INTERPOLATED_COLOR = "#4a0b89"
    GRID_COLOR = "#d9d9d9"
    ZERO_GRID_COLOR = "#b5b5b5"

    PRESET_KEYS = ("freehand", "linear", "bell")
    INTERPOLATION_KEYS = ("sharp", "curves")

    def __init__(self, parent, main_app, lower_bound, upper_bound, distribution=None):
        self.owner = parent
        self.main_app = main_app
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self.points = []
        self._user_points = []
        self._stroke = []
        self._editing = False
        self._erasing = False
        self._dragged_user_index = None
        self._dragged_user_point = None
        self._controls_scroll_update_scheduled = False

        settings = main_app.text_content["options_menu"]["playback_menu"]["distribution_drawer_settings"]
        super().__init__(settings["title"], 900, 540, parent)

        main_app.prevent_record = True
        self.settings = settings
        self.interpolation_var = StringVar()
        self.preset_var = StringVar()

        Label(self, text=settings["distribution_instruction_text"], font=("Segoe UI", 10)).pack(side=TOP, pady=(10, 8))

        button_area = Frame(self)
        Button(button_area, text=main_app.text_content["global"]["confirm_button"], command=self.apply).pack(side=LEFT, padx=5)
        Button(button_area, text=main_app.text_content["global"]["cancel_button"], command=self.destroy).pack(side=LEFT, padx=5)
        button_area.pack(side=BOTTOM, pady=8)

        content = Frame(self)
        content.pack(fill="both", expand=True, padx=15, pady=(0, 4))

        graph_frame = Frame(content)
        graph_frame.pack(side=LEFT, fill="both", expand=True)

        axis_information = settings["axis_information"]
        vertical_high_label = Label(graph_frame, text=axis_information["vertical"]["high_text"],)
        vertical_high_label.pack(side=TOP, pady=(0, 2))
        
        canvas_frame = Frame(graph_frame, relief="solid", borderwidth=1)
        canvas_frame.pack()

        self.canvas = Canvas(canvas_frame, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, highlightthickness=0, cursor="crosshair",)
        self.canvas.pack()
        self._draw_grid()

        info_area = Frame(graph_frame)
        horizontal_low_label = Label(info_area, text=settings["axis_information"]["horizontal"]["low_value_text"].format(value=self._format_number(lower_bound)),)
        horizontal_low_label.pack(side=LEFT)
        horizontal_high_label = Label(info_area, text=settings["axis_information"]["horizontal"]["high_value_text"].format(value=self._format_number(upper_bound)),)
        horizontal_high_label.pack(side=RIGHT)
        info_area.pack(fill="x", pady=(4, 0))

        vertical_low_label = Label(graph_frame, text=axis_information["vertical"]["low_text"],)
        vertical_low_label.pack(side=TOP, pady=(2, 0))
        Label(graph_frame, text=settings["help_instructions_text"], foreground="#666666",).pack(side=TOP, pady=(6, 0))

        control_frame = Frame(content, relief="solid", borderwidth=1, padding=0)
        control_frame.pack(side=RIGHT, fill="y", padx=(15, 0))

        self.control_canvas = Canvas(control_frame, width=self.CONTROL_WIDTH, highlightthickness=0, borderwidth=0)
        self.control_scrollbar = Scrollbar(control_frame, orient="vertical", command=self.control_canvas.yview)
        self.control_canvas.configure(yscrollcommand=self.control_scrollbar.set)
        self.control_canvas.pack(side=LEFT, fill="both", expand=True)

        controls_inner = Frame(self.control_canvas, padding=10)
        controls_window = self.control_canvas.create_window((0, 0), window=controls_inner, anchor="nw",)

        self.controls_inner = controls_inner
        self._controls_window = controls_window
        controls_inner.bind("<Configure>", self._update_controls_scroll_region)
        self.control_canvas.bind("<Configure>", self._resize_controls_inner)
        self._schedule_controls_scroll_update()
        self.control_canvas.bind("<MouseWheel>", self._scroll_controls, add="+")
        self.control_canvas.bind("<Button-4>", self._scroll_controls_up, add="+")
        self.control_canvas.bind("<Button-5>", self._scroll_controls_down, add="+")

        settings_information = settings["settings_information"]
        Label(controls_inner, text=settings_information["header_text"], font=("Segoe UI", 10, "bold"),).pack(anchor="w", pady=(0, 10))

        Label(controls_inner, text=settings_information["preset_text"]).pack(anchor="w")

        preset_labels = {
            key: settings["presets"][key]["label_text"] for key in self.PRESET_KEYS
        }
        self._preset_key_by_label = {
            label: key for key, label in preset_labels.items()
        }
        self._preset_label_by_key = preset_labels

        self.preset_var.set(preset_labels["freehand"])
        self.preset_box = Combobox(controls_inner, textvariable=self.preset_var, values=list(preset_labels.values()), state="readonly", width=18,)
        self.preset_box.pack(fill="x", pady=(2, 2))
        self.preset_box.bind("<<ComboboxSelected>>", self.apply_selected_preset)
        
        self.preset_description = Label(controls_inner, text=self._preset_description("freehand"), wraplength=195, justify="left", foreground="#555555",)
        self.preset_description.pack(anchor="w", pady=(0, 4))

        self.preset_note = Label(controls_inner, text=self._preset_note("freehand"), wraplength=195, justify="left", foreground="#555555",)
        self.preset_note.pack(anchor="w", pady=(0, 12))

        self.bell_frame = Frame(controls_inner)
        self._build_bell_controls(self.bell_frame)

        Label(controls_inner, text=settings_information["interpolate_text"]).pack(anchor="w", pady=(4, 0))
        interpolation_labels = {
            key: settings_information["interpolation_types"][key]["label_text"]
            for key in self.INTERPOLATION_KEYS
        }
        self._interpolation_key_by_label = {
            label: key for key, label in interpolation_labels.items()
        }
        self._interpolation_label_by_key = interpolation_labels

        self.interpolation_box = Combobox(controls_inner, textvariable=self.interpolation_var, values=list(interpolation_labels.values()), state="readonly", width=18,)
        self.interpolation_box.pack(fill="x", pady=(2, 2))
        self.interpolation_box.bind("<<ComboboxSelected>>", self._on_interpolation_changed,)
        self.interpolation_var.set(interpolation_labels["curves"])
        
        interpolate_button = Button(controls_inner, text=settings_information["interpolate_button_text"], command=self.interpolate_missing,)
        interpolate_button.pack(fill="x", pady=(10, 4))
        
        clear_button = Button(controls_inner, text=settings_information["clear_text"], command=self.clear,)
        clear_button.pack(fill="x", pady=4)
        
        self._bind_control_scroll(controls_inner)

        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.finish_drawing)
        self.canvas.bind("<Button-3>", self.start_erasing)
        self.canvas.bind("<B3-Motion>", self.erase)
        self.canvas.bind("<ButtonRelease-3>", self.finish_erasing)

        self.load_distribution(distribution)

        self.control_canvas.yview_moveto(0)
        self._schedule_controls_scroll_update()
        self.wait_window()
        main_app.prevent_record = False

    def _update_controls_scroll_region(self, _event=None):
        self.control_canvas.configure(scrollregion=self.control_canvas.bbox("all"))
        self._schedule_controls_scroll_update()

    def _resize_controls_inner(self, event):
        self.control_canvas.itemconfigure(self._controls_window, width=event.width)
        self._update_controls_scroll_region()

    def _schedule_controls_scroll_update(self):
        if self._controls_scroll_update_scheduled:
            return
        self._controls_scroll_update_scheduled = True
        self.after_idle(self._update_controls_scroll_state)

    def _update_controls_scroll_state(self):
        self._controls_scroll_update_scheduled = False
        bbox = self.control_canvas.bbox("all")
        if bbox is None:
            return

        content_height = bbox[3] - bbox[1]
        canvas_height = self.control_canvas.winfo_height()
        needs_scroll = content_height > canvas_height + 1

        if needs_scroll and not self.control_scrollbar.winfo_ismapped():
            self.control_scrollbar.pack(side=RIGHT, fill="y")
            self.control_canvas.update_idletasks()
            self.control_canvas.itemconfigure(self._controls_window, width=self.control_canvas.winfo_width())
            self.control_canvas.configure(scrollregion=self.control_canvas.bbox("all"))
            return

        if not needs_scroll and self.control_scrollbar.winfo_ismapped():
            self.control_scrollbar.pack_forget()
            self.control_canvas.update_idletasks()
            self.control_canvas.itemconfigure(self._controls_window, width=self.control_canvas.winfo_width())
            self.control_canvas.configure(scrollregion=self.control_canvas.bbox("all"))
            self.control_canvas.yview_moveto(0)

    def _has_control_scroll(self):
        bbox = self.control_canvas.bbox("all")
        if bbox is None:
            return False
        return (bbox[3] - bbox[1]) > self.control_canvas.winfo_height() + 1

    def _scroll_controls(self, event):
        if not self._has_control_scroll():
            return
        delta = event.delta or 0
        self.control_canvas.yview_scroll(int(-1 * delta / 120), "units")

    def _scroll_controls_up(self, _event=None):
        if self._has_control_scroll():
            self.control_canvas.yview_scroll(-1, "units")

    def _scroll_controls_down(self, _event=None):
        if self._has_control_scroll():
            self.control_canvas.yview_scroll(1, "units")

    def _control_canvas_yview(self, *args):
        self.control_canvas.yview(*args)
        self.after_idle(self._update_controls_scroll_state)

    def _bind_control_scroll(self, widget):
        widget.bind("<MouseWheel>", self._scroll_controls, add="+")
        widget.bind("<Button-4>", self._scroll_controls_up, add="+")
        widget.bind("<Button-5>", self._scroll_controls_down, add="+")
        for child in widget.winfo_children():
            self._bind_control_scroll(child)

    def _build_bell_controls(self, parent):
        bell_settings = self.settings["presets"]["bell"]["controls"]

        Label(parent, text=bell_settings["header_text"], font=("Segoe UI", 9, "bold"),).pack(anchor="w", pady=(0, 6))

        self.bell_center_var = IntVar(value=50)
        self.bell_width_var = IntVar(value=20)
        self.bell_tail_magnitude_var = IntVar(value=0)
        self.bell_peaks_var = IntVar(value=1)

        self._add_spin_control(parent, bell_settings["center_text"], self.bell_center_var, 0, 100, bell_settings["center_tooltip_text"],)
        self._add_spin_control(parent, bell_settings["width_text"], self.bell_width_var, 1, 100, bell_settings["width_tooltip_text"],)
        self._add_spin_control(parent, bell_settings["tail_magnitude_text"], self.bell_tail_magnitude_var, 0, 100, bell_settings["tail_magnitude_tooltip_text"],)

        Label(parent, text=bell_settings["tail_side_text"]).pack(anchor="w", pady=(5, 1))

        tail_side_labels = {
            "negative": bell_settings["tail_side_negative_text"],
            "positive": bell_settings["tail_side_positive_text"],
        }
        self._tail_side_key_by_label = {
            label: key for key, label in tail_side_labels.items()
        }
        self._tail_side_label_by_key = tail_side_labels

        self.bell_tail_side_var = StringVar(value=tail_side_labels["positive"])
        tail_side_box = Combobox(parent, textvariable=self.bell_tail_side_var, values=list(tail_side_labels.values()), state="readonly", width=18,)
        tail_side_box.pack(fill="x", pady=(1, 2))
        
        self._add_spin_control(parent, bell_settings["peaks_text"], self.bell_peaks_var, 0, 12, bell_settings["peaks_tooltip_text"],)

        reset_button = Button(parent, text=bell_settings["reset_text"], command=self.reset_bell_settings,)
        reset_button.pack(fill="x", pady=(6, 4))
        
        apply_button = Button(parent, text=bell_settings["apply_text"], command=self.apply_bell_settings,)
        apply_button.pack(fill="x", pady=(0, 8))
        
    def _add_spin_control(self, parent, label_text, variable, minimum, maximum, tooltip):
        Label(parent, text=label_text).pack(anchor="w", pady=(3, 1))
        spinbox = Spinbox(parent, textvariable=variable, from_=minimum, to=maximum, increment=1, width=18,)
        spinbox.pack(fill="x", pady=(0, 1))
        
    def _preset_description(self, key):
        return self.settings["presets"][key]["description_text"]

    def _preset_note(self, key):
        return self.settings["presets"][key]["note_text"]

    def _selected_preset_key(self):
        return self._preset_key_by_label[self.preset_var.get()]

    def _selected_interpolation_key(self):
        return self._interpolation_key_by_label[self.interpolation_var.get()]

    def _on_interpolation_changed(self, _event=None):
        self.redraw()

    def start_drawing(self, event):
        dragged_index = self._find_user_point(event.x, event.y)
        if dragged_index is not None:
            self._editing = True
            self._erasing = False
            self._dragged_user_index = dragged_index
            self._dragged_user_point = self._user_points[dragged_index]
            return

        self._dragged_user_index = None
        self._dragged_user_point = None
        self._editing = True
        self._erasing = False
        self._stroke = [
            (self._canvas_to_normalized_x(event.x),
                self._canvas_to_normalized_y(event.y),)
        ]
        self.redraw()

    def draw(self, event):
        if not self._editing or self._erasing:
            return

        if self._dragged_user_index is not None:
            self._drag_user_point(event.y)
            self.redraw()
            return

        self._stroke.append((self._canvas_to_normalized_x(event.x), self._canvas_to_normalized_y(event.y),))
        self._merge_stroke_into_curve()
        self.redraw()

    def finish_drawing(self, event):
        if not self._editing or self._erasing:
            return

        if self._dragged_user_index is not None:
            self._drag_user_point(event.y)
            self._dragged_user_index = None
            self._dragged_user_point = None
            self._editing = False
            self.redraw()
            return

        self._stroke.append((self._canvas_to_normalized_x(event.x), self._canvas_to_normalized_y(event.y),))
        self._merge_stroke_into_curve()
        self._stroke = []
        self._editing = False
        self.points = self._normalize_points(self.points)
        self._user_points = self._normalize_points(self._user_points)
        self.redraw()

    def _find_user_point(self, canvas_x, canvas_y):
        best_index = None
        best_distance = self.POINT_HIT_RADIUS_PX

        for index, (x, y) in enumerate(self._user_points):
            point_x, point_y = self._normalized_to_canvas(x, y)
            distance = math.hypot(point_x - canvas_x, point_y - canvas_y)
            if distance <= best_distance:
                best_index = index
                best_distance = distance

        return best_index

    def _drag_user_point(self, canvas_y):
        if self._dragged_user_index is None:
            return

        old_x, old_y = self._dragged_user_point
        new_y = self._canvas_to_normalized_y(canvas_y)
        self._user_points[self._dragged_user_index] = (old_x, new_y)

        for index, (point_x, point_y) in enumerate(self.points):
            if abs(point_x - old_x) < 0.002 and abs(point_y - old_y) < 0.01:
                self.points[index] = (point_x, new_y)
                break

        self._dragged_user_point = (old_x, new_y)

    def start_erasing(self, event):
        self._editing = True
        self._erasing = True
        self._dragged_user_index = None
        self._dragged_user_point = None
        self._erase_at(event.x, event.y)
        self.redraw()

    def erase(self, event):
        if not self._editing or not self._erasing:
            return
        self._erase_at(event.x, event.y)
        self.redraw()

    def finish_erasing(self, _event):
        self._stroke = []
        self._editing = False
        self._erasing = False
        self._dragged_user_index = None
        self._dragged_user_point = None
        self.points = self._normalize_points(self.points)
        self._user_points = self._normalize_points(self._user_points)
        self.redraw()

    def _merge_stroke_into_curve(self):
        if not self._stroke:
            return
        stroke = self._normalize_points(self._stroke)
        if not stroke:
            return

        stroke_min = stroke[0][0]
        stroke_max = stroke[-1][0]

        if not self.points:
            self.points = stroke
            self._user_points = stroke.copy()
            return

        left_y = self._interpolate(self.points, stroke_min)
        right_y = self._interpolate(self.points, stroke_max)
        merged = [
            (x, y)
            for x, y in self.points
            if x < stroke_min or x > stroke_max
        ]

        if not any(abs(x - stroke_min) < 1e-6 for x, _ in merged):
            merged.append((stroke_min, left_y))
        if not any(abs(x - stroke_max) < 1e-6 for x, _ in merged):
            merged.append((stroke_max, right_y))

        merged.extend(stroke)
        self.points = self._normalize_points(merged)

        self._user_points = [
            (x, y)
            for x, y in self._user_points
            if x < stroke_min or x > stroke_max
        ]
        self._user_points.extend(stroke)
        self._user_points = self._normalize_points(self._user_points)

    def _erase_at(self, canvas_x, canvas_y):
        x = self._canvas_to_normalized_x(canvas_x)
        y = self._canvas_to_normalized_y(canvas_y)

        self.points = [
            (px, py)
            for px, py in self.points
            if abs(px - x) > self.ERASE_RADIUS_X or abs(py - y) > 0.08
        ]
        self._user_points = [
            (px, py)
            for px, py in self._user_points
            if abs(px - x) > self.ERASE_RADIUS_X or abs(py - y) > 0.08
        ]

    def _canvas_to_normalized_x(self, x):
        x = max(0, min(self.CANVAS_WIDTH, x))
        return x / self.CANVAS_WIDTH

    def _canvas_to_normalized_y(self, y):
        y = max(0, min(self.CANVAS_HEIGHT, y))
        return 1.0 - (y / self.CANVAS_HEIGHT)

    def _canvas_to_normalized(self, x, y):
        return self._canvas_to_normalized_x(x), self._canvas_to_normalized_y(y)

    def _normalized_to_canvas(self, x, y):
        return x * self.CANVAS_WIDTH, (1.0 - y) * self.CANVAS_HEIGHT

    def _draw_grid(self):
        self.canvas.delete("grid")

        for index in range(11):
            x = self.CANVAS_WIDTH * index / 10
            self.canvas.create_line(x, 0, x, self.CANVAS_HEIGHT, fill=self.GRID_COLOR, tags="grid",)

        for index in range(11):
            y = self.CANVAS_HEIGHT * (1.0 - index / 10)
            self.canvas.create_line(0, y, self.CANVAS_WIDTH, y, fill=self.GRID_COLOR, tags="grid",)

        span = self.upper_bound - self.lower_bound
        if span <= 0 or not (self.lower_bound <= 0 <= self.upper_bound):
            return

        zero_x = ((0 - self.lower_bound) / span) * self.CANVAS_WIDTH
        nearest_tenth = round(zero_x / (self.CANVAS_WIDTH / 10))
        if abs(zero_x - nearest_tenth * (self.CANVAS_WIDTH / 10)) > 1:
            self.canvas.create_line(zero_x, 0, zero_x, self.CANVAS_HEIGHT, fill=self.ZERO_GRID_COLOR, tags="grid",)

    def _normalize_points(self, points):
        if not points:
            return []

        cleaned = []
        for x, y in points:
            x = max(0.0, min(1.0, float(x)))
            y = max(0.0, min(1.0, float(y)))
            cleaned.append((x, y))

        cleaned.sort(key=lambda point: point[0])

        merged = []
        for x, y in cleaned:
            if merged and abs(merged[-1][0] - x) < 0.002:
                old_x, old_y = merged[-1]
                merged[-1] = ((old_x + x) / 2, (old_y + y) / 2)
            else:
                merged.append((x, y))
        return merged

    def _is_user_point(self, point):
        x, y = point
        return any(abs(user_x - x) < 0.003 and abs(user_y - y) < 0.003 for user_x, user_y in self._user_points)

    def redraw(self):
        self.canvas.delete("distribution")

        if self.points:
            coords = []
            for x, y in self.points:
                canvas_x, canvas_y = self._normalized_to_canvas(x, y)
                coords.extend((canvas_x, canvas_y))

            if len(coords) >= 4:
                self.canvas.create_line(*coords, width=3, smooth=self._selected_interpolation_key() == "curves", splinesteps=12, fill=self.INTERPOLATED_COLOR, tags="distribution",)
            else:
                x, y = self._normalized_to_canvas(self.points[0][0], self.points[0][1],)
                self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=self.USER_POINT_COLOR, outline=self.USER_POINT_COLOR, tags="distribution",)

            for x, y in self.points:
                if not self._is_user_point((x, y)):
                    continue
                canvas_x, canvas_y = self._normalized_to_canvas(x, y)
                radius = 4 if self._dragged_user_index is not None else 3
                self.canvas.create_oval(canvas_x - radius, canvas_y - radius, canvas_x + radius, canvas_y + radius, fill=self.USER_POINT_COLOR, outline=self.USER_POINT_COLOR, tags="distribution",)

        if len(self._stroke) >= 2:
            stroke_coords = []
            for x, y in self._stroke:
                stroke_coords.extend(self._normalized_to_canvas(x, y))

            self.canvas.create_line(*stroke_coords, width=3, dash=(5, 3), fill=self.USER_POINT_COLOR, tags="distribution",)

            for x, y in self._stroke:
                canvas_x, canvas_y = self._normalized_to_canvas(x, y)
                radius = 3
                self.canvas.create_oval(canvas_x - radius, canvas_y - radius, canvas_x + radius, canvas_y + radius, fill=self.USER_POINT_COLOR, outline=self.USER_POINT_COLOR, tags="distribution",)

    def load_distribution(self, distribution):
        if not distribution:
            return

        try:
            points = []
            for point in distribution:
                if len(point) != 2:
                    continue
                x = max(0.0, min(1.0, float(point[0])))
                y = max(0.0, min(1.0, float(point[1])))
                points.append((x, y))

            self.points = self._normalize_points(points)
            self._user_points = self.points.copy()
            self.redraw()
        except (TypeError, ValueError):
            self.points = []
            self._user_points = []

    def clear(self):
        self.points = []
        self._user_points = []
        self._stroke = []
        self._dragged_user_index = None
        self._dragged_user_point = None
        self.redraw()

    def apply_selected_preset(self, _event=None):
        key = self._selected_preset_key()
        self.preset_description.config(text=self._preset_description(key))
        self.preset_note.config(text=self._preset_note(key))

        if key == "freehand":
            self.bell_frame.pack_forget()
            return

        if key == "bell":
            self.bell_frame.pack(fill="x", pady=(0, 6))
            self.apply_bell_settings()
            return

        self.bell_frame.pack_forget()
        self.points = self._make_linear_preset()
        self._user_points = self._linear_control_points()
        self._stroke = []
        self._dragged_user_index = None
        self._dragged_user_point = None
        self.redraw()

    def reset_bell_settings(self):
        if self._selected_preset_key() != "bell":
            return

        bell_settings = self.settings["presets"]["bell"]["controls"]
        self.bell_center_var.set(50)
        self.bell_width_var.set(20)
        self.bell_tail_magnitude_var.set(0)
        self.bell_tail_side_var.set(bell_settings["tail_side_positive_text"])
        self.bell_peaks_var.set(1)
        self.apply_bell_settings()

    def apply_bell_settings(self):
        if self._selected_preset_key() != "bell":
            return

        self.points, self._user_points = self._make_bell_preset(center_percent=self.bell_center_var.get(), width_percent=self.bell_width_var.get(), tail_magnitude_percent=self.bell_tail_magnitude_var.get(), tail_side=self._tail_side_key_by_label[self.bell_tail_side_var.get()], peak_count=self.bell_peaks_var.get(),)
        self._stroke = []
        self._dragged_user_index = None
        self._dragged_user_point = None
        self.redraw()

    def _linear_control_points(self):
        edge = self.LINEAR_EDGE_OFFSET
        return [
            (0.0, 0.5),
            (edge, 0.5),
            (1.0 - edge, 0.5),
            (1.0, 0.5),
        ]

    def _make_linear_preset(self):
        return self._normalize_points(self._linear_control_points())

    def _make_bell_preset(self,
        center_percent,
        width_percent,
        tail_magnitude_percent,
        tail_side,
        peak_count,):
        peak_count = max(0, int(peak_count))
        if peak_count == 0:
            points = self._make_linear_preset()
            return points, self._linear_control_points()

        center = max(0.0, min(1.0, int(center_percent) / 100.0))
        width = max(0.01, min(1.0, int(width_percent) / 100.0))
        tail_magnitude = max(0.0, min(1.0, int(tail_magnitude_percent) / 100.0),)

        centers = self._bell_centers(center, width, peak_count)
        sigma = max(0.006, width * 0.30)

        raw = []
        for index in range(self.PRESET_SAMPLE_COUNT):
            x = index / (self.PRESET_SAMPLE_COUNT - 1)
            y = 0.0
            for peak_center in centers:
                y += self._asymmetric_gaussian(x, peak_center, sigma, tail_magnitude, tail_side,)
            raw.append((x, y))

        max_y = max(y for _, y in raw)
        if max_y > 0:
            raw = [(x, y / max_y) for x, y in raw]

        control_points = []
        for peak_center in centers:
            peak_y = self._interpolate(raw, peak_center)
            control_points.append((peak_center, peak_y))

        self._add_bell_tail_control_points(control_points, centers, sigma, center,)

        return self._normalize_points(raw), self._normalize_points(control_points)

    @staticmethod
    def _bell_centers(center, width, peak_count):
        if peak_count <= 1:
            return [center]

        span = min(0.82, max(0.12, width * 4.0))
        left = center - (span / 2.0)
        right = center + (span / 2.0)

        if left < 0:
            right -= left
            left = 0.0
        if right > 1:
            left -= right - 1.0
            right = 1.0

        left = max(0.0, left)
        right = min(1.0, right)

        return [
            left + (right - left) * index / (peak_count - 1)
            for index in range(peak_count)
        ]

    @staticmethod
    def _asymmetric_gaussian(x,
        center,
        sigma,
        tail_magnitude,
        tail_side,):
        effective_sigma = sigma
        if tail_magnitude > 0:
            if tail_side == "negative" and x < center:
                effective_sigma *= 1.0 - (0.85 * tail_magnitude)
            elif tail_side == "positive" and x > center:
                effective_sigma *= 1.0 - (0.85 * tail_magnitude)

        effective_sigma = max(0.001, effective_sigma)
        distance = x - center
        return math.exp(-0.5 * (distance / effective_sigma) ** 2)

    def _add_bell_tail_control_points(self, control_points, centers, sigma, center):
        for peak_center in centers:
            control_points.append((max(0.0, peak_center - sigma * 1.5), self._bell_control_y(peak_center - sigma * 1.5, centers, sigma, center,),))
            control_points.append((min(1.0, peak_center + sigma * 1.5), self._bell_control_y(peak_center + sigma * 1.5, centers, sigma, center,),))

    def _bell_control_y(self, x, centers, sigma, center):
        value = 0.0
        for peak_center in centers:
            value += math.exp(-0.5 * ((x - peak_center) / max(0.001, sigma)) ** 2)
        return min(1.0, value)

    def interpolate_missing(self):
        if len(self.points) < 2:
            return

        sample_count = self.PRESET_SAMPLE_COUNT
        result = []
        for index in range(sample_count):
            x = index / (sample_count - 1)
            y = self._interpolate(self.points, x)
            result.append((x, max(0.0, min(1.0, y))))

        self.points = result
        self._user_points = self._normalize_points(self._user_points)
        self.redraw()

    def apply(self):
        if not self.points:
            self.owner.distribution = None
            self.destroy()
            return

        distribution = self._resample_distribution()
        self.owner.distribution = distribution
        self.destroy()

    def _resample_distribution(self):
        points = self._normalize_points(self.points)
        if len(points) < 2:
            return None

        if self._selected_interpolation_key() == "curves":
            return [
                [
                    round(index / (self.PRESET_SAMPLE_COUNT - 1), 6),
                    round(max(0.0, min(1.0, self._interpolate(points, index / (self.PRESET_SAMPLE_COUNT - 1),),),), 6,),
                ]
                for index in range(self.PRESET_SAMPLE_COUNT)
            ]

        return [
            [round(x, 6), round(max(0.0, min(1.0, y)), 6)]
            for x, y in points
        ]

    def _interpolate(self, points, x):
        if not points:
            return 0.0
        if len(points) == 1:
            return points[0][1]
        if x <= points[0][0]:
            return points[0][1]
        if x >= points[-1][0]:
            return points[-1][1]

        for index in range(1, len(points)):
            x1, y1 = points[index - 1]
            x2, y2 = points[index]
            if x <= x2:
                if x2 == x1:
                    return y2
                if self._selected_interpolation_key() == "sharp":
                    amount = (x - x1) / (x2 - x1)
                    return y1 + ((y2 - y1) * amount)
                return self._catmull_rom_y(points, index - 1, x)

        return points[-1][1]

    @staticmethod
    def _catmull_rom_y(points, segment_start_index, x):
        p0 = points[max(0, segment_start_index - 1)]
        p1 = points[segment_start_index]
        p2 = points[segment_start_index + 1]
        p3 = points[min(len(points) - 1, segment_start_index + 2)]

        x1, y1 = p1
        x2, y2 = p2
        if x2 == x1:
            return y2

        t = (x - x1) / (x2 - x1)
        t2 = t * t
        t3 = t2 * t

        # Catmull-Rom is applied in local segment coordinates. Using the
        # neighboring Y values controls the curve while X remains normalized.
        y0 = p0[1]
        y1 = p1[1]
        y2 = p2[1]
        y3 = p3[1]
        value = 0.5 * ((2.0 * y1)
            + (-y0 + y2) * t
            + (2.0 * y0 - 5.0 * y1 + 4.0 * y2 - y3) * t2
            + (-y0 + 3.0 * y1 - 3.0 * y2 + y3) * t3)
        return max(0.0, min(1.0, value))

    @staticmethod
    def _format_number(value):
        if float(value).is_integer():
            return str(int(value))
        return str(value)
