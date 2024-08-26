

## Overview
KrigMap-Pro is an geostatistical analysis tool designed to facilitate the modeling and visualisation of spatial data through variogram and Kriging techniques. This tool is specifically tailored for mapping radioactivity concentrations across geographical regions using UTM coordinates. It has a understandable graphical user interface, allowing users to adjust variogram and Kriging parameters dynamically without delving into code.

## Features
- **Variogram Modeling**: Configure and customise the variogram model parameters to fit the spatial structure of your data.
- **Kriging Estimation**: Perform Kriging to predict and interpolate unknown values based on the spatial correlation described by the variogram.
- **Interactive Maps**: View the Krige plot on top of satellite maps.
- **Flexible Data Handling**: Easily import and manage your spatial data using the GUI.
- **Plotting**: Generate and customise plots directly within the application to visualise data and analysis results.

# Getting Started with KrigMapPro

## Prerequisites
Before starting, ensure you have Python 3.8 or higher installed on your system. Make sure pip or pip3 is installed in your system too.

## Installation Steps

### 1. Download the Application Files
Download and save the following files to a single directory on your computer:
- `krigmap_pro.py`
- `krigmap_pro_selectfiles.py`
- `krigmap_pro_ui_files.zip`
- `example_data.zip`

### 2. Prepare the Environment
- **Unzip Files**: Extract the contents of `krigmap_pro_ui_files.zip` and `example_data.zip` into the same directory as the downloaded Python scripts.
- **IDE/Code Editor**: Ensure you have an IDE or a code editor like Spyder, Visual Studio Code, or any compatible software that can open Python files.

### 3. Configure Paths
- **Set UI File Paths**:
  - Open `krigmap_pro.py` with your IDE/code editor.
    - Modify line 216 to update the path: `uic.loadUi("path_to_your_ui_folder/krigmap_pro.ui", self)`
  - Open `krigmap_pro_selectfiles.py`.
    - Adjust line 239 similarly: `uic.loadUi("path_to_your_ui_folder/krigmap_pro_selectfiles.ui", self)`

### 4. Install Dependencies
- **Open your terminal or command prompt and navigate to the project directory**:
  - cd path_to_krigmap_pro
- **Run the following command to install all required Python packages**:
  - pip install PyQt5 PyQtWebEngine pandas geopandas shapely pyproj scipy scikit-learn scikit-gstat matplotlib seaborn contextily folium ipywidgets plotly geopandas pykrige rasterio numpy

### 5. Run the Application
- Open krigmap_pro.py in your IDE or code editor.
- Execute the script or press the "Run" button in your IDE to launch KrigMap-Pro.
- Once the application is running, you can start loading and analysyour spatial data using the provided interface.

## Additional Tips

- **Troubleshooting**: If you encounter issues with package installations, ensure your pip or Conda is up to date. For pip, you can upgrade with `pip install --upgrade pip`.
- **Documentation**: For detailed usage of each feature, refer to the Guide.md

This setup should provide you with a fully functional environment for doing geostatistical analyses using KrigMap-Pro. Enjoy mapping and analysing your spatial data! :)


