# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 09:25:39 2025

@author: sheilamonera
"""

import tkinter as tk
from .info_label import InfoLabel


class BooleanSelect:
    """
    A horizontal group of radio buttons for selecting between boolean-style options
    like True/False or Yes/No, with a label and optional tooltip.

    Parameters:
        parent (tk.Widget): Parent container widget.
        row (int): Row index for grid layout.
        label_text (str): Text for the label to the left of the radio buttons.
        options (list[str]): List of options (e.g., ['True', 'False'] or ['Yes', 'No']).
        default (str, optional): Default selected option.
        info_text (str, optional): Tooltip text for the label.
    """

    def __init__(self, parent, row, label_text, options, default=None, info_text=None):
        self.var = tk.StringVar(value=default if default is not None else options[0])

        # Label with optional info tooltip
        InfoLabel(parent, label_text, info=info_text).grid(row=row, column=0)

        # Frame to hold horizontal radio buttons
        radio_frame = tk.Frame(parent)
        radio_frame.grid(row=row, column=1, sticky="w", padx=5)

        for i, opt in enumerate(options):
            tk.Radiobutton(
                radio_frame,
                text=opt,
                variable=self.var,
                value=opt
            ).pack(side=tk.LEFT, padx=(0 if i == 0 else 10, 0))

    def get(self):
        """
        Return the selected value, automatically converting 'True'/'False' strings
        to Python booleans if possible.

        Returns:
            bool | str: Boolean value if the string matches 'True' or 'False',
                        otherwise returns the raw string.
        """
        val = self.var.get()
        if val == "True":
            return True
        elif val == "False":
            return False
        return val
