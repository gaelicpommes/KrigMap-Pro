so make the open one file can open all three file types,
when i press cancel then nothing is laoded
make selected multiple files three columns be opened in the excelscrollarea

So the very first step is you open the main_window.py, and then you see this (see Figure 1), you can see this main window is called Krige Application,and there are widgets in this window. So all the widgets can be seen by using the scrollbars in the right hand side of window, bottom of window(see Figure 1).

Now look at the widget called 1.Select File (Figure 2), there are two buttons Open One File and Open Multiple Files, so when Open One File is pressed, then you"ll get the file directory of all the files. So this tool only loads .xlsx, .xls, .csv, files, so when you press Open to pick your one file, the file will load inside the widget(Figure 2), and this file will only load if there are three columns. If there are more than three columns in the file, then a new window will pop up(Figure 3). This window will ask you which of the columns you choose as your Longitude, Latitude, Result, so from the left to right, its the 1st, 2nd, 3rd column. So once you selected and then press 'OK'. And then the columns are loaded in the widget.

Now if you press the Open Multiple Files button, then a new window called Select Files will open (Figure 4). So pressing the button 'Select Files', the files directory will open again, then you can pick as much files as you want, then press Open, then your files will be loaded into the Treeview widget and the Table widget (Figure 4). So what happens is that in the Treeview you can see the File names listed in when they're loaded. Then you'll see the drop down rows, it's the column names present in that file. And in the Table widget, you'll see your files loaded. So there are coloured combo boxes called Longitude, Latitude, Result, so when you press one, you'll see the column names from all the files, and you can pick which column name you want for your Longitude, Latitude and Result. You can see your selection as coloured highlights in Treeview and Table widget. Then when you're happy you then go press the Confirm Selection, and whhen you press it, you see a window called Selected Data (Figure 5). You see then the files that were used based on your column name selection. you will also then see the three columns which contains all the row data from the files, so once you're happy, then press the Confirm button. When you do the these columns will then be loaded in the 1.Select File widget. Then you are the same end result as just like Open One File.

Then the next widget(Figure 6) is 2.Enter Threshold Value, so essentially this is like the background how it works (So our data consists of longitude and latitude points. And these points are in WGS 84 coordinate system, which is good for global referencing because the coordinates are given in angular measurements (degrees). But what we want is to measure the distances between points in a more easier way, so the points are converted from degrees units to metres units. So the points go from WGS 84 to UTM coordinate system.

● So each location (longitude and latitude pair) in th excel sheet (DataFrame) is converted into a point object. These points are then used to create a GeoDataFrame, which is a type of DataFrame that understands geographic operations. Essentially, we have these locations in the excel sheet, and we're telling the code that these locations are in WGS 84 coordinate system, so the code can work with it.

● So now, we have this spatial join operation 'gpd.sjoin_nearest'. So this matches each point with its nearest neighbour based on the UTM coordinates. This process is the same to drawing a circle with a specified radius(in our case, the threshold is 0.04 metres) around each point and seeing which other points from the dataset fall within that circle. The function calculates the straight-line distance (Euclidean distance) between points. If this distance is less than or equal to the specified threshold, the points are considered "near" each other.

● Now when the nearest points are identified, the function reviews these pairings to see if the threshold is met. If the threshold is met, it marks these points as potential duplicates. And to avoid marking a point as its own duplicate (self-join), the function excludes pairs where a point is matched with itself.

● Essentially each point was marked as unique, and as the function checks each pair of nearby points, it marks points as 'possible duplicate' if they are closer than your defined threshold distance and not already marked.)
So when you press the Confirm Threshold button, you'll get a dataset which should have lesser rows than original dataset. You can also save this filtered dataset by pressing Save Threshold Data button.

Now the next widgets are the 3.Variogram Parameters(Figure 7) and when the Plot Variogram button is pressed then youll get the variogram fit or plot in a tab called Variogram Plot (whatever number), you'll see the Fit Parameters and the Variogram Parameters you use too in the mini windows beside the tab containing the plot. So I recommend that the fit_sigma be unticked so that there's no weights in the lag or distance. But its all on your preference, you will change the parameters depending on what you thing is a good fit to the data. Now if you select the fit_method manual(Figure 8), then you can input your own Fit parameters of psill, range,nugget, and then when you press the Plot Variogram button you get your fit.

Then you'll see the 3.Semivariance widget (Figure 9), which you see the np, lags, semivariance associated with the variogram fit. Then the button Save Semivariance Data if you press it then you can save this data.

So then you have the next widget 4.Krige Plot and 4.Krige Parameters, so in 4.Krige Parameters, this is where theres the set parameters, and theres the optional Basemap and Uncertainty Map checkboxes. So if you tick Basemap, then the satellite map of your choosing will appear below the Krige plot(Figure 10). Then if the Uncertainty Map checkbox is ticked, then then the uncertainty map plot will appear in a different plot but with the same number as the associated krige plot so if its krige plot 3 then it uncertainty map 3(Figure 11). 

Now the final widget is the 5.Plots ,which contains a button container 5.Plot Types and the area where the plots will load(Figure 12). So for the buttons Raw Histogram and Scatterplot, theres boxes to add in numbers, these numbers should be decimals, so you can see a fraction of the data(Figure 12),if you put no number then you just see the cleaned dataset(Figure 13). 

So for all the tabs there's this toolbar(Figure 14). So you can pan through the plot, zoom in and out the plot, you can change the width and height of the plot.then in Figure options, you can change the title, the axes titles, the axes min and max, the plots style. And you can save your plot in whatever place in your file.






