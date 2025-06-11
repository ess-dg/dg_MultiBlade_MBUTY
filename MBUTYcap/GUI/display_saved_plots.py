# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 13:35:13 2025

@author: sheilamonera
"""

# GUI/display_saved_plots.py
import os
import glob
import matplotlib
matplotlib.use("TkAgg")  # or Qt5Agg
import matplotlib.pyplot as plt

def show_saved_plots():
    # Plot directory relative to parent directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(script_dir, ".."))
    plot_dir = os.path.join(project_root, "gui_plots")

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

    plt.show()

if __name__ == "__main__":
    show_saved_plots()
