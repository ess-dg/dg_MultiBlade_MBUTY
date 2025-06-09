# -*- coding: utf-8 -*-
"""
Created on Wed May 21 16:43:15 2025

@author: sheilamonera
"""
###############################################################################
"""
Things to add/improve:
    - comment code better
    - Add a reset defaults button 
    - Add an option to save selected params in json
    - Add option to load default params from json 
    - Add styling/ make it look nicer
"""
###############################################################################
# === Imports ===
import os
import sys
import threading
import subprocess
import json
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox
from GUI.custom_classes import (
    SearchableDropDown,
    ExpandableSection,
    ValidatedEntry,
    RadioEntry,
    BooleanSelect,
    label_width,
    FIXED_INPUT_WIDTH,
    RangeEntryWidgets,
    MultiSelectDropDown
)
from GUI.gui_config import config
import matplotlib.pyplot as plt
import glob

# === Global State ===
analysis_running = False          # Flag to prevent concurrent runs
backend_thread = None             # Thread running backend analysis
proc = None                       # Subprocess object
widgets = {}                      # Dictionary to store all UI widgets by key


# === Scrollable Canvas Behavior ===
def resize_canvas(event=None): # Resize the canvas width to match its parent frame during layout updates.
    canvas.itemconfig("inner_frame", width=canvas.winfo_width())

def update_param_scrollregion(event=None):
    """
    Update the scroll region of the parameter canvas based on content size.
    Binds/unbinds mousewheel scrolling depending on whether scrolling is needed.
    """
    bbox = canvas.bbox("all")
    if bbox is None:
        return
    canvas.configure(scrollregion=bbox)
    content_height = bbox[3] - bbox[1]
    visible_height = canvas.winfo_height()
    if content_height <= visible_height:
        canvas.unbind_all("<MouseWheel>")
        canvas.yview_moveto(0)
    else:
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

def _on_mousewheel(event): # Scroll the canvas using the mouse wheel on Windows/macOS.
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

def _on_mousewheel_linux(event): # Scroll the canvas using the mouse wheel on Linux (button 4/5 events).
    canvas.yview_scroll(-1 if event.num == 4 else 1, "units")

def _bind_mousewheel(event): # Bind mousewheel events to the canvas for scrolling.
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", _on_mousewheel_linux)
    canvas.bind_all("<Button-5>", _on_mousewheel_linux)

def _unbind_mousewheel(event): # Unbind all mousewheel events from the canvas to disable scrolling.
    canvas.unbind_all("<MouseWheel>")
    canvas.unbind_all("<Button-4>")
    canvas.unbind_all("<Button-5>")
    
# === Build Parameter UI ===
def build_parameter_ui(parent_frame):
    """
    Build the full parameter input interface inside a scrollable canvas.

    This function creates:
    - A left-hand scrollable parameter panel (`canvas`) where all configuration
      inputs are grouped into static and expandable sections.
    - A right-hand output panel (`output_wrapper`) to display console output
      or plot previews during/after analysis.
    - Modifies global variables: `canvas`, `frame`, and `output_wrapper`.
    - Populates the global `widgets` dictionary with UI widget instances.
    
    For each parameter in the `config` dictionary, the appropriate widget is
    created and added to the UI by calling `display_param()`.

    Parameters:
        parent_frame (tk.Frame): The container frame where both the parameter
                                 section (left) and output section (right) are placed.
    """
    global frame, output_wrapper, canvas

    # Left side: scrollable parameter input
    wrapper = tk.LabelFrame(parent_frame, text="Parameters", width=600)
    wrapper.grid(row=0, column=0, sticky="ns", padx=(0, 5), pady=5)
    wrapper.grid_rowconfigure(0, weight=1)
    wrapper.grid_columnconfigure(0, weight=1)

    # Canvas with vertical scrollbar
    canvas = tk.Canvas(wrapper, width=600)
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar = ttk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame inside canvas that holds all widgets
    frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw", tags="inner_frame")

    # Scroll and resize bindings
    canvas.bind("<Configure>", resize_canvas)
    frame.bind("<Configure>", lambda e: canvas.after(50, update_param_scrollregion))
    frame.bind("<Enter>", _bind_mousewheel)
    frame.bind("<Leave>", _unbind_mousewheel)

    # Right side: output display
    output_wrapper = tk.LabelFrame(parent_frame, text="Output", width=600)
    output_wrapper.grid_rowconfigure(0, weight=1)
    output_wrapper.grid_columnconfigure(0, weight=1)
    output_wrapper.grid_propagate(True)

    # Static (always visible) inputs
    static_section = tk.Frame(frame)
    static_section.pack(fill="x", pady=5)
    static_section.grid_columnconfigure(0, minsize=label_width)
    static_section.grid_columnconfigure(1, minsize=FIXED_INPUT_WIDTH, weight=0)

    row = 0
    for key, item in config["static"].items(): # Static = always-visible top-level parameters
        row = display_param(static_section, key, item, row, widgets, config)

    # Other sections = collapsible/expandable grouped parameter sets
    for section_name, section_items in config.items():
        if section_name == "static":
            continue
        section = ExpandableSection(frame, section_name.replace("_", " ").title() + " Parameters")
        section.pack(fill="x", padx=10, pady=10)
        section_frame = section.get_content_frame()
        section_frame.grid_columnconfigure(0, minsize=label_width)
        section_frame.grid_columnconfigure(1, minsize=FIXED_INPUT_WIDTH, weight=0)

        row = 0
        for key, item in section_items.items():
            row = display_param(section_frame, key, item, row, widgets, config)


# === Display a Single Input Widget ===
def display_param(frame, key, item, row, widgets, config):
    """
    Create and place a dynamic parameter input widget based on config metadata.

    This function reads the configuration dictionary to determine the input
    type (e.g., entry, dropdown, range, etc.), creates the appropriate custom
    widget, and places it in the provided frame at the specified row. It also
    handles conditional visibility based on dependency rules (`dependsOn`).

    Parameters:
        frame (tk.Frame): The parent frame where the input row should be placed.
        key (str): The full config key representing the parameter (e.g., "parameters.plotting.savePlot").
        item (dict): A dictionary describing the parameter's metadata, including:
                     - type (str): input widget type
                     - label (str): label to display
                     - info (str, optional): tooltip text
                     - default: default value
                     - options (list, optional): for dropdowns/radio/multi
                     - dependsOn (tuple, optional): (key, required_value)
        row (int): The current row number in the grid layout.
        widgets (dict): A shared dictionary to store widget instances by key.
        config (dict): The full configuration structure for all parameters.

    Returns:
        int: The updated row index (row + 1), to be passed for the next widget.
    """
    input_type = item["type"]
    label = item["label"]
    depends_on = item.get("dependsOn")

    # Frame to hold label + widget
    row_frame = tk.Frame(frame)
    row_frame.grid(row=row, column=0, columnspan=2, sticky="ew")
    row_frame.grid_columnconfigure(0, minsize=label_width)
    row_frame.grid_columnconfigure(1, minsize=FIXED_INPUT_WIDTH, weight=0)
    
    # Dependency logic: only show if condition met
    def should_show():
        if not depends_on:
            return True
        controller_key, required_value = depends_on
        controller_val = widgets.get(controller_key)
        if controller_val is None:
            return False
        val = controller_val.get() if hasattr(controller_val, "get") else None
        return val == required_value or val in (required_value if isinstance(required_value, list) else [required_value])

    def on_dependency_change(*args):
        if should_show():
            row_frame.grid()
        else:
            row_frame.grid_remove()

    # Build kwargs - Basic arguments passed to all widget constructors
    kwargs = {
        "row": 0,
        "label_text": label,
        "info_text": item.get("info", None),
    }
    if "default" in item:
        kwargs["default"] = item["default"]

    # Create the correct widget type
    if input_type == "entry":
        kwargs.update({
            "validation_type": item.get("inputValidation", "any"),
            "value_range": item.get("range"),
        })
        widget = ValidatedEntry(row_frame, **kwargs)

    elif input_type == "range":
        kwargs["input_validation"] = item.get("inputValidation", "float")
        widget = RangeEntryWidgets(row_frame, **kwargs)

    elif input_type == "bool":
        kwargs["options"] = item["options"]
        widget = BooleanSelect(row_frame, **kwargs)

    elif input_type == "radio":
        kwargs["options"] = item["options"]
        widget = RadioEntry(row_frame, **kwargs)

    elif input_type == "dropdown":
        kwargs["options"] = item["options"]
        widget = SearchableDropDown(row_frame, **kwargs)
        
    elif input_type == "multiSelect":
        # Special case: dynamically gets files based on filePath
        if key == "parameters.fileManagement.fileName":
            file_path_widget = widgets.get("parameters.fileManagement.filePath")
    
            def update_file_list(*_):
                if file_path_widget:
                    folder = file_path_widget.get()
                    try:
                        file_list = [f for f in os.listdir(folder) if f.endswith(".pcapng")]
                    except Exception as e:
                        file_list = []
                    widget.set_options(file_list)
    
            # Initial options
            folder = file_path_widget.get() if file_path_widget else ""
            try:
                initial_files = [f for f in os.listdir(folder) if f.endswith(".pcapng")]
            except Exception as e:
                initial_files = []
    
            kwargs["options"] = initial_files
    
            widget = MultiSelectDropDown(row_frame, **kwargs)
    
            # Dynamically update options when filepath changes
            if hasattr(file_path_widget, "var"):
                file_path_widget.var.trace_add("write", update_file_list)
    
        else:
            widget = MultiSelectDropDown(row_frame, **kwargs)



    else:
        print(f"Unknown input type: {input_type} for key {key}")
        return row + 1

    # Register widget and setup visibility control for hiding/showing
    widgets[key] = widget
    widget._row_frame = row_frame  
    widget.should_show = should_show

    if depends_on:
        controller_key, _ = depends_on
        if controller_key in widgets:
            controller = widgets[controller_key]
            if hasattr(controller, "var"):  # handles most of your custom classes
                controller.var.trace_add("write", on_dependency_change)

    if not should_show():
        row_frame.grid_remove()

    return row + 1

# === Trigger Analysis ===
def run_analysis():
    """
    Trigger the backend analysis:
    - Validates inputs
    - Saves parameters to temp JSON
    - Spawns a subprocess to run the backend script
    - Displays output in a console widget
    - Opens resulting plots after analysis completes
    """
    global analysis_running, backend_thread
    # === Check if already running an analysis ===
    if analysis_running:
        messagebox.showwarning("Please Wait", "An analysis is already running.\nPlease wait for it to finish before starting another.")
        return
    analysis_running = True

    # === Redirect stdout to console widget ===
    class StdoutRedirector:
        """
        A helper class that redirects printed output (stdout) to a Tkinter Text widget.
    
        This allows backend messages and print statements to appear in the GUI's
        console area instead of the terminal.
    
        Attributes:
            text_widget (tk.Text): The Text widget where output should be displayed.
        """
        def __init__(self, text_widget):
            self.text_widget = text_widget
    
        def write(self, string):
            try:
                if self.text_widget.winfo_exists():
                    self.text_widget.insert(tk.END, string)
                    self.text_widget.see(tk.END)
                    self.text_widget.update_idletasks()
            except (tk.TclError, RuntimeError):
                pass
    
        def flush(self):
            pass

    # === Validate and gather selected parameters ===
    missing = []
    selected = {}
    for key, widget in widgets.items():
        if hasattr(widget, "should_show") and not widget.should_show():
            continue
        value = widget.get() if hasattr(widget, "get") else widget.get()
        if value in ("", None, []):
            label = key
            for section in config.values():
                if key in section:
                    label = section[key].get("label", key)
                    break
            missing.append(label)
        else:
            selected[key] = value

    if missing:
        messagebox.showerror("Missing Fields", "Please fill in or correct:\n- " + "\n- ".join(missing))
        analysis_running = False
        return
    
    # Save selected to a temp JSON file
    def save_to_temp_json(selected_dict):
        """
        Save selected configuration values to a temporary JSON file.

        Parameters:
            selected_dict (dict): Dictionary of validated input parameters.
    
        Returns:
            str: Path to the temporary JSON file.
        """
        tmp_file = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json")
        json.dump(selected_dict, tmp_file, indent=2)
        tmp_file.close()
        return tmp_file.name
    
    
    # === Prepare layout – show output panel and clear contents ===
    if not output_wrapper.winfo_ismapped():
        output_wrapper.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)

    for widget in output_wrapper.winfo_children():
        widget.destroy()
        
    plt.close("all")
    
    # === Create console output directly inside output_wrapper ===
    tk.Label(output_wrapper, text="Console Output", font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x", padx=10, pady=(10, 0))

    console_scrollbar = ttk.Scrollbar(output_wrapper)
    console_scrollbar.pack(side="right", fill="y")

    text_widget = tk.Text(
        output_wrapper,
        wrap="word",
        bg="black",
        fg="white",
        insertbackground="white",
        font=("Courier New", 10),
        yscrollcommand=console_scrollbar.set
    )
    text_widget.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=(0, 10))
    console_scrollbar.config(command=text_widget.yview)

    sys.stdout = StdoutRedirector(text_widget)

    # === Bind mousewheel directly to text_widget (output_canvas is gone) ===
    def on_console_enter(event):
        text_widget.bind_all("<MouseWheel>", lambda e: text_widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))
    def on_console_leave(event):
        text_widget.unbind_all("<MouseWheel>")
    text_widget.bind("<Enter>", on_console_enter)
    text_widget.bind("<Leave>", on_console_leave)

    def on_console_enter_linux(event):
        text_widget.bind_all("<Button-4>", lambda e: text_widget.yview_scroll(-1, "units"))
        text_widget.bind_all("<Button-5>", lambda e: text_widget.yview_scroll(1, "units"))
    def on_console_leave_linux(event):
        text_widget.unbind_all("<Button-4>")
        text_widget.unbind_all("<Button-5>")
    text_widget.bind("<Enter>", on_console_enter_linux, add='+')
    text_widget.bind("<Leave>", on_console_leave_linux, add='+')

    # === Backend thread runs computation and shows results ===
    def read_output(pipe, is_error=False):
        for line in iter(pipe.readline, ''):
            if is_error:
                print("STDERR:", line, end='')
            else:
                print(line, end='')
        pipe.close()
    
    def monitor_proc(proc):
        """
        Wait for the subprocess to finish and then open any saved plot images.
    
        Parameters:
            proc (subprocess.Popen): The running backend subprocess.
        """
        global analysis_running
        proc.wait()  # Wait for the backend process to finish
    
        # Mark analysis as complete so user can re-run
        analysis_running = False
        print("Analysis finished.")
    
        # === Open saved plots with interactive viewer ===
        def show_saved_plots():
            plot_dir = os.path.join(os.getcwd(), "gui_plots")
            image_files = sorted(glob.glob(os.path.join(plot_dir, "plot_*.png")))
            if not image_files:
                print("No plots found.")
                return
    
            for img_file in image_files:
                img = plt.imread(img_file)
                plt.figure()
                plt.imshow(img)
                plt.axis("off")
                plt.title(os.path.basename(img_file))
    
            plt.show()  # One single call to launch all figures
    
        output_wrapper.after(100, show_saved_plots)  # Ensure it runs on main thread

    
    def backend_work():
        """
        Internal worker thread that:
        - Saves parameter config
        - Launches the backend subprocess
        - Redirects stdout/stderr to GUI
        - Monitors completion
        """
        global analysis_running, proc
        try:
            print("\nRunning analysis with selected parameters...\n")
    
            # Save selected config to a temp file
            temp_config_path = save_to_temp_json(selected)
    
            # Start subprocess
            proc = subprocess.Popen(
                ["python", "-u", "MBUTYcap_V6x0.py", "from_gui", temp_config_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
    
            # Start threads to read output
            threading.Thread(target=read_output, args=(proc.stdout, False), daemon=True).start()
            threading.Thread(target=read_output, args=(proc.stderr, True), daemon=True).start()
    
            # Monitor when it's done
            threading.Thread(target=monitor_proc, args=(proc,), daemon=True).start()

        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            analysis_running = False  # Reset flag if error

    # Start backend in its own thread (non-blocking)
    backend_thread = threading.Thread(target=backend_work)
    backend_thread.start()

# === Main GUI Loop ===
def main():
    """
    Initialize and launch the Tkinter GUI:
    - Sets up window layout
    - Builds parameter input UI
    - Adds Run button
    - Handles graceful termination of subprocess on exit
    """
    global win, main_frame
    # Create window
    win = tk.Tk()
    win.title("MBUTY GUI")
    win.geometry("1200x700")
    win.grid_rowconfigure(2, weight=1)
    win.grid_columnconfigure(0, weight=1)

    # Welcome message
    user_name = os.environ.get('USER', os.environ.get('USERNAME', 'User'))
    tk.Label(win, text=f"Ciao {user_name}! Welcome to MBUTY 5.2", font=("Segoe UI", 14, "bold"), fg="#228B22", pady=10).grid(row=0, column=0, pady=(10, 0), sticky="n")
    tk.Label(win, text="―" * 40, fg="#aaa").grid(row=1, column=0, pady=(0, 5))

    # Main container
    main_frame = tk.Frame(win)
    main_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=0)
    main_frame.grid_rowconfigure(0, weight=1)

    build_parameter_ui(main_frame)

    # Run analysis button
    tk.Button(main_frame, text="Run Analysis", command=run_analysis, font=("Segoe UI", 12, "bold"), bg="#90ee90").grid(row=3, column=0, columnspan=2, pady=[10, 50], sticky="n")

    def on_closing():
        """Terminate any running process and close the GUI and plots cleanly."""
        global proc
        if proc and proc.poll() is None:
            proc.terminate()
        win.destroy()
        plt.close("all")

    win.protocol("WM_DELETE_WINDOW", on_closing)
    win.mainloop()


# === Entry Point ===
if __name__ == "__main__":
    main()



