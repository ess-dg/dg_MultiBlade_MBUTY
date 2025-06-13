# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 09:05:15 2025

@author: sheilamonera
"""
import tkinter as tk
import re
import os
from .info_label import InfoLabel


class ValidatedEntry:
    """
    A labeled entry field with built-in validation, dynamic background coloring,
    and support for various input types.

    Parameters:
        parent (tk.Widget): Parent container widget.
        row (int): Row index for placement in a grid layout.
        label_text (str): Text for the label to the left of the entry.
        validation_type (str): Type of validation ('int', 'float', 'scientific',
                                 'localPath', 'remotepath', 'host:port', 'file_numbers', 'any').
        default (str): Default value shown in the entry box.
        info_text (str, optional): Tooltip text for the label.
        value_range (tuple, optional): (min, max) bounds for numeric input validation.
    """

    def __init__(self, parent, row, label_text,
                 validation_type="any", default="",
                 info_text=None, value_range=None):
        self.var = tk.StringVar(value=default)
        self.validation_type = validation_type
        self.value_range = value_range

        # Label + optional tooltip
        InfoLabel(parent, label_text, info=info_text).grid(row=row, column=0)

        # Entry widget
        self.entry = tk.Entry(parent, textvariable=self.var)
        self.entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)

        # Dummy focus holder to allow manual focus clearing
        self.dummy_focus_holder = tk.Frame(parent)
        self.dummy_focus_holder.grid(row=row + 1, column=0)
        self.dummy_focus_holder.lower()

        # Bindings for validation on keyboard navigation
        self.entry.bind("<Return>", self.on_trigger)
        self.entry.bind("<Tab>", self.on_trigger)

        # Manual delay for click-based focus to override global bindings
        self.entry.bind("<Button-1>", lambda e: self.entry.after(10, self.entry.focus_set))

        # Bind global click detection to trigger validation if user clicks outside
        root = self.entry.winfo_toplevel()
        root.bind_all("<Button-1>", self.handle_click_outside, add="+")

        self.validate()

    @staticmethod
    def _parse_file_input(input_string):
        """
        Parses a string representing file numbers (e.g., "1-50", "1,2,5,8", "1-30,35,50")
        and returns a sorted list of unique integers. Returns an empty list if parsing fails
        or if the input is empty/invalid.
        """
        file_numbers = set()
        if not input_string.strip(): # Handle empty input gracefully
            return []

        parts = input_string.split(',')

        for part in parts:
            part = part.strip()
            if not part: # Skip empty parts resulting from e.g. "1,,3"
                continue

            if '-' in part:
                try:
                    start_str, end_str = part.split('-')
                    start = int(start_str)
                    end = int(end_str)
                    if start <= end:
                        file_numbers.update(range(start, end + 1))
                    else:
                        # Invalid range (e.g., 50-10) makes the whole input invalid for this part
                        return [] # Returning empty list indicates parsing failure for this input
                except ValueError:
                    return [] # Invalid range format (e.g., "a-b")
            else:
                try:
                    file_numbers.add(int(part))
                except ValueError:
                    return [] # Invalid individual number (e.g., "abc")

        return sorted(list(file_numbers))

    def on_trigger(self, event):
        """Trigger validation and clear focus when pressing Enter or Tab."""
        self.validate()
        self.dummy_focus_holder.focus_set()

    def handle_click_outside(self, event):
        """Trigger validation if the click occurs outside this entry."""
        if isinstance(event.widget, tk.Entry):
            return
        self.entry.after(1, self._delayed_validate, event.widget)

    def _delayed_validate(self, clicked_widget):
        """Validate input after focus loss due to clicking elsewhere."""
        if clicked_widget != self.entry:
            self.validate()

    def validate(self):
        """Validate current entry value and set background color accordingly."""
        value = self.var.get().strip()
        if not value and self.validation_type != 'file_numbers': # file_numbers can be empty and valid
            self.entry.config(bg="#ffdddd")
            return
        elif self.validation_type == 'file_numbers' and not value:
            # For 'file_numbers', an empty string is a valid (empty) input
            self.entry.config(bg="white")
            return

        if self._is_valid(value):
            self.entry.config(bg="white")
        else:
            self.entry.config(bg="#ffdddd")

    def _is_in_range(self, numeric_value):
        """Check if numeric value is within the specified range, if any."""
        if self.value_range is None:
            return True
        return self.value_range[0] <= numeric_value <= self.value_range[1]

    def _is_valid_file_numbers(self, value_string):
        """
        Validates if the input string can be parsed into a list of file numbers.
        Returns True if parsable, False otherwise.
        """
        # _parse_file_input returns an empty list for invalid/empty inputs.
        # We consider empty input valid for file numbers, but malformed input invalid.
        if not value_string.strip():
            return False # An empty input means no files, which is invalid.

        parsed_list = self._parse_file_input(value_string)
        # If parsing results in an empty list AND the original string was not empty,
        # it means there was a parsing error (invalid format).
        if not parsed_list and value_string.strip():
            return False
        return True

    def _is_valid(self, value):
        """Perform type-specific validation on the input string."""
        try:
            if self.validation_type == "int":
                return self._is_in_range(int(value))
            elif self.validation_type == "float":
                return self._is_in_range(float(value))
            elif self.validation_type == "scientific":
                return bool(re.fullmatch(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)([eE][-+]?\d+)?', value))
            elif self.validation_type == "localPath":
                return os.path.exists(value)
            elif self.validation_type == "remotepath":
                return bool(re.match(r"^[\w.-]+@[\d.]+:.*", value))
            elif self.validation_type == "host:port":
                parts = value.strip().split(":")
                if len(parts) != 2:
                    return False
                host, port = parts
                if not re.match(r"^[\w\.-]+$", host):
                    return False
                return 1 <= int(port) <= 65535
            elif self.validation_type == "fileNumbers":
                return self._is_valid_file_numbers(value)
            return True  # "any" or unsupported types default to valid
        except Exception:
            return False

    def get(self):
        """
        Return the parsed value if valid, else an empty string or empty list
        based on validation type.
        """
        value = self.var.get().strip()
        if not self._is_valid(value):
            if self.validation_type == "fileNumbers":
                return [] # Return an empty list for invalid file numbers
            return "" # Return empty string for other invalid types
        
        if self.validation_type == "int":
            return int(value)
        elif self.validation_type == "float":
            return float(value)
        elif self.validation_type == "scientific":
            return float(value)
        elif self.validation_type == "fileNumbers":
            return self._parse_file_input(value) # Return the parsed list
        else:
            return value