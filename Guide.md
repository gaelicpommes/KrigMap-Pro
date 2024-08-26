# Application Overview

## Introduction

Welcome to our geostatistical analysis application! Designed with user experience in focus, this tool integrates the robust PyQt5 framework to offer an intuitive environment for managing and analyzing spatial data. Here's a quick guide on how to get started and make the most of the application's features.

## Getting Started

### Initial Setup

Upon launching the application, you are presented with a main window organized into five primary sections, each dedicated to a specific part of the analysis process:

- **Select File**
- **Enter Threshold Value**
- **Variogram**
- **Krige Plot**
- **Plots**

### User Interface Layout

The main window, 'KrigeMapPro', displays five primary widgets. Here is the layout:

![KrigeMapPro Interface](images/fig1.png)

*Figure 3: KrigeMapPro Interface*

### Select File

- **Purpose**: Load your spatial data files (.xlsx, .xls, or .csv).
- **Functionality**:
  - **Single or Multiple File Selection**: Choose to load one or multiple files to suit your data size and needs.
  - **Flexible Data Handling**: Supports various formats with geographic coordinates and results in WGS84 format.

![Select File Widget](images/fig2a.png)

*Figure 4 (Left): Select File widget without any file loaded*

![Loaded File Display](images/fig2b.png)

*Figure 4 (Right): Select File widget with a sample .xlsx file loaded*

### Enter Threshold Value

- **Purpose**: Refine your data by setting a threshold to filter out closely spaced data points, which enhances the quality of analysis.
- **How to Use**:
  - Input a numerical value in meters to set the minimum distance between data points.
  - Adjust the threshold to see the impact on data quality and quantity directly in the interface.

![Threshold Adjustment](images/fig6a.png)

*Figure 7 (Left): Sample data after applying a 0.01m threshold*

![Data Reduction](images/fig6b.png)

*Figure 7 (Right): Sample data after a 0.4m threshold*

### Variogram

- **Purpose**: Analyze spatial correlations through semivariograms.
- **Features**:
  - **Variogram Parameters**: Customize your analysis by selecting the model type, estimator function, and other relevant parameters.
  - **Interactive Semivariogram Plot**: View and modify semivariograms based on your data and parameters.

![Semivariogram Plot](images/fig7.png)

*Figure 8: Illustration of the 3.Variogram widget with a semivariogram created from sample threshold data*

### Krige Plot

- **Purpose**: Perform spatial interpolation to predict phenomena across geographic areas.
- **Capabilities**:
  - **Adjustable Kriging Parameters**: Set the number of points and transparency to tailor the analysis.
  - **Satellite Imagery Overlay**: Enhance geographical context by overlaying maps on the Krige plot.

![Krige Plot](images/fig9b.png)

*Figure 10: Krige Plot widget demonstrating a sample semivariogram*

### Plots

- **Purpose**: Explore your data further with additional plotting options.
- **Options**:
  - **Histograms and Scatter Plots**: Visualize data distribution and relationships.
  - **Pair Plots**: Examine pairwise relationships within your dataset.

![Histogram Example](images/fig10.png)
*Figure 11 (Left): Raw Histogram created from sample threshold data*

![Scatter Plot on Map](images/fig11.png)
*Figure 11 (Right): Illustration of a scatterplot overlaid with Esri.World Imagery map*

## Conclusion

This guide should help you navigate through the application smoothly and make effective use of the geostatistical tools provided. Load your data, set your parameters, and start analyzing spatial phenomena with precision and ease.





