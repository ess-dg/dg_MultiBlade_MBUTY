# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 08:46:51 2025

@author: sheilamonera
"""
import tkinter as tk
from .base_constants import label_width

class Tooltip:
    """
    A class to create a tooltip window that appears when hovering over a widget.

    Attributes:
        widget (tk.Widget): The widget to which the tooltip is attached.
        text (str): The tooltip text to display.
    """
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        """Display the tooltip if it is not already shown."""
        if self.tip_window or not self.text:
            return

        screen_width = self.widget.winfo_screenwidth()
        screen_height = self.widget.winfo_screenheight()

        # Desired position relative to widget
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5

        # Create tooltip window off-screen to measure size
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.geometry("+10000+10000")  # temporarily off-screen

        label = tk.Label(
            self.tip_window,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 9),
            wraplength=500
        )
        label.pack(ipadx=5, ipady=2)

        # Measure tooltip size
        self.tip_window.update_idletasks()
        tooltip_width = self.tip_window.winfo_width()
        tooltip_height = self.tip_window.winfo_height()

        # Adjust position if tooltip would go off screen
        if x + tooltip_width > screen_width:
            x = screen_width - tooltip_width - 10
        if y + tooltip_height > screen_height:
            y = self.widget.winfo_rooty() - tooltip_height - 10

        self.tip_window.geometry(f"+{x}+{y}")

    def hide(self, event=None):
        """Hide the tooltip window."""
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


class InfoLabel(tk.Frame):
    """
    A label widget with an optional tooltip info button.

    Parameters:
        parent (tk.Widget): The parent widget.
        text (str): The main label text.
        info (str, optional): Tooltip text to show when hovering over the info button.
        total_width (int, optional): Fixed width of the label frame.
        **kwargs: Additional keyword arguments passed to the tk.Frame.
    """
    def __init__(self, parent, text, info=None, total_width=label_width, **kwargs):
        super().__init__(parent, **kwargs)

        # Enforce fixed width on the parent’s label column
        parent.grid_columnconfigure(0, minsize=total_width)

        self.config(width=total_width)
        self.grid_propagate(False)

        # Internal wrapper to allow dynamic height wrapping
        wrapper = tk.Frame(self, width=total_width)
        wrapper.pack(fill="both", expand=True)

        # Main label
        label = tk.Label(
            wrapper,
            text=text,
            justify="left",
            anchor="w",
            wraplength=total_width - 35
        )
        label.pack(side="left", fill="x", expand=True)

        # Optional info button with hover tooltip
        if info:
            info_btn = tk.Button(
                wrapper,
                text="ⓘ",
                padx=0,
                pady=0,
                fg="#0066cc",
                font=("Segoe UI", 9, "bold"),
                relief=tk.FLAT,
                borderwidth=0,
                width=2
            )
            info_btn.pack(side="left", padx=(4, 0))
            Tooltip(info_btn, info)

    def grid(self, **kwargs):
        """
        Overrides default grid behavior to add padding and alignment
        if not already specified.
        """
        kwargs.setdefault("sticky", "nw")
        kwargs.setdefault("padx", (5, 0))
        kwargs.setdefault("pady", 5)
        super().grid(**kwargs)
