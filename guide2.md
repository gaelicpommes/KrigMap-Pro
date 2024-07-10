# QT Application User Guide

Welcome to the user guide for this kiriging, designed to assist first-time users in navigating through the main window and its various widgets.

## Getting Started

Before diving into the specifics, here's a general overview of the main window.

### Main Window Overview

![image](https://github.com/gaelicpommes/krige_python/assets/172756556/4f1a798d-f035-4515-8e38-b38634d69c78)



*Figure 1: The Main Window of the Application*

The main window is structured with several interactive widgets which we will explore in this guide.

## Detailed Walkthrough

### 1. Select Excel/CSV File(s)

This widget is your starting point for importing data files into the application. It offers two main functionalities described below.

#### Open One File

- **Button**: Open One File
- **Description**: Click this button to open a standard file selection dialog.
- **Supported File Types**: `.xlsx`, `.xls`, `.csv`
- **How It Works**: Upon selecting a file, its contents will automatically populate in a scroll area below the button. Note that the file must contain exactly three columns.

![Single File Selection](path_to_single_file_selection_image.jpg)

*Figure 2: Single File Selection Interface*

#### Open Multiple Files

- **Button**: Open Multiple Files
- **Description**: This button opens the Multiple File Selection Window.

![Button to Open Multiple Files](path_to_open_multiple_files_button_image.jpg)

*Figure 3: Button for Opening Multiple Files*

## Multiple File Selection Window

This window enhances your capability to select and process multiple files simultaneously.

### Left Widget: File Tree View

- **Functionality**: Displays loaded files in a tree view format, listing file names alongside their respective column names.
- **Interaction**: Click the "Select Files(s)" button to choose multiple files as needed.

![File Tree View](path_to_file_tree_view_image.jpg)

*Figure 4: Tree View of Files*

### Right Widget: File Preview and Column Selection

- **Overview**: Shows the file content with a detailed table view below the file name.
- **Dropdown Boxes**: `lon_col`, `lat_col`, `result_col`
  - **Purpose**: Populate these boxes with the column names from your files. You'll need to select the appropriate columns for longitude, latitude, and results from here.
  - **Highlighting**: Selected columns will be highlighted in the table with distinct colors to indicate your choices.

![Column Selection](path_to_column_selection_image.jpg)

*Figure 5: Column Selection in File Preview*

### Confirm Selection

- **Button**: Confirm Selection
- **Action**: Confirm your file and column choices by pressing this button.
- **Result**: A new window will display, summarizing your selections and previewing the data from the `lon`, `lat`, and `result` columns.

## Confirmation and Final Display

### Data Confirmation Window

- **Details**: This window lists all chosen files and the count of data rows per file, excluding header rows. It also shows a preview table of the `lon`, `lat`, and `result` data columns.

![Data Confirmation Window](path_to_data_confirmation_window_image.jpg)

*Figure 6: Data Confirmation Window*

- **Final Confirmation**: Click the "Confirm" button to finalize your selections.

### Displaying the Data

- **Location**: The final selected data will be displayed in the scroll area of the main window.

![Final Data Display](path_to_final_data_display_image.jpg)

*Figure 7: Final Display of Selected Data in Main Window*

## Managing and Utilizing Data

After successfully importing and confirming your data in the previous steps, the application now displays the data in three primary columns: Longitude, Latitude, and Result. These columns can be re-arranged as desired, but ensure that their order (Longitude, Latitude, Result) corresponds to the sequence (1, 2, 3) for the application to function correctly.

### 2. Enter Threshold Value

This widget is used to filter or 'clean' your data based on a specific threshold value.

#### How to Use:

- **Input**: Enter the desired threshold value in the provided input field.
- **Button**: Press the "Confirm" button after entering the value.
- **Outcome**: The application will display a 'cleaned' version of the longitude, latitude, and result columns in the table below, which will have fewer rows than the original, depending on your threshold setting.

![Threshold Widget](path_to_threshold_widget_image.jpg)

*Figure 8: Entering and Confirming a Threshold Value*

### 3. Variogram Parameters

This widget allows for the customization of variogram parameters, crucial for geostatistical analysis.

#### Available Options and Functionalities:

- **Checkboxes and Dropdown Menus**: Each checkbox represents a variogram parameter with a default value that can be adjusted via dropdown menus.
- **Manual Entry**: If 'Manual' is selected in the 'fit_method' checkbox, you can input custom parameters (psill, range, and nugget) to tailor the fit of the theoretical variogram.

![Variogram Parameters](path_to_variogram_parameters_image.jpg)

*Figure 9: Variogram Parameters Selection*

#### Plotting the Variogram

- **Button**: Click "Plot Variogram" to generate and display the variogram plot.
- **Tabs**: The plot appears in a new tab within the widget, allowing for easy navigation between current and past variogram plots.
- **Interactivity**: You can zoom in, change the display settings, and save the variogram plot as needed.
- **Displayed Information**: Above the tabs, the fit parameters (psill, range, nugget) are displayed for reference.

![Variogram Plot](path_to_variogram_plot_image.jpg)

*Figure 10: Variogram Plot Display*

### 3. Semivariance Widget

Adjacent to the Variogram Parameters widget, the Semivariance Widget displays data related to the np lags and semivariance, which are associated with the variogram plot.

- **Purpose**: This widget provides a detailed view of the semivariance data used in the variogram calculations.
- **Functionality**: It enhances understanding of the spatial relationships and variabilities present in your data.

![Semivariance Widget](path_to_semivariance_widget_image.jpg)

*Figure 11: Semivariance Data Display*

## Advanced Data Analysis and Visualization

After setting up data and variogram parameters, the application offers advanced geostatistical tools like Kriging and various data visualization options.

### 4. Krige Parameters

This widget is designed to configure the settings for generating Kriging plots, which are crucial for spatial interpolation and creating heat maps.

#### Configuration Options:

- **Min Points**: Minimum number of points required for Kriging. Must be greater than 0; otherwise, an error will occur.
- **Max Points**: Optimally set to 100 to balance detail and processing time. Increasing this number may slow down the generation of the Krige plot.
- **Levels**: Defines the number of heat levels in the Kriging plot. A default of 30 levels is recommended but can be adjusted as needed to enhance the distinction in heat levels.
- **Alpha**: Controls the opacity of the Krige plot, with values ranging from 0 (completely transparent) to 1 (completely opaque).
- **Basemap Checkbox**: When enabled, a satellite image will serve as the base layer beneath the Krige plot, enhancing the contextual understanding of the data.
- **Uncertainty Map Checkbox**: If checked, alongside the Krige plot, an uncertainty map will be generated in a separate tab, providing insights into the confidence of the interpolated values.

![Krige Parameters](path_to_krige_parameters_image.jpg)

*Figure 12: Krige Parameters Widget*

### 5. Plots Widget

This widget provides tools for visualizing the original data loaded through the "1. Select Excel/CSV File(s)" widget. It offers different types of plots to understand data distribution and relationships.

#### Available Plots:

- **Raw Histogram**: Displays a histogram of the raw data. Below this button, there's an entry box to specify the fraction of data to display, which helps in examining different subsets of the data.
- **Scatterplot**: Generates a scatterplot to visualize the relationships between different data columns. Similar to the histogram, an entry box allows for specifying the fraction of data to be plotted.
- **Pairplot**: Offers a comprehensive view by plotting pairwise relationships across all data dimensions.

![Plots Widget](path_to_plots_widget_image.jpg)

*Figure 13: Data Visualization Options in the Plots Widget*

## Conclusion

By utilizing these advanced settings and visualization tools, you can perform detailed spatial analysis and better understand the distribution and relationships within your data. These functionalities are designed to support both novice and experienced users in making informed decisions based on spatial data analysis.


## Conclusion

Thank you for using our application. Should you have any questions then log in a bug report :3 

