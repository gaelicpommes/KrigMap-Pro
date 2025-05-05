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


9. **Edit the `KrigMapPro.spec` file**:
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
     - ![image](https://github.com/user-attachments/assets/0246afa5-f9c3-4496-8eae-97ee0298e5cd)
     - ![image](https://github.com/user-attachments/assets/3745f821-13ae-4b4e-97af-726699e05813)
     - 


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
