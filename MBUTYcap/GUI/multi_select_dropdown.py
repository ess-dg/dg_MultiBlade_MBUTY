# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 09:27:20 2025

@author: sheilamonera
"""
import tkinter as tk
import tkinter.font as tkfont
from .info_label import InfoLabel
from .base_constants import FIXED_INPUT_WIDTH

class MultiSelectDropDown:
    """
    A dropdown widget that allows selecting multiple items, displayed as tags.

    Parameters:
        parent (tk.Widget): The parent container.
        row (int): The grid row for widget placement.
        label_text (str): Label text shown to the left of the dropdown.
        options (list[str]): List of selectable options.
        default (list[str], optional): List of initially selected items.
        info_text (str, optional): Tooltip text for the label.
    """

    def __init__(self, parent, row, label_text, options, default=None, info_text=None):
        self.options = options
        self.selected = set(default) if default else set()
        self.filtered_options = options[:]
        self.parent = parent
        self.is_open = False
        self.dropdown_win = None
        self.listbox = None
        self.dropdown_width = None

        InfoLabel(parent, label_text, info=info_text).grid(row=row, column=0, sticky="nw", padx=5, pady=5)

        self.wrapper = tk.Frame(parent, bd=1, relief="solid", width=FIXED_INPUT_WIDTH)
        self.wrapper.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        parent.grid_columnconfigure(1, weight=1)

        self.tags_frame = tk.Frame(self.wrapper)
        self.entry_wrapper = tk.Frame(self.wrapper)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.entry_wrapper, textvariable=self.entry_var, borderwidth=0)
        self.entry.pack(side=tk.LEFT, fill="x", expand=True)

        self.toggle_btn = tk.Button(self.entry_wrapper, text="▼", width=2, command=self.toggle_dropdown)
        self.toggle_btn.pack(side=tk.LEFT)

        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<Button-1>", self.show_dropdown, add="+")
        self.entry.bind("<Return>", self.add_first_match)

        self.root = parent.winfo_toplevel()
        self.canvas = self._find_canvas(parent)
        self.root.bind_all("<Button-1>", self.handle_click_outside, add="+")

        self.entry_wrapper.pack(side=tk.BOTTOM, fill="x")
        self.refresh_tags()
        self.validate_selection()

    def _find_canvas(self, widget):
        while widget:
            if isinstance(widget, tk.Canvas):
                return widget
            widget = widget.master
        return None

    def toggle_dropdown(self):
        if self.is_open:
            self.hide_dropdown()
        else:
            self.show_dropdown()

    def show_dropdown(self, event=None):
        if self.dropdown_win:
            return

        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()

        font = tkfont.Font(font=self.entry.cget("font"))
        longest = max(self.filtered_options, key=lambda s: font.measure(s), default="")
        px_width = font.measure(longest) + 40
        char_width = max(int(px_width / font.measure("0")), 20)

        root_width = self.root.winfo_width()
        max_width = self.root.winfo_rootx() + root_width - x
        self.dropdown_width = min(int(px_width), max_width)

        self.dropdown_win = tk.Toplevel(self.parent)
        self.dropdown_win.overrideredirect(True)
        self.dropdown_win.attributes("-topmost", True)
        self.dropdown_win.geometry(f"{self.dropdown_width}x100+{x}+{y}")

        self.listbox = tk.Listbox(
            self.dropdown_win,
            height=5,
            width=char_width,
            selectmode="multiple",
            exportselection=False,
            takefocus=0
        )
        self.listbox.pack(fill="both", expand=True)
        self.listbox.update_idletasks()
        self.listbox.config(width=char_width)

        self.listbox.bind("<ButtonRelease-1>", self.on_select)
        self.listbox.bind("<Return>", self.add_selected_from_listbox)

        self.update_listbox()
        self.is_open = True
        self._update_dropdown_position()
        self.entry.after_idle(self.entry.focus_set)

    def _update_dropdown_position(self):
        if not self.dropdown_win or not self.entry.winfo_ismapped():
            self.hide_dropdown()
            return

        try:
            entry_x_on_screen = self.entry.winfo_rootx()
            entry_y_on_screen = self.entry.winfo_rooty()
            entry_height = self.entry.winfo_height()

            dropdown_target_x = entry_x_on_screen
            dropdown_target_y = entry_y_on_screen + entry_height

            width = self.dropdown_width or self.wrapper.winfo_width()
            self.dropdown_win.geometry(f"{width}x100+{dropdown_target_x}+{dropdown_target_y}")

            if self.canvas and self.canvas.winfo_ismapped():
                canvas_visible_top_on_screen = self.canvas.winfo_rooty()
                canvas_visible_bottom_on_screen = canvas_visible_top_on_screen + self.canvas.winfo_height()
                dropdown_bottom = dropdown_target_y + self.listbox.winfo_height()
                if (dropdown_bottom < canvas_visible_top_on_screen or
                        dropdown_target_y > canvas_visible_bottom_on_screen):
                    self.hide_dropdown()
                    return

            if self.is_open:
                self.entry.after(100, self._update_dropdown_position)

        except Exception as e:
            print(f"Dropdown positioning error: {e}")
            if self.is_open:
                self.entry.after(100, self._update_dropdown_position)

    def update_listbox(self):
        if not self.listbox:
            return

        self.listbox.delete(0, tk.END)

        font = tkfont.Font(font=self.entry.cget("font"))
        longest = max(self.filtered_options, key=lambda s: font.measure(s), default="")
        pixel_width = font.measure(longest) + 40
        char_width = max(int(pixel_width / font.measure("0")), 20)
        self.listbox.config(width=char_width)

        for i, option in enumerate(self.filtered_options):
            self.listbox.insert(tk.END, option)
            if option in self.selected:
                self.listbox.itemconfigure(i, background='#ADD8E6')
            else:
                self.listbox.itemconfigure(i, background='white')

    def on_entry_key(self, event=None):
        typed = self.entry_var.get().strip().lower()
        self.filtered_options = [opt for opt in self.options if typed in opt.lower()]
        self.show_dropdown()
        self.update_listbox()

    def on_select(self, event=None):
        if not self.listbox:
            return
        try:
            clicked_index = self.listbox.nearest(event.y)
            clicked_item = self.listbox.get(clicked_index)
        except ValueError:
            return

        if clicked_item in self.selected:
            self.selected.discard(clicked_item)
        else:
            self.selected.add(clicked_item)

        self.refresh_tags()
        self.update_listbox()
        self.validate_selection()
        self.entry.focus_set()

    def add_selected_from_listbox(self, event=None):
        if self.listbox and self.listbox.curselection():
            selected_idx = self.listbox.curselection()[0]
            selected_item = self.listbox.get(selected_idx)
            if selected_item not in self.selected:
                self.selected.add(selected_item)

        self.entry_var.set("")
        self.refresh_tags()
        self.hide_dropdown()
        self.validate_selection()

    def add_first_match(self, event=None):
        if self.filtered_options:
            item_to_add = self.filtered_options[0]
            if item_to_add not in self.selected:
                self.selected.add(item_to_add)
            self.entry_var.set("")
            self.refresh_tags()
            self.hide_dropdown()
            self.validate_selection()

    def refresh_tags(self):
        for widget in self.tags_frame.winfo_children():
            widget.destroy()

        if not self.selected:
            self.tags_frame.pack_forget()
        else:
            try:
                self.tags_frame.pack(side=tk.TOP, anchor="w", fill="x")
            except tk.TclError:
                pass

            for item in sorted(self.selected):
                tag = tk.Frame(self.tags_frame, bd=1, relief="ridge", padx=2, pady=1)
                tk.Label(tag, text=item, font=("Segoe UI", 9),
                         wraplength=FIXED_INPUT_WIDTH - 40, justify="left").pack(side=tk.LEFT)
                tk.Button(tag, text="✕", command=lambda i=item: self.remove_tag(i),
                          padx=1, pady=0, font=("Segoe UI", 8), width=2).pack(side=tk.LEFT)
                tag.pack(fill="x", pady=2, padx=2, anchor="w")

        self.tags_frame.update_idletasks()
        self.wrapper.update_idletasks()

    def remove_tag(self, item):
        self.selected.discard(item)
        self.refresh_tags()
        self.validate_selection()
        if self.listbox:
            self.update_listbox()

    def on_backspace(self, event):
        pass

    def hide_dropdown(self, trigger_focus_out=False):
        if self.dropdown_win:
            self.dropdown_win.destroy()
            self.dropdown_win = None
        self.listbox = None
        self.is_open = False
        if trigger_focus_out:
            self.validate_selection()

    def handle_click_outside(self, event):
        if self.dropdown_win and str(event.widget).startswith(str(self.dropdown_win)):
            return
        if event.widget not in (self.entry, self.toggle_btn):
            self.hide_dropdown()

    def set_options(self, new_options):
        self.options = new_options
        self.selected = {item for item in self.selected if item in new_options}
        typed_text = self.entry_var.get().strip().lower()
        if typed_text:
            self.filtered_options = [opt for opt in self.options if typed_text in opt.lower()]
        else:
            self.filtered_options = new_options[:]
        self.entry_var.set("")
        self.refresh_tags()
        self.hide_dropdown()
        if self.listbox:
            self.update_listbox()
        self.validate_selection()

    def validate_selection(self):
        color = "#ffdddd" if not self.selected else "white"
        self.wrapper.config(bg=color)
        self.tags_frame.config(bg=color)
        self.entry.config(bg=color)

    def get(self):
        return list(self.selected)
