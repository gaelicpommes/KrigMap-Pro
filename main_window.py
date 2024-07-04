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
