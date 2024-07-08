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
from PyQt5.QtWidgets import QFileDialog, QTableWidget, QTableWidgetItem, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
import skgstat as skg
from PyQt5 import QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QWidget

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

class ExcelLoaderApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("D:/qtkrige.ui", self)
        self.setupTableWidget(self.excelTableWidget)
        self.setupTableWidget(self.thresholdTableWidget)
        self.df = None
        self.unique_df = None  # Initialize it here
        self.plot_parameters = []
        self.clean_df = None

          
        # Find the QGroupBoxes and their children
        self.groupBoxSelectFile = self.findChild(QtWidgets.QGroupBox, 'selectexcelfile') #groupbox
        # Assuming group boxes are found, find children
        if self.groupBoxSelectFile:
            self.pushButtonOpenFile = self.groupBoxSelectFile.findChild(QtWidgets.QPushButton, 'openexcelfile')
            self.scrollAreaExcel = self.groupBoxSelectFile.findChild(QtWidgets.QScrollArea, 'excelscrollarea')
        # Connect signals to slots
        if self.pushButtonOpenFile:
            self.pushButtonOpenFile.clicked.connect(self.loadAndDisplayExcel)
          
        self.groupBoxThreshold = self.findChild(QtWidgets.QGroupBox, 'enterthresholdvalue') #groupbox
        if self.groupBoxThreshold:
            self.lineEditThreshold = self.groupBoxThreshold.findChild(QtWidgets.QLineEdit, 'thresholdvalue')
            self.pushButtonConfirmThreshold = self.groupBoxThreshold.findChild(QtWidgets.QPushButton, 'confirmthreshold')
            self.scrollAreaThreshold = self.groupBoxThreshold.findChild(QtWidgets.QScrollArea, 'thresholdscrollarea')
        if self.pushButtonConfirmThreshold:
            self.pushButtonConfirmThreshold.clicked.connect(self.applyThresholdAndDisplay)
          
        self.groupBoxVariogramParameters = self.findChild(QtWidgets.QGroupBox, 'variogramparameters') #groupbox
        # Setup for variogram parameters
        if self.groupBoxVariogramParameters:
            self.setupVariogramWidgets()
          
        self.pushButtonPlotVariogram = self.findChild(QtWidgets.QPushButton, 'plotvariogram')
        if self.pushButtonPlotVariogram:
            self.pushButtonPlotVariogram.clicked.connect(self.plotVariogram)

        # Attempt to find the GroupBoxes
        self.krigePlotsGroupBox = self.findChild(QtWidgets.QGroupBox, 'krigeplotsgroupbox')
        # Check if GroupBoxes are found
        if not self.krigePlotsGroupBox:
            print("Failed to find 'krigeplotsgroupbox'.")
        else:
            # Find krigePlots tab widget inside the GroupBox
            self.krigePlots = self.krigePlotsGroupBox.findChild(QtWidgets.QTabWidget, 'krigeplots')
        if not self.krigePlots:
            print("krigeplots tab widget not found inside 'krigeplotsgroupbox'.")
      
        self.groupBoxSemivariance = self.findChild(QtWidgets.QGroupBox, 'semivariance') #groupbox
        if self.groupBoxSemivariance:
            self.scrollAreaSemivariance = self.groupBoxSemivariance.findChild(QtWidgets.QScrollArea, 'semivariancescrollarea')

        self.plotsGroupBox = self.findChild(QtWidgets.QGroupBox, 'plotsgroupbox')
        if not self.plotsGroupBox:
            print("Failed to find 'plotsgroupbox'.")
        else:
            # Find plotTabWidget inside the GroupBox
            self.plotTabWidget = self.plotsGroupBox.findChild(QtWidgets.QTabWidget, 'plotfuck')
        if not self.plotTabWidget:
            print("Failed to find 'plotTabWidget' inside 'plotsgroupbox'.")
      


        # Debugging to see if group boxes are found
        #print("Group Box for Select File found." if self.groupBoxSelectFile else "Group Box for Select File not found.")
       # print("Group Box for Threshold found." if self.groupBoxThreshold else "Group Box for Threshold not found.")
        #print("Group Box for Variogram Parameters found." if self.groupBoxVariogramParameters else "Group Box for Variogram Parameters not found.")
       # print("Group Box for Semivariance found." if self.groupBoxSemivariance else "Group Box for Semivariance not found.")


         # Assuming the QLabel is in a frame named 'fitparametersframe'
        self.labelFitParameters = self.findChild(QtWidgets.QLabel, 'fitparameterslabel')
        if not self.labelFitParameters:
            self.labelFitParameters = QtWidgets.QLabel("No parameters available.")
            layout = QVBoxLayout(self.framefitparameters)
            layout.addWidget(self.labelFitParameters)
            self.framefitparameters.setLayout(layout)
        
        # Initialize your application components here
        self.tabVariogramPlots.currentChanged.connect(self.onTabChange)
##################################################################################

        self.setupTableWidget(self.excelTableWidget)
        self.setupTableWidget(self.thresholdTableWidget)
        self.setupTableWidget(self.semivarianceTableWidget)
        # Initialize UI and connections
        self.setupUI() 
        self.setupConnections()

    def setupTableWidget(self, tableWidget):
        # Enable column moving
        tableWidget.horizontalHeader().setSectionsMovable(True)
        tableWidget.horizontalHeader().setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
    
        # Enable sorting for columns and prevent flipping the entire data
        tableWidget.setSortingEnabled(False)
    
        # Enable editing of headers and cells
        tableWidget.horizontalHeader().setSectionsClickable(True)
        tableWidget.horizontalHeader().sectionDoubleClicked.connect(
            lambda index: self.editHeader(tableWidget, index)
        )
        tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
    
        # Set alternating row colors for better readability
        tableWidget.setAlternatingRowColors(True)
        tableWidget.setStyleSheet("alternate-background-color: #f0f0f0; background-color: #ffffff;")
    
    def editHeader(self, tableWidget, index):
        old_text = tableWidget.horizontalHeaderItem(index).text()
        new_text, ok = QtWidgets.QInputDialog.getText(self, "Edit Header", "New header name:", QtWidgets.QLineEdit.Normal, old_text)
        if ok and new_text:
            tableWidget.horizontalHeaderItem(index).setText(new_text)
        
    def setupUI(self):
        # Find and setup UI components here
        self.fitMethodCombo = self.findChild(QtWidgets.QComboBox, 'fit_methodcombo')
        self.fitNuggetLineEdit = self.findChild(QtWidgets.QLineEdit, 'fit_nuggetlineedit')
        self.fitSillLineEdit = self.findChild(QtWidgets.QLineEdit, 'fit_silllineedit')
        self.fitRangeLineEdit = self.findChild(QtWidgets.QLineEdit, 'fit_rangelineedit')
        
       
        # Check if components are loaded correctly
        if not self.fitMethodCombo or not self.fitNuggetLineEdit or not self.fitSillLineEdit or not self.fitRangeLineEdit:
            print("Error: One or more variogram parameter widgets could not be found.")
            return  # Handle this situation appropriately, maybe disable functionality or show error

        # Initially disable line edits until manual is selected
        self.toggleManualFitInputs(False)
        
        # Set tabs to be closable
        self.krigePlots.setTabsClosable(True)
        self.tabVariogramPlots.setTabsClosable(True)
    
        #Connect the tab close request to a slot
        self.krigePlots.tabCloseRequested.connect(self.closeTab)
        self.tabVariogramPlots.tabCloseRequested.connect(self.closeTab)

        self.minPointsLineEdit = self.findChild(QtWidgets.QLineEdit, 'min_points')
        self.maxPointsLineEdit = self.findChild(QtWidgets.QLineEdit, 'max_points')
        self.levelsLineEdit = self.findChild(QtWidgets.QLineEdit, 'levels')
        self.alphaLineEdit = self.findChild(QtWidgets.QLineEdit, 'alpha')
        
        self.chkBasemap = self.findChild(QtWidgets.QCheckBox, 'chkbasemap')
        self.basemapCombo = self.findChild(QtWidgets.QComboBox, 'basemapcombo')
        self.chkUncertaintymap = self.findChild(QtWidgets.QCheckBox, 'chkuncertaintymap')
        self.uncertaintymapCombo = self.findChild(QtWidgets.QComboBox, 'uncertaintymapcombo')
        
        self.chkKrigemap = self.findChild(QtWidgets.QCheckBox, 'includekrigeplot')
        
        # Initially disable basemap combo until checkbox is checked
        self.basemapCombo.setEnabled(False)
        self.uncertaintymapCombo.setEnabled(False)

    def setupConnections(self):
        self.fitMethodCombo.currentTextChanged.connect(self.onFitMethodChanged)

        self.tabVariogramPlots.currentChanged.connect(self.onTabChange)

        # Correcting the button connection using the correct QPushButton name
        self.plotKrigingButton = self.findChild(QtWidgets.QPushButton, 'plotkrige')
        if self.plotKrigingButton:
            self.plotKrigingButton.clicked.connect(self.plotKriging)

        self.chkBasemap.stateChanged.connect(self.toggleBasemapCombo)
        self.chkUncertaintymap.stateChanged.connect(self.toggleUncertaintymapCombo)

        # Finding QPushButton widgets
        self.pushButtonRawHistogram = self.findChild(QtWidgets.QPushButton, 'rawhistogram')
        self.pushButtonScatterPlot = self.findChild(QtWidgets.QPushButton, 'scatterplot')
        self.pushButtonPairPlot = self.findChild(QtWidgets.QPushButton, 'pairplot')

        # Finding QLineEdit widgets associated with the push buttons
        self.lineEditRawHistogram = self.findChild(QtWidgets.QLineEdit, 'rawhistogramlineedit')
        self.lineEditScatterPlot = self.findChild(QtWidgets.QLineEdit, 'scatterplotlineedit')

        # Connecting buttons to their respective functions
        if self.pushButtonRawHistogram:
            self.pushButtonRawHistogram.clicked.connect(self.plotRawHistogram)
        else:
            print("Failed to find 'rawhistogram' QPushButton.")

        if self.pushButtonScatterPlot:
            self.pushButtonScatterPlot.clicked.connect(self.plotScatterPlot)
        else:
            print("Failed to find 'scatterplot' QPushButton.")

        if self.pushButtonPairPlot:
            self.pushButtonPairPlot.clicked.connect(self.plotPairPlot)
        else:
            print("Failed to find 'pairplot' QPushButton.")

    def onFitMethodChanged(self, method):
        if method == "manual":
            self.toggleManualFitInputs(True)
        else:
            self.toggleManualFitInputs(False)

    def toggleManualFitInputs(self, enable):
        self.fitNuggetLineEdit.setEnabled(enable)
        self.fitSillLineEdit.setEnabled(enable)
        self.fitRangeLineEdit.setEnabled(enable)


    def closeTab(self, index):
        # Close the tab at the specified index
        tab_widget = self.sender()  # Gets the sender of the signal
        tab_widget.removeTab(index)
    

    def onTabChange(self, index):
        self.updateFitParametersDisplay(index)

    def updateFitParametersDisplay(self, index):
        if index < len(self.plot_parameters):
            params = self.plot_parameters[index]
            self.labelFitParameters.setText(
                f"Psill: {params['psill']:.4f}\n"
                f"Range: {params['range']:.4f}\n"
                f"Nugget: {params['nugget']:.4f}"
            )
        else:
            self.labelFitParameters.setText("Select a plot to see parameters.")
            
    def setupVariogramWidgets(self):
        # Widgets and checkboxes in the variogram parameter group box
        widget_names = ['estimator', 'model', 'bin_func', 'fit_sigma', 'normalize', 'use_nugget', 'fit_method']
        line_edit_names = ['maxlag', 'n_lags']

        self.widgets = {}
        self.checkboxes = {}

        for name in widget_names + line_edit_names:
            if name in widget_names:
                widget = self.groupBoxVariogramParameters.findChild(QtWidgets.QComboBox, name.lower() + 'combo')
            else:
                widget = self.groupBoxVariogramParameters.findChild(QtWidgets.QLineEdit, name.lower() + 'lineedit')

            checkbox = self.groupBoxVariogramParameters.findChild(QtWidgets.QCheckBox, 'chk' + name.lower())

            if widget and checkbox:
                self.widgets[name] = widget
                checkbox.stateChanged.connect(lambda state, w=widget: w.setEnabled(state == Qt.Checked))
                print(f"Connected {name} widget to checkbox.")
            else:
                print(f"Error: Could not find widget or checkbox for {name}")



        self.tabVariogramPlots = self.findChild(QtWidgets.QTabWidget, 'variogramplots')
        #self.scrollAreaSemivariance = self.findChild(QtWidgets.QScrollArea, 'semivariancescrollarea')
        #self.framefitParameters = self.findChild(QtWidgets.QFrame, 'fitparametersframe')
        
    

    def setupAndDisplayTable(self, df,tableWidget):
        # Clear the existing rows and columns
        tableWidget.clear()
        tableWidget.setRowCount(0)
        tableWidget.setColumnCount(0)

        
        # Set new row count, column count, and headers
        tableWidget.setRowCount(df.shape[0])
        tableWidget.setColumnCount(df.shape[1])
        tableWidget.setHorizontalHeaderLabels(df.columns.tolist())
        
        for index, row in df.iterrows():
            for col_index, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                tableWidget.setItem(index, col_index, item)


    def loadAndDisplayExcel(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Select Excel File", "", "Excel Files (*.xlsx);;All Files (*)")
        if filePath:
            self.df = pd.read_excel(filePath)
            self.setupAndDisplayTable(self.df, self.excelTableWidget)
            self.clean_df = self.prepare_data_for_processing(self.df.copy())  # Ensure this is where clean_df is set
            
    def tableWidgetToDataFrame(self, tableWidget):
        column_count = tableWidget.columnCount()
        row_count = tableWidget.rowCount()
        headers = [tableWidget.horizontalHeaderItem(i).text() for i in range(column_count)]
        df = pd.DataFrame(columns=headers, index=range(row_count))

        for row in range(row_count):
            for col in range(column_count):
                item = tableWidget.item(row, col)
                df.iloc[row, col] = item.text() if item else None

        return df

    def applyThresholdAndDisplay(self):
        if self.df is not None:
            # Update DataFrame from the table widget before processing
            current_df = self.tableWidgetToDataFrame(self.excelTableWidget)
            # Get column names based on their current order in the table
            lon_col = current_df.columns[0]  # First column for longitude
            lat_col = current_df.columns[1]  # Second column for latitude
            threshold_meters = float(self.lineEditThreshold.text())
            duplicates_df = self.detect_possible_duplicates_with_improved_sjoin(current_df, lon_col, lat_col, threshold_meters)
            self.unique_df = self.remove_possible_duplicates(current_df, duplicates_df)
            self.setupAndDisplayTable(self.unique_df, self.thresholdTableWidget)

    def detect_possible_duplicates_with_improved_sjoin(self,current_df, lon_col, lat_col, threshold_meters):
        gdf = gpd.GeoDataFrame(current_df, geometry=gpd.points_from_xy(current_df[lon_col],current_df[lat_col]), crs="EPSG:4326")
        gdf = gdf.to_crs(epsg=32633)
        duplicates = gpd.sjoin_nearest(gdf, gdf, how='left', max_distance=threshold_meters, distance_col='distance')
        duplicates = duplicates[duplicates.index != duplicates['index_right']]
        duplicates['Status'] = 'Unique'
        duplicates.loc[duplicates.index < duplicates['index_right'], 'Status'] = 'Duplicate'
        return duplicates

    def remove_possible_duplicates(self,current_df, duplicates_df):
        duplicate_indices = duplicates_df[duplicates_df['Status'] == 'Duplicate'].index
        self.unique_df = current_df.drop(index=duplicate_indices, errors='ignore').reset_index(drop=True)
        #print(self.unique_df)
        return self.unique_df
    
    def prepare_gdf_utm_from_result(self, unique_df, lon_col, lat_col, result_col):
        # Assuming df is already defined with columns 'lon', 'lat', and a 'result'
        gdf = gpd.GeoDataFrame(unique_df, geometry=gpd.points_from_xy(unique_df[lon_col], unique_df[lat_col]), crs="EPSG:4326")
        gdf_utm = gdf.to_crs(epsg=32633)
        return gdf_utm

    def initializeFitParametersLabel(self):
        if not self.labelFitParameters:
            self.labelFitParameters = QtWidgets.QLabel("No parameters available.")
            layout = QVBoxLayout(self.framefitparameters)
            layout.addWidget(self.labelFitParameters)
    
    
    def prepare_data_for_processing(self, df):
        # Convert data to numeric and handle NaNs or inappropriate data types
        for col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        df.dropna(inplace=True)
        return df
    
    def validate_and_prepare_data(self):
        if self.unique_df is None or self.unique_df.empty:
            QMessageBox.warning(self, "Data Error", "No data available to plot.")
            return False
    
        self.unique_df = self.prepare_data_for_processing(self.unique_df.copy())
        if self.unique_df.empty:
            QMessageBox.warning(self, "Data Error", "Data contains non-numeric values or all entries are NaN after conversion.")
            return False
    
        return True

    def plotVariogram(self):
        if not self.validate_and_prepare_data():
            return
       
        # Dynamically get column names based on their position
        lon_col = self.unique_df.columns[0]  # First column as longitude
        lat_col = self.unique_df.columns[1]  # Second column as latitude
        result_col = self.unique_df.columns[-1]  # Last column as result
        



        #Prepare the GeoDataFrame and get UTM coordinates
        gdf_utm = self.prepare_gdf_utm_from_result(self.clean_df, lon_col, lat_col, result_col)
        utm_coords = np.column_stack((gdf_utm.geometry.x, gdf_utm.geometry.y))
        hull = ConvexHull(utm_coords)
        self.hull_path = MplPath(utm_coords[hull.vertices])
        # Create the grid for interpolation
        lon_range = np.linspace(utm_coords[:, 0].min(), utm_coords[:, 0].max(), 100)
        lat_range = np.linspace(utm_coords[:, 1].min(), utm_coords[:, 1].max(), 100)
        self.xgrid, self.ygrid = np.meshgrid(lon_range, lat_range)
        grid_points = np.column_stack([self.xgrid.ravel(), self.ygrid.ravel()])

        # Extract the results from the unique GeoDataFrame
        values = gdf_utm[result_col].values
        
        params={'coordinates': utm_coords,
                'values': values
        }
        
         # Add optional parameters only if their respective checkboxes are checked
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
        # Check if manual method is selected and parameters are filled
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


        for key, (widget_name, cast_type) in optional_params.items():
            checkbox = self.findChild(QtWidgets.QCheckBox, 'chk' + key.lower())
            if checkbox:
                print(f"Checkbox {key} found: {checkbox.isChecked()}")
                if checkbox and checkbox.isChecked():
                    widget = self.findChild(QtWidgets.QWidget, widget_name)
                    if widget:
                        value = widget.text() if cast_type is int else widget.currentText()
                        params[key] = cast_type(value)
                        print(f"Added {key}: {params[key]}")  # Print each parameter added
                    else:
                        print(f"Widget {widget_name} not found")
                else:
                    print(f"Checkbox {key} is not checked")
            else:
                print(f"Checkbox for {key} not found")

        # Create and plot variogram
        print("Parameters for Variogram:", params)
        
        
        try:
            self.variogram = skg.Variogram(**params)
            self.displayVariogram(self.variogram)
        except Exception as e:
            QMessageBox.critical(self, "Variogram Error", str(e))
            return
   
   # self.plot_parameters = []
    
    def displayVariogram(self, variogram,show_in_spyder=False):
        # Create a matplotlib figure
        fig = Figure(figsize=(10,6))
        ax = fig.add_subplot(111)
        
        pair_counts = variogram.bin_count
        lags = variogram.bins
        experimental_variogram = variogram.experimental
        
        # Create DataFrame from variogram data
        dem = pd.DataFrame({
        "np": variogram.bin_count,
        "lags": variogram.bins,
        "semivariance": variogram.experimental
        })
        

        # Plot the theoretical variogram model
        max_lag = max(variogram.bins) * 1.2
        lag_range = np.linspace(0, max_lag, 100)
        theoretical_variogram = variogram.model(lag_range, *variogram.parameters)
        ax.plot(lag_range, theoretical_variogram, color='red', label='Theoretical', linewidth=2)
        ax.scatter(lags, experimental_variogram, color='blue', label='Experimental')
 
        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        ax.set_xlabel('Distance')
        ax.set_ylabel('Semivariance')
        ax.set_title('Variogram with Fit')
        ax.legend()
        ax.grid(False)
        
        fig.tight_layout()
        # Store parameters
        self.plot_parameters.append({
            "nugget": variogram.parameters[-1] if variogram.use_nugget else 0,
            "psill": variogram.parameters[1] if variogram.use_nugget else variogram.parameters[0],
            "range": variogram.parameters[0]
        })
        
        # If you want to see the plot in Spyder or any other interactive environment that supports it
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

        # Create a canvas to embed the figure
        canvas = FigureCanvas(fig)
    
        # Create a navigation toolbar for the canvas
        toolbar = NavigationToolbar(canvas, self)
    
        # Create a QWidget and set its layout to hold both the toolbar and canvas
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(toolbar)
        layout.addWidget(canvas)
        widget.setLayout(layout)
    
        # Add the widget to the tab
        tab_index = self.tabVariogramPlots.addTab(widget, f"Variogram Plot {self.tabVariogramPlots.count() + 1}")
        self.tabVariogramPlots.setCurrentIndex(tab_index)
    
        # Optionally show in Spyder or other environments
        if show_in_spyder:
            plt.show()

        # Additional functionality, such as displaying data in a scroll area or updating fit parameters
        self.displayTableInScrollArea(dem, self.scrollAreaSemivariance)
        self.updateFitParametersDisplay(tab_index)
        
        
        
    def toggleBasemapCombo(self, state):
        self.basemapCombo.setEnabled(state == Qt.Checked)
        
    def toggleUncertaintymapCombo(self, state):
        self.uncertaintymapCombo.setEnabled(state == Qt.Checked)

    def validateInputs(self):
        # Validate min_points and max_points to ensure they are non-zero and valid integers
        try:
            min_points = int(self.minPointsLineEdit.text())
            max_points = int(self.maxPointsLineEdit.text())
            levels = int(self.levelsLineEdit.text())
            alpha = float(self.alphaLineEdit.text())

            if min_points <= 0 or max_points <= 0 or levels < 1:
                QMessageBox.warning(self, "Input Error", "Min points, max points, and levels must be greater than zero.")
                return False
            
            if alpha < 0 or alpha > 1:
                QMessageBox.warning(self, "Input Error", "Alpha must be between 0 and 1.")
                return False
            
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numerical values.")
            return False
        
        return True

    def plotKriging(self):
        if not self.validateInputs():
            return
        if not hasattr(self, 'variogram') or self.variogram is None:
            QMessageBox.warning(self, "Variogram Error", "Please generate a valid variogram before kriging.")
            return
        
        # Extract and convert inputs
        min_points = int(self.minPointsLineEdit.text())
        max_points = int(self.maxPointsLineEdit.text())
        levels = int(self.levelsLineEdit.text())
        alpha = float(self.alphaLineEdit.text())

        # Perform Kriging using the OrdinaryKriging model from skgstat
        try:
            OK = skg.OrdinaryKriging(
                self.variogram,
                min_points=min_points,
                max_points=max_points
            )
            # Perform Kriging interpolation using `transform`
            zgrid = OK.transform(self.xgrid.ravel(), self.ygrid.ravel())

            # Reshape results back to the grid shape
            zgrid = zgrid.reshape(self.xgrid.shape)

            # Reshape the gridded data to match the meshgrid shape
            Z = zgrid.reshape(self.xgrid.shape)

            # Mask out the areas outside the convex hull
            mask = np.array([self.hull_path.contains_point((x, y)) for x, y in zip(self.xgrid.flatten(), self.ygrid.flatten())])
            mask = mask.reshape(self.xgrid.shape)
            Z_masked = np.where(mask, Z, np.nan)
            
 
        except Exception as e:
            QMessageBox.critical(self, "Kriging Error", str(e))
            return

        # Convert predictions back to original CRS
        gdf_pred = gpd.GeoDataFrame(geometry=gpd.points_from_xy(self.xgrid.ravel(), self.ygrid.ravel()), crs="EPSG:32633")
        gdf_pred = gdf_pred.to_crs("EPSG:4326")
        lon_pred, lat_pred = gdf_pred.geometry.x, gdf_pred.geometry.y

        # Reshape the geographic coordinates to match the grid shape
        lon_grid = lon_pred.values.reshape(self.xgrid.shape)
        lat_grid = lat_pred.values.reshape(self.ygrid.shape)

        # Create a new tab for the plot
        fig = Figure(figsize=(200,190))
        ax = fig.add_subplot(111)
        contourf = ax.contourf(lon_grid, lat_grid, Z_masked, levels=levels, alpha=alpha, cmap="rainbow")

        # Optionally add a basemap
        if self.chkBasemap.isChecked():
            # Dynamically get the selected basemap from the combo box
            selected_basemap = self.basemapCombo.currentText()

            # Mapping the readable names to ctx.providers attributes
            basemap_mapping = {
                "Esri.WorldImagery": ctx.providers.Esri.WorldImagery,
                "OpenStreetMap.Mapnik": ctx.providers.OpenStreetMap.Mapnik,
                "Esri.DeLorme": ctx.providers.Esri.DeLorme,
                "CartoDB.Positron": ctx.providers.CartoDB.Positron,
                "CartoDB.DarkMatter": ctx.providers.CartoDB.DarkMatter,
                "OpenTopoMap": ctx.providers.OpenTopoMap,
                 #  Add other mappings here
            }

            try:
                # Access the basemap using the mapping
                basemap_source = basemap_mapping[selected_basemap]
                print("Basemap Source:", basemap_source)  # Debugging output to confirm correct attribute access

                ctx.add_basemap(ax, crs="EPSG:4326", source=basemap_source)
            except KeyError as e:
                print("Failed to access the basemap:", e)  # If an error occurs, it will show which part failed
        
        if self.chkUncertaintymap.isChecked():
            selected_uncertaintymap=self.uncertaintymapCombo.currentText()
            
            # Get the kriging standard deviations
            sigma = OK.transform(self.xgrid.ravel(), self.ygrid.ravel())

            # Reshape the standard deviations to match the original grid shape
            sigma = OK.sigma.reshape(self.xgrid.shape)
 
            # Apply the mask to the standard deviations
            sigma_masked = np.where(mask, sigma, np.nan)

            relative_error = np.where(Z_masked != 0, Z_masked / sigma_masked * 100, np.nan)
   
            
            uncertaintymap_mapping = {
                  "viridis": "viridis_r",
                  "inferno": "inferno_r",
                      "jet": "jet_r",
                  "rainbow": "rainbow_r",
                   "plasma": "plasma_r",
                    "turbo": "turbo_r"
                       
            }
            
            try:
                uncertaintymap_source=uncertaintymap_mapping[selected_uncertaintymap]
                print("Uncertaintymap Source:", uncertaintymap_source)
                
                contourfo = ax.contourf(lon_grid, lat_grid, relative_error, cmap=uncertaintymap_source, levels=100, alpha=0.6)
                # Format axis to display longitude and latitude in plain numbers
                #ax.xaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))
               # ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))

                # Add a color bar to the plot to indicate the scale of the standard deviations
                #cbaro = plt.colorbar(contourfo, ax, label='Uncertainty (%)')
                #vmax = cbaro.vmax
               # vmin = cbaro.vmin
                #ticks = np.linspace(vmin, vmax, num=20)
               # cbaro.set_ticks(ticks)
               # cbaro.set_ticklabels(['{:.1f}'.format(tick) for tick in ticks[::-1]])
            except KeyError as e:
                print("Failed to access the uncertaintymap:", e)  # If an error occurs, it will show which part failed    
       
        # Setup toolbar and canvas
        canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar(canvas, self)
        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(canvas)
        widget.setLayout(layout)

        # Add the widget to the tab
        idx = self.krigePlots.addTab(widget, f"Krige Plot {self.krigePlots.count() + 1}")
        self.krigePlots.setCurrentIndex(idx)

        # Add color bar and labels
        colorbar = fig.colorbar(contourf, ax=ax, label='nGy/h', shrink=0.6) 
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title('Krige Plot')
        ax.xaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))
        ax.yaxis.set_major_formatter(mticker.ScalarFormatter(useOffset=False))

        canvas.draw()


    
    def format_value(self,value):
        """Format the value to show up to four decimal places, or as an integer if it is a whole number."""
        try:
            float_value = float(value)
            if float_value.is_integer():
                return f"{int(float_value)}"
            else:
                return f"{float_value:.4f}"
        except ValueError:
            return value
    
    def displayTableInScrollArea(self, df, scrollArea):
        tableWidget = QTableWidget()
        tableWidget.setRowCount(df.shape[0])
        tableWidget.setColumnCount(df.shape[1])
        tableWidget.setHorizontalHeaderLabels(df.columns.tolist())

        # Fill the table with data, formatting the values to four decimal places where necessary
        for index, row in df.iterrows():
            for col_index, value in enumerate(row):
                formatted_value = self.format_value(value)
                item = QTableWidgetItem(formatted_value)
                item.setTextAlignment(Qt.AlignCenter)
                tableWidget.setItem(index, col_index, item)

        # Manage scroll area contents
        scrollAreaWidgetContents = scrollArea.widget()
        if scrollAreaWidgetContents is None:
            scrollAreaWidgetContents = QtWidgets.QWidget()
            scrollArea.setWidget(scrollAreaWidgetContents)
            layout = QVBoxLayout(scrollAreaWidgetContents)
            scrollAreaWidgetContents.setLayout(layout)
        else:
            layout = scrollAreaWidgetContents.layout()
            if layout is None:
                layout = QVBoxLayout(scrollAreaWidgetContents)
                scrollAreaWidgetContents.setLayout(layout)

        # Clear existing widgets in the layout
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        layout.addWidget(tableWidget)
        

    def prepare_plot_data(self):
        if self.unique_df is None or self.unique_df.empty:
            QMessageBox.warning(self, "Data Error", "No data available for processing.")
            return None

        processed_data = self.unique_df.copy()
        for i in range(processed_data.shape[1]):
            processed_data.iloc[:, i] = pd.to_numeric(processed_data.iloc[:, i], errors='coerce')
        processed_data.dropna(inplace=True)
        
        if processed_data.empty:
            QMessageBox.warning(self, "Data Error", "No valid data available after processing.")
            return None
        return processed_data

    def plotRawHistogram(self):
        fraction_input = self.lineEditRawHistogram.text()
        processed_data = self.prepare_plot_data()
        if processed_data is None:
            return

        try:
            fraction = float(fraction_input) if fraction_input else 0
            data = processed_data.sample(frac=fraction) if fraction > 0 else processed_data
            base_title = "Subset Histogram" if fraction > 0 else "Raw Histogram"
            title = f"{base_title} {self.getNextTabIndex(base_title)}"
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Invalid fraction value.")
            return

        fig = Figure()
        ax = fig.add_subplot(111)
        sns.histplot(data.iloc[:, -1], kde=False, bins=30, ax=ax)
        ax.set_title(title)
        ax.set_xlabel('Values')
        ax.set_ylabel('Frequency')
        self.addPlotToTab(fig, title)

    def plotScatterPlot(self):
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

        fig = Figure()
        ax = fig.add_subplot(111)
        scatter = ax.scatter(data.iloc[:, 0], data.iloc[:, 1], c=data.iloc[:, 2])
        cbar = fig.colorbar(scatter, ax=ax)
        cbar.set_label('Values')
        ax.set_title(title)

        self.addPlotToTab(fig, title)

    def plotPairPlot(self):
        processed_data = self.prepare_plot_data()
        if processed_data is None:
            return

        sns.pairplot(processed_data)
        title = f"Pair Plot {self.getNextTabIndex('Pair Plot')}"
        self.addPlotToTab(plt.gcf(), title)

    def addPlotToTab(self, fig, title):
        canvas = FigureCanvasQTAgg(fig)
        toolbar = NavigationToolbar2QT(canvas, self)
        widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(widget)
        layout.addWidget(toolbar)
        layout.addWidget(canvas)
        widget.setLayout(layout)
        idx = self.plotTabWidget.addTab(widget, title)
        self.plotTabWidget.setCurrentIndex(idx)

    def getNextTabIndex(self, baseTitle):
        count = 0
        existing_titles = [self.plotTabWidget.tabText(i) for i in range(self.plotTabWidget.count())]
        while f"{baseTitle} {count}" in existing_titles:
            count += 1
        return count
def apply_white_theme(app):
    # Set the Fusion style
    app.setStyle('Fusion')

    # Create a new palette for a clean, modern look
    palette = QtGui.QPalette()

    # Set the palette colors
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor(255, 255, 255))  # White background for windows
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(0, 0, 0))  # Black text for readability
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor(255, 255, 255))  # White for base widget backgrounds, like text fields
    palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(245, 245, 245))  # Slightly off white for alternating backgrounds
    palette.setColor(QtGui.QPalette.Button, QtGui.QColor(255, 255, 255))  # White for buttons
    palette.setColor(QtGui.QPalette.ButtonText, QtGui.QColor(0, 0, 0))  # Black text on buttons
    palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(173, 216, 230))  # Light blue for highlights
    palette.setColor(QtGui.QPalette.HighlightedText, QtGui.QColor(0, 0, 0))  # Black text for highlighted items
    palette.setColor(QtGui.QPalette.ButtonText,QtGui.QColor(255,256,255))
    palette.setColor(QtGui.QPalette.HighlightedText,QtGui.QColor


        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    apply_white_theme(app)
    mainWindow = ExcelLoaderApp()
    mainWindow.show()
    sys.exit(app.exec_())




