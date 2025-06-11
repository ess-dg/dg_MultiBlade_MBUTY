# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 09:24:56 2025

@author: sheilamonera
"""

import tkinter as tk
from .info_label import InfoLabel


class RadioEntry:
    """
    A group of vertically stacked radio buttons with a label and optional tooltip.

    Parameters:
        parent (tk.Widget): Parent container widget.
        row (int): Grid row index for widget placement.
        label_text (str): Text for the label to the left of the radio buttons.
        options (list[str]): List of radio button options.
        default (str, optional): Default selected value. Defaults to the first option.
        info_text (str, optional): Tooltip text for the label.
    """

    def __init__(self, parent, row, label_text, options, default=None, info_text=None):
        self.var = tk.StringVar(value=default or options[0])

        # Label with optional info tooltip
        InfoLabel(parent, label_text, info=info_text).grid(row=row, column=0)

        # Frame to hold radio buttons
        radio_frame = tk.Frame(parent)
        radio_frame.grid(row=row, column=1, sticky="w", padx=5, pady=5)

        for i, opt in enumerate(options):
            tk.Radiobutton(
                radio_frame,
                text=opt,
                variable=self.var,
                value=opt
            ).grid(row=i, column=0, sticky="w")

    def get(self):
        """
        Return the currently selected radio button value.

        Returns:
            str: The selected option.
        """
        return self.var.get()
