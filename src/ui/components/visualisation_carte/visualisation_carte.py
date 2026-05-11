from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QCheckBox, QScrollArea, QFrame, QPushButton,
    QMenu, QWidgetAction
)
from PySide6.QtCore import Qt, Signal, QObject, Slot, QPoint, QSize
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebChannel import QWebChannel
from PySide6.QtGui import QIcon
import os
import json
import pandas as pd
from ...utils import resource_path

class WebBridge(QObject):
    nappe_clicked = Signal(str)

    @Slot(str)
    def on_nappe_click(self, filepath: str):
        self.nappe_clicked.emit(filepath)


class VisualisationCarte(QWidget):
    nappe_selected = Signal(str)
    filter_changed  = Signal(set, set)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._types_actifs = {"inertielle", "reactive"}
        self.setAttribute(Qt.WA_StyledBackground, True)
        self._nappes_data   = []
        self._selected      = None
        self._geo_features  = []   # features GeoJSON filtrées par pipeline
        self._dept_actifs   = set()
        self._dept_list     = []   # [{id, name}]
        self._geojson_path  = os.path.join(
            os.path.dirname(__file__), "..", "..", "assets", "departements.geojson"
        )
        self._setup_ui()

    def _setup_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Container principal (important)
        container = QWidget()
        container.setObjectName("map_container")
        container.setAttribute(Qt.WA_StyledBackground, True)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)

        # Carte
        self.web = QWebEngineView(container)
        layout.addWidget(self.web)

        # Overlay bouton
        self.btn_filter = QPushButton(container)
        self.btn_filter.setObjectName("btn_filter")

        icon_path = resource_path("img", "funnel.svg")
        self.btn_filter.setIcon(QIcon(icon_path))
        self.btn_filter.setIconSize(QSize(18, 18))
        self.btn_filter.setFixedSize(36, 36)

        self.btn_filter.clicked.connect(self._show_filter_menu)

        # Position ABSOLUE (overlay)
        self.btn_filter.move(self.width() - 48, 12)
        self.btn_filter.raise_()  

        root.addWidget(container)

        # WebChannel
        self.channel = QWebChannel()
        self.bridge  = WebBridge()
        self.bridge.nappe_clicked.connect(self._on_nappe_clicked)
        self.channel.registerObject("bridge", self.bridge)
        self.web.page().setWebChannel(self.channel)

        self._render_map()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if hasattr(self, "btn_filter"):
            self.btn_filter.move(self.width() - 48, 12)

    def _show_filter_menu(self):
        if not self._dept_list:
            return

        menu = QMenu(self)
        menu.setObjectName("dept_menu")

        lbl_type = QLabel("  Type de nappe")
        lbl_type.setObjectName("menu_section_label")
        wa_lbl = QWidgetAction(menu)
        wa_lbl.setDefaultWidget(lbl_type)
        menu.addAction(wa_lbl)

        for type_val, label in [("inertielle", "🔵  Inertielle"), ("reactive", "🟢  Réactive")]:
            w  = QWidget()
            hl = QHBoxLayout(w)
            hl.setContentsMargins(8, 2, 8, 2)
            chk = QCheckBox(label)
            chk.setObjectName("dept_checkbox")
            chk.setChecked(type_val in self._types_actifs)
            chk.stateChanged.connect(
                lambda state, t=type_val: self._toggle_type(t, state)
            )
            hl.addWidget(chk)
            wa = QWidgetAction(menu)
            wa.setDefaultWidget(w)
            menu.addAction(wa)

        menu.addSeparator()

        lbl_dept = QLabel("  Départements")
        lbl_dept.setObjectName("menu_section_label")
        wa_dept = QWidgetAction(menu)
        wa_dept.setDefaultWidget(lbl_dept)
        menu.addAction(wa_dept)

        menu.setStyleSheet("""
        QMenu {
            background-color: #1e1e2e;
            border: 1px solid #313244;
        }
        """)

        # Tout sélectionner / désélectionner
        action_all = menu.addAction("Tout sélectionner")
        action_none = menu.addAction("Tout désélectionner")
        menu.addSeparator()

        checkboxes = []
        for dept in self._dept_list:
            did   = dept["id"]
            dname = dept["name"]
            w   = QWidget()
            hl  = QHBoxLayout(w)
            hl.setContentsMargins(8, 2, 8, 2)
            chk = QCheckBox(f"{did} – {dname}")
            chk.setObjectName("dept_checkbox")
            chk.setChecked(did in self._dept_actifs)
            chk.stateChanged.connect(
                lambda state, d=did: self._toggle_dept(d, state)
            )
            hl.addWidget(chk)
            wa = QWidgetAction(menu)
            wa.setDefaultWidget(w)
            menu.addAction(wa)
            checkboxes.append((did, chk))

        def select_all():
            for _, chk in checkboxes:
                chk.setChecked(True)
        def select_none():
            for _, chk in checkboxes:
                chk.setChecked(False)

        action_all.triggered.connect(select_all)
        action_none.triggered.connect(select_none)

        pos = self.btn_filter.mapToGlobal(QPoint(0, self.btn_filter.height()))
        menu.exec(pos)

    def _toggle_type(self, type_val: str, state: int):
        if state:
            self._types_actifs.add(type_val)
        else:
            self._types_actifs.discard(type_val)
        self._render_map()
        self.filter_changed.emit(self._dept_actifs, self._types_actifs)

    def _toggle_dept(self, dept_id: str, state: int):
        if state:
            self._dept_actifs.add(dept_id)
        else:
            self._dept_actifs.discard(dept_id)
        self._render_map()
        self.filter_changed.emit(self._dept_actifs, self._types_actifs)

    def load_config(self, cfg: dict):
        dept_pipeline = cfg.get("pipeline", {}).get("departements", [])
        dept_str = [str(d).zfill(2) for d in dept_pipeline]

        if not os.path.exists(self._geojson_path):
            # Cherche aussi à la racine src
            alt = resource_path("..", "..", "..", "departements.geojson")
            if os.path.exists(alt):
                self._geojson_path = alt

        if os.path.exists(self._geojson_path):
            with open(self._geojson_path, "r", encoding="utf-8") as f:
                raw = json.load(f)

            all_features = raw.get("features", [])

            # Filtre sur les départements du pipeline si spécifiés
            if dept_str:
                self._geo_features = [
                    feat for feat in all_features
                    if str(feat.get("properties", {}).get("code", "")).zfill(2) in dept_str
                    or str(feat.get("properties", {}).get("CODE_DEPT", "")).zfill(2) in dept_str
                    or str(feat.get("properties", {}).get("num_dep", "")).zfill(2) in dept_str
                    or str(feat.get("properties", {}).get("departement", "")).zfill(2) in dept_str
                ]
            else:
                self._geo_features = all_features

            # Construit la liste des départements pour le menu
            self._dept_list = []
            for feat in self._geo_features:
                props = feat.get("properties", {})
                did   = (
                    str(props.get("code",        props.get("CODE_DEPT",
                    props.get("num_dep",         props.get("departement", ""))))).zfill(2)
                )
                dname = props.get("nom", props.get("NOM_DEPT", props.get("name", did)))
                if did and not any(d["id"] == did for d in self._dept_list):
                    self._dept_list.append({"id": did, "name": dname})

            self._dept_actifs = {d["id"] for d in self._dept_list}

        self._render_map()

    def load_nappes(self, folders: list):
        self._nappes_data.clear()
        for folder in folders:
            nappe_type = "inertielle" if "inertielle" in folder else "reactive"
            if not os.path.exists(folder):
                continue
            for f in sorted(os.listdir(folder)):
                if not f.endswith(".csv"):
                    continue
                filepath = os.path.join(folder, f)
                try:
                    df       = pd.read_csv(filepath, sep=";")
                    df_valid = df[["lat", "lon"]].dropna() if "lat" in df.columns and "lon" in df.columns else pd.DataFrame()
                    if df_valid.empty:
                        continue
                    lat = float(df_valid["lat"].iloc[0])
                    lon = float(df_valid["lon"].iloc[0])
                    self._nappes_data.append({
                        "name":     f.replace(".csv", ""),
                        "lat":      lat,
                        "lon":      lon,
                        "filepath": filepath,
                        "type":     nappe_type,
                    })
                except Exception:
                    pass
        self._render_map()

    def highlight_nappe(self, filepath: str):
        self._selected = filepath
        self._render_map()

    def _on_nappe_clicked(self, filepath: str):
        self._selected = filepath
        self.nappe_selected.emit(filepath)
        self._render_map()
        
    def _filter_nappes_by_dept(self, features: list) -> list:
        # Filtre par type d'abord
        type_filtered = [n for n in self._nappes_data if n["type"] in self._types_actifs]

        if not features:
            return type_filtered
        try:
            from shapely.geometry import Point, shape
            polygons = [shape(f["geometry"]) for f in features]
            return [n for n in type_filtered if any(
                poly.contains(Point(n["lon"], n["lat"])) for poly in polygons
            )]
        except ImportError:
            return type_filtered

    def _render_map(self):
        geo_filtered = [
            f for f in self._geo_features
            if self._get_dept_id(f) in self._dept_actifs
        ]

        nappes_filtered = self._filter_nappes_by_dept(geo_filtered)

        geojson  = json.dumps({"type": "FeatureCollection", "features": geo_filtered})
        markers  = json.dumps(nappes_filtered)
        selected = json.dumps(self._selected)

        html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="qrc:///qtwebchannel/qwebchannel.js"></script>

<style>
body, html {{
    margin:0;
    padding:0;
    background: #11111b;
}}

#map {{
    width:100%;
    height:100vh;
    background: #242424;
}}

.nappe-tooltip {{
    background-color: #313244 !important;
    color: #cdd6f4 !important;
    border: 1px solid #89b4fa !important;
    border-radius: 6px;
    padding: 5px 10px;
    font-family: "Segoe UI", sans-serif;
    font-size: 12px;
}}
</style>
</head>

<body>
<div id="map"></div>

<script>
// ===== WebChannel =====
let bridge = null;
new QWebChannel(qt.webChannelTransport, function(ch){{
    bridge = ch.objects.bridge;
}});

// ===== MAP =====
const map = L.map('map',{{
    center:[46.8,2.3],
    zoom:6,
    zoomControl:true
}});

// ===== FOND ARCGIS DARK =====
L.tileLayer(
    'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{{z}}/{{y}}/{{x}}',
    {{ attribution: 'Tiles © Esri', maxZoom: 16 }}
).addTo(map);

L.tileLayer(
    'https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{{z}}/{{y}}/{{x}}',
    {{ attribution: 'Esri', maxZoom: 16 }}
).addTo(map);

// ===== GEOJSON (NON INTERACTIF = FIX BUG) =====
const geo = {geojson};

if (geo.features.length > 0) {{
    L.geoJSON(geo, {{
        interactive: false,

        style: {{
            color: '#89b4fa',
            weight: 1.2,
            fillColor: '#313244',
            fillOpacity: 0.15,
            dashArray: '3 3'
        }}
    }}).addTo(map);
}}

// ===== MARKERS =====
const markers  = {markers};
const selected = {selected};

markers.forEach(m => {{

    const isSel = selected && m.filepath === selected;

    const color = isSel
        ? '#f38ba8'
        : (m.type === 'inertielle' ? '#89b4fa' : '#a6e3a1');

    const circle = L.circleMarker([m.lat, m.lon], {{
        radius: isSel ? 11 : 7,
        fillColor: color,
        color: isSel ? '#ffffff' : '#11111b',
        weight: isSel ? 2.5 : 1.5,
        opacity: 1,
        fillOpacity: isSel ? 1.0 : 0.8
    }}).addTo(map);

    circle.bindTooltip(m.name, {{
        permanent: false,
        direction: 'top',
        className: 'nappe-tooltip',
        offset: [0, -8]
    }});

    circle.on('click', function () {{
        if (bridge) {{
            bridge.on_nappe_click(m.filepath);
        }}
    }});

    if (isSel) circle.bringToFront();
}});

// ===== ZOOM SUR SELECTION =====
if (selected) {{
    const sel = markers.find(m => m.filepath === selected);
    if (sel) {{
        map.setView([sel.lat, sel.lon], 10, {{ animate: true }});
    }}
}}

</script>
</body>
</html>
"""
        self.web.setHtml(html)

    def _get_dept_id(self, feature: dict) -> str:
        props = feature.get("properties", {})
        raw   = props.get("code", props.get("CODE_DEPT", props.get("num_dep", props.get("departement", ""))))
        return str(raw).zfill(2)

    def _load_style(self):
        qss_path = resource_path("components", "visualisation_carte", "visualisation_carte.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r") as f:
                self.setStyleSheet(f.read())