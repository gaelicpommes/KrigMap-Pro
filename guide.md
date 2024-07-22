# KrigMap Pro User Guide

Welcome to the KrigMap Pro user guide. This document will help you navigate and utilize the features of KrigMap Pro effectively. Below is a step-by-step guide to each component of the application.

## Getting Started with KrigMap Pro

### Main Window Overview
Upon launching `main_window.py`, you will be presented with the main window titled "Krige Application." This window contains several widgets that can be accessed using the scrollbars on the right and bottom sides of the window.

<p align="center">
  <img src="https://github.com/user-attachments/assets/4075b190-9997-4fd9-b5c6-190a2d247eea" alt="Sample Image">
  <br>
  <em>Figure 1: Main Application Window</em>
</p>

### 1. Select File

#### Open One File
- Click the **Open One File** button to browse and select a file.
- Only `.xlsx`, `.xls`, and `.csv` files can be loaded.
- If the selected file has more than three columns, a new window will pop up asking you to specify which columns to use as Longitude, Latitude, and Result.

![Figure 2: Select File Widget](path/to/figure2.png)
![Figure 3: Column Selection Dialog](path/to/figure3.png)

<p align="center">
  <img src="https://github.com/user-attachments/assets/c759f590-97c4-4813-b465-403f0cf2b341"
 alt="Sample Image">
  <br>
  <em>Figure 2: Select File Widget</em>
</p>

<p align="center">
  <img src="https://github.com/user-attachments/assets/effddf72-f1b2-429f-adb9-22a1e3e77444"

 alt="Sample Image">
  <br>
  <em>Figure 3: Column Selection Dialog</em>
</p>

#### Open Multiple Files
- Click the **Open Multiple Files** button to select multiple files from your directory.
- The files will appear in the Treeview widget, showing file names and dropdowns for column names.
- Use the colored combo boxes to select the columns for Longitude, Latitude, and Result.

![Figure 4: Multiple File Selection](path/to/figure4.png)

### 2. Enter Threshold Value

This widget allows you to set a threshold value to filter spatial points. Points are converted from WGS 84 to UTM coordinates to facilitate this.

- Press **Confirm Threshold** to apply the filter. 
- Use the **Save Threshold Data** button to save the filtered dataset.

### 3. Variogram Parameters

Set the parameters for variogram analysis in this widget. 

- Untick **fit_sigma** to exclude weights in the lag or distance.
- For manual fit methods, specify your parameters for psill, range, and nugget.

Press **Plot Variogram** to generate the variogram plot in a new tab labeled "Variogram Plot."

![Figure 7: Variogram Parameters Widget](path/to/figure7.png)
![Figure 8: Manual Fit Method](path/to/figure8.png)

### 4. Kriging Plot and Parameters

In this section, set the parameters for Kriging. Optional checkboxes for Basemap and Uncertainty Map are available.

- If **Basemap** is ticked, a satellite map will appear beneath the Krige plot.
- If **Uncertainty Map** is selected, a corresponding uncertainty map will be displayed in a separate plot.

### 5. Plots

This final widget allows you to generate different types of plots:

- **Raw Histogram**: Input a decimal to view a fraction of the dataset; leave blank to see the entire set.
- **Scatterplot**: Similar input method as Raw Histogram.

### Toolbars and Plot Customization

Each plot window comes with a toolbar allowing you to pan, zoom, and modify plot dimensions. The **Figure Options** dialog lets you adjust plot titles, axes labels, and style.

![Figure 14: Toolbar Options](path/to/figure14.png)






