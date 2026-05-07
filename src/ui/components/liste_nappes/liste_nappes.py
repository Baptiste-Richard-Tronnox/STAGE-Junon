from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QLineEdit
)
from PySide6.QtCore import Qt, Signal, QSize
import os
import pandas as pd


class ListeNappes(QWidget):
    nappe_selected = Signal(str)  # filepath

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(260)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setObjectName("liste_nappes_panel")
        self._all_items = []  # (name, filepath, type)
        self._setup_ui()
        self._load_style()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 16, 12, 12)
        layout.setSpacing(8)

        title = QLabel("Nappes")
        title.setObjectName("panel_title")
        layout.addWidget(title)

        self.search = QLineEdit()
        self.search.setPlaceholderText("🔍  Rechercher...")
        self.search.setObjectName("nappe_search")
        self.search.textChanged.connect(self._filter)
        layout.addWidget(self.search)

        self.list_widget = QListWidget()
        self.list_widget.setObjectName("nappe_list_view")
        self.list_widget.currentItemChanged.connect(self._on_item_changed)
        layout.addWidget(self.list_widget)

        self.list_widget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.list_widget.setWordWrap(True)

    def load_nappes(self, folders: list):
        self._all_items.clear()
        self._coords_cache = {}   # filepath -> (lat, lon)
        self.list_widget.clear()

        for folder in folders:
            nappe_type = "inertielle" if "inertielle" in folder else "reactive"
            if not os.path.exists(folder):
                continue
            for f in sorted(os.listdir(folder)):
                if not f.endswith(".csv"):
                    continue
                filepath = os.path.join(folder, f)
                name     = f.replace(".csv", "")
                self._all_items.append((name, filepath, nappe_type))

                # Cache des coordonnées
                try:
                    import pandas as pd
                    df   = pd.read_csv(filepath, sep=";", nrows=5)
                    df_v = df[["lat", "lon"]].dropna() if "lat" in df.columns and "lon" in df.columns else pd.DataFrame()
                    if not df_v.empty:
                        self._coords_cache[filepath] = (
                            float(df_v["lat"].iloc[0]),
                            float(df_v["lon"].iloc[0])
                        )
                except Exception:
                    pass

        self._render_items(self._all_items)

    def apply_filter(self, dept_actifs: set, types_actifs: set):
        """Filtre la liste selon les départements actifs et les types autorisés."""
        try:
            from shapely.geometry import Point, shape
            # Récupère les polygones depuis la carte si dispo
            has_shapely = True
        except ImportError:
            has_shapely = False

        filtered = []
        for name, filepath, nappe_type in self._all_items:
            # Filtre par type
            if nappe_type not in types_actifs:
                continue

            # Filtre géographique si on a shapely et les features
            if has_shapely and hasattr(self, "_geo_features") and self._geo_features:
                try:
                    import pandas as pd
                    from shapely.geometry import Point, shape
                    df = pd.read_csv(filepath, sep=";", nrows=5)
                    df_v = df[["lat", "lon"]].dropna()
                    if df_v.empty:
                        continue
                    lat = float(df_v["lat"].iloc[0])
                    lon = float(df_v["lon"].iloc[0])
                    pt  = Point(lon, lat)
                    active_features = [f for f in self._geo_features
                                    if self._get_dept_id(f) in dept_actifs]
                    if not any(shape(f["geometry"]).contains(pt) for f in active_features):
                        continue
                except Exception:
                    pass

            filtered.append((name, filepath, nappe_type))

        search = self.search.text()
        if search:
            filtered = [(n, fp, t) for n, fp, t in filtered if search.lower() in n.lower()]

        self._render_items(filtered)

    def _get_dept_id(self, feature: dict) -> str:
        props = feature.get("properties", {})
        return str(props.get("code", props.get("CODE_DEPT", props.get("num_dep", "")))).zfill(2)

    def _render_items(self, items):
        self.list_widget.clear()
        for name, filepath, nappe_type in items:
            item = QListWidgetItem()
            item.setData(Qt.UserRole, filepath)
            icon = "🔵" if nappe_type == "inertielle" else "🟢"
            item.setText(f"{icon}  {name}")
            item.setSizeHint(QSize(240, 32))
            self.list_widget.addItem(item)

    def _filter(self, text: str):
        filtered = [
            (n, fp, t) for n, fp, t in self._all_items
            if text.lower() in n.lower()
        ]
        self._render_items(filtered)

    def _on_item_changed(self, current, previous):
        if current:
            filepath = current.data(Qt.UserRole)
            if filepath:
                self.nappe_selected.emit(filepath)

    def _load_style(self):
        qss_path = os.path.join(os.path.dirname(__file__), "liste_nappes.qss")
        if os.path.exists(qss_path):
            with open(qss_path, "r") as f:
                self.setStyleSheet(f.read())