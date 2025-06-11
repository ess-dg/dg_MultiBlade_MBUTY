# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 09:23:46 2025

@author: sheilamonera
"""

import tkinter as tk
from .info_label import InfoLabel
from .base_constants import FIXED_INPUT_WIDTH


class RangeEntryWidgets:
    """
    A pair of linked entry fields for entering a numeric range (min and max).

    Supports integer or float validation, with dynamic background coloring on error.

    Parameters:
        parent (tk.Widget): Parent container widget.
        row (int): Grid row for widget placement.
        label_text (str): Text for the label on the left.
        default (tuple): Default (min, max) values as strings or numbers.
        info_text (str, optional): Tooltip text for the label.
        input_validation (str): Either 'int' or 'float' (default: 'float').
    """

    def __init__(self, parent, row, label_text, default=(0, 1), info_text=None, input_validation="float"):
        self.var_min = tk.StringVar(value=str(default[0]))
        self.var_max = tk.StringVar(value=str(default[1]))
        self.input_validation = input_validation

        TO_LABEL_WIDTH_PX = 30
        TOTAL_PADDING_PX = 10
        AVG_CHAR_WIDTH_PX = 8
        entry_char_width = (FIXED_INPUT_WIDTH - TO_LABEL_WIDTH_PX - TOTAL_PADDING_PX) // 2 // AVG_CHAR_WIDTH_PX

        InfoLabel(parent, label_text, info=info_text).grid(
            row=row, column=0, padx=(5, 0), pady=5, sticky="nw"
        )

        wrapper = tk.Frame(parent, width=FIXED_INPUT_WIDTH)
        wrapper.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid_columnconfigure(1, minsize=TO_LABEL_WIDTH_PX)
        wrapper.grid_columnconfigure(2, weight=1)

        self.entry_min = tk.Entry(wrapper, textvariable=self.var_min, width=entry_char_width)
        self.entry_min.grid(row=0, column=0, sticky="ew")

        tk.Label(wrapper, text="to").grid(row=0, column=1, sticky="n", padx=4)

        self.entry_max = tk.Entry(wrapper, textvariable=self.var_max, width=entry_char_width)
        self.entry_max.grid(row=0, column=2, sticky="ew")

        # Dummy focus holder to shift focus away from entry fields
        self.dummy_focus_holder = tk.Frame(parent)
        self.dummy_focus_holder.grid(row=row + 1, column=0)
        self.dummy_focus_holder.lower()

        # Bind validation on keyboard interaction
        for entry in [self.entry_min, self.entry_max]:
            entry.bind("<Button-1>", lambda e, ent=entry: ent.after(10, ent.focus_set))
            entry.bind("<Return>", self.on_trigger)
            entry.bind("<Tab>", self.on_trigger)

        root = parent.winfo_toplevel()
        root.bind_all("<Button-1>", self.handle_click_outside, add="+")

        self.validate()

    def on_trigger(self, *_):
        """Trigger validation when user presses Enter or Tab."""
        self.validate()
        self.dummy_focus_holder.focus_set()

    def handle_click_outside(self, event):
        """Validate range when user clicks outside the entry boxes."""
        if isinstance(event.widget, tk.Entry):
            return
        self.entry_min.after(1, self.validate)

    def validate(self, *_):
        """Update background color to indicate whether the range is valid."""
        color = "white" if self._is_valid() else "#ffdddd"
        self.entry_min.config(bg=color)
        self.entry_max.config(bg=color)

    def get(self):
        """
        Return the range as a list [min, max] if valid, otherwise return [].

        Returns:
            list[int | float]: The validated numeric range.
        """
        if self._is_valid():
            return [self._convert(self.var_min.get()), self._convert(self.var_max.get())]
        return []

    def _convert(self, val):
        """Convert string input to int or float depending on input_validation."""
        val = val.strip()
        return int(val) if self.input_validation == "int" else float(val)

    def _is_valid(self):
        """Check that min ≤ max and both values are valid numbers."""
        try:
            return self._convert(self.var_min.get()) <= self._convert(self.var_max.get())
        except ValueError:
            return False
