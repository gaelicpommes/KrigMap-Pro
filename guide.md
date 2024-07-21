# ExcelLoaderApp Setup and Usage Guide

This guide provides detailed instructions on setting up and using the ExcelLoaderApp, a Python Qt application for loading and processing data files.

## Prerequisites

Before you begin, ensure you have a Python environment with PyQt installed, as this application uses Qt for the graphical user interface.

## Installation and Setup

### Configure File Paths

The application requires paths to UI files to be configured before running:

#### Main Window

1. Open the file `main_window.py`.
2. Navigate to the `ExcelLoaderApp` class and find the `__init__` method.
3. Modify the file path at line 128 to point to your `main_window.ui` file:
   ```python
   self.ui = uic.loadUi("path/to/main_window.ui", this)

Multiple Files Selection Window
Open select_multiple_files_window.py.
Update the file path at line 41 to point to your select_multiple_files_window.ui
self.ui = uic.loadUi("path/to/select_multiple_files_window.ui", self)

Running the Application
Execute the script main_window.py to start the application.
Using the Application
Main Window
Upon launching, the main window displays the Select File widget, featuring two main functionalities:

Open One File
Click the Open One File button to launch a file chooser.
Select a file with the extensions .xlsx, .xls, or .csv.
If the file has exactly three columns, it will be loaded directly into the application.
For files with more than three columns, a new window prompts you to specify columns for longitude, latitude, and results.
Open Multiple Files
Use the Open Multiple Files button to manage multiple file selections at once.
Enter Threshold Value
After loading a file, enter a numerical threshold value in the Enter Threshold Value widget.
This threshold determines the proximity required to filter data points relative to a specified UTM coordinate.
Data points within this threshold from the original point are filtered out.
Save Your Data
Following data processing, save your results in .xlsx, .csv, or .txt format.
Choose the desired file format and specify the save location.

