# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 14:55:22 2025

@author: sheilamonera
"""
import tkinter as tk
import sys
import re

class ANSIColorTextWidget(tk.Text):
    """
    A Tkinter Text widget that can interpret basic ANSI color escape codes.
    It is read-only for the user.
    """
    ANSI_ESCAPE_PATTERN = re.compile(r'\x1b\[([0-9;]+)m')

    # Mapping of ANSI color codes to Tkinter color names
    COLOR_MAP = {
        '30': 'black', '31': 'red', '32': 'green', '33': 'yellow',
        '34': 'blue', '35': 'magenta', '36': 'cyan', '37': 'white',
        '90': 'gray', # Bright black
        '91': 'lightcoral', # Bright red
        '92': 'lightgreen', # Bright green
        '93': 'lightyellow', # Bright yellow
        '94': 'lightblue', # Bright blue
        '95': 'plum', # Bright magenta
        '96': 'lightcyan', # Bright cyan
        '97': 'white', # Bright white (already white, but good for consistency)
    }

    # Style mapping (minimal for this example, focusing on bold)
    STYLE_MAP = {
        '1': 'bold',
        '0': 'reset', # Explicitly handle reset for styles too
    }

    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.current_tags = set()
        self._configure_tags()
        self.insert_index = tk.END # To keep track of where to insert text
        self.config(state="disabled") # Make the widget read-only by default

    def _configure_tags(self):
        """Configures the Tkinter Text widget tags based on ANSI codes."""
        # Default tag for resetting
        self.tag_configure("reset", foreground="white", font=("Courier New", 10))

        # Color tags
        for code, color_name in self.COLOR_MAP.items():
            self.tag_configure(f"fg_{code}", foreground=color_name)

        # Style tags (e.g., bold)
        self.tag_configure("bold", font=("Courier New", 10, "bold"))


    def write(self, string):
        """
        Processes the incoming string, interpreting ANSI escape codes
        and applying tags.
        """
        self.config(state="normal") # Temporarily enable writing

        # Find all ANSI escape sequences and split the string
        parts = self.ANSI_ESCAPE_PATTERN.split(string)
        
        # Keep track of active tags
        current_color_tag = None
        current_style_tag = None

        for i, part in enumerate(parts):
            if i % 2 == 0:  # This is a text segment
                if part: # Only insert if there's actual text
                    tags_to_apply = []
                    if current_color_tag:
                        tags_to_apply.append(current_color_tag)
                    if current_style_tag:
                        tags_to_apply.append(current_style_tag)
                    
                    if not tags_to_apply: # If no specific tags, use reset for default
                        tags_to_apply.append("reset")

                    self.insert(tk.END, part, tuple(tags_to_apply))
            else:  # This is an ANSI escape code parameter string (e.g., '1;32')
                codes = part.split(';')
                for code in codes:
                    if code == '0':  # Reset
                        current_color_tag = None
                        current_style_tag = None
                    elif code in self.COLOR_MAP:
                        current_color_tag = f"fg_{code}"
                    elif code in self.STYLE_MAP:
                        style_name = self.STYLE_MAP[code]
                        if style_name == 'bold':
                            current_style_tag = 'bold'
                        elif style_name == 'reset':
                            current_style_tag = None # Reset styles too

        self.see(tk.END) # Scroll to the end
        self.update_idletasks() # Update the display immediately
        self.config(state="disabled") # Disable writing again

    def flush(self):
        """Required for stdout redirection."""
        pass

class ConsoleRedirector:
    """Redirects stdout to the ANSIColorTextWidget."""
    def __init__(self, text_widget):
        self.text_widget = text_widget
        # Store a direct reference to Python's actual original stdout stream
        # This is more robust than sys.stdout because sys.stdout itself can be redirected.
        self.original_stdout_fallback = sys.__stdout__ 

    def write(self, string):
        try:
            # Check if the text_widget still exists and is mapped (visible) before writing
            # winfo_exists() is critical here.
            if self.text_widget and self.text_widget.winfo_exists():
                self.text_widget.write(string)
            else:
                # If widget is gone, print to the actual console stdout as a fallback
                self.original_stdout_fallback.write(string)
        except Exception:
            # Catch any other potential errors during writing to the widget and fall back
            self.original_stdout_fallback.write(f"GUI Console Error: {string}")
            self.original_stdout_fallback.flush()
