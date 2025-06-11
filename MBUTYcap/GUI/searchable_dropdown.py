# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 09:02:44 2025

@author: sheilamonera
"""

import tkinter as tk
from .info_label import InfoLabel


class SearchableDropDown:
    """
    A custom dropdown widget with search/autocomplete functionality.

    Parameters:
        parent (tk.Widget): Parent container widget.
        row (int): Grid row index for widget placement.
        label_text (str): Text for the label to the left of the dropdown.
        options (list[str]): List of selectable string options.
        default (str, optional): Default selected value. Defaults to "".
        info_text (str, optional): Tooltip text for the label.
    """

    def __init__(self, parent, row, label_text, options, default="", info_text=None):
        self.options = options
        self.default = default
        self.is_open = False
        self.dropdown_win = None
        self.listbox = None
        self.parent = parent

        # Label with optional info tooltip
        InfoLabel(parent, label_text, info=info_text).grid(row=row, column=0, padx=5, pady=5)

        # Wrapper for entry and button
        wrapper = tk.Frame(parent)
        wrapper.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        parent.grid_columnconfigure(1, weight=1)

        self.entry = tk.Entry(wrapper)
        self.entry.pack(side=tk.LEFT, fill="x", expand=True)
        self.entry.insert(0, default)

        self.button = tk.Button(wrapper, text="▼", width=2, command=self.toggle_dropdown)
        self.button.pack(side=tk.LEFT)

        # Bindings
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown)
        self.entry.bind("<FocusOut>", self.validate_selection)
        self.entry.bind("<Return>", self.on_enter)
        self.entry.bind("<Down>", self.focus_listbox)
        self.entry.bind("<Up>", self.focus_listbox)
        self.entry.bind("<Tab>", self.on_tab)

        self.root = parent.winfo_toplevel()
        self.entry.bind("<Button-1>", self._on_entry_click, add="+")
        self.button.bind("<Button-1>", lambda e: None, add="+")  # Prevent button from triggering blur

        self.canvas = self._find_canvas(parent)
        
        self.root.after_idle(lambda: self.root.bind_all("<Button-1>", self.handle_click_outside, add="+"))

    def _find_canvas(self, widget):
        """Recursively search for a canvas ancestor (used for scroll positioning)."""
        while widget:
            if isinstance(widget, tk.Canvas):
                return widget
            widget = widget.master
        return None

    def _on_entry_click(self, event):
        # Re-focus the entry and delay validation slightly
        self.entry.after(1, lambda: self.entry.focus_set())

    def get(self):
        """
        Return the current value typed or selected in the dropdown.

        Returns:
            str: The current entry value (trimmed).
        """
        return self.entry.get().strip()

    def set_options(self, new_options):
        """
        Update the list of selectable options and clear the entry
        if the current value becomes invalid.

        Parameters:
            new_options (list[str]): New options to populate the dropdown with.
        """
        self.options = new_options
        current = self.get()
        if current not in new_options:
            self.entry.delete(0, tk.END)
            if self.default in new_options:
                self.entry.insert(0, self.default)
        self.update_list(new_options)
        self.validate_selection()

    def on_entry_key(self, event):
        """Filter options based on typed value and update dropdown list."""
        value = self.entry.get().strip().lower()
        filtered = [opt for opt in self.options if opt.lower().startswith(value)]
        self.show_dropdown()
        self.update_list(filtered)

    def update_list(self, options):
        """Update the listbox with a new set of filtered options."""
        if not self.listbox:
            return
        self.listbox.delete(0, tk.END)
        for option in options:
            self.listbox.insert(tk.END, option)

    def on_select(self, event):
        """Handle item selection from listbox (mouse click or Enter key)."""
        if self.listbox and self.listbox.curselection():
            selected = self.listbox.get(self.listbox.curselection())
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected)
            self.entry.configure(bg="white")
            self.on_entry_key(None)
            self.on_enter()

    def toggle_dropdown(self):
        """Show or hide the dropdown based on its current state."""
        if self.is_open:
            self.hide_dropdown()
        else:
            self.show_dropdown()

    def show_dropdown(self, event=None):
        """Create and display the dropdown list below the entry field."""
        if self.dropdown_win:
            return

        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()

        self.dropdown_win = tk.Toplevel(self.parent)
        self.dropdown_win.overrideredirect(True)
        self.dropdown_win.geometry(f"{self.entry.winfo_width()}x100+{x}+{y}")
        self.dropdown_win.attributes("-topmost", True)

        self.listbox = tk.Listbox(self.dropdown_win, height=5)
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<ButtonRelease-1>", self.on_select)
        self.listbox.bind("<Return>", self.on_listbox_enter)
        self.listbox.bind("<Tab>", lambda e: "break")
        self.listbox.bind("<MouseWheel>", lambda e: self.listbox.yview_scroll(int(-1 * e.delta / 120), "units"))
        self.listbox.bind("<Button-4>", lambda e: self.listbox.yview_scroll(-1, "units"))  # Linux scroll up
        self.listbox.bind("<Button-5>", lambda e: self.listbox.yview_scroll(1, "units"))   # Linux scroll down

        self.update_list(self.options)
        self.is_open = True
        self._update_dropdown_position()
        self.entry.focus_set()

    def _update_dropdown_position(self):
        """Continuously reposition dropdown relative to scrollable canvas (if any)."""
        if not self.dropdown_win or not self.entry.winfo_ismapped() or not self.canvas:
            return

        try:
            entry_root_y = self.entry.winfo_rooty()
            canvas_root_y = self.canvas.winfo_rooty()
            entry_canvas_y = self.canvas.canvasy(entry_root_y - canvas_root_y)
            entry_height = self.entry.winfo_height()
            dropdown_top = entry_canvas_y + entry_height

            visible_top = self.canvas.canvasy(0)
            visible_bottom = visible_top + self.canvas.winfo_height()

            if dropdown_top < visible_top or dropdown_top > visible_bottom:
                self.hide_dropdown(trigger_focus_out=True)
                return

            x = self.entry.winfo_rootx()
            y = entry_root_y + entry_height
            self.dropdown_win.geometry(f"{self.entry.winfo_width()}x100+{x}+{y}")

            self.entry.after(100, self._update_dropdown_position)

        except Exception as e:
            print(f"Dropdown canvas positioning error: {e}")

    def hide_dropdown(self, trigger_focus_out=False):
        """Hide the dropdown and optionally trigger validation."""
        if self.dropdown_win:
            self.dropdown_win.destroy()
            self.dropdown_win = None
        self.listbox = None
        self.is_open = False

        if trigger_focus_out:
            self.validate_selection()
            self.parent.focus_set()

    def handle_click_outside(self, event):
        """
        Hide dropdown if user clicks outside entry, button, or dropdown.
        Do NOT steal typing focus unless truly outside.
        """
        widgets_to_ignore = {self.entry, self.button}

        # Also ignore clicks inside the dropdown window
        if self.dropdown_win and str(event.widget).startswith(str(self.dropdown_win)):
            return

        if event.widget not in widgets_to_ignore:
            self.hide_dropdown(trigger_focus_out=True)

        elif event.widget == self.entry:
            self.entry.focus_set()



    def validate_selection(self, event=None):
        """Color the entry background red if the input is not a valid option."""
        typed = self.get()
        if typed not in self.options or typed == "":
            self.entry.configure(bg="#ffdddd")
        else:
            self.entry.configure(bg="white")

    def on_enter(self, event=None):
        """Auto-select first item in listbox on Enter and validate."""
        if self.listbox and self.listbox.size() > 0:
            first_option = self.listbox.get(0)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, first_option)
        self.validate_selection()
        self.hide_dropdown(trigger_focus_out=True)
        return "break"

    def focus_listbox(self, event=None):
        """Move keyboard focus to the listbox when navigating with arrow keys."""
        if self.listbox and self.listbox.size() > 0:
            self.listbox.focus_set()
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            return "break"

    def on_listbox_enter(self, event=None):
        """Trigger selection when pressing Enter on a listbox item."""
        self.on_select(event)
        self.on_enter()
        return "break"

    def on_tab(self, event=None):
        """Validate input when user presses Tab and hide the dropdown."""
        self.validate_selection()
        self.hide_dropdown(trigger_focus_out=True)
        return None
