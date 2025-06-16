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
import ctypes
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from GUI import (
    SearchableDropDown,
    ValidatedEntry,
    MultiSelectDropDown,
    RangeEntryWidgets,
    RadioEntry,
    BooleanSelect,
    ExpandableSection,
    FIXED_INPUT_WIDTH,
    label_width
)
from GUI.gui_config import config, parameters
from GUI.console_widgets import ANSIColorTextWidget, ConsoleRedirector
import matplotlib.pyplot as plt
from MBUTYcap import MBUTYmain

# === Global State ===
analysis_running = False          # Flag to prevent concurrent runs
backend_thread = None             # Thread running backend analysis
widgets = {}                      # Dictionary to store all UI widgets by key
plot_process = None               # Global handle to the viewer subprocess
stop_button = None

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

def setup_dynamic_file_options(widget, file_path_widget, file_filter):
    """
    Dynamically updates `widget` options based on the folder path from `file_path_widget`.

    On initialization, preserves the widget's current selection.
    On path change, clears and updates options.
    """
    def update_file_list(*_):
        if file_path_widget:
            folder = file_path_widget.get()
            try:
                file_list = [f for f in os.listdir(folder) if f.endswith(file_filter)]
            except Exception:
                file_list = []

            # Apply new options and clear current value
            widget.set_options(file_list)

    # === Initial setup (preserve any pre-set default) ===
    folder = file_path_widget.get() if file_path_widget else ""
    try:
        initial_files = [f for f in os.listdir(folder) if f.endswith(file_filter)]
    except Exception:
        initial_files = []

    # Only set initial options — don't reset selection
    if hasattr(widget, "set_options"):
        widget.set_options(initial_files)


    # === Register path change listener ===
    if hasattr(file_path_widget, "var"):
        file_path_widget.var.trace_add("write", update_file_list)



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
        item (dict): Metadata describing the parameter (type, label, default, dependsOn, etc.).
        row (int): Current row number in the layout grid.
        widgets (dict): Dictionary of all created widget instances keyed by config path.
        config (dict): Full configuration schema (not used directly here, but included for extensibility).

    Returns:
        int: The updated row index (row + 1), to be used for the next widget.
    """
    input_type = item["type"]
    label = item["label"]
    depends_on = item.get("dependsOn")

    # === Helper: Evaluates complex dependency expressions (with support for nested 'and' / 'or') ===
    def should_show(depends_on):
        """
        Evaluates whether a widget should be visible, based on `dependsOn` logic.

        Supports:
            - Single (key, value) or (key, [value1, value2])
            - Nested {'and': [...]}, {'or': [...]}
        """
        if not depends_on:
            return True  # No dependency means always show

        def evaluate(condition):
            # Base case: (key, expected_value)
            if isinstance(condition, tuple) and len(condition) == 2:
                key, required = condition
                widget = widgets.get(key)
                if widget is None:
                    return False
                val = widget.get() if hasattr(widget, "get") else None
                return val == required or (isinstance(required, (list, tuple)) and val in required)

            # Nested logic
            if isinstance(condition, dict):
                if "and" in condition:
                    return all(evaluate(sub) for sub in condition["and"])
                if "or" in condition:
                    return any(evaluate(sub) for sub in condition["or"])

            return False  # fallback for malformed input

        return evaluate(depends_on)

    # === Helper: Recursively collect all keys involved in a dependency expression ===
    def extract_dependency_keys(depends_on):
        """
        Recursively extracts all widget keys involved in the dependency logic,
        so that we can attach trace callbacks to them.

        Supports:
            - Single (key, value)
            - Nested {'and': [...]}, {'or': [...]}
            - Lists of conditions
        """
        keys = set()
        if not depends_on:
            return keys
        if isinstance(depends_on, tuple) and len(depends_on) == 2:
            keys.add(depends_on[0])
        elif isinstance(depends_on, dict):
            logic_key = "and" if "and" in depends_on else "or"
            for sub in depends_on.get(logic_key, []):
                keys.update(extract_dependency_keys(sub))
        elif isinstance(depends_on, list):  # handle legacy or flat lists
            for sub in depends_on:
                keys.update(extract_dependency_keys(sub))
        return keys

    # === Create row frame to hold label + input ===
    row_frame = tk.Frame(frame)
    row_frame.grid(row=row, column=0, columnspan=2, sticky="ew")
    row_frame.grid_columnconfigure(0, minsize=label_width)
    row_frame.grid_columnconfigure(1, minsize=FIXED_INPUT_WIDTH, weight=0)

    # === Callback when any controlling widget value changes ===
    def on_dependency_change(*args):
        if should_show(depends_on):
            row_frame.grid()
        else:
            row_frame.grid_remove()

    # === Shared kwargs passed to widget constructors ===
    kwargs = {
        "row": 0,
        "label_text": label,
        "info_text": item.get("info", None),
    }
    if "default" in item:
        kwargs["default"] = item["default"]

    # === Create the correct widget type ===
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
        kwargs["options"] = item.get("options", [])
        widget = SearchableDropDown(row_frame, **kwargs)

        # If dynamic file loading is used
        dynamic_path_key = item.get("optionsFromPath")
        file_filter = item.get("fileTypeFilter")
        if dynamic_path_key and file_filter:
            file_path_widget = widgets.get(dynamic_path_key)
            setup_dynamic_file_options(widget, file_path_widget, file_filter)

    elif input_type == "multiSelect":
        kwargs["options"] = item.get("options", [])
        widget = MultiSelectDropDown(row_frame, **kwargs)

        # If dynamic file loading is used
        dynamic_path_key = item.get("optionsFromPath")
        file_filter = item.get("fileTypeFilter")
        if dynamic_path_key and file_filter:
            file_path_widget = widgets.get(dynamic_path_key)
            setup_dynamic_file_options(widget, file_path_widget, file_filter)

    elif input_type == "subheading":
        heading = tk.Label(
            frame,
            text=label,
            font=("Segoe UI", 10, "bold", "underline"),
            anchor="w",
            pady=5,
        )
        heading.grid(row=row, column=0, columnspan=2, sticky="ew", pady=(10, 5))
        return row + 1

    else:
        print(f"Unknown input type: {input_type} for key {key}")
        return row + 1

    # === Register the widget in the global widgets dictionary ===
    widgets[key] = widget
    widget._row_frame = row_frame  # Save reference to parent row frame
    widget.should_show = lambda: should_show(depends_on)

    # === Attach dependency listeners to all controlling keys ===
    for controller_key in extract_dependency_keys(depends_on):
        controller = widgets.get(controller_key)
        if controller and hasattr(controller, "var"):
            controller.var.trace_add("write", on_dependency_change)

    # === Initial visibility check ===
    if not should_show(depends_on):
        row_frame.grid_remove()

    return row + 1



def raise_keyboard_interrupt(thread):
    """Forcefully raise KeyboardInterrupt in a thread."""
    if not thread or not thread.is_alive():
        return
    tid = ctypes.c_long(thread.ident)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(KeyboardInterrupt))
    if res == 0:
        raise ValueError("Invalid thread ID")
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")



def close_saved_plots():
    """Terminate the saved plot viewer subprocess if running."""
    global plot_process
    try:
        if plot_process and plot_process.poll() is None:
            print("Closing plot viewer...")
            plot_process.terminate()
            plot_process = None
    except Exception as e:
        print(f"Warning: Failed to close plot viewer: {e}")

def stop_back_end():
    global backend_thread
    try:
        raise_keyboard_interrupt(backend_thread)
        print("Stop signal sent to backend thread.")
    except Exception as e:
        print(f"Failed to stop backend thread: {e}")


def clear_plot_folder():
    """
    Delete and recreate the gui_plots folder to ensure it's clean before saving new plots.
    """
    plot_dir = os.path.join(os.getcwd(), "gui_plots")
    try:
        if os.path.exists(plot_dir):
            shutil.rmtree(plot_dir)
        os.makedirs(plot_dir)
    except Exception as e:
        print(f"Failed to clear plot folder: {e}")
        
    


    def flush(self):
        # Also ensure flush attempts to use the widget only if it exists
        if self.text_widget and self.text_widget.winfo_exists():
            self.text_widget.flush()
        else:
            self.original_stdout_fallback.flush()


# === Trigger Analysis ===
def run_analysis():
    """
    Trigger the backend analysis:
    - Validates inputs
    - Applies config to parameters
    - Runs backend logic in a thread
    - Displays output in console
    - Shows saved plots after analysis
    """
    global analysis_running, backend_thread

    if analysis_running:
        messagebox.showwarning("Please Wait", "An analysis is already running.\nPlease wait for it to finish before starting another.")
        return
    analysis_running = True

    # --- Start of modified code ---
    # Remove your custom StdoutRedirector class from here.
    # It's now defined globally (or just above where it's used the first time, in this case).

    # === Validate and gather input values ===
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
    
    
    # === Apply input values to parameters ===
    for key, value in selected.items():
        for section_dict in config.values():
            if key in section_dict:
                setter = section_dict[key].get("set")
                if setter:
                    setter(value)
                break

    # === Prepare layout and clear output ===
    stop_button.grid() # Display the "stop analysis" button
    if not output_wrapper.winfo_ismapped(): # Display the output panel if not already displayed
        output_wrapper.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=5)
        main_frame.grid_columnconfigure(0, weight=0)
        main_frame.grid_columnconfigure(1, weight=1)

    for widget in output_wrapper.winfo_children(): # clear output panel ready for new analysis
        widget.destroy()
    
    # Close the plots from previous run and clear the folder before starting new analysis
    close_saved_plots()
    clear_plot_folder()

    # === Setup console output area ===
    tk.Label(output_wrapper, text="Console Output", font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x", padx=10, pady=(10, 0))

    console_scrollbar = ttk.Scrollbar(output_wrapper)
    console_scrollbar.pack(side="right", fill="y")

    # Change this line:
    console_text_widget = ANSIColorTextWidget( # Use the new class
        output_wrapper,
        wrap="word",
        bg="black",
        fg="white",
        insertbackground="white", # This will be ignored since state is disabled
        font=("Courier New", 10),
        yscrollcommand=console_scrollbar.set
    )
    console_text_widget.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=(0, 10))
    console_scrollbar.config(command=console_text_widget.yview) # Link scrollbar to the new widget

    # Change this line to use your new ConsoleRedirector:
    sys.stdout = ConsoleRedirector(console_text_widget)

    # === Mousewheel behavior ===
    # These bindings should now be applied to console_text_widget
    def on_console_enter(event):
        console_text_widget.bind_all("<MouseWheel>", lambda e: console_text_widget.yview_scroll(int(-1 * (e.delta / 120)), "units"))
    def on_console_leave(event):
        console_text_widget.unbind_all("<MouseWheel>")
    console_text_widget.bind("<Enter>", on_console_enter)
    console_text_widget.bind("<Leave>", on_console_leave)

    def on_console_enter_linux(event):
        console_text_widget.bind_all("<Button-4>", lambda e: console_text_widget.yview_scroll(-1, "units"))
        console_text_widget.bind_all("<Button-5>", lambda e: console_text_widget.yview_scroll(1, "units"))
    def on_console_leave_linux(event):
        console_text_widget.unbind_all("<Button-4>")
        console_text_widget.unbind_all("<Button-5>")
    console_text_widget.bind("<Enter>", on_console_enter_linux, add='+')
    console_text_widget.bind("<Leave>", on_console_leave_linux, add='+')

    # --- End of modified code ---

    # === Define plot showing logic ===
    def launch_plot_viewer():
        global plot_process
        plot_script = os.path.join(os.path.dirname(__file__), "GUI", "display_saved_plots.py")
        try:
            plot_process = subprocess.Popen([sys.executable, plot_script])
        except Exception as e:
            print(f" Failed to launch plot viewer: {e}")


    # === Backend work in thread ===
    def backend_work():
        global analysis_running
        try:
            print("\nRunning analysis with selected parameters...\n")
            # for k, v in selected.items():  # debug code - use to check if params are interpreted properly e.g True vs "True", string vs int etc
            #     print(f"{k}: {v}")
            # print(parameters.dataReduction.softThArray.ThW[:,:])
            MBUTYmain(parameters, runFromGui=True)
            print("\n Analysis complete.\n")
            output_wrapper.after(100, launch_plot_viewer)
        except Exception as e:
            print(f" Error during analysis: {e}")
        finally:
            analysis_running = False
            stop_button.grid_remove()

    backend_thread = threading.Thread(target=backend_work)
    backend_thread.start()

def stop_analysis():
    global analysis_running
    print("\nStop Analysis requested by user.")
    stop_back_end()
    analysis_running = False
    #hide the button again
    if stop_button and stop_button.winfo_ismapped():
        stop_button.grid_remove()
    


# === Main GUI Loop ===
def main():
    """
    Initialize and launch the Tkinter GUI:
    - Sets up window layout
    - Builds parameter input UI
    - Adds Run button
    - Handles graceful termination of subprocess on exit
    """
    global win, main_frame, stop_button
    # Create window
    win = tk.Tk()
    win.title("MBUTY GUI")
    win.geometry("1200x700")
    win.grid_rowconfigure(2, weight=1)
    win.grid_columnconfigure(0, weight=1)
    
    # === Header Frame ===
    header = tk.Frame(win)
    header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
    header.grid_columnconfigure(0, weight=1)
    header.grid_columnconfigure(1, weight=2)
    header.grid_columnconfigure(2, weight=1)
    
    # === Left Logo ===
    left_logo_path = os.path.join("GUI", "logos", "DetGlogo.png")
    if os.path.isfile(left_logo_path):
        try:
            img = Image.open(left_logo_path)
            img_resized = img.resize((120, 60))
            left_img = ImageTk.PhotoImage(img_resized, master=header)
            left_logo = tk.Label(header, image=left_img)
            left_logo.image = left_img
            left_logo.grid(row=0, column=0, rowspan=2, sticky="w", padx=10)
        except Exception as e:
            print(f"Error loading left logo: {e}")
    else:
        print(f"Left logo not found: {left_logo_path}")
    
    # === Center Title ===
    user_name = os.environ.get('USER', os.environ.get('USERNAME', 'User'))
    title = tk.Label(
        header,
        text=f"Ciao {user_name}! Welcome to MBUTY 6.0",
        font=("Segoe UI", 14, "bold"),
        fg="#228B22",
    )
    title.grid(row=0, column=1, sticky="n", pady=(10, 0))
    
    # === Right Logo ===
    right_logo_path = os.path.join("GUI", "logos", "MBlogo.png")
    if os.path.isfile(right_logo_path):
        try:
            img = Image.open(right_logo_path)
            img_resized = img.resize((120, 60))
            right_img = ImageTk.PhotoImage(img_resized, master=header)
            right_logo = tk.Label(header, image=right_img)
            right_logo.image = right_img
            right_logo.grid(row=0, column=2, rowspan=2, sticky="e", padx=10)
        except Exception as e:
            print(f"Error loading right logo: {e}")
    else:
        print(f"Right logo not found: {right_logo_path}")
    
    # === Divider Line ===
    divider = ttk.Separator(win, orient="horizontal")
    divider.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))

    # Main container
    main_frame = tk.Frame(win)
    main_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=0)
    main_frame.grid_rowconfigure(0, weight=1)

    build_parameter_ui(main_frame)

    # Run Analysis button
    run_button = tk.Button(
        main_frame,
        text="Run",
        command=run_analysis,
        font=("Segoe UI", 12, "bold"),
        bg="#90ee90"
    )
    run_button.grid(row=3, column=0, pady=[10, 50], sticky="n")
    
    # Stop Analysis button (initially hidden, appears to right of Run button)
    stop_button = tk.Button(
        main_frame,
        text="Stop",
        command=stop_analysis,
        font=("Segoe UI", 12, "bold"),
        bg="#ff6961"
    )
    stop_button.grid(row=3, column=1, pady=[10, 50], sticky="n")
    stop_button.grid_remove()  # Hidden initially
    
    # Store the original stdout here, before any redirection happens
    original_stdout = sys.stdout 
    
    def on_closing():
        """Terminate any running process and close GUI and plots cleanly."""
        stop_back_end()
        close_saved_plots()
        # Restore original stdout *before* win.destroy()
        sys.stdout = original_stdout 
        win.destroy()
        plt.close("all")


    win.protocol("WM_DELETE_WINDOW", on_closing)
    win.mainloop()


# === Entry Point ===
if __name__ == "__main__":
    main()



