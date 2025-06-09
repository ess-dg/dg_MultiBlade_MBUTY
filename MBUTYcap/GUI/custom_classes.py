# -*- coding: utf-8 -*-
"""
Created on Wed May 21 13:25:21 2025

@author: sheilamonera
"""
from tkinter import *
from tkinter import messagebox, Entry
import re
import os


FIXED_INPUT_WIDTH = 300  # pixels
label_width = 200
##########################################################################
###To do: Add styling
##Comment all classes
######################
class SearchableDropDown:
    def __init__(self, parent, row, label_text, options, default="", info_text=None):
        self.options = options
        self.var = StringVar(value=default)
        self.is_open = False
        self.dropdown_win = None
        self.listbox = None
        self.parent = parent

        InfoLabel(parent, label_text, info=info_text).grid(row=row, column=0, padx=5, pady=5)

        wrapper = Frame(parent)
        wrapper.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        parent.grid_columnconfigure(1, weight=1)

        self.entry = Entry(wrapper, textvariable=self.var)
        self.entry.pack(side=LEFT, fill="x", expand=True)

        self.button = Button(wrapper, text="▼", width=2, command=self.toggle_dropdown)
        self.button.pack(side=LEFT)

        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown)
        self.entry.bind("<FocusOut>", self.validate_selection)
        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<Down>", self._focus_listbox)
        self.entry.bind("<Up>", self._focus_listbox)
        self.entry.bind("<Tab>", self._on_tab)

        self.root = parent.winfo_toplevel()
        self.root.bind_all("<Button-1>", self.handle_click_outside, add="+")

        # 🆕 Auto-detect the canvas containing this widget
        self.canvas = self._find_canvas(parent)

        self.validate_selection()

    def _find_canvas(self, widget):
        while widget:
            if isinstance(widget, Canvas):
                return widget
            widget = widget.master
        return None

    def on_entry_key(self, event):
        value = self.entry.get().strip().lower()
        filtered = [opt for opt in self.options if opt.lower().startswith(value)]
        self.show_dropdown()
        self.update_list(filtered)

    def update_list(self, options):
        if not self.listbox:
            return
        self.listbox.delete(0, END)
        for option in options:
            self.listbox.insert(END, option)

    def on_select(self, event):
        if self.listbox and self.listbox.curselection():
            selected = self.listbox.get(self.listbox.curselection())
            self.entry.delete(0, END)
            self.entry.insert(0, selected)
            self.entry.configure(bg="white")
            self.on_entry_key(None)
            self._on_enter()

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
        self.dropdown_win = Toplevel(self.parent)
        self.dropdown_win.overrideredirect(True)
        self.dropdown_win.geometry(f"{self.entry.winfo_width()}x100+{x}+{y}")
        self.dropdown_win.attributes("-topmost", True)

        self.listbox = Listbox(self.dropdown_win, height=5)
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<ButtonRelease-1>", self.on_select)
        self.listbox.bind("<Return>", self._on_listbox_enter)
        self.listbox.bind("<Tab>", lambda e: "break")
        self.listbox.bind("<MouseWheel>", lambda e: self.listbox.yview_scroll(int(-1 * e.delta / 120), "units"))
        self.listbox.bind("<Button-4>", lambda e: self.listbox.yview_scroll(-1, "units"))
        self.listbox.bind("<Button-5>", lambda e: self.listbox.yview_scroll(1, "units"))

        self.update_list(self.options)
        self.is_open = True
        self._update_dropdown_position()

    def _update_dropdown_position(self):
        if not self.dropdown_win or not self.entry.winfo_ismapped() or not self.canvas:
            return
    
        try:
            entry_root_y = self.entry.winfo_rooty()
            canvas_root_y = self.canvas.winfo_rooty()
            entry_canvas_y = self.canvas.canvasy(entry_root_y - canvas_root_y)
            entry_height = self.entry.winfo_height()
            dropdown_top = entry_canvas_y + entry_height  # top of dropdown in canvas coordinates
    
            visible_top = self.canvas.canvasy(0)
            visible_bottom = visible_top + self.canvas.winfo_height()
    
            # ✅ New logic:
            if dropdown_top < visible_top or dropdown_top > visible_bottom:
                self.hide_dropdown(trigger_focus_out=True)
                return
    
            # Update geometry
            x = self.entry.winfo_rootx()
            y = entry_root_y + entry_height
            self.dropdown_win.geometry(f"{self.entry.winfo_width()}x100+{x}+{y}")
    
            self.entry.after(100, self._update_dropdown_position)
    
        except Exception as e:
            print(f"Dropdown canvas positioning error: {e}")


    def hide_dropdown(self, trigger_focus_out=False):
        if self.dropdown_win:
            self.dropdown_win.destroy()
            self.dropdown_win = None
        self.listbox = None
        self.is_open = False

        if trigger_focus_out:
            self.validate_selection()
            self.parent.focus_set()

    def handle_click_outside(self, event):
        if self.dropdown_win and str(event.widget).startswith(str(self.dropdown_win)):
            return
        if event.widget not in (self.entry, self.button):
            self.hide_dropdown(trigger_focus_out=True)

    def validate_selection(self, event=None):
        typed = self.get()
        if typed not in self.options or typed == "":
            self.entry.configure(bg="#ffdddd")
        else:
            self.entry.configure(bg="white")
                
    def get(self):
        return self.entry.get().strip()

    def _on_enter(self, event=None):
        if self.listbox and self.listbox.size() > 0:
            first_option = self.listbox.get(0)
            self.entry.delete(0, END)
            self.entry.insert(0, first_option)
        self.validate_selection()
        self.hide_dropdown(trigger_focus_out=True)
        return "break"

    def _focus_listbox(self, event=None):
        if self.listbox and self.listbox.size() > 0:
            self.listbox.focus_set()
            self.listbox.selection_clear(0, END)
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            return "break"

    def _on_listbox_enter(self, event=None):
        self.on_select(event)
        self._on_enter()
        return "break"

    def _on_tab(self, event=None):
        self.validate_selection()
        self.hide_dropdown(trigger_focus_out=True)
        return None
###############################################################################
# Expandable Section Class
###############################################################################
class ExpandableSection:
    def __init__(self, parent, title):
        self.frame = Frame(parent)
        self.title = title
        self.is_expanded = False

        self.header = Button(self.frame, text="▶ " + title, anchor="w", command=self.toggle)
        self.header.pack(fill="x", pady=2)

        self.content = Frame(self.frame)
        self.content.pack(fill="x", expand=True)
        self.content.forget()

    def toggle(self):
        if self.is_expanded:
            self.content.forget()
            self.header.config(text="▶ " + self.title)
        else:
            self.content.pack(fill="x", expand=True)
            self.header.config(text="▼ " + self.title)
        self.is_expanded = not self.is_expanded

    def pack(self, **kwargs):
        self.frame.pack(**kwargs)

    def get_content_frame(self):
        return self.content

###############################################################################
# Label with info Class
###############################################################################
class InfoLabel(Frame):
    def __init__(self, parent, text, info=None, total_width=label_width, **kwargs):
        super().__init__(parent, **kwargs)

        # Enforce fixed width on label column
        parent.grid_columnconfigure(0, minsize=total_width)

        # Outer frame fixed width
        self.config(width=total_width)
        self.grid_propagate(False)

        # Wrapper for dynamic height
        wrapper = Frame(self, width=total_width)
        wrapper.pack(fill="both", expand=True)

        # Label
        label = Label(
            wrapper,
            text=text,
            justify="left",
            anchor="w",
            wraplength=total_width - 35
        )
        label.pack(side="left", fill="x", expand=True)

        # Info button with tooltip
        if info:
            info_btn = Button(
                wrapper,
                text="ⓘ",
                padx=0,
                pady=0,
                fg="#0066cc",
                font=("Segoe UI", 9, "bold"),
                relief=FLAT,
                borderwidth=0,
                width=2
            )
            info_btn.pack(side="left", padx=(4, 0))
            Tooltip(info_btn, info)

    def grid(self, **kwargs):
        kwargs.setdefault("sticky", "nw")
        kwargs.setdefault("padx", (5, 0))
        kwargs.setdefault("pady", 5)
        super().grid(**kwargs)

# 🔧 Tooltip class for hover info
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None

        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, event=None):
        if self.tip_window or not self.text:
            return
    
        # Get screen dimensions
        screen_width = self.widget.winfo_screenwidth()
        screen_height = self.widget.winfo_screenheight()
    
        # Desired position relative to widget
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
    
        # Create tooltip window off-screen to measure it
        self.tip_window = Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.geometry("+10000+10000")  # temporarily off-screen
    
        # Create the label
        label = Label(
            self.tip_window,
            text=self.text,
            justify="left",
            background="#ffffe0",
            relief="solid",
            borderwidth=1,
            font=("Segoe UI", 9),
            wraplength=500  # Max width of tooltip
        )
        label.pack(ipadx=5, ipady=2)
    
        # Measure tooltip size
        self.tip_window.update_idletasks()
        tooltip_width = self.tip_window.winfo_width()
        tooltip_height = self.tip_window.winfo_height()
    
        # Adjust position if going off screen
        if x + tooltip_width > screen_width:
            x = screen_width - tooltip_width - 10  # pad from edge
        if y + tooltip_height > screen_height:
            y = self.widget.winfo_rooty() - tooltip_height - 10  # show above widget
    
        # Place final geometry
        self.tip_window.geometry(f"+{x}+{y}")
        
    def hide(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None

###############################################################################
# Validated entry class
###############################################################################
class ValidatedEntry:
    def __init__(self, parent, row, label_text, validation_type="any", default="", info_text=None, value_range=None):
        self.var = StringVar(value=default)
        self.validation_type = validation_type
        self.value_range = value_range

        # Label + Info in column 0
        InfoLabel(parent, label_text, info=info_text).grid(row=row, column=0)

        # Entry field in column 1 (with padding)
        self.entry = Entry(parent, textvariable=self.var)
        self.entry.grid(row=row, column=1, sticky="ew", padx=5, pady=5)

        # Dummy holder for removing focus
        self.dummy_focus_holder = Frame(parent)
        self.dummy_focus_holder.grid(row=row + 1, column=0)
        self.dummy_focus_holder.lower()

        # Bindings for keyboard-based focus loss
        self.entry.bind("<Return>", self._on_trigger)
        self.entry.bind("<Tab>", self._on_trigger)

        # Delay focus setting to avoid interference from canvas or global bindings
        self.entry.bind("<Button-1>", lambda e: self.entry.after(10, self.entry.focus_set))

        # Global click detection for outside clicks (only if NOT an Entry)
        root = self.entry.winfo_toplevel()
        root.bind_all("<Button-1>", self._handle_click_outside, add="+")
        
        # Initial validation
        self.validate()

    def _on_trigger(self, event):
        self.validate()
        self.dummy_focus_holder.focus_set()

    def _handle_click_outside(self, event):
        # Do not interfere when clicking on another Entry
        if isinstance(event.widget, Entry):
            return
        self.entry.after(1, self._delayed_validate, event.widget)

    def _delayed_validate(self, clicked_widget):
        if clicked_widget != self.entry:
            self.validate()

    def validate(self):
        value = self.var.get().strip()
        if not value:
            self.entry.config(bg="#ffdddd")
            return

        if self._is_valid(value):
            self.entry.config(bg="white")
        else:
            self.entry.config(bg="#ffdddd")

    def _is_in_range(self, numeric_value):
        if self.value_range is None:
            return True
        return self.value_range[0] <= numeric_value <= self.value_range[1]

    def _is_valid(self, value):
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
            return True
        except:
            return False

    def get(self):
        value = self.var.get().strip()
        if not self._is_valid(value):
            return ""
        if self.validation_type == "int":
            return int(value)
        elif self.validation_type == "float":
            return float(value)
        elif self.validation_type == "scientific":
            return float(value)
        else:
            return value


###############################################################################
# Range entry class
###############################################################################
class RangeEntryWidgets:
    def __init__(self, parent, row, label_text, default=(0, 1), info_text=None, input_validation="float"):
        self.var_min = StringVar(value=str(default[0]))
        self.var_max = StringVar(value=str(default[1]))
        self.input_validation = input_validation

        TO_LABEL_WIDTH_PX = 30
        TOTAL_PADDING_PX = 10
        AVG_CHAR_WIDTH_PX = 8
        entry_char_width = (FIXED_INPUT_WIDTH - TO_LABEL_WIDTH_PX - TOTAL_PADDING_PX) // 2 // AVG_CHAR_WIDTH_PX

        InfoLabel(parent, label_text, info=info_text).grid(
            row=row, column=0, padx=(5, 0), pady=5, sticky="nw"
        )

        wrapper = Frame(parent, width=FIXED_INPUT_WIDTH)
        wrapper.grid(row=row, column=1, padx=5, pady=5, sticky="ew")

        wrapper.grid_columnconfigure(0, weight=1)
        wrapper.grid_columnconfigure(1, minsize=TO_LABEL_WIDTH_PX)
        wrapper.grid_columnconfigure(2, weight=1)

        self.entry_min = Entry(wrapper, textvariable=self.var_min, width=entry_char_width)
        self.entry_min.grid(row=0, column=0, sticky="ew")

        Label(wrapper, text="to").grid(row=0, column=1, sticky="n", padx=4)

        self.entry_max = Entry(wrapper, textvariable=self.var_max, width=entry_char_width)
        self.entry_max.grid(row=0, column=2, sticky="ew")

        # Dummy holder to remove focus
        self.dummy_focus_holder = Frame(parent)
        self.dummy_focus_holder.grid(row=row + 1, column=0)
        self.dummy_focus_holder.lower()

        for entry in [self.entry_min, self.entry_max]:
            entry.bind("<Button-1>", lambda e, ent=entry: ent.after(10, ent.focus_set))
            entry.bind("<Return>", self._on_trigger)
            entry.bind("<Tab>", self._on_trigger)

        root = parent.winfo_toplevel()
        root.bind_all("<Button-1>", self._handle_click_outside, add="+")

        self.validate()

    def _convert(self, val):
        val = val.strip()
        return int(val) if self.input_validation == "int" else float(val)

    def _is_valid(self):
        try:
            return self._convert(self.var_min.get()) <= self._convert(self.var_max.get())
        except ValueError:
            return False

    def _on_trigger(self, *_):
        self.validate()
        self.dummy_focus_holder.focus_set()

    def _handle_click_outside(self, event):
        if isinstance(event.widget, Entry):
            return
        self.entry_min.after(1, self.validate())

    def validate(self, *_):
        color = "white" if self._is_valid() else "#ffdddd"
        self.entry_min.config(bg=color)
        self.entry_max.config(bg=color)

    def get(self):
        if self._is_valid():
            return [self._convert(self.var_min.get()), self._convert(self.var_max.get())]
        return []




###############################################################################
# Radio entry class
###############################################################################
class RadioEntry:
    def __init__(self, parent, row, label_text, options, default=None, info_text=None):
        self.var = StringVar(value=default or options[0])

        # 👈 Left: Label + info
        InfoLabel(parent, label_text, info=info_text).grid(row=row, column=0)

        # 👉 Right: Radio buttons vertically stacked in a frame
        radio_frame = Frame(parent)
        radio_frame.grid(row=row, column=1, sticky="w", padx=5, pady=5)

        for i, opt in enumerate(options):
            Radiobutton(radio_frame, text=opt, variable=self.var, value=opt).grid(
                row=i, column=0, sticky="w"
            )

    def get(self):
        return self.var.get()
  
###############################################################################
# Boolean entry class
###############################################################################
class BooleanSelect:
    def __init__(self, parent, row, label_text, options, default=None, info_text=None):
        self.var = StringVar(value=default if default is not None else options[0])

        # 👈 Label + Info
        InfoLabel(parent, label_text, info=info_text).grid(row=row, column=0)

        # 👉 Horizontal radio buttons in column 1
        radio_frame = Frame(parent)
        radio_frame.grid(row=row, column=1, sticky="w", padx=5)

        for i, opt in enumerate(options):
            Radiobutton(radio_frame, text=opt, variable=self.var, value=opt).pack(
                side=LEFT, padx=(0 if i == 0 else 10, 0)
            )

    def get(self):
        val = self.var.get()
        if val == "True":
            return True
        elif val == "False":
            return False
        return val
###############################################################################
 # Multi select class
 ###############################################################################   
class MultiSelectDropDown:
    def __init__(self, parent, row, label_text, options, default=None, info_text=None):
        self.options = options
        self.selected = set(default) if default else set()
        self.filtered_options = options[:]
        self.parent = parent
        self.is_open = False
        self.dropdown_win = None
        self.listbox = None

        Label(parent, text=label_text).grid(row=row, column=0, sticky="nw", padx=5, pady=5)

        # Outer wrapper frame
        self.wrapper = Frame(parent, bd=1, relief="solid", width=FIXED_INPUT_WIDTH)
        self.wrapper.grid(row=row, column=1, sticky="ew", padx=5, pady=5)
        parent.grid_columnconfigure(1, weight=1)

        # Inner layout: tags above entry + toggle
        self.tags_frame = Frame(self.wrapper)
        self.tags_frame.pack(side=TOP, anchor="w", fill="x")

        entry_wrapper = Frame(self.wrapper)
        entry_wrapper.pack(side=TOP, fill="x")

        self.entry_var = StringVar()
        self.entry = Entry(entry_wrapper, textvariable=self.entry_var, borderwidth=0)
        self.entry.pack(side=LEFT, fill="x", expand=True)

        self.toggle_btn = Button(entry_wrapper, text="▼", width=2, command=self.toggle_dropdown)
        self.toggle_btn.pack(side=LEFT)

        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown)
        self.entry.bind("<Return>", self.add_first_match)
        self.entry.bind("<BackSpace>", self._on_backspace)

        self.root = parent.winfo_toplevel()
        self.canvas = self._find_canvas(parent)
        self.root.bind_all("<Button-1>", self.handle_click_outside, add="+")

        self.refresh_tags()

    def _find_canvas(self, widget):
        while widget:
            if isinstance(widget, Canvas):
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
        self.dropdown_win = Toplevel(self.parent)
        self.dropdown_win.overrideredirect(True)
        self.dropdown_win.geometry(f"{self.wrapper.winfo_width()}x100+{x}+{y}")
        self.dropdown_win.attributes("-topmost", True)

        self.listbox = Listbox(self.dropdown_win, height=5, selectmode="multiple")
        self.listbox.pack(fill="both", expand=True)
        self.listbox.bind("<ButtonRelease-1>", self.on_select)

        self.update_listbox()
        self.is_open = True
        self._update_dropdown_position()

    def _update_dropdown_position(self):
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
                self.hide_dropdown()
                return

            x = self.entry.winfo_rootx()
            y = entry_root_y + entry_height
            self.dropdown_win.geometry(f"{self.wrapper.winfo_width()}x100+{x}+{y}")

            self.entry.after(100, self._update_dropdown_position)

        except Exception as e:
            print("Dropdown positioning error:", e)

    def update_listbox(self):
        if not self.listbox:
            return
        self.listbox.delete(0, END)
        for option in self.filtered_options:
            self.listbox.insert(END, option)
            if option in self.selected:
                self.listbox.selection_set(END)

    def on_entry_key(self, event=None):
        typed = self.entry_var.get().strip().lower()
        self.filtered_options = [opt for opt in self.options if typed in opt.lower() and opt not in self.selected]
        self.show_dropdown()
        self.update_listbox()

    def on_select(self, event=None):
        if not self.listbox:
            return
        indices = self.listbox.curselection()
        for i in indices:
            item = self.listbox.get(i)
            if item not in self.selected:
                self.selected.add(item)
        self.entry_var.set("")
        self.refresh_tags()
        self.hide_dropdown()

    def add_first_match(self, event=None):
        if self.filtered_options:
            self.selected.add(self.filtered_options[0])
            self.entry_var.set("")
            self.refresh_tags()
            self.hide_dropdown()

    def refresh_tags(self):
        for widget in self.tags_frame.winfo_children():
            widget.destroy()
    
        for item in self.selected:
            tag = Frame(self.tags_frame, bd=1, relief="ridge", padx=2, pady=1)
            Label(tag, text=item, font=("Segoe UI", 9), wraplength=FIXED_INPUT_WIDTH - 40, justify="left").pack(side=LEFT)
            Button(tag, text="✕", command=lambda i=item: self.remove_tag(i),
                   padx=1, pady=0, font=("Segoe UI", 8), width=2).pack(side=LEFT)
            tag.pack(fill="x", pady=2, padx=2, anchor="w")

    def remove_tag(self, item):
        self.selected.discard(item)
        self.refresh_tags()

    def _on_backspace(self, event):
        if not self.entry_var.get() and self.selected:
            last = list(self.selected)[-1]
            self.remove_tag(last)

    def hide_dropdown(self):
        if self.dropdown_win:
            self.dropdown_win.destroy()
            self.dropdown_win = None
        self.listbox = None
        self.is_open = False

    def handle_click_outside(self, event):
        if self.dropdown_win and str(event.widget).startswith(str(self.dropdown_win)):
            return
        if event.widget not in (self.entry, self.toggle_btn):
            self.hide_dropdown()
    
    def set_options(self, new_options):
        self.options = new_options
        self.filtered_options = new_options[:]  # reset filtered view
        self.selected.clear()  # clear all previous selections
        self.entry_var.set("")  # clear the entry box
        self.refresh_tags()  # remove visual tags
        if self.listbox:  # refresh dropdown if open
            self.update_listbox()



    def get(self):
        return list(self.selected)


    