import sys
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from scipy.spatial import ConvexHull
import matplotlib.path as MplPath
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox,QPushButton
from PyQt5.QtCore import Qt
import skgstat as skg
from PyQt5 import QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QScrollArea
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QSpacerItem
from PyQt5.QtWidgets import QSizePolicy
from PyQt5.QtWidgets import QAbstractItemView
from PyQt5.QtWidgets import QListWidget

# - Core Libraries: Filesystem, numerical computing, data handling, collections.
import os
import numpy as np
import pandas as pd
from pathlib import Path
from collections import Counter

# - Visualization Libraries: Plotting and data visualization.
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.ticker as mticker

# - Geospatial Libraries: Geospatial data handling and analysis.
import geopandas as gpd
import contextily as ctx
from shapely.geometry import Point
from pyproj import Transformer
from scipy.spatial import ConvexHull, distance_matrix

# - Scientific Computing & Data Analysis: Mathematical optimization, interpolation, filters, spatial analysis.
from matplotlib.path import Path as MplPath
from scipy.optimize import minimize, curve_fit
from scipy.interpolate import griddata, interp1d
from scipy.ndimage import gaussian_filter, uniform_filter, median_filter
from scipy.signal import savgol_filter
from scipy.special import kv, gamma
from sklearn.neighbors import BallTree
from sklearn.model_selection import train_test_split

# - Geostatistical Analysis: Geostatistical analysis tools.
import skgstat as skg
from skgstat import Variogram
from pykrige.ok import OrdinaryKriging

# - Interactive Visualization & Widgets: Interactive notebook visualization.
from IPython.display import display, HTML
import ipywidgets as widgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import seaborn as sns
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import  QHeaderView
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QLabel, QComboBox, QPushButton, QFileDialog
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QFont, QBrush
from PyQt5.QtWidgets import QProgressDialog


class QtSelectFiles(QMainWindow):
    # Define a signal that carries data as a dictionary
    dataSelected = pyqtSignal(pd.DataFrame)  # Change to emit DataFrame directly
    def __init__(self, parent=None):
        super(QtSelectFiles, self).__init__(parent)
        super().__init__()
        uic.loadUi("D:/queet.ui", self)
        self.setWindowTitle("Select Files")  # Set the window title here
        self.file_df = pd.DataFrame(columns=['File Number', 'File Name'])
        self.file_counter = 0
        self.columns_added_to_combos = []
        self.tables = []
        self.last_selections = {'loncol': None, 'latcol': None, 'resultcol': None}
        self.color_map = {
            'loncol': "#ADD8E6",  # Light Blue
            'latcol': "#90EE90",  # Soft Green
            'resultcol': "#F08080"  # Light Coral
        }
        self.active_highlights = {}  # Tracks active highlights for each combobox
        self.current_df = None
        self.dataFrames = []  # Store all loaded DataFrames
        self.fileInfo = []    # Store file names and row counts


        self.SelectFile = self.findChild(QPushButton, 'selectfile')
        self.ClearFilesButton = self.findChild(QPushButton, 'clearfile')
        self.FileScrollArea = self.findChild(QScrollArea, 'filescrollarea')
        self.FileShowScrollArea=self.findChild(QScrollArea, 'fileshowscrollarea')
        #self.treeView =self.findChild(QTreeView, 'treeviewno')
        


        self.LonColCombo = self.findChild(QComboBox, 'loncolcombo')
        self.LatColCombo = self.findChild(QComboBox, 'latcolcombo')
        self.ResultColCombo = self.findChild(QComboBox, 'resultcolcombo')
        
        #self.LonColCombo.currentTextChanged.connect(lambda: self.highlightColumn(self.LonColCombo.currentText(), "yellow", 'loncol'))
        #self.LatColCombo.currentTextChanged.connect(lambda: self.highlightColumn(self.LatColCombo.currentText(), "green", 'latcol'))
       # self.ResultColCombo.currentTextChanged.connect(lambda: self.highlightColumn(self.ResultColCombo.currentText(), "blue", 'resultcol'))

        # Tree View and Model for File Information
        self.treeView = QTreeView()
        self.model = QStandardItemModel()
        self.treeView.setModel(self.model)
        self.treeView.setAlternatingRowColors(True)  # This should be set after setting the model
        self.treeView.setStyleSheet("QTreeView { background-color: white; alternate-background-color: #f0f0f0; }")
        self.model.setHorizontalHeaderLabels(['File Details'])
        self.rootNode = self.model.invisibleRootItem()  # The invisible root node

        # Set the model view widget to the scroll area
        self.FileScrollArea.setWidget(self.treeView)

   
            
        # Initialize the layout for file content display in the FileShowScrollArea
        self.file_show_layout = QVBoxLayout()
        self.file_show_widget = QWidget()
        self.file_show_widget.setLayout(self.file_show_layout)
        self.FileShowScrollArea.setWidget(self.file_show_widget)

        self.SelectFile.clicked.connect(self.loadFiles)
     
        self.LonColCombo.currentTextChanged.connect(lambda text: self.highlightColumn(text, 'loncol'))
        self.LatColCombo.currentTextChanged.connect(lambda text: self.highlightColumn(text, 'latcol'))
        self.ResultColCombo.currentTextChanged.connect(lambda text: self.highlightColumn(text, 'resultcol'))
        
        self.confirmSelectionButton = self.findChild(QPushButton, 'confirmselection')
        self.confirmSelectionButton.clicked.connect(self.showSelectionWindow)
        
    def loadFiles(self):
        file_paths, _ = QFileDialog.getOpenFileNames(self, "Select .xlsx,.csv,.xls Files", "", "All Files (*);;Excel Files (*.xlsx *.xls);;CSV Files (*.csv)")
        if file_paths:
            progress = QProgressDialog("Loading files...", "Cancel", 0, len(file_paths), self)
            progress.setWindowTitle("Loading Data")
            progress.setWindowModality(Qt.WindowModal)
            progress.show()
            
            new_columns_set = set()  # Create a set to keep track of unique new columns
            for index, file_path in enumerate(file_paths):
                if progress.wasCanceled():
                    break
                progress.setValue(index)
                progress.setLabelText(f"Loading: {file_path.split('/')[-1]}")
                
                self.file_counter += 1
                file_name = file_path.split('/')[-1]
                self.file_df = pd.concat([self.file_df, pd.DataFrame({'File Number': [self.file_counter], 'File Name': [file_name]})], ignore_index=True)

                df = pd.read_excel(file_path) if file_path.lower().endswith(('.xlsx', '.xls')) else pd.read_csv(file_path)
                row_count = len(df)
                columns = df.columns.tolist()
                new_columns_set.update(df.columns)  # Update the set with new columns from this file
                
                #self.updateComboBoxes(columns)
                self.dataFrames.append(df)
                self.fileInfo.append(f"{file_name} - Rows:  {row_count}")
                
                # Create a bold font for the tree item
                bold_font = QFont()
                bold_font.setBold(True)
                
                # Creating the parent item with bold text
                parent_text = f"File {self.file_counter}: {file_name} - {row_count} Rows"
                parent_item = QStandardItem(parent_text)
                parent_item.setFont(bold_font)
                self.rootNode.appendRow(parent_item)
            


                for idx, col in enumerate(columns):
                    # Use the original column name for both the tree view and the combo boxes
                    child_item = QStandardItem(f"{idx + 1}. {col}")
                    parent_item.appendRow(child_item)

                for col in columns:
                    normalized_col = col  # Assuming normalization if needed has been handled during file read
                    if normalized_col not in self.columns_added_to_combos:
                        self.columns_added_to_combos.append(normalized_col)
                        for combo in [self.LonColCombo, self.LatColCombo, self.ResultColCombo]:
                            combo.addItem(normalized_col)

                self.treeView.expandAll()

                file_display_widget = QWidget()
                file_display_layout = QVBoxLayout(file_display_widget)
                file_display_label = QLabel(f"<b>File {self.file_counter}: {file_name} - {row_count} Rows</b>")
                file_display_label.setTextFormat(Qt.RichText)  # Set the text format to rich text to interpret HTML
                file_display_layout.addWidget(file_display_label)


                data_table = self.createDataTable(df, columns)
                data_table.setAlternatingRowColors(True)
                data_table.setStyleSheet("QTableWidget { background-color: white; alternate-background-color: #f0f0f0; }")
                file_display_layout.addWidget(data_table)
                self.file_show_layout.addWidget(file_display_widget)
                
                # Store the loaded DataFrame in an instance variable for later use
                self.current_df = df
             
            progress.setValue(len(file_paths))
            # Update comboboxes only once with all new unique columns combined from all files
            new_columns_list = list(new_columns_set - set(self.columns_added_to_combos))
            self.columns_added_to_combos.extend(new_columns_list)  # Update the main list
            self.updateComboBoxes(list(new_columns_set))  # Update comboboxes with new unique columns            
                
    def updateComboBoxes(self, new_columns):
        for combo in [self.LonColCombo, self.LatColCombo, self.ResultColCombo]:
            combo.blockSignals(True)  # Block signals to prevent automatic selection triggering
            if combo.count() == 0 or combo.itemText(0) != "":
                combo.insertItem(0, "")  # Ensure the first item is blank
            for col in new_columns:
                    if col not in [combo.itemText(i) for i in range(combo.count())]:
                        combo.addItem(col)
            # Set the current index to the blank item after updating
            combo.setCurrentIndex(0)
            combo.blockSignals(False)   
            
    #def addItemsToComboBox(self, combo, items):
        #combo.blockSignals(True)  # Block signals to prevent automatic selection triggering
       # combo.clear()
       # combo.addItem("")  # Add a blank item that won't trigger highlighting
      #  combo.addItems(items)
      #  combo.blockSignals(False)    
                
    def createDataTable(self, df, columns):
        # Adjusting column count for the index column
        data_table = QTableWidget(len(df), len(columns) + 1)  # +1 for the index column
        
        # Creating header labels including the index column
        headers = ['Index'] + columns
       # data_table = QTableWidget(len(df), len(columns))
        data_table.setHorizontalHeaderLabels(headers)
        data_table.verticalHeader().setVisible(False)
        data_table.setDragDropMode(QTableWidget.InternalMove)
        data_table.setSelectionBehavior(QTableWidget.SelectRows)
        data_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        data_table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        data_table.setFixedHeight(400)
        data_table.setFixedWidth(800)
        
        # Enabling column reordering by the user
        data_table.horizontalHeader().setSectionsMovable(True)
        data_table.horizontalHeader().setDragDropMode(QAbstractItemView.InternalMove)
        data_table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        data_table.setAlternatingRowColors(True)
        data_table.setStyleSheet("QTableWidget { background-color: white; alternate-background-color: #f0f0f0; }")
        
        # Reversing the columns to initially display them in reverse order, including the new index column
        #reversed_indices = list(range(1, len(columns) + 1))[::-1]  # Reverse the index list starting from 1 to skip index column
        #reversed_indices = [0] + reversed_indices  # Add index column at the start
        
      
        for row_idx in range(len(df)):
            # Set the index for each row, starting at 1
            index_item = QTableWidgetItem(str(row_idx + 1))
            index_item.setTextAlignment(Qt.AlignCenter)
            data_table.setItem(row_idx, 0, index_item)
            
            for col_idx, col_name in enumerate(columns):
                #reversed_idx = reversed_indices[col_idx + 1]  # +1 because index 0 is the row index column
                item = QTableWidgetItem(str(df[col_name].iloc[row_idx]))
                item.setTextAlignment(Qt.AlignCenter)
                data_table.setItem(row_idx, col_idx + 1, item)  # +1 to offset for the index column
            
        
        # Set headers considering the reversed order
        #reversed_headers = [headers[idx] for idx in reversed_indices]
        #data_table.setHorizontalHeaderLabels(reversed_headers)
        self.tables.append(data_table)
        return data_table

                

                    
    def clearFiles(self):
        try:
            # Clear the file DataFrame
            self.file_df = pd.DataFrame(columns=['File Number', 'File Name'])  # Recreate the DataFrame to ensure it's empty
            # Reset the file counter
            self.file_counter = 0
        
            self.model.clear()
            self.model.setHorizontalHeaderLabels(['File Details'])
        
            # Block signals during the cleanup to avoid any event processing on removed widgets
            self.file_show_layout.blockSignals(True)

            # Ensure the layout is completely cleared
            while self.file_show_layout.count():
                item = self.file_show_layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                
            # Unblock signals after cleanup
            self.file_show_layout.blockSignals(False)
        
            # Clear ComboBoxes
            self.LonColCombo.clear()
            self.LatColCombo.clear()
            self.ResultColCombo.clear()   
            self.columns_added_to_combos.clear()  # Also clear this list
            self.tables.clear()
        
        except Exception as e:
            print(f"An error occurred: {e}")
        

        
    def highlightColumn(self, column_name, combobox_key):
        if not column_name:
            if combobox_key in self.active_highlights:
                del self.active_highlights[combobox_key]
        else:
            current_color = self.color_map[combobox_key]
            self.active_highlights[combobox_key] = (column_name, current_color)

        self.updateHighlights()


    def clearHighlights(self, combobox_key):
        if combobox_key in self.active_highlights:
            del self.active_highlights[combobox_key]
            self.updateHighlights()

    def setHighlights(self, column_name, color):
        self.updateHighlights(column_name, color=color)

    def updateHighlights(self):
        # Define the default and alternate colors
        default_color = "white"
        alternate_color = "#f0f0f0"
        # Clear all current highlights first, then reapply based on active highlights
        self.clearAllHighlights(default_color, alternate_color)
        
        # Reapply all active highlights from the dictionary
        for key, (column_name, color) in self.active_highlights.items():
            self.applyHighlightToTree(self.rootNode, column_name, color, False)
            for table_widget in self.tables:
                self.applyHighlightToTable(table_widget, column_name, color, False, alternate_color)
 
    def clearAllHighlights(self, default_color, alternate_color):
        # Clear highlights in TreeView
        self.clearTreeView(self.rootNode, default_color, alternate_color)
        # Clear highlights in all TableViews
        for table_widget in self.tables:
            self.clearTableView(table_widget, default_color, alternate_color)
    
    def clearTreeView(self, parent_item, default_color, alternate_color):
        for row in range(parent_item.rowCount()):
            item = parent_item.child(row)
            bg_color = alternate_color if row % 2 == 1 else default_color
            item.setBackground(QtGui.QBrush(QtGui.QColor(bg_color)))
            if item.hasChildren():
                self.clearTreeView(item, default_color, alternate_color)
        
    def clearTableView(self, table_widget, default_color, alternate_color):
        for row in range(table_widget.rowCount()):
            for col in range(table_widget.columnCount()):
                item = table_widget.item(row, col)
                if item:
                    bg_color = alternate_color if row % 2 == 1 else default_color
                    item.setBackground(QtGui.QBrush(QtGui.QColor(bg_color))) 
                    
    def applyHighlightToTree(self, parent_item, column_name, color,clear):
        # Define the default and alternate colors for rows
        default_color = "white"
        alternate_color = "#f0f0f0"
        
        for row in range(parent_item.rowCount()):
            item = parent_item.child(row)
            # Ensure that we're stripping any unexpected whitespace from the text
            current_item_text = item.text().split('. ', 1)[-1].strip()
            print(f"Checking item: '{current_item_text}' against column: '{column_name}'")
            
            if current_item_text == column_name and not clear:
                print(f"Highlighting '{current_item_text}' with color {color}")  # Debug output
                item.setBackground(QtGui.QBrush(QtGui.QColor(color)))
            if item.hasChildren():
                self.applyHighlightToTree(item, column_name, color, clear)
            

    def applyHighlightToTable(self, table_widget, column_name, color, clear, alternate_color):
        columns = [table_widget.horizontalHeaderItem(i).text() for i in range(table_widget.columnCount())]
        for col_index, header in enumerate(columns):
            if header == column_name:
                for row in range(table_widget.rowCount()):
                    item = table_widget.item(row, col_index)
                    if item:
                        # Apply alternate row colors based on the row index
                        bg_color = alternate_color if row % 2 == 1 else "white"
                        item.setBackground(QtGui.QBrush(QtGui.QColor(color if not clear else bg_color)))
                        

    def showSelectionWindow(self):
        self.selectionWindow = QWidget()
        self.selectionWindow.setWindowTitle('Selected Data')
        layout = QVBoxLayout()
        self.selectionWindow.setLayout(layout)

        # Displaying loaded files information
        #fileInfoLabel = QLabel("\n".join(self.fileInfo))
        #layout.addWidget(fileInfoLabel)

        #table = QTableWidget()
        #layout.addWidget(table)
        
        selected_columns = [
            ('loncol', self.LonColCombo.currentText()),
            ('latcol', self.LatColCombo.currentText()),
            ('resultcol', self.ResultColCombo.currentText())
        ]
       
        relevant_files = []
        aggregated_data = {label: [] for _, label in selected_columns}
        file_labels = []
        for idx, df in enumerate(self.dataFrames):
                if any(col in df.columns for _, col in selected_columns):
                    relevant_files.append(f"File {idx + 1}: {self.fileInfo[idx]}")
                    file_labels.append(f"File {idx + 1}")
                    
                    # Aggregate data for matching columns
                    for _, col_name in selected_columns:
                        if col_name in df.columns:
                            aggregated_data[col_name].extend(df[col_name].tolist())
      
        # Displaying relevant files information
        if relevant_files:
            fileInfoLabel = QLabel("\n".join(relevant_files))
        else:
            fileInfoLabel = QLabel("No data matching the selected columns in any file.")
        layout.addWidget(fileInfoLabel)
        
        # Prepare the data table
        table = QTableWidget()
        layout.addWidget(table)
        
        # Set up table headers and row count
        headers = [label for _, label in selected_columns]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        
        # Calculate the max rows needed for the table
        max_rows = max(len(data) for data in aggregated_data.values())
        table.setRowCount(max_rows)

       
        for col_index, (_, col_name) in enumerate(selected_columns):
            for row_index, value in enumerate(aggregated_data[col_name]):
                table.setItem(row_index, col_index, QTableWidgetItem(str(value)))
        
        # Create and add the Confirm button
        confirmButton = QPushButton("Confirm")
        layout.addWidget(confirmButton)
        confirmButton.clicked.connect(self.confirmSelection)

        self.selectionWindow.resize(500, 300)  # Adjust size as needed
        self.selectionWindow.show()
    
    def confirmSelection(self):
       # Handle the confirmation action, such as emitting the selected data
       print("Confirmation button clicked")
       # Initialize a list to collect DataFrames
       frames = []

       selected_columns = [
           self.LonColCombo.currentText(),
           self.LatColCombo.currentText(),
           self.ResultColCombo.currentText()
       ]
       # Combine data from all loaded DataFrames for the selected columns
       for df in self.dataFrames:
           if all(col in df.columns for col in selected_columns):
               # Select only the required columns and add to the list
               frames.append(df[selected_columns])

       if frames:
           # Concatenate all the DataFrames in the list
           aggregated_df = pd.concat(frames, ignore_index=True)
           self.dataSelected.emit(aggregated_df)  # Emit the aggregated DataFrame
       else:
            # Handle the case where no data matches the selected columns
            print("No matching data found in any loaded files.")
            self.dataSelected.emit(pd.DataFrame())  # Emit an empty DataFrame or handle differently
  
    def getCurrentSelectionData(self):
        # This method should return the currently selected data in a format that can be processed by the receiver
        # Implement the logic to fetch data from your UI elements or internal data structures
        # For simplicity, returning an example dictionary
        return {
            'loncol': self.LonColCombo.currentText(), 
            'latcol': self.LatColCombo.currentText(), 
            'resultcol': self.ResultColCombo.currentText()
        }

    
def apply_white_theme(app):
    # Set the Fusion style
    app.setStyle('Fusion')

    # Create a new palette for a clean, modern look
    palette = QtGui.QPalette()

    # Set the palette colors
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255))  # White background for main window
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0))  # Black text for readability
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))  # White for base widget backgrounds, like QLineEdit
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(245, 245, 245))  # A different shade of white for alternate backgrounds like QGroupBox
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(255, 255, 255))  # White for buttons
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(0, 0, 0))  # Black text on buttons
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(173, 216, 230))  # Light blue for highlights
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 0, 0))  # Black text for highlighted items

    app.setPalette(palette)

    # Applying custom stylesheets for QPushButton, QComboBox, QTreeView, and QTableWidget to add blue outlines and manage alternating row colors
    app.setStyleSheet("""
        QPushButton {
            background-color: white;
            border: 2px solid #add8e6;  # Light blue border
            border-radius: 5px;
            padding: 5px;
        }
        QPushButton:hover {
            border: 2px solid #a0c0d0;  # A darker shade of blue on hover
        }
        QPushButton:pressed {
            background-color: #f0f0f0;  # A light grey background when pressed
        }
        QComboBox {
            border: 2px solid #add8e6;
            border-radius: 3px;
            padding: 2px 5px;
        }
        QLabel {
            color: black;
            background-color: #f0f0f0;  # A different shade of white for contrast
        }
        QGroupBox {
            background-color: #f0f0f0;  # A different shade of white for QGroupBox
            border: 2px solid #e7e7e7;  # Light grey border for group box
            border-radius: 5px;
            margin-top: 20px;  /* leave space at the top for the title */
        }
        QGroupBox:title {
            subcontrol-origin: margin;
            subcontrol-position: top center;  /* position at the top center */
            padding: 0 10px;
            background-color: #f0f0f0;
        }
        QTreeView, QTableWidget {
            alternate-background-color: #f0f0f0;
            background-color: white;
        }
        QTreeView::item:selected, QTableWidget::item:selected {
            background-color: #ADD8E6;  /* highlight color */
            color: black;  /* text color for highlighted items */
        }
    """)

                        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_white_theme(app)
    mainWindow = QtSelectFiles()
    mainWindow.show()
    sys.exit(app.exec_())
