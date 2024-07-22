## Overview
KrigMap-Pro is an geostatistical analysis tool designed to facilitate the modeling and visualisation of spatial data through variogram and Kriging techniques. This tool is specifically tailored for mapping radioactivity concentrations across geographical regions using UTM coordinates. It has a understandable graphical user interface, allowing users to adjust variogram and Kriging parameters dynamically without delving into code.

## Features
- **Variogram Modeling**: Configure and customize the variogram model parameters to fit the spatial structure of your data.
- **Kriging Estimation**: Perform Kriging to predict and interpolate unknown values based on the spatial correlation described by the variogram.
- **Interactive Maps**: View and interact with geographical data overlays on satellite maps.
- **Flexible Data Handling**: Easily import and manage your spatial data using an integrated GUI.
- **Plotting**: Generate and customize plots directly within the application to visualize data and analysis results.

## Getting Started

### Prerequisites
Before you can run KrigMap-Pro, ensure you have the following installed:
- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

### Installation Steps

1. **Download Required Files**:
   - Download the following files to a folder on your computer:
     - `main_window.py`
     - `select_multiple_files_window.py`
     - `main_window.ui`
     - `select_multiple_files_window.ui`

2. **Configure File Paths**:
   - Open `main_window.py` in a text editor.
     - Locate line 128 and modify the path to point to where you saved `main_window.ui`.
   - Open `select_multiple_files_window.py` in a text editor.
     - Locate line 41 and adjust the path to point to where you saved `select_multiple_files_window.ui`.

3. **Install Python Dependencies**:
   - Ensure you have Python and pip installed. You can download Python from [python.org](https://www.python.org/downloads/). Installing Python will also install pip.
   - Create a `requirements.txt` file in the same folder as your scripts and fill it with the necessary packages:
     ```
     numpy
     pandas
     geopandas
     matplotlib
     seaborn
     contextily
     scipy
     scikit-learn
     skgstat
     pyqt5
     ipywidgets
     ```
   - Open your command prompt (Windows) or terminal (macOS/Linux), navigate to the directory containing your project, and run:
     ```
     pip install -r requirements.txt
     ```
     Alternatively, if you use Conda, you may need to find the equivalent Conda packages and install them using `conda install`.

4. **Run the Application**:
   - With all dependencies installed and configurations set, run `main_window.py`:
     ```
     python main_window.py
     ```
   - This will launch the KrigMap-Pro interface. From here, you can follow the on-screen instructions and use the guide provided within the application to get started with your geostatistical analysis.

## Additional Tips

- **Troubleshooting**: If you encounter issues with package installations, ensure your pip or Conda is up to date. For pip, you can upgrade with `pip install --upgrade pip`.
- **Documentation**: For detailed usage of each feature, refer to the guide.md

This setup should provide you with a fully functional environment for doing geostatistical analyses using KrigMap-Pro. Enjoy mapping and analysing your spatial data! :)
