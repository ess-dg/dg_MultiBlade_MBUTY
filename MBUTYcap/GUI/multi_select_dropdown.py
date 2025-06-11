# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 09:27:20 2025

@author: sheilamonera
"""
import tkinter as tk
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
        self.filtered_options = options[:] # Initially, all options are filtered_options (no text typed yet)
        self.parent = parent
        self.is_open = False
        self.dropdown_win = None
        self.listbox = None

        # Label with optional tooltip
        InfoLabel(parent, label_text, info=info_text).grid(row=row, column=0, sticky="nw", padx=5, pady=5)

        # Outer wrapper frame
        self.wrapper = tk.Frame(parent, bd=1, relief="solid", width=FIXED_INPUT_WIDTH)
        self.wrapper.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        parent.grid_columnconfigure(1, weight=1)

        # Tags display frame (will be packed/forgotten dynamically in refresh_tags)
        self.tags_frame = tk.Frame(self.wrapper)
        
        # Entry wrapper frame (contains entry and toggle button)
        self.entry_wrapper = tk.Frame(self.wrapper)

        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(self.entry_wrapper, textvariable=self.entry_var, borderwidth=0)
        self.entry.pack(side=tk.LEFT, fill="x", expand=True)

        self.toggle_btn = tk.Button(self.entry_wrapper, text="▼", width=2, command=self.toggle_dropdown)
        self.toggle_btn.pack(side=tk.LEFT)

        # Bindings
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<Button-1>", self.show_dropdown, add="+") # Show dropdown explicitly on entry click
        self.entry.bind("<Return>", self.add_first_match)
        # Removed the custom Backspace binding; Tkinter's default will apply for entry text deletion.

        self.root = parent.winfo_toplevel()
        self.canvas = self._find_canvas(parent)
        # Your provided handle_click_outside, UNMODIFIED.
        self.root.bind_all("<Button-1>", self.handle_click_outside, add="+")

        # Correct Packing Order (Entry below tags)
        self.entry_wrapper.pack(side=tk.BOTTOM, fill="x")
        self.refresh_tags() # Will pack tags_frame with side=TOP if selected items exist
        
        self.validate_selection()

    def _find_canvas(self, widget):
        """Recursively find parent canvas (for dropdown placement logic)."""
        while widget:
            if isinstance(widget, tk.Canvas):
                return widget
            widget = widget.master
        return None

    def toggle_dropdown(self):
        """Toggle the dropdown open or closed."""
        if self.is_open:
            self.hide_dropdown()
        else:
            self.show_dropdown()

    def show_dropdown(self, event=None):
        """Create and display the dropdown list below the entry field."""
        if self.dropdown_win: # Prevent showing if already open
            return

        # Calculate position for the dropdown window
        x = self.entry.winfo_rootx()
        y = self.entry.winfo_rooty() + self.entry.winfo_height()

        self.dropdown_win = tk.Toplevel(self.parent)
        self.dropdown_win.overrideredirect(True) # Remove window decorations
        self.dropdown_win.geometry(f"{self.wrapper.winfo_width()}x100+{x}+{y}")
        self.dropdown_win.attributes("-topmost", True) # Keep dropdown on top

        # Prevent Listbox from Stealing Focus (takefocus=0) and allow multiple selections
        self.listbox = tk.Listbox(self.dropdown_win, height=5, selectmode="multiple", exportselection=False, takefocus=0)
        self.listbox.pack(fill="both", expand=True)

        self.listbox.bind("<ButtonRelease-1>", self.on_select)
        self.listbox.bind("<Return>", self.add_selected_from_listbox)
        # Additional bindings for listbox navigation (e.g., arrow keys, mouse wheel) can be added here if needed.

        self.update_listbox() # Populate the listbox with current filtered options
        self.is_open = True
        self._update_dropdown_position()
        
        # Delay focus_set() using after_idle to ensure the entry receives focus after the Toplevel is fully rendered.
        self.entry.after_idle(self.entry.focus_set) 

    def _update_dropdown_position(self):
        """Continuously reposition dropdown relative to scrollable canvas (if any)."""
        if not self.dropdown_win or not self.entry.winfo_ismapped():
            self.hide_dropdown() # Hide if entry disappears
            return

        try:
            # Get the absolute screen coordinates of the entry widget
            entry_x_on_screen = self.entry.winfo_rootx()
            entry_y_on_screen = self.entry.winfo_rooty()
            entry_height = self.entry.winfo_height()

            # Calculate the desired top-left corner of the dropdown on screen
            dropdown_target_x = entry_x_on_screen
            dropdown_target_y = entry_y_on_screen + entry_height

            # Update the dropdown window's geometry
            self.dropdown_win.geometry(f"{self.wrapper.winfo_width()}x100+{dropdown_target_x}+{dropdown_target_y}")

            # Check if the dropdown is within the *visible part* of the canvas
            if self.canvas and self.canvas.winfo_ismapped():
                canvas_visible_top_on_screen = self.canvas.winfo_rooty()
                canvas_visible_bottom_on_screen = canvas_visible_top_on_screen + self.canvas.winfo_height()

                # Calculate the absolute screen coordinates of the dropdown's bottom edge
                dropdown_bottom_on_screen = dropdown_target_y + self.listbox.winfo_height() # Use listbox actual height

                # If the entire dropdown is above the visible canvas area OR below the visible canvas area
                if (dropdown_bottom_on_screen < canvas_visible_top_on_screen or
                    dropdown_target_y > canvas_visible_bottom_on_screen):
                    self.hide_dropdown() # Hide if it moves entirely out of canvas view
                    return # Stop subsequent updates if hidden

            # Schedule the next update only if the dropdown is still intended to be open
            if self.is_open:
                self.entry.after(100, self._update_dropdown_position)

        except Exception as e:
            print(f"Dropdown positioning error: {e}")
            # Even if an error occurs, try to reschedule to prevent the update loop from breaking
            if self.is_open:
                self.entry.after(100, self._update_dropdown_position)

    def update_listbox(self):
        """Update dropdown listbox contents to match filtered options, applying highlights."""
        if not self.listbox:
            return
        self.listbox.delete(0, tk.END) # Clear existing items
        
        # Insert options and apply background color based on selection status
        for i, option in enumerate(self.filtered_options):
            self.listbox.insert(tk.END, option)
            if option in self.selected:
                self.listbox.itemconfigure(i, background='#ADD8E6') # Light blue for selected items
            else:
                self.listbox.itemconfigure(i, background='white') # Default background for unselected

    def on_entry_key(self, event=None):
        """Filter options based on typed text and update dropdown."""
        typed = self.entry_var.get().strip().lower()
        # --- FIX: Filter all options, do not exclude already selected items ---
        self.filtered_options = [opt for opt in self.options if typed in opt.lower()]
        # --- End FIX ---
        self.show_dropdown() # Show dropdown as user types
        self.update_listbox() # Update listbox with filtered options

    def on_select(self, event=None):
        """
        Handle selection/deselection of items from the listbox via mouse click.
        Toggles selection status and updates UI without hiding dropdown.
        """
        if not self.listbox:
            return
        
        # Get the index of the clicked item
        try:
            clicked_index = self.listbox.nearest(event.y)
            clicked_item = self.listbox.get(clicked_index)
        except ValueError:
            # Click might not have been precisely on an item
            return

        if clicked_item in self.selected:
            # If already selected, deselect it
            self.selected.discard(clicked_item)
        else:
            # If not selected, select it
            self.selected.add(clicked_item)

        # Do NOT clear entry_var or hide dropdown here, allow multi-selection interaction
        self.refresh_tags() # Re-render tags to reflect changes
        self.update_listbox() # Update listbox highlights
        self.validate_selection() # Update wrapper background
        self.entry.focus_set() # Return focus to entry 

    def add_selected_from_listbox(self, event=None):
        """Handle adding selected items from listbox when Enter is pressed."""
        # This is typically used to finalize selection and close the dropdown.
        # Ensure the currently highlighted item is selected before finalizing.
        if self.listbox and self.listbox.curselection():
            selected_idx = self.listbox.curselection()[0]
            selected_item = self.listbox.get(selected_idx)
            if selected_item not in self.selected:
                self.selected.add(selected_item)

        self.entry_var.set("") # Clear entry text after final selection
        self.refresh_tags() # Re-render tags
        self.hide_dropdown() # Collapse dropdown after final selection
        self.validate_selection() # Update wrapper background


    def add_first_match(self, event=None):
        """Add the first matching filtered item to the selection."""
        if self.filtered_options:
            item_to_add = self.filtered_options[0]
            if item_to_add not in self.selected: # Only add if not already selected
                self.selected.add(item_to_add)
            self.entry_var.set("") # Clear entry text
            self.refresh_tags() # Re-render tags
            self.hide_dropdown() # Hide dropdown
            self.validate_selection() # Update wrapper background

    def refresh_tags(self):
        """
        Re-render the visual tags for selected items.
        Manages the packing of self.tags_frame to ensure it collapses when empty.
        """
        # Destroy all existing tag widgets
        for widget in self.tags_frame.winfo_children():
            widget.destroy()

        if not self.selected:
            # If no items are selected, hide the tags_frame completely
            self.tags_frame.pack_forget()
        else:
            # If there are selected items, ensure the tags_frame is packed.
            # It will occupy the space at the top of the wrapper due to entry_wrapper packed at BOTTOM.
            try:
                self.tags_frame.pack(side=tk.TOP, anchor="w", fill="x")
            except tk.TclError:
                pass # Already packed, no action needed

            # Create and pack new tag widgets for each selected item
            for item in sorted(list(self.selected)): # Sort for consistent display
                tag = tk.Frame(self.tags_frame, bd=1, relief="ridge", padx=2, pady=1)
                tk.Label(tag, text=item, font=("Segoe UI", 9),
                                 wraplength=FIXED_INPUT_WIDTH - 40, justify="left").pack(side=tk.LEFT)
                tk.Button(tag, text="✕", command=lambda i=item: self.remove_tag(i),
                                 padx=1, pady=0, font=("Segoe UI", 8), width=2).pack(side=tk.LEFT)
                tag.pack(fill="x", pady=2, padx=2, anchor="w")
        
        self.tags_frame.update_idletasks()
        self.wrapper.update_idletasks()
            
    def remove_tag(self, item):
        """Remove an item from the selection."""
        self.selected.discard(item)
        self.refresh_tags() # Re-render tags (will collapse frame if empty)
        self.validate_selection() # Update background color
        
        # --- FIX: Update listbox to remove highlight if dropdown is open ---
        if self.listbox: 
            self.update_listbox()
        # --- End FIX ---

    def on_backspace(self, event):
        # Your provided on_backspace, UNMODIFIED, which means the custom logic is removed.
        # Tkinter's default backspace behavior will apply to the Entry.
        pass # This method is now empty, allowing default Backspace behavior


    def hide_dropdown(self, trigger_focus_out=False):
        """Hide the dropdown and optionally trigger validation."""
        if self.dropdown_win:
            self.dropdown_win.destroy()
            self.dropdown_win = None
        self.listbox = None
        self.is_open = False

        if trigger_focus_out:
            # Directly call validation.
            self.validate_selection()


    def handle_click_outside(self, event):
        # Your provided handle_click_outside, UNMODIFIED.
        """Close dropdown if click occurs outside the entry or toggle button."""
        if self.dropdown_win and str(event.widget).startswith(str(self.dropdown_win)):
            return
        if event.widget not in (self.entry, self.toggle_btn):
            self.hide_dropdown()


    def set_options(self, new_options):
        """
        Set a new list of selectable options, preserving valid current selections.

        Parameters:
            new_options (list[str]): The new options to set.
        """
        self.options = new_options
        # Preserve selected items that are still present in the new_options list
        self.selected = {item for item in self.selected if item in new_options}
        
        # --- FIX: Reset filtered options based on current entry text if any, else all new options ---
        typed_text = self.entry_var.get().strip().lower()
        if typed_text:
            self.filtered_options = [opt for opt in self.options if typed_text in opt.lower()]
        else:
            self.filtered_options = new_options[:]
        # --- End FIX ---
        
        self.entry_var.set("") # Clear entry text (important for correct filtering if user starts typing)
        self.refresh_tags() # Re-render tags
        self.hide_dropdown() # Always hide dropdown when options are externally set.
        
        # If the dropdown was open, update its listbox content with the new options
        if self.listbox: 
            self.update_listbox()
        
        self.validate_selection() # Update background color

    def validate_selection(self):
        """
        Set background color based on whether selection is empty.
        Applies color to the wrapper, tags frame, and entry.
        """
        color = "#ffdddd" if not self.selected else "white"
        self.wrapper.config(bg=color)
        self.tags_frame.config(bg=color)
        self.entry.config(bg=color)

    def get(self):
        """
        Return a list of currently selected items.

        Returns:
            list[str]: Selected option strings.
        """
        return list(self.selected)