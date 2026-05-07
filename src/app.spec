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
    # Config
    ("config.toml",                                         "."),

    # Assets UI
    ("ui/assets/departements.geojson",                      "ui/assets"),

    # Images SVG
    ("ui/img/*.svg",                                        "ui/img"),

    # Style global
    ("ui/style/global.qss",                                 "ui/style"),

    # QSS des composants
    ("ui/components/extraction_departement/*.qss",          "ui/components/extraction_departement"),
    ("ui/components/extraction_departement/*.ui",           "ui/components/extraction_departement"),
    ("ui/components/heatmap/*.qss",                         "ui/components/heatmap"),
    ("ui/components/heatmap/*.ui",                          "ui/components/heatmap"),
    ("ui/components/liste_nappes/*.qss",                    "ui/components/liste_nappes"),
    ("ui/components/liste_nappes/*.ui",                     "ui/components/liste_nappes"),
    ("ui/components/menu/*.qss",                            "ui/components/menu"),
    ("ui/components/menu/*.ui",                             "ui/components/menu"),
    ("ui/components/sidebar/*.qss",                         "ui/components/sidebar"),
    ("ui/components/trieur/*.qss",                          "ui/components/trieur"),
    ("ui/components/trieur/*.ui",                           "ui/components/trieur"),
    ("ui/components/visualisation_carte/*.qss",             "ui/components/visualisation_carte"),
    ("ui/components/visualisation_donnee/*.qss",            "ui/components/visualisation_donnee"),

    # QSS des pages
    ("ui/pages/clusterisation/*.qss",                       "ui/pages/clusterisation"),
    ("ui/pages/clusterisation/*.ui",                        "ui/pages/clusterisation"),
    ("ui/pages/configuration/*.qss",                        "ui/pages/configuration"),
    ("ui/pages/extraction/*.qss",                           "ui/pages/extraction"),
    ("ui/pages/extraction/*.ui",                            "ui/pages/extraction"),
    ("ui/pages/resultat/*.qss",                             "ui/pages/resultat"),
    ("ui/pages/resultat/*.ui",                              "ui/pages/resultat"),
    ("ui/pages/visualisation/*.qss",                        "ui/pages/visualisation"),
    ("ui/pages/visualisation/*.ui",                         "ui/pages/visualisation"),
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
#  Analyse                                                             #
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
#  Exécutable                                                          #
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
    # icon="ui/img/geo-alt-fill.ico",  # Décommente si tu as une icône .ico
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
