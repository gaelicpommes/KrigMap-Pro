## Overview
KrigMap Pro is an geostatistical analysis tool designed to facilitate the modeling and visualisation of spatial data through variogram and Kriging techniques. This tool is specifically tailored for mapping radioactivity concentrations across geographical regions using UTM coordinates. It has a understandable graphical user interface, allowing users to adjust variogram and Kriging parameters dynamically without delving into code.

## Features
- **Variogram Modeling**: Configure and customize the variogram model parameters to fit the spatial structure of your data.
- **Kriging Estimation**: Perform Kriging to predict and interpolate unknown values based on the spatial correlation described by the variogram.
- **Interactive Maps**: View and interact with geographical data overlays on satellite maps.
- **Flexible Data Handling**: Easily import and manage your spatial data using an integrated GUI.
- **Plotting**: Generate and customize plots directly within the application to visualize data and analysis results.

## Getting Started

### Prerequisites
Before you can run KrigMap Pro, ensure you have the following installed:
- Python 3.8 or higher
- Dependencies listed in `requirements.txt`

### Installation
Clone the repository to your local machine:
```bash
git clone https://github.com/yourusername/krigmap-pro.git

Running the Application
To start the application, navigate to the project directory and run:
python main.py
Replace main.py with the path to your main Python script if different.

Usage
Data Loading: Use the file dialog to select and load your data files.
Setting Parameters: Adjust variogram and Kriging parameters using the provided interfaces.
Visualization: Access various plotting tools to visualize data, variograms, and Kriging results.
Contributing
Contributions to KrigMap Pro are welcome. Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests to us.

License
This project is licensed under the MIT License - see the LICENSE.md file for details.
