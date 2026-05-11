# -*- mode: python ; coding: utf-8 -*-
# app.spec — PyInstaller pour le projet nappes phréatiques
# Place ce fichier dans src/ puis lance : pyinstaller app.spec

import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

# ------------------------------------------------------------------ #
#  Données statiques à embarquer                                       #
# ------------------------------------------------------------------ #
added_files = [

    # Assets UI
    ("ui/assets/departements.geojson",                      "assets"),

    # Images SVG
    ("ui/img/*.svg",                                        "img"),

    # Style global
    ("ui/style/global.qss",                                 "style"),

    # QSS des composants
    ("ui/components/extraction_departement/*.qss",          "components/extraction_departement"),
    ("ui/components/extraction_departement/*.ui",           "components/extraction_departement"),
    ("ui/components/heatmap/*.qss",                         "components/heatmap"),
    ("ui/components/heatmap/*.ui",                          "components/heatmap"),
    ("ui/components/liste_nappes/*.qss",                    "components/liste_nappes"),
    ("ui/components/liste_nappes/*.ui",                     "components/liste_nappes"),
    ("ui/components/menu/*.qss",                            "components/menu"),
    ("ui/components/menu/*.ui",                             "components/menu"),
    ("ui/components/sidebar/*.qss",                         "components/sidebar"),
    ("ui/components/trieur/*.qss",                          "components/trieur"),
    ("ui/components/trieur/*.ui",                           "components/trieur"),
    ("ui/components/visualisation_carte/*.qss",             "components/visualisation_carte"),
    ("ui/components/visualisation_donnee/*.qss",            "components/visualisation_donnee"),

    # QSS des pages
    ("ui/pages/clusterisation/*.qss",                       "pages/clusterisation"),
    ("ui/pages/clusterisation/*.ui",                        "pages/clusterisation"),
    ("ui/pages/configuration/*.qss",                        "pages/configuration"),
    ("ui/pages/extraction/*.qss",                           "pages/extraction"),
    ("ui/pages/extraction/*.ui",                            "pages/extraction"),
    ("ui/pages/resultat/*.qss",                             "pages/resultat"),
    ("ui/pages/resultat/*.ui",                              "pages/resultat"),
    ("ui/pages/visualisation/*.qss",                        "pages/visualisation"),
    ("ui/pages/visualisation/*.ui",                         "pages/visualisation"),
]

# ------------------------------------------------------------------ #
#  Imports cachés (modules non détectés automatiquement)              #
# ------------------------------------------------------------------ #
hidden_imports = [
    # PySide6
    "PySide6.QtCore",
    "PySide6.QtWidgets",
    "PySide6.QtGui",
    "PySide6.QtWebEngineWidgets",
    "PySide6.QtCharts",
    "PySide6.QtWebChannel",
    "PySide6.QtUiTools",

    # Keras / PyTorch
    "keras",
    "keras.saving",
    "torch",

    # Scikit-learn
    "sklearn.ensemble",
    "sklearn.preprocessing",
    "sklearn.neighbors",

    # Data
    "pandas",
    "numpy",
    "scipy.spatial",
    "joblib",

    # Réseau
    "requests",

    # Config
    "tomllib",
    "toml",

    # Modules internes
    "data",
    "data.extraction",
    "data.fusion",
    "data.loader",
    "data.prepare",
    "data.clusterisation",
    "methodes",
    "methodes.interpolations",
    "methodes.autres",
    "methodes.reseaux_neuronnes",
    "evaluations",
    "evaluations.general",
    "evaluations.ia",
    "visualisations",
    "visualisations.graphs",
    "pipeline",
]

# ------------------------------------------------------------------ #
#  Analyse                                                           #
# ------------------------------------------------------------------ #
a = Analysis(
    ["app.py"],
    pathex=["."],
    binaries=[],
    datas=added_files,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "matplotlib",   # retire si tu l'utilises dans l'UI
        "tkinter",
        "IPython",
        "jupyter",
        "notebook",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# ------------------------------------------------------------------ #
#  Exécutable                                                        #
# ------------------------------------------------------------------ #
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,     # On utilise un dossier (COLLECT) plutôt que --onefile
    name="NappesApp",          # Nom de l'exe
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,                  # Compression UPX si disponible
    console=False,             # Pas de fenêtre console (windowed)
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="ui/img/icon.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="NappesApp",
)
