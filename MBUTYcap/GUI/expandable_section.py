# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 09:30:32 2025

@author: sheilamonera
"""

import tkinter as tk


class ExpandableSection:
    """
    A collapsible/expandable section frame with a toggleable header.

    Parameters:
        parent (tk.Widget): Parent container widget.
        title (str): Title text displayed on the section header.
    """

    def __init__(self, parent, title):
        self.frame = tk.Frame(parent)
        self.title = title
        self.is_expanded = False

        # Header button with arrow indicator
        self.header = tk.Button(
            self.frame,
            text="▶ " + title,
            anchor="w",
            command=self.toggle
        )
        self.header.pack(fill="x", pady=2)

        # Content area (initially hidden)
        self.content = tk.Frame(self.frame)
        self.content.pack(fill="x", expand=True)
        self.content.forget()

    def toggle(self):
        """
        Toggle the section between expanded and collapsed states.
        """
        if self.is_expanded:
            self.content.forget()
            self.header.config(text="▶ " + self.title)
        else:
            self.content.pack(fill="x", expand=True)
            self.header.config(text="▼ " + self.title)
        self.is_expanded = not self.is_expanded

    def pack(self, **kwargs):
        """
        Pack the outer frame into the parent layout.

        Accepts any standard tk.Frame .pack() keyword arguments.
        """
        self.frame.pack(**kwargs)

    def get_content_frame(self):
        """
        Return the internal content frame where widgets should be placed.

        Returns:
            tk.Frame: The content frame for placing widgets.
        """
        return self.content
