import sys  # System-specific parameters and functions

import pandas as pd  # Data manipulation and analysis
import numpy as np  # Numerical operations

from PyQt5 import QtWidgets, QtGui, uic  # Comprehensive set of Python bindings for Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton,
    QFileDialog, QMessageBox, QProgressDialog, QTableWidget, QTableWidgetItem, QScrollArea,
    QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt, pyqtSignal  # Core non-GUI functionality
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont, QBrush  # GUI-related classes for item models, fonts, etc.

from matplotlib.figure import Figure  # Base class for creating figures in Matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # Canvas widget for Matplotlib plotting
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar  # Navigation toolbar for Matplotlib on Qt

import geopandas as gpd  # Geospatial data in Python
from shapely.geometry import Point  # Geometric objects for geometric operations
from scipy.spatial import ConvexHull  # Convex hull algorithms
import matplotlib.path as MplPath  # General polygonal patch for plotting

import skgstat as skg  # Geostatistical analyses

import seaborn as sns  # Statistical data visualization
import matplotlib.pyplot as plt  # Plotting with Matplotlib

class QtSelectFiles(QMainWindow):
    # Initialization and setup of the class
    ############initialisation and setup################
    # Define a signal that carries data as a pandas DataFrame
    dataSelected = pyqtSignal(pd.DataFrame)  # This signal can be connected to other parts of the program to send data dynamically

    def __init__(self, parent=None):
        # Call the constructor of the parent class, QMainWindow
        super(QtSelectFiles, self).__init__(parent)
        super().__init__()

        # Load the user interface from a file
        uic.loadUi("D:/queet.ui", self)
        
        # Set the title of the window to "Select Files"
        self.setWindowTitle("Select Files")  

        # Initialize the DataFrame that will keep track of files loaded
        self.file_df = pd.DataFrame(columns=['File Number', 'File Name'])
        
        # Counter to keep track of the number of files loaded
        self.file_counter = 0
        
        # List to keep track of columns added to combo boxes for selection
        self.columns_added_to_combos = []
        
        # List to store tables displayed in the UI
        self.tables = []
        
        # Dictionary to store last selections in combo boxes for longitude, latitude, and result columns
        self.last_selections = {'loncol': None, 'latcol': None, 'resultcol': None}
        
        # Dictionary defining the color map for highlighting columns in the UI
        self.color_map = {
            'loncol': "#ADD8E6",  # Light Blue
            'latcol': "#90EE90",  # Soft Green
            'resultcol': "#F08080"  # Light Coral
        }
        
        # Dictionary to keep track of which columns are currently highlighted in the UI
        self.active_highlights = {}
        
        # Variable to store the current DataFrame loaded from the file
        self.current_df = None
        
        # List to store all DataFrames loaded
        self.dataFrames = []
        
        # List to store information about the files loaded
        self.fileInfo = []

        # Find and store UI components for later use
        self.SelectFile = self.findChild(QPushButton, 'selectfile')
        self.ClearFilesButton = self.findChild(QPushButton, 'clearfile')
        self.FileScrollArea = self.findChild(QScrollArea, 'filescrollarea')
        self.FileShowScrollArea = self.findChild(QScrollArea, 'fileshowscrollarea')
        self.LonColCombo = self.findChild(QComboBox, 'loncolcombo')
        self.LatColCombo = self.findChild(QComboBox, 'latcolcombo')
        self.ResultColCombo = self.findChild(QComboBox, 'resultcolcombo')

        # Setup for the tree view displaying file details
        self.treeView = QTreeView()
        self.model = QStandardItemModel()
        self.treeView.setModel(self.model)
        self.treeView.setAlternatingRowColors(True)
        self.treeView.setStyleSheet("QTreeView { background-color: white; alternate-background-color: #f0f0f0; }")
        self.model.setHorizontalHeaderLabels(['File Details'])
        self.rootNode = self.model.invisibleRootItem()  # Root node for the tree

        # Set the model view widget to the scroll area
        self.FileScrollArea.setWidget(self.treeView)

        # Initialize layout for displaying files loaded
        self.file_show_layout = QVBoxLayout()
        self.file_show_widget = QWidget()
        self.file_show_widget.setLayout(self.file_show_layout)
        self.FileShowScrollArea.setWidget(self.file_show_widget)

        # Connect signals to methods for interactive behavior
        self.SelectFile.clicked.connect(self.loadFiles)
        self.LonColCombo.currentTextChanged.connect(lambda text: self.highlightColumn(text, 'loncol'))
        self.LatColCombo.currentTextChanged.connect(lambda text: self.highlightColumn(text, 'latcol'))
        self.ResultColCombo.currentTextChanged.connect(lambda text: self.highlightColumn(text, 'resultcol'))
        self.confirmSelectionButton = self.findChild(QPushButton, 'confirmselection')
        self.confirmSelectionButton.clicked.connect(self.showSelectionWindow)
    
############File Loading and Data Handling######################

    def loadFiles(self):
        # Open a file dialog to allow user to select multiple .xlsx, .csv, or .xls files
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select .xlsx,.csv,.xls Files", "", "All Files (*);;Excel Files (*.xlsx *.xls);;CSV Files (*.csv)")
        
        # Check if any files were selected
        if file_paths:
            # Create a progress dialog to show file loading progress
            progress = QProgressDialog("Loading files...", "Cancel", 0, len(file_paths), self)
            progress.setWindowTitle("Loading Data")
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            
            # A set to track unique column names across all loaded files
            new_columns_set = set()
            
            # Iterate through each selected file
            for index, file_path in enumerate(file_paths):
                # Allow the user to cancel the loading process
                if progress.wasCanceled():
                    break
                
                # Update progress dialog with the current file number and file name
                progress.setValue(index)
                progress.setLabelText(f"Loading: {file_path.split('/')[-1]}")
                
                # Increment file counter and store file info
                self.file_counter += 1
                file_name = file_path.split('/')[-1]
                self.file_df = pd.concat([self.file_df, pd.DataFrame({'File Number': [self.file_counter], 'File Name': [file_name]})], ignore_index=True)
                
                # Load the data from file using pandas
                df = pd.read_excel(file_path) if file_path.lower().endswith(('.xlsx', '.xls')) else pd.read_csv(file_path)
                row_count = len(df)
                columns = df.columns.tolist()
                
                # Update the set of unique columns
                new_columns_set.update(df.columns)
                
                # Store DataFrame and file information
                self.dataFrames.append(df)
                self.fileInfo.append(f"{file_name} - Rows:  {row_count}")
                
                # Create a bold font for displaying the file name in the tree view
                bold_font = QFont()
                bold_font.setBold(True)
                
                # Add a tree view item for the file with the number of rows indicated
                parent_text = f"File {self.file_counter}: {file_name} - {row_count} Rows"
                parent_item = QStandardItem(parent_text)
                parent_item.setFont(bold_font)
                self.rootNode.appendRow(parent_item)
                
                # Add child items for each column in the file
                for idx, col in enumerate(columns):
                    child_item = QStandardItem(f"{idx + 1}. {col}")
                    parent_item.appendRow(child_item)

                # Add the column names to the combo boxes if they are new
                for col in columns:
                    normalized_col = col
                    if normalized_col not in self.columns_added_to_combos:
                        self.columns_added_to_combos.append(normalized_col)
                        for combo in [self.LonColCombo, self.LatColCombo, self.ResultColCombo]:
                            combo.addItem(normalized_col)

                # Expand all nodes in the tree view
                self.treeView.expandAll()

                # Create widgets to display the file's data in a table
                file_display_widget = QWidget()
                file_display_layout = QVBoxLayout(file_display_widget)
                file_display_label = QLabel(f"<b>File {self.file_counter}: {file_name} - {row_count} Rows</b>")
                file_display_label.setTextFormat(Qt.RichText)  # Interpret HTML in the text
                file_display_layout.addWidget(file_display_label)

                # Create a data table for the file's contents
                data_table = self.createDataTable(df, columns)
                data_table.setAlternatingRowColors(True)
                data_table.setStyleSheet("QTableWidget { background-color: white; alternate-background-color: #f0f0f0; }")
                file_display_layout.addWidget(data_table)
                self.file_show_layout.addWidget(file_display_widget)
                
                # Remember the current DataFrame loaded
                self.current_df = df
             
            # Update progress and close it
            progress.setValue(len(file_paths))
            
            # Update combo boxes with new unique columns from all files
            new_columns_list = list(new_columns_set - set(self.columns_added_to_combos))
            self.columns_added_to_combos.extend(new_columns_list)
            self.updateComboBoxes(list(new_columns_set))        


    def createDataTable(self, df, columns):
        # Create a table widget with one more column than the number of columns in the DataFrame to include an index column.
        data_table = QTableWidget(len(df), len(columns) + 1) 
        
        # Define headers for the table; the first header is 'Index' for the new index column.
        headers = ['Index'] + columns
        data_table.setHorizontalHeaderLabels(headers)  # Set the headers to the table
        
        # Hide the vertical headers (row numbers on the left side of the table).
        data_table.verticalHeader().setVisible(False)
        
        # Allow rows to be moved internally within the table.
        data_table.setDragDropMode(QTableWidget.InternalMove)
        
        # Set the behavior to select entire rows at a time.
        data_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Enable scroll bars as needed based on the table's content size.
        data_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        data_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Fix the height and width of the table for consistency.
        data_table.setFixedHeight(400)
        data_table.setFixedWidth(800)
        
        # Allow headers to be rearranged by dragging.
        data_table.horizontalHeader().setSectionsMovable(True)
        
        # Set interactive resizing for headers.
        data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        
        # Alternate row colors for better readability.
        data_table.setAlternatingRowColors(True)
        
        # Set the table style for a cleaner look with alternate row colors.
        data_table.setStyleSheet("QTableWidget { background-color: white; alternate-background-color: #f0f0f0; }")
        
        # Populate the table rows with data.
        for row_idx in range(len(df)):
            # Create an index item for each row that displays the row number starting from 1.
            index_item = QTableWidgetItem(str(row_idx + 1))
            index_item.setTextAlignment(Qt.AlignCenter)  # Center align the index text
            data_table.setItem(row_idx, 0, index_item)  # Set the index item in the first column
            
            # Fill the rest of the columns with data from the DataFrame.
            for col_idx, col_name in enumerate(columns):
                # Create a table item for each data cell
                item = QTableWidgetItem(str(df[col_name].iloc[row_idx]))
                item.setTextAlignment(Qt.AlignCenter)  # Center align the text
                data_table.setItem(row_idx, col_idx + 1, item)  # Set the item in the corresponding column (+1 to account for the index column)
        
        # Store the created table in the instance's list to keep track of all created tables.
        self.tables.append(data_table)
        
        # Return the populated data table.
        return data_table
    

    def updateComboBoxes(self, new_columns):
        # Iterate over each combo box (dropdown list) used for longitude, latitude, and result columns.
        for combo in [self.LonColCombo, self.LatColCombo, self.ResultColCombo]:
            # Temporarily disable emitting signals when changes occur in the combo box to prevent any unwanted actions.
            combo.blockSignals(True)

            # Ensure the first item in the dropdown is blank for a clear selection.
            # This checks if the combo box is empty or if the first item is not already blank.
            if combo.count() == 0 or combo.itemText(0) != "":
                combo.insertItem(0, "")

            # Loop through each new column name passed to this function.
            for col in new_columns:
                # Check if the column name is not already in the combo box to avoid duplicates.
                if col not in [combo.itemText(i) for i in range(combo.count())]:
                    # Add the column name to the combo box.
                    combo.addItem(col)

            # Reset the current selection of the combo box to the blank item, ensuring no column is selected by default.
            combo.setCurrentIndex(0)

            # Re-enable signals after updating the combo box, allowing changes to trigger actions again.
            combo.blockSignals(False)
            
#######################UI Updates and Event Handling####################

    def showSelectionWindow(self):
        # Create a new window widget for displaying selected data
        self.selectionWindow = QWidget()
        self.selectionWindow.setWindowTitle('Selected Data')  # Set the window's title
        layout = QVBoxLayout()  # Create a vertical layout to arrange widgets vertically
        self.selectionWindow.setLayout(layout)  # Set this layout as the main layout of the window

        # Define columns that are currently selected in the dropdown menus
        selected_columns = [
            ('loncol', self.LonColCombo.currentText()),  # Longitude column
            ('latcol', self.LatColCombo.currentText()),  # Latitude column
            ('resultcol', self.ResultColCombo.currentText())  # Results column
        ]
        
        relevant_files = []  # List to store descriptions of files that contain the selected columns
        aggregated_data = {label: [] for _, label in selected_columns}  # Dictionary to store data from the selected columns

        # Iterate over each DataFrame loaded from files
        for idx, df in enumerate(self.dataFrames):
            if any(col in df.columns for _, col in selected_columns):  # Check if any selected column is present in the DataFrame
                relevant_files.append(f"File {idx + 1}: {self.fileInfo[idx]}")  # Add file info to the list
                # Gather data from the DataFrame for selected columns
                for _, col_name in selected_columns:
                    if col_name in df.columns:
                        aggregated_data[col_name].extend(df[col_name].tolist())
        
        # Display information about files containing selected columns
        if relevant_files:
            fileInfoLabel = QLabel("\n".join(relevant_files))  # Join file info into a single string with new lines
        else:
            fileInfoLabel = QLabel("No data matching the selected columns in any file.")  # No relevant files found
        layout.addWidget(fileInfoLabel)  # Add this label to the layout

        # Create a table to display the data from selected columns
        table = QTableWidget()
        layout.addWidget(table)  # Add the table to the layout

        # Set headers and the number of rows and columns for the table
        headers = [label for _, label in selected_columns]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        max_rows = max(len(data) for data in aggregated_data.values())  # Determine the maximum number of rows needed
        table.setRowCount(max_rows)

        # Fill the table with data
        for col_index, (_, col_name) in enumerate(selected_columns):
            for row_index, value in enumerate(aggregated_data[col_name]):
                table.setItem(row_index, col_index, QTableWidgetItem(str(value)))  # Set each cell in the table
        
        # Add a button to confirm the selection
        confirmButton = QPushButton("Confirm")
        layout.addWidget(confirmButton)
        confirmButton.clicked.connect(self.confirmSelection)  # Connect the button's click event to a method

        self.selectionWindow.resize(500, 300)  # Set the window size
        self.selectionWindow.show()  # Display the window
        

    def highlightColumn(self, column_name, combobox_key):
        # Check if a column name is given
        if not column_name:
            # If no column name is given and it was previously highlighted, remove the highlight
            if combobox_key in self.active_highlights:
                del self.active_highlights[combobox_key]
        else:
            # If a column name is given, fetch the corresponding color and store in the highlights
            current_color = self.color_map[combobox_key]
            self.active_highlights[combobox_key] = (column_name, current_color)

        # Update the highlights across the application
        self.updateHighlights()

    def clearHighlights(self, combobox_key):
        # Check if a particular combobox key has any active highlights
        if combobox_key in self.active_highlights:
            # Remove the highlight from this key
            del self.active_highlights[combobox_key]
            # Update all highlights to reflect this change
            self.updateHighlights()

    def setHighlights(self, column_name, color):
        # This function would set new highlights, but it's not complete. Instead, it updates existing highlights.
        # To fully implement, you would set the new highlight and then update.
        self.updateHighlights(column_name, color=color)

    def updateHighlights(self):
        # Define default colors for non-highlighted items
        default_color = "white"
        alternate_color = "#f0f0f0"

        # First, clear all highlights to reset the visual state
        self.clearAllHighlights(default_color, alternate_color)
        
        # Apply new highlights based on the current state of 'active_highlights'
        for key, (column_name, color) in self.active_highlights.items():
            # Highlight in the tree structure view
            self.applyHighlightToTree(self.rootNode, column_name, color, False)
            # Highlight in all tables displaying data
            for table_widget in self.tables:
                self.applyHighlightToTable(table_widget, column_name, color, False, alternate_color)
                
##################Clearing and Resetting#############
                
    #def clearFiles(self):
        #try:
            # Clear the file DataFrame
            #self.file_df = pd.DataFrame(columns=['File Number', 'File Name'])  # Recreate the DataFrame to ensure it's empty
            # Reset the file counter
            #self.file_counter = 0
        
            #self.model.clear()
            #self.model.setHorizontalHeaderLabels(['File Details'])
        
            # Block signals during the cleanup to avoid any event processing on removed widgets
            #self.file_show_layout.blockSignals(True)

            # Ensure the layout is completely cleared
            #while self.file_show_layout.count():
                #item = self.file_show_layout.takeAt(0)
                #widget = item.widget()
                #if widget is not None:
                   # widget.deleteLater()
                
            # Unblock signals after cleanup
            #self.file_show_layout.blockSignals(False)
        
            # Clear ComboBoxes
            #self.LonColCombo.clear()
            #self.LatColCombo.clear()
           # self.ResultColCombo.clear()   
            #self.columns_added_to_combos.clear()  # Also clear this list
            #self.tables.clear()
        
        #except Exception as e:
            #print(f"An error occurred: {e}")
            
###########################Selection Confirmation and Data Emission##################

    def confirmSelection(self):
        print("Confirmation button clicked")
        selected_columns = [
            ('Longitude', self.LonColCombo.currentText()),
            ('Latitude', self.LatColCombo.currentText()),
            ('Results', self.ResultColCombo.currentText())
        ]

        relevant_files = []
        aggregated_data = {label: [] for _, label in selected_columns}

        # Iterate over each DataFrame loaded from files
        for idx, df in enumerate(self.dataFrames):
            if any(col in df.columns for _, col in selected_columns):
                relevant_files.append(f"File {idx + 1}: {self.fileInfo[idx]}")
                # Gather data from the DataFrame for selected columns
                for _, col_name in selected_columns:
                    if col_name in df.columns:
                        aggregated_data[col_name].extend(df[col_name].tolist())

        # Find the shortest list length to standardize the length of all columns
        min_length = min(len(lst) for lst in aggregated_data.values())

        # Trim all lists in aggregated_data to the shortest length
        for key in aggregated_data:
            aggregated_data[key] = aggregated_data[key][:min_length]

        # Create a DataFrame from the standardized aggregated data
        try:
            aggregated_df = pd.DataFrame(aggregated_data)
            print("DataFrame displayed in 'Selected Data':")
            print(aggregated_df)
            self.dataSelected.emit(aggregated_df)
        except Exception as e:
            print("Error while creating DataFrame:", e)

################Utility Functions##################

    def getCurrentSelectionData(self):
        """
        Retrieves the current selections from the user interface and compiles them into a dictionary.
        This dictionary can be used elsewhere in the application to reference the selected column names for 
        longitude, latitude, and results based on the user's choices from dropdown menus.

        Returns:
            dict: A dictionary containing the currently selected column names for longitude, latitude, and results.
        """

        # Fetch the currently selected text from the longitude column combobox
        lon_column = self.LonColCombo.currentText()

        # Fetch the currently selected text from the latitude column combobox
        lat_column = self.LatColCombo.currentText()

        # Fetch the currently selected text from the result column combobox
        result_column = self.ResultColCombo.currentText()

        # Compile the fetched selections into a dictionary and return it
        # The keys in the dictionary ('loncol', 'latcol', 'resultcol') correspond to longitude, latitude, and results
        return {
            'loncol': lon_column, 
            'latcol': lat_column, 
            'resultcol': result_column
        }
    
#######################UI Highlight Helpers##################

    def applyHighlightToTree(self, parent_item, column_name, color, clear):
        """
        Apply a specified color highlight to tree view items that match the column name.

        Args:
            parent_item (QStandardItem): The root item or parent under which to search for children.
            column_name (str): The name of the column to match for highlighting.
            color (QColor): The color to apply as the highlight.
            clear (bool): If True, remove highlights; if False, apply highlights.
        """
        # Define default and alternate colors for rows to manage alternate row coloring
        default_color = "white"
        alternate_color = "#f0f0f0"
        
        for row in range(parent_item.rowCount()):
            item = parent_item.child(row)
            # Remove any extra whitespace and split to ensure we're comparing the correct column names
            current_item_text = item.text().split('. ', 1)[-1].strip()
            # Debugging output to check the process
            print(f"Checking item: '{current_item_text}' against column: '{column_name}'")
            
            # If the item's text matches the column name and we are not clearing highlights, apply the color
            if current_item_text == column_name and not clear:
                print(f"Highlighting '{current_item_text}' with color {color}")
                item.setBackground(QtGui.QBrush(QtGui.QColor(color)))
            # Recursively apply this method to all children of the current item
            if item.hasChildren():
                self.applyHighlightToTree(item, column_name, color, clear)
            
    def applyHighlightToTable(self, table_widget, column_name, color, clear, alternate_color):
        """
        Apply or clear highlights in a table widget based on the column name.

        Args:
            table_widget (QTableWidget): The table in which to apply or clear highlights.
            column_name (str): The name of the column to be highlighted.
            color (QColor): The color used for highlighting.
            clear (bool): If True, remove highlights; if False, apply highlights.
            alternate_color (QColor): The alternate row color for better readability.
        """
        # Retrieve column headers to match with the column name
        columns = [table_widget.horizontalHeaderItem(i).text() for i in range(table_widget.columnCount())]
        for col_index, header in enumerate(columns):
            if header == column_name:
                for row in range(table_widget.rowCount()):
                    item = table_widget.item(row, col_index)
                    if item:
                        # Apply color based on whether we're clearing the highlight and manage alternate row colors
                        bg_color = alternate_color if row % 2 == 1 else "white"
                        item.setBackground(QtGui.QBrush(QtGui.QColor(color if not clear else bg_color)))

    def clearAllHighlights(self, default_color, alternate_color):
        """
        Clear all highlights from both the tree view and table widgets.

        Args:
            default_color (QColor): The default color for non-alternate rows.
            alternate_color (QColor): The color for alternate rows.
        """
        # Clear highlights from the tree view
        self.clearTreeView(self.rootNode, default_color, alternate_color)
        # Clear highlights from all registered table widgets
        for table_widget in self.tables:
            self.clearTableView(table_widget, default_color, alternate_color)
            
    def clearTreeView(self, parent_item, default_color, alternate_color):
        """
        Clear highlights from a tree view, resetting to default or alternate colors based on row index.

        Args:
            parent_item (QStandardItem): The parent item from which to start clearing.
            default_color (QColor): The default row color.
            alternate_color (QColor): The color for alternate rows.
        """
        for row in range(parent_item.rowCount()):
            item = parent_item.child(row)
            bg_color = alternate_color if row % 2 == 1 else default_color
            item.setBackground(QtGui.QBrush(QtGui.QColor(bg_color)))
            if item.hasChildren():
                self.clearTreeView(item, default_color, alternate_color)
        
    def clearTableView(self, table_widget, default_color, alternate_color):
        """
        Clear highlights from a table view by resetting background colors based on row index.

        Args:
            table_widget (QTableWidget): The table widget from which to clear highlights.
            default_color (QColor): The default color for table rows.
            alternate_color (QColor): The color for alternate rows.
        """
        for row in range(table_widget.rowCount()):
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                if item:
                    # Reset the background color based on the row index
                    bg_color = alternate_color if row % 2 == 1 else default_color
                    item.setBackground(QtGui.QBrush(QtGui.QColor(bg_color)))
                    
                    
                    
def apply_white_theme(app):
    """
    Applies a white theme to the given application with specific styles and color palettes.

    Args:
        app (QApplication): The application to which the theme will be applied.
    """
    # Set the application style to 'Fusion', a modern style provided by Qt
    app.setStyle('Fusion')

    # Create a new color palette for the application to define colors for various elements
    palette = QtGui.QPalette()

    # Set different parts of the interface with specific colors
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255))  # White background for main window areas
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0))  # Black text for a readable contrast on the white background
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))  # White background for items like LineEdit
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(245, 245, 245))  # Slightly off-white for alternating row colors
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(255, 255, 255))  # White background for button faces
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(0, 0, 0))  # Black text on buttons for readability
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(173, 216, 230))  # Light blue for highlighted items like selections
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 0, 0))  # Black text for highlighted text for contrast

    # Set the created palette to the application
    app.setPalette(palette)

    # Customize the appearance of specific widgets using CSS-like styles
    app.setStyleSheet("""
        QPushButton {
            background-color: white;  # Button background color
            border: 2px solid #add8e6;  # Light blue border for buttons
            border-radius: 5px;  # Rounded corners for buttons
            padding: 5px;  # Padding inside the buttons
        }
        QPushButton:hover {
            border: 2px solid #a0c0d0;  # A darker blue border when the mouse hovers over the button
        }
        QPushButton:pressed {
            background-color: #f0f0f0;  # A light grey background when the button is pressed
        }
        QComboBox {
            border: 2px solid #add8e6;  # Light blue border for combo boxes
            border-radius: 3px;  # Rounded corners for combo boxes
            padding: 2px 5px;  # Padding inside the combo boxes
        }
        QLabel {
            color: black;  # Black text color for labels
            background-color: #f0f0f0;  # A light grey background for labels, providing contrast
        }
        QGroupBox {
            background-color: #f0f0f0;  # A light grey background for group boxes
            border: 2px solid #e7e7e7;  # Light grey border for group boxes
            border-radius: 5px;  # Rounded corners for group boxes
            margin-top: 20px;  # Space above the group box title
        }
        QGroupBox:title {
            subcontrol-origin: margin;  # Positioning the title within the margin area
            subcontrol-position: top center;  # Center the title at the top of the group box
            padding: 0 10px;  # Padding around the title
            background-color: #f0f0f0;  # Background color for the title area
        }
        QTreeView, QTableWidget {
            alternate-background-color: #f0f0f0;  # Set alternating row colors in tree and table views
            background-color: white;  # Background color for tree and table views
        }
        QTreeView::item:selected, QTableWidget::item:selected {
            background-color: #ADD8E6;  # Background color for selected items
            color: black;  # Text color for selected items
        }
    """)

# This section is the entry point of the application where the theme function is called
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Create a new application instance
    apply_white_theme(app)  # Apply the white theme to the application
    mainWindow = QtSelectFiles()  # Create the main window
    mainWindow.show()  # Show the main window
    sys.exit(app.exec_())  # Start the application's event loop
