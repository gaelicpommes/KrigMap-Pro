# Standard Library Imports: Basic utilities for operating system interaction, file paths, and data handling.
import os
import sys
from pathlib import Path
from collections import Counter

# Numerical and Data Handling Libraries: Handling and manipulating numerical data and structures.
import numpy as np
import pandas as pd

# Geospatial Data Handling Libraries: Working with geographical and spatial data.
import geopandas as gpd
from shapely.geometry import Point
from pyproj import Transformer
from scipy.spatial import ConvexHull, distance_matrix

# Visualization Libraries: Creating charts, plots, and interactive visualizations.
import matplotlib.pyplot as plt
import seaborn as sns
import contextily as ctx
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.path import Path as MplPath


# User Interface (Qt/PyQt) Libraries: Building graphical user interfaces.
from PyQt5 import QtWidgets, QtGui, uic
from PyQt5.QtWidgets import QApplication, QFileDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal

# Scientific and Mathematical Libraries
from scipy.optimize import minimize, curve_fit
from scipy.interpolate import griddata, interp1d
from scipy.ndimage import gaussian_filter, uniform_filter, median_filter
from scipy.signal import savgol_filter
from scipy.special import kv, gamma

# Machine Learning Libraries: Data modeling and validation.
from sklearn.neighbors import BallTree
from sklearn.model_selection import train_test_split

# Geostatistical Libraries: Variogram modeling and kriging for spatial data.
import skgstat as skg
from skgstat import Variogram
from pykrige.ok import OrdinaryKriging

# Interactive Visualization & Widgets: Enhancing interactivity and display 
from IPython.display import display, HTML
import ipywidgets as widgets

# Custom Module Imports: Ensure the custom module and classes are available.
from krig3 import QtSelectFiles  



class ColumnSelectorDialog(QtWidgets.QDialog):
    """
    A dialog that prompts the user to select three columns from a list of available columns.
    This is typically used when a data file has more than three columns, and the user needs to specify
    which columns should be used for longitude, latitude, and a result measure.
    
    Parameters:
    - columns: A list of column names from which the user can select.
    - parent: The parent widget of this dialog, typically the main window of the application.
    """
    
    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Columns")  # Title of the dialog window
        layout = QtWidgets.QVBoxLayout(self)  # Main layout is vertical
        
        # Labels for the comboboxes to indicate what each combobox is for
        labels = ["Longitude", "Latitude", "Results"]
        
        self.comboBoxes = []  # List to store the comboboxes for later retrieval of their selected values
        
        for i in range(3):
            # Create a horizontal layout for each label-combobox pair
            hLayout = QtWidgets.QHBoxLayout()
            
            # Create label with the specified text aligned to the right and vertically centered
            label = QtWidgets.QLabel(labels[i])
            label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            
            # Create combobox, setting it as a child of this dialog, and populate it with the column names
            combo = QtWidgets.QComboBox(self)
            combo.addItems(columns)  # Adding all column names to the combobox
            
            # Add label and combobox to the horizontal layout
            hLayout.addWidget(label)
            hLayout.addWidget(combo)
            
            # Add the horizontal layout to the main vertical layout
            layout.addLayout(hLayout)
            
            # Keep a reference to the comboboxes to access their selected values later
            self.comboBoxes.append(combo)
        
        # Create a standard button box with OK and Cancel buttons
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        # Connect the button actions to the dialog's accept and reject slots
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        layout.addWidget(self.buttonBox)  # Add the button box to the main layout

    def selected_columns(self):
        """
        Retrieves the currently selected items from the comboboxes.
        
        Returns:
        A list of strings representing the selected column names for longitude, latitude, and results, respectively.
        """
        return [combo.currentText() for combo in self.comboBoxes]
    
    
    
    
class ExcelLoaderApp(QtWidgets.QMainWindow):
    """
    Main application window for the Krige Application which handles loading and processing Excel data,
    and generating geostatistical plots such as variograms and kriging plots.
    """

    def __init__(self):
        super().__init__()
        # Load the user interface from a .ui file designed in Qt Designer
        uic.loadUi("D:/qute.ui", self)
        self.setWindowTitle("Krige Application")  # Set the window title
        self.setupTableWidget(self.excelTableWidget)  # Setup for the main data table
        self.setupTableWidget(self.thresholdTableWidget)  # Setup for the threshold data table
        
        # Initialize variables to store data and parameters
        self.unique_df = None  # DataFrame to store unique data after processing
        self.plot_parameters = []  # List to store parameters for each variogram plot
        self.clean_df = None  # DataFrame to store cleaned data
        self.krigePlotCount = 0  # Counter for the number of kriging plots generated
        self.kriging_parameters = []  # List to store parameters for each kriging plot

        # Find and configure the button for selecting multiple files
        self.pushButtonSelectMultiFiles = self.findChild(QtWidgets.QPushButton, 'openmultifiles')
        #if self.pushButtonSelectMultiFiles:
            #self.pushButtonSelectMultiFiles.clicked.connect(self.openSelectFilesUI)
        #else:
            #print("PushButton 'selectmultifiles' not found")

        # Finding and setting up group boxes and their contents
        self.groupBoxSelectFile = self.findChild(QtWidgets.QGroupBox, 'selectexcelfile')
        if self.groupBoxSelectFile:
            self.pushButtonOpenFile = self.groupBoxSelectFile.findChild(QtWidgets.QPushButton, 'openexcelfile')
            self.scrollAreaExcel = self.groupBoxSelectFile.findChild(QtWidgets.QScrollArea, 'excelscrollarea')

        self.groupBoxThreshold = self.findChild(QtWidgets.QGroupBox, 'enterthresholdvalue')
        if self.groupBoxThreshold:
            self.lineEditThreshold = self.groupBoxThreshold.findChild(QtWidgets.QLineEdit, 'thresholdvalue')
            self.pushButtonConfirmThreshold = self.groupBoxThreshold.findChild(QtWidgets.QPushButton, 'confirmthreshold')
            self.scrollAreaThreshold = self.groupBoxThreshold.findChild(QtWidgets.QScrollArea, 'thresholdscrollarea')

        self.groupBoxSemivariance = self.findChild(QtWidgets.QGroupBox, 'semivariance')
        if self.groupBoxSemivariance:
            self.scrollAreaSemivariance = self.groupBoxSemivariance.findChild(QtWidgets.QScrollArea, 'semivariancescrollarea')

        self.groupBoxVariogramParameters = self.findChild(QtWidgets.QGroupBox, 'variogramparameters')
        if self.groupBoxVariogramParameters:
            self.setupVariogramWidgets()

        # Setup for plotting variograms
        self.pushButtonPlotVariogram = self.findChild(QtWidgets.QPushButton, 'plotvariogram')
        if self.pushButtonPlotVariogram:
            self.pushButtonPlotVariogram.clicked.connect(self.plotVariogram)

        # Connection setup for opening files and applying thresholds
        if self.pushButtonOpenFile:
            self.pushButtonOpenFile.clicked.connect(self.loadAndDisplayExcel)
        if self.pushButtonConfirmThreshold:
            self.pushButtonConfirmThreshold.clicked.connect(self.applyThresholdAndDisplay)

        # Setup for displaying fit parameters in a QLabel
        self.labelFitParameters = self.findChild(QtWidgets.QLabel, 'fitparameterslabel')
        if not self.labelFitParameters:
            self.labelFitParameters = QtWidgets.QLabel("No parameters available.")
            layout = QtWidgets.QVBoxLayout(self.framefitparameters)
            layout.addWidget(self.labelFitParameters)
            self.framefitparameters.setLayout(layout)

        # Dataframe to store loaded data
        self.df = None

        # Checking and handling for plot group boxes
        self.krigePlotsGroupBox = self.findChild(QtWidgets.QGroupBox, 'krigeplotsgroupbox')
        if not self.krigePlotsGroupBox:
            print("Failed to find 'krigeplotsgroupbox'.")
        else:
            self.krigePlots = self.krigePlotsGroupBox.findChild(QtWidgets.QTabWidget, 'krigeplots')
        if not self.krigePlots:
            print("krigeplots tab widget not found inside 'krigeplotsgroupbox'.")

        self.plotsGroupBox = self.findChild(QtWidgets.QGroupBox, 'plotsgroupbox')
        if not self.plotsGroupBox:
            print("Failed to find 'plotsgroupbox'.")
        else:
            self.plotTabWidget = self.plotsGroupBox.findChild(QtWidgets.QTabWidget, 'plotfuck')
        if not self.plotTabWidget:
            print("Failed to find 'plotTabWidget' inside 'plotsgroupbox'.")

        # Initialize UI elements and their connections to functionality
        self.setupTableWidget(self.excelTableWidget)
        self.setupTableWidget(self.thresholdTableWidget)
        self.setupTableWidget(self.semivarianceTableWidget)
        self.setupUI()
        self.setupConnections()
        
        

    def setupUI(self):
        # Search for UI components defined in the Qt Designer file by their object names and initialize them.
        
        # Dropdown menu to select the method for fitting the variogram
        self.fitMethodCombo = self.findChild(QtWidgets.QComboBox, 'fit_methodcombo')
        
        # Line edit fields for entering the nugget, sill, and range values manually
        self.fitNuggetLineEdit = self.findChild(QtWidgets.QLineEdit, 'fit_nuggetlineedit')
        self.fitSillLineEdit = self.findChild(QtWidgets.QLineEdit, 'fit_silllineedit')
        self.fitRangeLineEdit = self.findChild(QtWidgets.QLineEdit, 'fit_rangelineedit')
        
        # Check if all components have been loaded correctly from the UI file. If not, print an error message.
        if not self.fitMethodCombo or not self.fitNuggetLineEdit or not self.fitSillLineEdit or not self.fitRangeLineEdit:
            print("Error: One or more variogram parameter widgets could not be found.")
            return  # Exit the function if any of the components are missing.

        # Disable the nugget, sill, and range inputs by default. They will be enabled when the manual method is selected from fitMethodCombo.
        self.toggleManualFitInputs(False)
        
        # Make the tabs in both the Kriging and Variogram plots sections closable.
        self.krigePlots.setTabsClosable(True)
        self.tabVariogramPlots.setTabsClosable(True)
    
        # Connect the tab close request signals to the closeTab function to handle closing of tabs.
        self.krigePlots.tabCloseRequested.connect(self.closeTab)
        self.tabVariogramPlots.tabCloseRequested.connect(self.closeTab)

        # Find and setup input fields for minimum points, maximum points, levels, and alpha for kriging calculations.
        self.minPointsLineEdit = self.findChild(QtWidgets.QLineEdit, 'min_points')
        self.maxPointsLineEdit = self.findChild(QtWidgets.QLineEdit, 'max_points')
        self.levelsLineEdit = self.findChild(QtWidgets.QLineEdit, 'levels')
        self.alphaLineEdit = self.findChild(QtWidgets.QLineEdit, 'alpha')
        
        # Find and setup checkbox and dropdown for enabling and selecting a basemap.
        self.chkBasemap = self.findChild(QtWidgets.QCheckBox, 'chkbasemap')
        self.basemapCombo = self.findChild(QtWidgets.QComboBox, 'basemapcombo')
        
        # Initially disable the basemap dropdown until the basemap checkbox is checked.
        self.basemapCombo.setEnabled(False)
        
        # Find and setup the checkbox for including uncertainty maps. Connect its state change to a handler.
        self.chkUncertaintymap = self.findChild(QtWidgets.QCheckBox, 'chkuncertaintymap')
        if not self.chkUncertaintymap:
            print("Error: Checkbox 'chkUncertaintymap' not found.")
        else:
            self.chkUncertaintymap.stateChanged.connect(self.handleUncertaintyMapToggle)
        
        # Find and setup the checkbox for including or excluding the kriging plot.
        self.chkKrigemap = self.findChild(QtWidgets.QCheckBox, 'includekrigeplot')



    def setupConnections(self):
        # Connect changes in the currently selected tab in the Kriging plots tab widget to the parameter display update function.
        self.krigePlots.currentChanged.connect(self.updateKrigingParametersDisplay)
       
        # Connect changes in the selected fitting method from the dropdown to a method that adjusts the UI accordingly.
        self.fitMethodCombo.currentTextChanged.connect(self.onFitMethodChanged)

        # Connect changes in the currently selected tab in the Variogram plots tab widget to handle tab changes.
        self.tabVariogramPlots.currentChanged.connect(self.onTabChange)

        # Locate and connect the button for plotting Kriging to its function.
        self.plotKrigingButton = self.findChild(QtWidgets.QPushButton, 'plotkrige')
        if self.plotKrigingButton:
            self.plotKrigingButton.clicked.connect(self.plotKriging)

        # Connect the state change of the Basemap checkbox to toggle the availability of the Basemap combo box.
        self.chkBasemap.stateChanged.connect(self.toggleBasemapCombo)
      
        # Locate and establish connections for buttons associated with plotting various histogram and scatter plots.
        self.pushButtonRawHistogram = self.findChild(QtWidgets.QPushButton, 'rawhistogram')
        if self.pushButtonRawHistogram:
            self.pushButtonRawHistogram.clicked.connect(self.plotRawHistogram)
        else:
            print("Failed to find 'rawhistogram' QPushButton.")

        self.pushButtonScatterPlot = self.findChild(QtWidgets.QPushButton, 'scatterplot')
        if self.pushButtonScatterPlot:
            self.pushButtonScatterPlot.clicked.connect(self.plotScatterPlot)
        else:
            print("Failed to find 'scatterplot' QPushButton.")
            
        # Finding QLineEdit widgets associated with the push buttons
        self.lineEditRawHistogram = self.findChild(QtWidgets.QLineEdit, 'rawhistogramlineedit')
        self.lineEditScatterPlot = self.findChild(QtWidgets.QLineEdit, 'scatterplotlineedit')

        self.pushButtonPairPlot = self.findChild(QtWidgets.QPushButton, 'pairplot')
        if self.pushButtonPairPlot:
            self.pushButtonPairPlot.clicked.connect(self.plotPairPlot)
        else:
            print("Failed to find 'pairplot' QPushButton.")
        
        # Establish connections for saving data from threshold and semivariance analysis.
        self.pushButtonSaveThreshold = self.findChild(QtWidgets.QPushButton, 'savethreshold')
        if self.pushButtonSaveThreshold:
            self.pushButtonSaveThreshold.clicked.connect(self.saveThresholdData)
        else:
            print("PushButton 'savethreshold' not found")

        self.pushButtonSaveSemivariance = self.findChild(QtWidgets.QPushButton, 'savesemivariance')
        if self.pushButtonSaveSemivariance:
            self.pushButtonSaveSemivariance.clicked.connect(self.saveSemivarianceData)
        else:
            print("PushButton 'savesemivariance' not found")
            
        # Connect tab changes in the Variogram plots to update their parameters display
        self.tabVariogramPlots.currentChanged.connect(self.updateVariogramParametersDisplay)
        self.krigePlots.currentChanged.connect(self.updateKrigingParametersDisplay)
        
        self.pushButtonSelectMultiFiles.clicked.connect(self.openSelectFilesUI)
        #self.selectFilesWindow.dataSelected.connect(self.loadDataIntoTable)  # Connect to the dataSelected signal from QtSelectFiles


    def setupTableWidget(self, tableWidget):
        """
        Configures the properties of a QTableWidget to enhance its functionality and appearance.

        Args:
        tableWidget (QTableWidget): The table widget to be configured.
        """

        # Allow columns to be reordered by dragging them to a new position within the table.
        tableWidget.horizontalHeader().setSectionsMovable(True)
        
        # Enable dragging and dropping of the header sections within the table itself.
        tableWidget.horizontalHeader().setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
    
        # Disable automatic sorting to maintain the data order unless specifically sorted by the user.
        tableWidget.setSortingEnabled(False)
    
        # Make the headers clickable, enabling functionality such as sorting or editing the header labels.
        tableWidget.horizontalHeader().setSectionsClickable(True)

        # Connect a function to the signal that is emitted when a header section is double-clicked.
        # This allows the user to edit the header text by double-clicking on it.
        tableWidget.horizontalHeader().sectionDoubleClicked.connect(
            lambda index: self.editHeader(tableWidget, index)
        )

        # Allow all cells and headers to be editable directly in the table through the UI.
        tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
    
        # Set alternating row colors to improve readability, making it easier to differentiate between rows.
        tableWidget.setAlternatingRowColors(True)

        # Apply a style to the table to set the background colors of the alternating rows.
        tableWidget.setStyleSheet("alternate-background-color: #f0f0f0; background-color: #ffffff;")
    
    def initializeFitParametersLabel(self):
        """
        Initializes the label that displays fitting parameters if it hasn't been initialized.
        This ensures there's a label available to display messages about the fitting parameters.
        """
        
        # Check if the label for displaying fit parameters exists, and if not, create it.
        if not self.labelFitParameters:
            # Create a new QLabel to display messages about parameters when no parameters are available.
            self.labelFitParameters = QtWidgets.QLabel("No parameters available.")
            
            # Create a layout to hold the label within its frame.
            layout = QVBoxLayout(self.framefitparameters)
            
            # Add the newly created label to the layout.
            layout.addWidget(self.labelFitParameters)
            
            

    def setupVariogramWidgets(self):
        """
        Initializes and configures widgets in the variogram parameters group box. This method dynamically
        searches for and connects widgets and their corresponding checkboxes based on predefined lists.
        """

        # Lists defining the names of widgets that will be searched in the UI file. Widgets control various
        # aspects of the variogram calculation such as estimation method, variogram model, etc.
        widget_names = ['estimator', 'model', 'bin_func', 'fit_sigma', 'normalize', 'use_nugget', 'fit_method']
        line_edit_names = ['maxlag', 'n_lags']  # Additional parameters that are entered as numerical values

        self.widgets = {}  # Dictionary to store references to the widgets
        self.checkboxes = {}  # Dictionary to store references to the corresponding checkboxes

        # Iterate over both lists to find and setup each widget and its checkbox
        for name in widget_names + line_edit_names:
            if name in widget_names:
                # Attempt to find a combobox for each widget name in widget_names
                widget = self.groupBoxVariogramParameters.findChild(QtWidgets.QComboBox, name.lower() + 'combo')
            else:
                # Attempt to find a line edit for each name in line_edit_names
                widget = self.groupBoxVariogramParameters.findChild(QtWidgets.QLineEdit, name.lower() + 'lineedit')

            # Find the checkbox associated with the widget based on its name
            checkbox = self.groupBoxVariogramParameters.findChild(QtWidgets.QCheckBox, 'chk' + name.lower())

            if widget and checkbox:
                # Store widget in dictionary and setup a connection between the checkbox state and widget's enable state
                self.widgets[name] = widget
                if name == 'fit_sigma':
                    # Special handling for 'fit_sigma' to toggle additional options based on the checkbox state
                    checkbox.stateChanged.connect(lambda state, w=widget: self.toggleFitSigma(state, w))
                else:
                    # General case where the widget's enabled state is directly tied to the checkbox
                    checkbox.stateChanged.connect(lambda state, w=widget: w.setEnabled(state == Qt.Checked))
                print(f"Connected {name} widget to checkbox.")  # Debug output to confirm connection
            else:
                # Output an error message if either the widget or checkbox could not be found
                print(f"Error: Could not find widget or checkbox for {name}")

        # Find the QTabWidget responsible for displaying variogram plots
        self.tabVariogramPlots = self.findChild(QtWidgets.QTabWidget, 'variogramplots')
   
#########################Data Loading and Fle Handling ###########

    def openSelectFilesUI(self):
        """
        Opens a file selection dialog that allows the user to select multiple files.
        Upon selection, it triggers loading of data into a table.
        """
        # Create an instance of a custom file selection dialog.
        self.selectFilesWindow = QtSelectFiles()
        # Connect a signal that is emitted when data is selected to a method that handles the data loading.
        self.selectFilesWindow.dataSelected.connect(self.loadDataIntoTable)
        # Display the file selection window.
        self.selectFilesWindow.show()
        
    def loadDataIntoTable(self, data):
        """
        Loads data into a table widget if the data is in DataFrame format.

        Args:
        data (DataFrame): The data to be loaded into the table widget.
        """
        # Check if the data is a DataFrame, which is suitable for display in a table widget.
        if isinstance(data, pd.DataFrame):
            print("DataFrame loaded with columns:", data.columns.tolist())  # Output the column names for debugging.
            # If there are exactly three columns, assume these are the correct data format.
            if not data.empty and data.shape[1] == 3:
                self.df = data
                self.setupAndDisplayTable(self.df, self.excelTableWidget)
            # If more than three columns, prompt the user to select the correct columns to use.
            elif data.shape[1] > 3:
                print("More than three columns found, opening ColumnSelectorDialog...")
                dialog = ColumnSelectorDialog(data.columns.tolist(), self)
                # Show the column selector dialog and wait for user response.
                if dialog.exec_() == QtWidgets.QDialog.Accepted:
                    selected_columns = dialog.selected_columns()
                    print("Selected columns:", selected_columns)
                    # Check if three columns were selected.
                    if len(selected_columns) == 3:
                        # Subset the DataFrame to the selected columns.
                        self.df = data[selected_columns]
                        # Display the DataFrame in the specified table widget.
                        self.setupAndDisplayTable(self.df, self.excelTableWidget)
                    else:
                        # Display an error if the wrong number of columns were selected.
                        QtWidgets.QMessageBox.warning(self, "Selection Error", "You must select exactly three columns.")
                else:
                    print("Dialog cancelled")
            else:
                # Display an error if the DataFrame does not contain enough columns.
                QtWidgets.QMessageBox.warning(self, "Data Error", "The dataset must have at least three columns.")
                return
            # Update the table display with the DataFrame.
            self.setupAndDisplayTable(self.df, self.excelTableWidget)
        else:
            # Display an error if the data is not a DataFrame.
            QtWidgets.QMessageBox.warning(self, "Data Error", "No valid DataFrame loaded.")

    def handleDataReceived(self, data):
        """
        Handles data received through other components or data signals.

        Args:
        data (any): Data received from external sources.
        """
        print("Data received:", data)
        # This example method updates the Excel display area with the received data.
        self.updateExcelDisplayArea(data)
  
    def loadAndDisplayExcel(self):
        # Open a file dialog to select a file, allowing multiple formats.
        filePath, _ = QFileDialog.getOpenFileName(self, "Select Data File", "", "Excel Files (*.xlsx *.xls);;CSV Files (*.csv);;All Files (*)")
        if filePath:
            try:
                # Determine the file extension and load data accordingly.
                if filePath.lower().endswith(('.xlsx', '.xls')):
                    self.df = pd.read_excel(filePath)
                elif filePath.lower().endswith('.csv'):
                    self.df = pd.read_csv(filePath)
                else:
                    raise ValueError("Unsupported file format")

                print("File loaded successfully:", filePath)

                # If the file has more than three columns, prompt the user to select which columns to use.
                if self.df.shape[1] > 3:
                    dialog = ColumnSelectorDialog(self.df.columns.tolist(), self)
                    if dialog.exec_() == QtWidgets.QDialog.Accepted:
                        selected_columns = dialog.selected_columns()
                        if len(selected_columns) == 3:
                            self.df = self.df[selected_columns]
                            self.setupAndDisplayTable(self.df, self.excelTableWidget)
                        else:
                            QtWidgets.QMessageBox.warning(self, "Selection Error", "You must select exactly three columns.")
                    else:
                        print("Column selection cancelled.")
                        return  # Exit the function if the dialog is cancelled
                else:
                    # If the file has three or fewer columns, display it directly.
                    self.setupAndDisplayTable(self.df, self.excelTableWidget)

            except Exception as e:
                print("Failed to load file:", e)
                QtWidgets.QMessageBox.warning(self, "File Loading Error", "Failed to load the specified file.")

                
    def saveTableToFile(self, tableWidget, defaultName="data"):
        """
        Saves data from a specified table widget to a file chosen by the user.

        Args:
        tableWidget (QTableWidget): The table from which data is to be saved.
        defaultName (str): Default filename for the save dialog.
        """
        # Convert the table widget data to a DataFrame.
        df = self.tableWidgetToDataFrame(tableWidget)
        # Open a save file dialog with specified file type filters.
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "Save File", f"{defaultName}.csv", "All Files (*);;Text Files (*.txt);;CSV Files (*.csv);;Excel Files (*.xlsx)", options=options)
        if fileName:
            # Save the DataFrame to the file depending on the file extension chosen.
            if fileName.endswith('.csv'):
                df.to_csv(fileName, index=False)
            elif fileName.endswith('.xlsx'):
                df.to_excel(fileName, index=False)
            elif fileName.endsWith('.txt'):
                df.to_csv(fileName, index=False, sep='\t')
            # Notify the user that the file has been successfully saved.
            QMessageBox.information(self, "File Saved", "Data successfully saved to:\n" + fileName)

    def saveThresholdData(self):
        """
        Saves the data displayed in the threshold table widget.
        """
        self.saveTableToFile(self.thresholdTableWidget, "threshold_data")

    def saveSemivarianceData(self):
        """
        Saves the data displayed in the semivariance table widget.
        """
        self.saveTableToFile(self.semivarianceTableWidget, "semivariance_data")

#################Data Processing and Management##########

    def prepare_data_for_processing(self, unique_df):
        """
        Converts all column data in the DataFrame to numeric type, coercing errors to NaN,
        and then drops any rows that contain NaN values to ensure data cleanliness.

        Args:
        unique_df (DataFrame): The DataFrame to process.

        Returns:
        DataFrame: The cleaned DataFrame with only numeric data and no missing values.
        """
        # Convert each column to numeric type, coercing errors to NaN.
        for col in unique_df.columns:
            unique_df[col] = pd.to_numeric(unique_df[col], errors='coerce')
        # Drop all rows that now contain NaN values.
        unique_df.dropna(inplace=True)
        return unique_df
    
    def validate_and_prepare_data(self):
        """
        Validates if the DataFrame is ready for processing and attempts to clean it.

        Returns:
        bool: True if the DataFrame is clean and not empty, False otherwise.
        """
        # Check if DataFrame is empty or not set.
        if self.unique_df is None or self.unique_df.empty:
            QMessageBox.warning(self, "Data Error", "No data available to plot.")
            return False

        # Process the DataFrame to ensure it's clean and usable.
        self.unique_df = self.prepare_data_for_processing(self.unique_df.copy())
        # Check if the DataFrame is still empty after processing.
        if self.unique_df.empty:
            QMessageBox.warning(self, "Data Error", "Data contains non-numeric values or all entries are NaN after conversion.")
            return False
        
        return True
    
    def prepare_plot_data(self):
        """
        Prepares the DataFrame for plotting by ensuring all data is numeric and non-missing.

        Returns:
        DataFrame: The processed DataFrame ready for plotting or None if data is invalid.
        """
        # Check if there's valid data to process.
        if self.unique_df is None or self.unique_df.empty:
            QMessageBox.warning(self, "Data Error", "No data available for processing.")
            return None

        processed_data = self.unique_df.copy()
        # Ensure all data is numeric and handle non-numeric entries gracefully.
        for i in range(processed_data.shape[1]):
            processed_data.iloc[:, i] = pd.to_numeric(processed_data.iloc[:, i], errors='coerce')
        # Remove any rows that contain NaN values after conversion.
        processed_data.dropna(inplace=True)

        # Verify there's still data left after processing.
        if processed_data.empty:
            QMessageBox.warning(self, "Data Error", "No valid data available after processing.")
            return None
        return processed_data
    
    def applyThresholdAndDisplay(self):
        """
        Applies a user-defined threshold to filter out duplicate data based on geographic coordinates.
        """
        # Ensure there's data to process.
        if self.df is not None:
            # Retrieve DataFrame from table widget for processing.
            current_df = self.tableWidgetToDataFrame(self.excelTableWidget)
            # Extract specific columns for longitude and latitude based on their current order.
            lon_col = current_df.columns[0]
            lat_col = current_df.columns[1]
            threshold_meters = float(self.lineEditThreshold.text())
            # Detect duplicates based on the specified threshold.
            duplicates_df = self.detect_possible_duplicates_with_improved_sjoin(current_df, lon_col, lat_col, threshold_meters)
            # Remove duplicates from the DataFrame.
            self.unique_df = self.remove_possible_duplicates(current_df, duplicates_df)
            # Display the cleaned DataFrame in the specified table widget.
            self.setupAndDisplayTable(self.unique_df, self.thresholdTableWidget)

    def detect_possible_duplicates_with_improved_sjoin(self, current_df, lon_col, lat_col, threshold_meters):
        """
        Detects possible duplicate entries within a specified distance threshold using spatial join.

        Args:
        current_df (DataFrame): DataFrame containing the data.
        lon_col (str): Column name for longitude.
        lat_col (str): Column name for latitude.
        threshold_meters (float): Distance threshold for considering two points as duplicates.

        Returns:
        DataFrame: A DataFrame indicating duplicate status for each row.
        """
        # Convert DataFrame to GeoDataFrame for spatial operations.
        gdf = gpd.GeoDataFrame(current_df, geometry=gpd.points_from_xy(current_df[lon_col], current_df[lat_col]), crs="EPSG:4326")
        # Transform to UTM coordinates to handle distance-based operations more accurately.
        gdf = gdf.to_crs(epsg=32633)
        # Perform a spatial join to itself to find nearest neighbors within the specified threshold.
        duplicates = gpd.sjoin_nearest(gdf, gdf, how='left', max_distance=threshold_meters, distance_col='distance')
        # Filter out self-matches and mark as 'Duplicate' if conditions are met.
        duplicates = duplicates[duplicates.index != duplicates['index_right']]
        duplicates['Status'] = 'Unique'
        duplicates.loc[duplicates.index < duplicates['index_right'], 'Status'] = 'Duplicate'
        return duplicates

    def remove_possible_duplicates(self, current_df, duplicates_df):
        """
        Removes rows marked as duplicates in the duplicates DataFrame.

        Args:
        current_df (DataFrame): Original DataFrame from which duplicates need to be removed.
        duplicates_df (DataFrame): DataFrame containing duplicate status for each row.

        Returns:
        DataFrame: The cleaned DataFrame with duplicates removed.
        """
        # Identify indices of rows marked as 'Duplicate'.
        duplicate_indices = duplicates_df[duplicates_df['Status'] == 'Duplicate'].index
        # Drop duplicates from the original DataFrame and reset index for cleanliness.
        self.unique_df = current_df.drop(index=duplicate_indices, errors='ignore').reset_index(drop=True)
        return self.unique_df
    
    def prepare_gdf_utm_from_result(self, unique_df, lon_col, lat_col, result_col):
        """
        Converts geographic data to UTM (Universal Transverse Mercator) coordinate system for accurate spatial analysis.

        Args:
        unique_df (DataFrame): DataFrame containing the geographic data.
        lon_col (str): Column name for longitude.
        lat_col (str): Column name for latitude.
        result_col (str): Column name for additional data, typically the results of some analysis.

        Returns:
        GeoDataFrame: GeoDataFrame with data in UTM coordinates.
        """
        # Create a GeoDataFrame from the DataFrame by setting geometry based on longitude and latitude.
        gdf = gpd.GeoDataFrame(unique_df, geometry=gpd.points_from_xy(unique_df[lon_col], unique_df[lat_col]), crs="EPSG:4326")
        # Convert the GeoDataFrame to UTM coordinates for accurate distance and area calculations.
        gdf_utm = gdf.to_crs(epsg=32633)
        return gdf_utm
    
############User Interface Interactions############
      
    def editHeader(self, tableWidget, index):
        """
        Allows editing of table header names by displaying a prompt with a text input dialog.

        Args:
        tableWidget (QTableWidget): The table where the header needs editing.
        index (int): The index of the column header that is being edited.
        """
        # Retrieve the current text of the header at the specified index.
        old_text = tableWidget.horizontalHeaderItem(index).text()
        # Open a dialog box to get new text from the user. Pre-fill it with the old header text.
        new_text, ok = QtWidgets.QInputDialog.getText(self, "Edit Header", "New header name:", QtWidgets.QLineEdit.Normal, old_text)
        # If the user presses OK and provides new text, update the header with the new text.
        if ok and new_text:
            tableWidget.horizontalHeaderItem(index).setText(new_text)
            
    def toggleManualFitInputs(self, enable):
        """
        Enables or disables the input fields for manually entering fit parameters.

        Args:
        enable (bool): If True, enable the fields; if False, disable them.
        """
        # Enable or disable each of the line edit fields based on the 'enable' parameter.
        self.fitNuggetLineEdit.setEnabled(enable)
        self.fitSillLineEdit.setEnabled(enable)
        self.fitRangeLineEdit.setEnabled(enable)
        
    def toggleFitSigma(self, state, widget):
        """
        Enable or disable the fit_sigma widget based on the state of its associated checkbox.

        Args:
        state (Qt.CheckState): The current state of the checkbox (checked or unchecked).
        widget (QWidget): The widget to be enabled or disabled.
        """
        # If the checkbox is checked, enable the widget.
        if state == Qt.Checked:
            widget.setEnabled(True)
        else:
            # If the checkbox is unchecked, disable the widget and set its value to "None".
            widget.setEnabled(False)
            widget.setCurrentIndex(widget.findText("None"))  # Ensure "None" is an available option in the ComboBox.
    
    def toggleBasemapCombo(self, state):
        """
        Toggles the availability of the basemap selection combo box based on a checkbox.

        Args:
        state (int): The state of the checkbox (checked or unchecked).
        """
        # Enable the basemap combo box only if the checkbox is checked.
        self.basemapCombo.setEnabled(state == Qt.Checked)
        
    def handleUncertaintyMapToggle(self, state):
        """
        Handles the state change of the uncertainty map checkbox to enable or disable related options.

        Args:
        state (int): The state of the checkbox (checked or unchecked).
        """
        # Output the current state of the uncertainty map checkbox for debugging.
        if state == Qt.Checked:
            print("Uncertainty map checkbox is checked.")
        else:
            print("Uncertainty map checkbox is not checked.")
            
    def closeTab(self, index):
        """
        Closes a tab in a tab widget.

        Args:
        index (int): The index of the tab to be closed.
        """
        # Retrieve the tab widget that emitted the signal for a tab close request.
        tab_widget = self.sender()
        # Remove the specified tab from the tab widget.
        tab_widget.removeTab(index)
        
    def onTabChange(self, index):
        """
        Responds to a change in the selected tab, typically to update display or data related to the new tab.

        Args:
        index (int): The index of the new active tab.
        """
        # Call a function to update the display of fit parameters based on the newly selected tab.
        self.updateFitParametersDisplay(index)
        
##########Plotting and Visualization########

    def plotVariogram(self):
        """
        This function handles the plotting of a variogram based on geographic data. It first validates and prepares the data,
        then constructs a variogram using the specified parameters.
        """
        # Check if the data is valid and ready for plotting; if not, terminate the function early.
        if not self.validate_and_prepare_data():
            return
       
        # Extract column names dynamically based on their order in the DataFrame
        lon_col = self.unique_df.columns[0]  # First column assumed to be longitude
        lat_col = self.unique_df.columns[1]  # Second column assumed to be latitude
        result_col = self.unique_df.columns[-1]  # Last column assumed to be the result variable

        # Prepare a GeoDataFrame with UTM (Universal Transverse Mercator) coordinates for accurate spatial analysis
        gdf_utm = self.prepare_gdf_utm_from_result(self.unique_df, lon_col, lat_col, result_col)
        # Combine x and y coordinates into a single array for processing
        utm_coords = np.column_stack((gdf_utm.geometry.x, gdf_utm.geometry.y))
        # Create a convex hull around data points to determine the outer boundary of the data
        hull = ConvexHull(utm_coords)
        # Convert the convex hull into a path object for later use in masking out-of-bounds points
        self.hull_path = MplPath(utm_coords[hull.vertices])
        
        # Generate a grid over the area covered by the convex hull to interpolate the variogram
        lon_range = np.linspace(utm_coords[:, 0].min(), utm_coords[:, 0].max(), 100)
        lat_range = np.linspace(utm_coords[:, 1].min(), utm_coords[:, 1].max(), 100)
        self.xgrid, self.ygrid = np.meshgrid(lon_range, lat_range)

        # Extract result values for the variogram analysis
        values = gdf_utm[result_col].values
        # Prepare parameters for the variogram calculation
        params = {'coordinates': utm_coords, 'values': values}

        # Prepare additional optional parameters based on user input through checkboxes and widgets
        optional_params = {
            'estimator': ('estimatorcombo', str),
            'model': ('modelcombo', str),
            'bin_func': ('bin_funccombo', str),
            'fit_sigma': ('fit_sigmacombo', str),
            'fit_method': ('fit_methodcombo', str),
            'normalize': ('normalizecombo', bool),
            'use_nugget': ('use_nuggetcombo', bool),
            'maxlag': ('maxlaglineedit', int),
            'n_lags': ('n_lagslineedit', int)
        }

        # If the manual method is selected, fetch additional parameters from the interface
        if self.fitMethodCombo.currentText() == "manual":
            try:
                params['fit_nugget'] = float(self.fitNuggetLineEdit.text())
                params['fit_sill'] = float(self.fitSillLineEdit.text())
                params['fit_range'] = float(self.fitRangeLineEdit.text())
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Please provide valid numerical inputs for nugget, sill, and range.")
                return
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))
                return

        # Add each optional parameter to the params dictionary if its corresponding checkbox is checked
        for key, (widget_name, cast_type) in optional_params.items():
            checkbox = self.findChild(QtWidgets.QCheckBox, 'chk' + key.lower())
            if checkbox and checkbox.isChecked():
                widget = self.findChild(QtWidgets.QWidget, widget_name)
                if widget:
                    value = widget.text() if cast_type is int else widget.currentText()
                    params[key] = cast_type(value)
                else:
                    print(f"Widget {widget_name} not found")

        # Output the parameters for debugging purposes
        print("Parameters for Variogram:", params)
        
        # Attempt to create a variogram object using the specified parameters; handle exceptions gracefully
        try:
            self.variogram = skg.Variogram(**params)
            # If successful, display the variogram using a predefined display method
            self.displayVariogram(self.variogram)
        except Exception as e:
            QMessageBox.critical(self, "Variogram Error", str(e))
            return
        
        

    def displayVariogram(self, variogram, show_in_spyder=False):
        """
        Displays the variogram plot based on the calculated variogram data. This method visualizes both experimental 
        and theoretical variogram values and provides options for additional debugging in an interactive Python environment.

        Args:
        variogram (Variogram object): The variogram object containing all the necessary data.
        show_in_spyder (bool): If True, additionally display the plot in an interactive environment like Spyder.
        """
        # Initialize a matplotlib figure with specified size
        fig = Figure(figsize=(10,6))
        ax = fig.add_subplot(111)  # Add a subplot in the figure
        
        # Retrieve data from the variogram object
        pair_counts = variogram.bin_count  # Number of pairs per lag
        lags = variogram.bins  # The distances (lags) at which the variogram was calculated
        experimental_variogram = variogram.experimental  # The calculated semivariance values for each lag
        
        # Create a DataFrame from variogram data to possibly use later for displaying or further analysis
        dem = pd.DataFrame({
            "np": pair_counts,  # Pair counts
            "lags": lags,  # Lag distances
            "semivariance": experimental_variogram  # Semivariance values
        })

        # Plot the theoretical and experimental variogram on the axes
        theoretical_variogram = variogram.model(lags, *variogram.parameters)  # The theoretical model computed from parameters
        ax.plot(lags, theoretical_variogram, color='red', label='Theoretical', linewidth=2)
        ax.scatter(lags, experimental_variogram, color='blue', label='Experimental')

        # Set plot limits and labels
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        ax.set_xlabel('Distance')
        ax.set_ylabel('Semivariance')
        ax.set_title('Variogram with Fit')
        ax.legend()  # Show legend
        ax.grid(False)  # Disable grid
        
        fig.tight_layout()  # Adjust layout to make room for all labels

        # Store the plot parameters for potential debugging or display purposes
        self.plot_parameters.append({
            'estimator': self.widgets['estimator'].currentText() if 'estimator' in self.widgets else 'default',
            'model': variogram.model.__name__,
            'bin_func': self.widgets['bin_func'].currentText() if 'bin_func' in self.widgets else 'default',
            'fit_sigma': self.widgets['fit_sigma'].currentText() if 'fit_sigma' in self.widgets else 'default',
            'normalize': self.widgets['normalize'].currentText() if 'normalize' in self.widgets else 'default',
            'use_nugget': self.widgets['use_nugget'].currentText() if 'use_nugget' in self.widgets else 'default',
            'maxlag': self.widgets['maxlag'].text() if 'maxlag' in self.widgets else 'default',
            'n_lags': self.widgets['n_lags'].text() if 'n_lags' in self.widgets else 'default',
            'fit_method': self.widgets['fit_method'].currentText() if 'fit_method' in self.widgets else 'default',
            "nugget":self.variogram.parameters[-1] if self.variogram.use_nugget else 0,
            "psill": self.variogram.parameters[1] if self.variogram.use_nugget else self.variogram.parameters[0],
            "range": self.variogram.parameters[0]
        })
        
        # If requested to show in Spyder or similar environment, setup the plot for interactive viewing
        if show_in_spyder:
            plt.figure(figsize=(10, 9))
            plt.scatter(lags, experimental_variogram, color='blue', label='Experimental')
            plt.plot(lags, theoretical_variogram, color='red', label='Theoretical', linewidth=2)
            plt.xlim(left=0)
            plt.ylim(bottom=0)
            plt.xlabel('Distance')
            plt.ylabel('Semivariance')
            plt.title('Variogram with Fit')
            plt.legend()
            plt.grid(True)
            plt.show()

        # Setup the matplotlib canvas and toolbar for embedding in the Qt widget framework
        canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar(canvas, self)
        
        # Create a QWidget and set its layout to include the plot and toolbar
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(toolbar)
        layout.addWidget(canvas)
        widget.setLayout(layout)
        
        # Add the new plot as a tab in the application's tab widget
        tab_index = self.tabVariogramPlots.addTab(widget, f"Variogram Plot {self.tabVariogramPlots.count() + 1}")
        self.tabVariogramPlots.setCurrentIndex(tab_index)  # Make the new tab active
        
        # Optionally show the plot in Spyder or other environments if required
        if show_in_spyder:
            plt.show()

        # Display the DataFrame containing the variogram data in a specified scroll area and update fit parameters
        self.displayTableInScrollArea(dem, self.scrollAreaSemivariance)
        self.updateFitParametersDisplay(tab_index)
        
        

    def plotKriging(self):
        """
        Generates a kriging plot based on previously computed variogram parameters. It includes
        options to add a basemap and an uncertainty map.
        """
        # Validate the input parameters are correctly set
        if not self.validateInputs():
            return
        # Ensure a valid variogram is present before proceeding
        if not hasattr(self, 'variogram') or self.variogram is None:
            QMessageBox.warning(self, "Variogram Error", "Please generate a valid variogram before kriging.")
            return
        
        # Retrieve current input values from the UI
        current_params = {
            'min_points': int(self.minPointsLineEdit.text()),
            'max_points': int(self.maxPointsLineEdit.text()),
            'levels': int(self.levelsLineEdit.text()),
            'alpha': float(self.alphaLineEdit.text()),
        }

        # Perform Kriging using the OrdinaryKriging model from skgstat library
        try:
            OK = skg.OrdinaryKriging(
                self.variogram,
                min_points=current_params['min_points'],
                max_points=current_params['max_points']
            )
            # Apply the kriging model to transform coordinate grid data
            zgrid = OK.transform(self.xgrid.ravel(), self.ygrid.ravel())
            # Reshape the output to match the original grid dimensions
            Z = zgrid.reshape(self.xgrid.shape)

            # Apply a mask to only include data points within the convex hull of the sample points
            mask = np.array([self.hull_path.contains_point((x, y)) for x, y in zip(self.xgrid.flatten(), self.ygrid.flatten())])
            mask = mask.reshape(self.xgrid.shape)
            Z_masked = np.where(mask, Z, np.nan)

            # Convert geographic coordinates back to the original Coordinate Reference System (CRS)
            gdf_pred = gpd.GeoDataFrame(geometry=gpd.points_from_xy(self.xgrid.ravel(), self.ygrid.ravel()), crs="EPSG:32633")
            gdf_pred = gdf_pred.to_crs("EPSG:4326")
            lon_grid = gdf_pred.geometry.x.values.reshape(self.xgrid.shape)
            lat_grid = gdf_pred.geometry.y.values.reshape(self.ygrid.shape)

            # Create a new tab for displaying the plot
            fig = Figure(figsize=(200, 190))
            ax = fig.add_subplot(111)
            contourf = ax.contourf(lon_grid, lat_grid, Z_masked, levels=current_params['levels'], alpha=current_params['alpha'], cmap="rainbow")
            fig.colorbar(contourf, ax=ax, label='nGy/h')

            ax.set_title('Krige Plot')
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')

            # Add a basemap if the corresponding checkbox is checked
            if self.chkBasemap.isChecked():
                selected_basemap = self.basemapCombo.currentText()
                basemap_mapping = {
                    "Esri.WorldImagery": ctx.providers.Esri.WorldImagery,
                    "OpenStreetMap.Mapnik": ctx.providers.OpenStreetMap.Mapnik,
                    "Esri.DeLorme": ctx.providers.Esri.DeLorme,
                    "CartoDB.Positron": ctx.providers.CartoDB.Positron,
                    "CartoDB.DarkMatter": ctx.providers.CartoDB.DarkMatter,
                    "OpenTopoMap": ctx.providers.OpenTopoMap,
                }
                basemap_source = basemap_mapping[selected_basemap]
                ctx.add_basemap(ax, crs="EPSG:4326", source=basemap_source)

            # Setup the widget and add it to the application's tab widget
            krige_widget = QWidget()
            krige_layout = QVBoxLayout()
            krige_canvas = FigureCanvas(fig)
            toolbar = NavigationToolbar(krige_canvas, krige_widget)
            krige_layout.addWidget(toolbar)
            krige_layout.addWidget(krige_canvas)
            krige_widget.setLayout(krige_layout)
            krige_plot_label = f"Krige Plot {self.krigePlotCount + 1}"
            self.krigePlots.addTab(krige_widget, krige_plot_label)
            self.krigePlotCount += 1
            self.kriging_parameters.append(current_params)
            self.updateKrigingParametersDisplay()

            # Optionally add an uncertainty map if the corresponding checkbox is checked
            if self.chkUncertaintymap.isChecked():
                fig_uncertainty = Figure(figsize=(10, 6))
                ax_uncertainty = fig_uncertainty.add_subplot(111)
                sigma = OK.transform(self.xgrid.ravel(), self.ygrid.ravel())
                sigma = OK.sigma.reshape(self.xgrid.shape)
                sigma_std = np.sqrt(sigma)
                relative_uncertainty = 100 * sigma_std / Z_masked
                relative_uncertainty_masked = np.where(mask, relative_uncertainty, np.nan)
                contourf_uncertainty = ax_uncertainty.contourf(lon_grid, lat_grid, relative_uncertainty_masked, levels=100, cmap="rainbow", alpha=0.6)
                fig_uncertainty.colorbar(contourf_uncertainty, ax=ax_uncertainty, label='Uncertainty (%)')
                ax_uncertainty.set_title('Uncertainty Map')
                ax_uncertainty.set_xlabel('Longitude')
                ax_uncertainty.set_ylabel('Latitude')
                uncertainty_widget = QWidget()
                uncertainty_layout = QVBoxLayout()
                uncertainty_canvas = FigureCanvas(fig_uncertainty)
                uncertainty_toolbar = NavigationToolbar(uncertainty_canvas, uncertainty_widget)
                uncertainty_layout.addWidget(uncertainty_toolbar)
                uncertainty_layout.addWidget(uncertainty_canvas)
                uncertainty_widget.setLayout(uncertainty_layout)
                uncertainty_map_label = f"Uncertainty Map {self.krigePlotCount}"
                self.krigePlots.addTab(uncertainty_widget, uncertainty_map_label)

        except Exception as e:
            QMessageBox.critical(self, "Kriging Error", str(e))
            return       
        
        

    def plotRawHistogram(self):
        """
        Plots a histogram of the last column of the data currently loaded, with an optional subset fraction.
        """
        # Read the fraction from the user input, defaulting to 0 (plot all data)
        fraction_input = self.lineEditRawHistogram.text()
        processed_data = self.prepare_plot_data()
        if processed_data is None:
            return  # Exit if no data is available

        try:
            # Convert the fraction input to a float; handle invalid input gracefully
            fraction = float(fraction_input) if fraction_input else 0
            # Sample a fraction of the data if specified; otherwise use all data
            data = processed_data.sample(frac=fraction) if fraction > 0 else processed_data
            base_title = "Subset Histogram" if fraction > 0 else "Raw Histogram"
            title = f"{base_title} {self.getNextTabIndex(base_title)}"
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid fraction value.")
            return

        # Create the histogram plot
        fig = Figure()
        ax = fig.add_subplot(111)
        sns.histplot(data.iloc[:, -1], kde=False, bins=30, ax=ax)
        ax.set_title(title)
        ax.set_xlabel('Values')
        ax.set_ylabel('Frequency')
        self.addPlotToTab(fig, title)  # Add the plot to the application's tab widget

    def plotScatterPlot(self):
        """
        Creates a scatter plot using the first two columns for coordinates and the third for color coding.
        """
        fraction_input = self.lineEditScatterPlot.text()
        processed_data = self.prepare_plot_data()
        if processed_data is None:
            return

        try:
            fraction = float(fraction_input) if fraction_input else 0
            data = processed_data.sample(frac=fraction) if fraction > 0 else processed_data
            title = f"Scatter Plot {self.getNextTabIndex('Scatter Plot')}"
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid fraction value.")
            return

        # Create the scatter plot
        fig = Figure()
        ax = fig.add_subplot(111)
        scatter = ax.scatter(data.iloc[:, 0], data.iloc[:, 1], c=data.iloc[:, 2])
        cbar = fig.colorbar(scatter, ax=ax)
        cbar.set_label('Values')
        ax.set_title(title)
        self.addPlotToTab(fig, title)  # Add the plot to the application's tab widget

    def plotPairPlot(self):
        """
        Generates a pair plot for the data currently loaded, showing relationships between all columns.
        """
        processed_data = self.prepare_plot_data()
        if processed_data is None:
            return

        sns.pairplot(processed_data)
        title = f"Pair Plot {self.getNextTabIndex('Pair Plot')}"
        self.addPlotToTab(plt.gcf(), title)  # Add the plot to the application's tab widget using matplotlib's current figure

    def addPlotToTab(self, fig, title):
        """
        Adds a matplotlib figure to a new tab in the plot tab widget.

        Args:
        fig (matplotlib.figure.Figure): The figure to display.
        title (str): The title for the new tab.
        """
        # Wrap the figure in a Qt canvas to integrate with the Qt framework
        canvas = FigureCanvas(fig)
        # Add a toolbar to provide interaction tools to the plot
        toolbar = NavigationToolbar(canvas, self)
        # Create a widget to hold the layout
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.addWidget(toolbar)
        layout.addWidget(canvas)
        widget.setLayout(layout)
        # Add the widget to the tab widget and make it the active tab
        idx = self.plotTabWidget.addTab(widget, title)
        self.plotTabWidget.setCurrentIndex(idx)
        
#########Table Display and Management############

    def setupAndDisplayTable(self, df, tableWidget):
        """
        Sets up a QTableWidget to display data from a pandas DataFrame.

        Args:
        df (pandas.DataFrame): The data frame containing the data to display.
        tableWidget (QTableWidget): The table widget where data will be displayed.
        """
        # Clear the table to ensure it's empty before adding new data
        tableWidget.clear()
        tableWidget.setRowCount(0)
        tableWidget.setColumnCount(0)

        # Set the number of rows and columns based on the DataFrame's shape
        tableWidget.setRowCount(df.shape[0])
        tableWidget.setColumnCount(df.shape[1])
        # Set the column headers from the DataFrame column names
        tableWidget.setHorizontalHeaderLabels(df.columns.tolist())

        # Populate the table with items from the DataFrame
        for row_index in range(df.shape[0]):
            for col_index in range(df.shape[1]):
                # Convert each value to a string and create a table cell item
                item = QtWidgets.QTableWidgetItem(str(df.iloc[row_index, col_index]))
                item.setTextAlignment(Qt.AlignCenter)  # Center align text in the cell
                tableWidget.setItem(row_index, col_index, item)  # Place the item in the table

    def tableWidgetToDataFrame(self, tableWidget):
        """
        Converts a QTableWidget back into a pandas DataFrame.

        Args:
        tableWidget (QTableWidget): The table widget to convert.

        Returns:
        pandas.DataFrame: DataFrame containing the table's data.
        """
        # Retrieve the number of columns and rows in the table widget
        column_count = tableWidget.columnCount()
        row_count = tableWidget.rowCount()
        # Extract headers from the table widget
        headers = [tableWidget.horizontalHeaderItem(i).text() for i in range(column_count)]
        # Create an empty DataFrame with the headers and appropriate number of rows
        df = pd.DataFrame(columns=headers, index=range(row_count))

        # Fill the DataFrame with items from the table widget
        for row in range(row_count):
            for col in range(column_count):
                item = tableWidget.item(row, col)
                # Assign the item text to the DataFrame cell, handle None items gracefully
                df.iloc[row, col] = item.text() if item else None

        return df
    
    def displayTableInScrollArea(self, df, scrollArea):
        """
        Displays a DataFrame in a QScrollArea using a QTableWidget.

        Args:
        df (pandas.DataFrame): The DataFrame containing the data to display.
        scrollArea (QScrollArea): The scroll area where the table will be displayed.
        """
        # Ensure the scroll area is cleared before adding a new table
        scrollArea.setWidget(None)

        # Create a new QTableWidget and set its dimensions based on the DataFrame
        tableWidget = QTableWidget()
        tableWidget.setRowCount(df.shape[0])
        tableWidget.setColumnCount(df.shape[1])
        # Set column headers from the DataFrame
        tableWidget.setHorizontalHeaderLabels(df.columns.tolist())

        # Populate the table widget with formatted data from the DataFrame
        for index, row in df.iterrows():
            for col_index, value in enumerate(row):
                formatted_value = self.format_value(value)
                item = QTableWidgetItem(formatted_value)
                item.setTextAlignment(Qt.AlignCenter)
                tableWidget.setItem(index, col_index, item)

        # Create or get the current widget contained in the scroll area
        scrollAreaWidgetContents = scrollArea.widget()
        if scrollAreaWidgetContents is None:
            scrollAreaWidgetContents = QtWidgets.QWidget()
            scrollArea.setWidget(scrollAreaWidgetContents)
            layout = QVBoxLayout(scrollAreaWidgetContents)
        else:
            layout = scrollAreaWidgetContents.layout()
            if layout is None:
                layout = QVBoxLayout(scrollAreaWidgetContents)

        # Remove any existing widgets in the layout to avoid duplicates
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add the newly populated table widget to the layout
        layout.addWidget(tableWidget)

#######Event Handling and Dynamic Updates##############

    def onFitMethodChanged(self, method):
        """
        Handles changes in the selected fitting method for variogram computation.
        Args:
        method (str): The selected method from the dropdown.
        """
        # Enable or disable manual input fields based on the selected method
        if method == "manual":
            self.toggleManualFitInputs(True)  # Enable manual inputs for fitting parameters
        else:
            self.toggleManualFitInputs(False)  # Disable manual inputs

    def updateFitParametersDisplay(self, index):
        """
        Updates the displayed fitting parameters when a different variogram plot tab is selected.
        Args:
        index (int): The index of the currently active tab.
        """
        # Check if the index is within the bounds of stored parameters
        if index < len(self.plot_parameters):
            params = self.plot_parameters[index]
            # Update the label to show the parameters of the selected plot
            self.labelFitParameters.setText(
                f"Psill: {params['psill']:.4f}\n"
                f"Range: {params['range']:.4f}\n"
                f"Nugget: {params['nugget']:.4f}"
            )
        else:
            # Set text when no plot is selected or available
            self.labelFitParameters.setText("Select a plot to see parameters.")
            
    def updateKrigingParametersDisplayOnTab(self):
        """
        Updates the kriging parameters displayed in the UI when a different kriging plot tab is selected.
        """
        current_index = self.krigePlots.currentIndex()
        if current_index < 0 or current_index >= len(self.kriging_parameters):
            self.framekrigeparameters.setText("No kriging parameters to display.")
            return
        
        # Get the current parameters and update them in the UI
        updated_params = {
            'min_points': int(self.minPointsLineEdit.text()),
            'max_points': int(self.maxPointsLineEdit.text()),
            'levels': int(self.levelsLineEdit.text()),
            'alpha': float(self.alphaLineEdit.text()),
        }
        # Check if there are parameters to update for the current tab
        if current_index < len(self.kriging_parameters):
            self.kriging_parameters[current_index] = updated_params
        self.updateKrigingParametersDisplay()
        
    def updateKrigingParametersDisplay(self):
        """
        Updates the display of kriging parameters based on the currently selected tab.
        """
        current_index = self.krigePlots.currentIndex()
        if 0 <= current_index < len(self.kriging_parameters):
            params = self.kriging_parameters[current_index]
            # Format and set the text for the kriging parameters
            params_text = f"Min Points: {params['min_points']}\nMax Points: {params['max_points']}\nLevels: {params['levels']}\nAlpha: {params['alpha']:.2f}"
            self.framekrigeparameters.setText(params_text)
        else:
            self.framekrigeparameters.setText("No kriging parameters to display.")
            
    def updateVariogramParametersDisplay(self):
        """
        Updates the display of variogram parameters for the currently selected variogram plot.
        """
        current_index = self.tabVariogramPlots.currentIndex()
        if current_index < 0 or current_index >= len(self.plot_parameters):
            return

        variogram_params = self.plot_parameters[current_index]
        params_text = ""

        # Dynamic parameter display based on whether checkboxes are checked
        parameter_keys = [
            'estimator', 'model', 'bin_func', 'fit_sigma', 
            'normalize', 'use_nugget', 'maxlag', 'n_lags', 'fit_method'
        ]

        for key in parameter_keys:
            # Check if the checkbox associated with this parameter is checked
            checkbox = self.findChild(QtWidgets.QCheckBox, 'chk' + key.lower())
            if checkbox and checkbox.isChecked():
                # Only add the parameter to the text if the checkbox is checked
                if key in ['maxlag', 'n_lags']:  # Numeric values
                    value = f"{float(variogram_params[key]):.1f}" if key in variogram_params else "default"
                else:
                    value = variogram_params.get(key, 'default')

                params_text += f"{key}: {value}\n"
  
        self.framevariogramparameters.setText(params_text.strip())
        
    def getNextTabIndex(self, baseTitle):
        """
        Finds a unique index for a new tab based on the base title to avoid title duplication.
        Args:
        baseTitle (str): The base title to use for finding a unique tab index.
        
        Returns:
        int: A unique index for the new tab.
        """
        count = 1
        existing_titles = [self.plotTabWidget.tabText(i) for i in range(self.plotTabWidget.count())]
        # Increment count until a unique title is found
        while f"{baseTitle} {count}" in existing_titles:
            count += 1
        return count
    
########Utilities and Validation##########
    def format_value(self, value):
        """
        Formats a given value to display up to four decimal places if it's a decimal number,
        or as an integer if it is a whole number. This helps in displaying numerical values neatly.
        
        Args:
        value (str): The string value to format, expected to be convertible to a float.
        
        Returns:
        str: The formatted string of the number with up to four decimal places or as an integer.
        """
        try:
            # Try to convert the value to a float
            float_value = float(value)
            # If the float is an integer (no decimal part), format it as an integer
            if float_value.is_integer():
                return f"{int(float_value)}"
            else:
                # Otherwise, format it with four decimal places
                return f"{float_value:.4f}"
        except ValueError:
            # If conversion to float fails, return the original value unchanged
            return value
        
    def validateInputs(self):
        """
        Validates the user inputs from the GUI to ensure they are appropriate for kriging.
        This includes checking that numeric values are within specified ranges and are valid numbers.
        
        Returns:
        bool: True if all inputs are valid, False otherwise.
        """
        # Validate min_points and max_points to ensure they are non-zero and valid integers
        try:
            # Read values from the GUI and try to convert them to appropriate types
            min_points = int(self.minPointsLineEdit.text())
            max_points = int(self.maxPointsLineEdit.text())
            levels = int(self.levelsLineEdit.text())
            alpha = float(self.alphaLineEdit.text())

            # Check if the numeric values are within acceptable ranges
            if min_points <= 0 or max_points <= 0 or levels < 1:
                QMessageBox.warning(self, "Input Error", "Min points, max points, and levels must be greater than zero.")
                return False
            
            if alpha < 0 or alpha > 1:
                QMessageBox.warning(self, "Input Error", "Alpha must be between 0 and 1.")
                return False
            
        except ValueError:
            # If there is an error in conversion, show an error message
            QMessageBox.warning(self, "Input Error", "Please enter valid numerical values.")
            return False
        
        # Return True if all checks are passed
        return True
    
############################
def apply_white_theme(app):
    """
    Applies a white theme to the Qt application to enhance its appearance with a modern look.

    Args:
    app (QtWidgets.QApplication): The application object to which the theme will be applied.
    """
    # Set the application's style to 'Fusion', a style provided by Qt which is suitable for customization
    app.setStyle('Fusion')

    # Create a new color palette to define colors for various interface elements
    palette = QtGui.QPalette()

    # Configure colors for different parts of the interface:
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255))  # Set the background color of windows to white
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0))  # Set the text color in windows to black for contrast
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))  # Set the background color of base widgets like QLineEdit to white
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(245, 245, 245))  # Use a slightly off-white color for alternate rows in views
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(255, 255, 255))  # Set button background color to white
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(0, 0, 0))  # Set text color on buttons to black
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(173, 216, 230))  # Use a light blue color for highlight effects
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 0, 0))  # Set highlighted text color to black

    # Apply the configured palette to the application to change colors globally
    app.setPalette(palette)

    # Apply additional custom styles using CSS to fine-tune the appearance:
    app.setStyleSheet("""
        QPushButton {
            background-color: white;  # Button background color
            border: 2px solid #add8e6;  # Light blue border for buttons
            border-radius: 5px;  # Rounded corners for buttons
            padding: 5px;  # Padding around text in buttons
        }
        QPushButton:hover {
            border: 2px solid #a0c0d0;  # Darker blue border on mouse hover
        }
        QPushButton:pressed {
            background-color: #f0f0f0;  # Light grey background when button is pressed
        }
        QComboBox {
            border: 2px solid #add8e6;  # Light blue border for combo boxes
            border-radius: 3px;  # Rounded corners for combo boxes
            padding: 2px 5px;  # Padding inside combo boxes
        }
        QLabel {
            color: black;  # Text color for labels
            background-color: #f0f0f0;  # Light grey background for labels for better readability
        }
        QGroupBox {
            background-color: #f0f0f0;  # Light grey background for group boxes
            border: 2px solid #e7e7e7;  # Light grey border for group boxes
            border-radius: 5px;  # Rounded corners for group boxes
            margin-top: 20px;  # Space above the group box title
        }
        QGroupBox:title {
            subcontrol-origin: margin;  # Align title with the border margin
            subcontrol-position: top center;  # Position the title at the top center
            padding: 0 10px;  # Padding around the title
            background-color: #f0f0f0;  # Background color of the title
        }
    """)

# If this script is the main program that is run, set up the application and apply the theme
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)  # Create an application instance
    apply_white_theme(app)  # Apply the white theme to the application
    mainWindow = ExcelLoaderApp()  # Create the main window of the application
    mainWindow.show()  # Display the main window
    sys.exit(app.exec_())  # Start the application's event loop
