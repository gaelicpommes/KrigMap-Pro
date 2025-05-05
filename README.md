

## Overview
KrigMapPro is an geostatistical analysis tool designed to do the modeling and visualisation of spatial data through Kriging. This tool is for mapping radioactivity concentrations across geographical regions using UTM coordinates. It has an easy-to-use graphical user interface, which allows you to adjust variogram and Kriging parameters dynamically without delving deeply into code.

## Features
- **Variogram Modeling**: Configure and customise the variogram model parameters to fit the spatial structure of your data.
- **Kriging Estimation**: Perform Kriging to predict and interpolate unknown values based on the spatial correlation described by the variogram.
- **Interactive Maps**: View the Krige plot on top of satellite maps.
- **Flexible Data Handling**: Easily import and manage your spatial data using the GUI.
- **Plotting**: Generate and customise plots directly within the application to visualise data and analysis results.

# Getting Started with KrigMapPro
- Download the KrigMapPro.exe at this Google Drive link (https://drive.google.com/file/d/1SA7lob7Ze1RGNh5xXkaAQ8VlvlmsQwzX/view?usp=drive_link)
- Unzip the .zip file and run the .exe file. You may get a Windows Defender popup saying the .exe file is not safe. Ignore this and run the .exe.
- You will see this terminal and splash image when starting the .exe:
- ![image](https://github.com/user-attachments/assets/af96c652-592a-4844-84d9-dc45fe187db8)
- After 3-5 minutes you'll get to see the KrigMapPro interface:
- ![image](https://github.com/user-attachments/assets/5ee64f48-4bce-447a-a5fa-61355bc7344c)
-Remember to press the square at the top right corner, to see the scrollbars and see the whole interface.
![image](https://github.com/user-attachments/assets/2c25fba2-9d1e-47cc-913f-3bce6d267e3c)

- Read the KrigMapPro Guide.docx (or be a wildcard and not read it :)) 
- Happy Kriging!


## (Optional) Compile the KrigMapPro `.exe` File Yourself

If you'd like to build the KrigMapPro application yourself, here’s how to do it:

### Instructions

1. **Switch to the `compile-app` branch** of this repository.
   - ![image](https://github.com/user-attachments/assets/3bdeee22-d634-42b1-8812-6d483bc391ab)


3. In that branch, you'll find the following files:
   - `krig1.py`, `krig2.py`
   - `krigappicon.ico`, `krigsplash.jpg`
   - `KrigMapPro.spec`
   - `krigmap_pro.ui`, `krigmap_pro_selectfiles.ui`

4. **Install Anaconda** (if you don’t already have it):
   - Download: [https://www.anaconda.com/download/success](https://www.anaconda.com/download/success)
   - Anaconda is recommended because it comes with many of the required libraries used in this application.

5. **Download all files into a  folder** on your computer.
   - In my case I downloaded the files into the folder "testkrig" -  C:/Users/irish/Downloads/testkrig

7. **Open Anaconda Prompt in that folder**:
   - open *Anaconda Prompt* and navigate (`cd`) to the folder.
   - ![image](https://github.com/user-attachments/assets/68567d10-424e-4853-aa25-a9ffbc5ffe93)
   - ![image](https://github.com/user-attachments/assets/974a10e9-9e45-4336-b5f9-3384f9a655aa)


8. **Install PyInstaller** (if not installed already):
   ```bash
   pip install pyinstaller
   ```
   - ![image](https://github.com/user-attachments/assets/37d34e35-ba5f-4440-b13c-12b5c52941d6)


9. **Edit the `pyinstaller.txt` file**:
   - Update all file paths (e.g., for `krigappicon.ico`, `krigsplash.jpg`, `krigmap_pro.ui`,`krigmap_pro_selectfiles.ui`, `anaconda3`) to match your system's file structure.
   - For example:
     - Change:
       ```
       C:/Users/irish/Downloads/testkrig/krigappicon.ico
       ```
       to:
       ```
       C:/Users/yourname/YourFolder/krigappicon.ico
       ```
     - And similarly for the Anaconda path:
       ```
       C:/Users/irish/anaconda3/...
       ```
       should become:
       ```
       C:/Users/yourname/anaconda3/...
       ```

10. **Run PyInstaller with the `.spec` file**:
   ```bash
   pyinstaller --clean KrigMapPro.spec
   ```
-![image](https://github.com/user-attachments/assets/d64640ca-5f66-475e-a3c4-361048345bea)


11. **Wait for the build to complete**:
   - This may take several minutes depending on your system.
   - You’ll see messages indicating that PyInstaller is analyzing dependencies and packaging your app.

11. **Locate your application**:
    - After the build completes, go to the `dist/` folder inside your project directory.
    - You will find:
      ```
      KrigMapPro.exe
      ```
    - Double-click it to launch your compiled application.

---

You’re all set! 









## (Optional) Run KrigMapPro Without Creating an `.exe` File

If you don’t want to build the executable, you can run KrigMapPro directly from the Python source code.
### Instructions

1. **Switch to the `python-files` branch** of this repository.
   - ![image](https://github.com/user-attachments/assets/29f54117-b963-46ad-8e63-1c1dd10f0324)



2. **Download the following files** into a folder or directory of your choice:
   - `krigmap_pro.py`
   - `krigmap_pro_selectfiles.py`
   - `krigmap_pro_ui_files.zip`
   - `example_data.zip`
   - `requirement.txt`

3. **Unzip** both `krigmap_pro_ui_files.zip` and `example_data.zip` in the same folder.

4. **Edit UI file paths in the code**:
   - Open `krigmap_pro.py` in your Python editor (I personally use Spyder).
   - Go to **line 217**, and replace:
     ```python
     uic.loadUi("D:/krigmap_pro.ui", self)
     ```
     with the path to where your own `krigmap_pro.ui` file is located (after unzipping).

   - Then open `krigmap_pro_selectfiles.py`.
   - Go to **line 240**, and replace:
     ```python
     uic.loadUi("D:/krigmap_pro_selectfiles.ui", self)
     ```
     with the correct path to your unzipped `krigmap_pro_selectfiles.ui` file.

5. **Install required Python packages**:
   - Open a terminal or Anaconda Prompt in the project folder.
   - Run:
     ```bash
     pip install -r requirement.txt
     ```

6. **Run the application**:
   - Open `krigmap_pro.py` in your Python editor.
   - Click **Run**.
   - The GUI for KrigMapPro will appear, and you're good to go!

---

That’s it! You can now explore KrigMapPro without creating an executable.

