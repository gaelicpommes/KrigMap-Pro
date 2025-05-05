

## (Optional) Run KrigMapPro Without Creating an `.exe` File

If you don’t want to build the executable, you can run KrigMapPro directly from the Python source code.


1. **Download the following files** into a folder or directory of your choice:
   - `krigmap_pro.py`
   - `krigmap_pro_selectfiles.py`
   - `krigmap_pro_ui_files.zip`
   - `example_data.zip`
   - `requirement.txt`

2. **Unzip** both `krigmap_pro_ui_files.zip` and `example_data.zip` in the same folder.

3. **Edit UI file paths in the code**:
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

4. **Install required Python packages**:
   - Open a terminal or Anaconda Prompt in the project folder.
   - Run:
     ```bash
     pip install -r requirement.txt
     ```

5. **Run the application**:
   - Open `krigmap_pro.py` in your Python editor.
   - Click **Run**.
   - The GUI for KrigMapPro will appear, and you're good to go!

---

That’s it! You can now explore KrigMapPro without creating an executable.



