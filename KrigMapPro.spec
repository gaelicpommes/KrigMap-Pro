# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['krig1.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/irish/Downloads/testkrig/krigmap_pro.ui', '.'), ('C:/Users/irish/Downloads/testkrig/krigmap_pro_selectfiles.ui', '.'), ('C:/Users/irish/anaconda3/Lib/site-packages/pyproj/proj_dir/share/proj/proj.db', '.'), ('C:/Users/irish/anaconda3/Lib/site-packages/rasterio/gdal_data', '.')],
    hiddenimports=['gdal', 'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.QtWebEngineWidgets', 'PyQt5.QtWebEngineCore', 'PyQt5.QtWebChannel', 'PyQt5.QtNetwork', 'pandas', 'numpy', 'numpy.core.multiarray', 'scipy', 'shapely', 'pyproj', 'geopandas', 'sklearn', 'skgstat', 'matplotlib', 'seaborn', 'contextily', 'folium', 'plotly', 'ipywidgets', 'numpy.random.common', 'numpy.random.bounded_integers', 'numpy.random.entropy', 'rtree', 'fiona', 'pykrige', 'rasterio', 'pyproj', 'rasterio.sample', 'rasterio._io', 'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'PyQt5.QtWebEngineWidgets', 'geopandas', 'scipy._lib.array_api_compat.numpy.fft', 'scipy.special._special_ufuncs', '_openpyxl', 'openpyxl.cell._writer', 'xlsxwriter', 'xlwt', 'pyi_splash'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)
splash = Splash(
    'C:/Users/irish/Downloads/testkrig/krigsplash.jpg',
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=False,
)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    splash,
    splash.binaries,
    [],
    name='KrigMapPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\irish\\Downloads\\testkrig\\krigappicon.ico'],
)
