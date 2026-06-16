# PROJET JUNON — ETL et complétion de données hydrogéologiques

Projet réalisé par **Baptiste RICHARD** dans le cadre d’un stage de 3ᵉ année de BUT Informatique.

---

## 🧭 Contexte

Ce projet s’inscrit dans le cadre du **Projet Junon**, visant la création de **jumeaux numériques de nappes phréatiques**.

Il a pour objectif principal la **complétion de données environnementales manquantes** à partir de séries temporelles hétérogènes (météo, hydrologie, sol).

Le projet est destiné à un usage de **recherche scientifique**.

---

## 🎯 Objectif

Construire un **pipeline ETL automatisé** permettant :

- l’extraction de données environnementales
- leur fusion et harmonisation
- la clusterisation des nappes phréatiques
- l’entraînement de modèles de complétion
- la génération de données complétées sous format CSV

---

## 🛠️ Stack technique

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide6-6.11.0-41cd52?logo=qt&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-2.10.0+cu126-ee4c2c?logo=pytorch&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-3.13.2-d00000?logo=keras&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-2.4.3-013243?logo=numpy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-3.0.1-150458?logo=pandas&logoColor=white)
![scikit--learn](https://img.shields.io/badge/scikit--learn-1.8.0-f7931e?logo=scikitlearn&logoColor=white)
![SciPy](https://img.shields.io/badge/SciPy-1.17.1-8caae6?logo=scipy&logoColor=white)
![GeoPandas](https://img.shields.io/badge/GeoPandas-1.1.3-139c5a)
![Shapely](https://img.shields.io/badge/Shapely-2.1.2-333333)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.10.8-11557c)
![Requests](https://img.shields.io/badge/Requests-2.33.0-2b2d42)

---

## ⚙️ Pipeline global

Le projet est entièrement automatisé via un fichier de configuration `config.toml`.

Le pipeline exécute les étapes suivantes :

- extraction des données
- fusion des datasets
- clusterisation des nappes
- entraînement des modèles
- complétion des données manquantes
- visualisation des résultats

Chaque étape peut être activée ou désactivée via la configuration.

---

## 🧠 Méthodes utilisées

### 📌 Clusterisation des nappes

- méthode inertielle
- méthode réactive

---

### 📌 Complétion des données

#### Méthodes statistiques :

- interpolation linéaire
- interpolation cubique
- kNN

#### Méthodes IA :

- CNN
- LSTM
- BiLSTM

Les modèles sont utilisés pour **compléter des séries temporelles de données hydrologiques**.

---

## 📁 Structure du projet

```
data/
├── extraction/          # données brutes
├── fusion/              # données fusionnées
├── clusterisation/      # résultats de clustering
│   ├── inertielle/
│   └── reactive/
├── completion/         # données complétées
│   ├── inertielle/
│   └── reactive/
├── summary.csv         # résumé global
models/                 # modèles entraînés
scaler/                 # normalisation
notebooks/              # notebooks expérimentaux
src/                    # code source
LSTM/                   # expérimentations LSTM
output/                 # sorties diverses
```

---

## ⚙️ Configuration (`config.toml`)

Le pipeline est piloté par un fichier de configuration :

### Exemple :

```toml
[dossier]
dossier_extraction = "data/extraction"
dossier_extraction_tmp = "data/extraction/tmp"

meteo_name_extraction = "meteo"
nappe_name_extraction = "nappes"
etp_name_extraction = "etp"
impermeabilite_name_extraction = "impermeabilite"

mailles_name_extraction = "maille"
communes_name_extraction = "communes"

dossier_fusion = "data/fusion"

dossier_nappe_inertielle = "data/clusterisation/inertielle"
dossier_nappe_reactive = "data/clusterisation/reactive"

dossier_completion = "data/completion"
dossier_completion_inertielle = "data/completion/inertielle"
dossier_completion_reactive = "data/completion/reactive"

dossier_summary = "data"
summary_name = "summary.csv"

dossier_model = "models"
dossier_scaler = "scaler"

[entrainement_model]
window_size = 120
models = ["CNN","LSTM","BILSTM"] # valeur : ["CNN","LSTM","BILSTM"]
global = true
fine_tune = true
local = false

[fusion]
PRELIQ_Q = "sum" # valeur : "sum" ou "mean"

[completion]
[completion.niveau_nappe_eau]
realiser = true
methodes = ["knn_nappe", "lineaire"]

[completion.PRELIQ_Q]
realiser = false
methodes = ["lineaire","cubique", "global/CNN"]

[completion.T_Q]
realiser = false
methodes = []

[completion.ETP_Q]
realiser = false
methodes = []


[pipeline]
departements = [45] # liste des departements avec lesquels on veut travailler
qualite_continue = 1 # nombre maximum d'année continue
qualite_total = 5 # nombre d'année de donné que possède châque dataset. valeur : 30, 20, 10, 5, 0

type = [] # type de nappe sur lequel on veut travailler. valeur : ["reactive", "inertielle"]  ou []

extraction = false
fusion = false
clusterisation = false
entrainement = false
completion = false
affichage = true
````

---

## ▶️ Exécution

Lancement du pipeline :

```bash
c:\Users\tronn\Documents\STAGE-Junon\venv\Scripts\python.exe src/pipeline.py config.toml
```

---

## 📦 Installation

### Création de l’environnement virtuel

```bash
python -m venv venv
venv\Scripts\activate
```

### Installation des dépendances

```bash
pip install torch==2.10.0+cu126 --index-url https://download.pytorch.org/whl/cu126

pip install -r requirements.txt
```

---
Voici un bloc prêt à coller dans ton README :

---

## 🚀 Mise en production (`.exe`)

L'interface graphique peut être compilée en exécutable Windows autonome via **PyInstaller**.

### Compilation

Depuis le dossier `src/` :

```bash
cd src
pyinstaller app.spec
```

L'exécutable est généré dans `src/dist/NappesApp/NappesApp.exe`, accompagné de ses dépendances dans le même dossier.

### Points importants

- Le `config.toml` doit être présent à la racine du dossier `NappesApp/` au moment de l'exécution.
- La carte interactive (page Visualisation) nécessite une **connexion Internet** pour charger les tuiles cartographiques Leaflet et ArcGIS.
- Les dossiers de données (`data/`, `models/`, `scaler/`) doivent être placés **à côté de l'exécutable**, aux chemins définis dans `config.toml`.

---

## 📊 Sorties du projet

Le pipeline génère :

* fichiers CSV de données complétées
* résultats par méthode
* modèles entraînés
* visualisations
* métriques d’évaluation

---

## 🧪 Évaluation

Les méthodes de complétion sont évaluées via des fonctions définies dans :

```
src/evaluations/
```

---

## 🌍 Données utilisées

### Sources principales :

* Niveau des nappes : [https://ades.eaufrance.fr](https://ades.eaufrance.fr)
* Données météo (PRELIQ, T) : data.gouv.fr
* ETP FAO Hargreaves : data.gouv.fr
* Imperméabilisation des sols : data.gouv.fr
* Correspondance communes : data.gouv.fr
* Correspondance mailles : Météo-France

---

## 🧠 Utilisation des modèles

Les modèles sont utilisés pour la **complétion de données manquantes** dans les séries temporelles.

Ils exploitent une fenêtre temporelle définie par :

```toml
window_size = 120
```

---

## 📌 Stack technique

* Python 3.10
* PyTorch
* Keras / TensorFlow
* Pandas / NumPy
* Scikit-learn
* Matplotlib / Seaborn

---

## 📍 Portée

Le pipeline est initialement configuré pour le **département du Loiret (45)**, mais est compatible avec l’ensemble des départements français.

---

## 🚧 État du projet

Projet en cours (stage en développement)

---

## 👤 Auteur

Baptiste RICHARD
BUT Informatique — Stage 3ᵉ année

---

## 📦 Données récupérées

### 🌊 Données hydrologiques et météorologiques

- [x] Niveau des nappes phréatiques (`niveau_nappe_eau`)  
  https://ades.eaufrance.fr/recherche  

- [x] Précipitations mensuelles (`PRELIQ_Q`, en mm)  
  https://www.data.gouv.fr/datasets/donnees-climatologiques-de-base-mensuelles  

- [x] Température moyenne mensuelle (`T_Q`, en °C)  
  https://www.data.gouv.fr/datasets/donnees-climatologiques-de-base-mensuelles  

- [x] Évapotranspiration (`ETP_Q`, total mensuel)  
  https://www.data.gouv.fr/datasets/etp-fao-hargreaves  

---

### 🏞️ Données géographiques et environnementales

- [x] Imperméabilisation des sols  
  https://www.data.gouv.fr/datasets/impermeabilisation-des-sols-donnees-par-region-departement-scot-commune-et-epci  

---

### 🗺️ Correspondances spatiales

- Correspondance des mailles météorologiques  
  https://donneespubliques.meteofrance.fr/client/document/metadonnees_swi_276.csv  

- Correspondance communes → latitude / longitude  
  https://www.data.gouv.fr/datasets/donnees-sur-les-communes-de-france-metropolitaine  

---

### 🌡️ Estimation de l’ETP

- Méthodologie Evapotranspiration  
  https://www.campbellsci.fr/blog/evapotranspiration-101  
  → nécessite des données météorologiques complémentaires  

- Alternative climatique  
  https://www.drias-climat.fr/accompagnement/sections/310  

---

## 📚 Documentation utilisée

### 🌍 Fonctionnement des nappes phréatiques

- https://gsienv.com/wp-content/uploads/2023/09/Textbook_Kresic_Hydrogeology-101_rev-1.pdf  

---

### 📊 Clusterisation des nappes

- https://www.brgm.fr/fr/actualite/dossier-thematique/eau-souterraine-secheresse-inondations-faq-questions-frequentes  
- https://www.mdpi.com/2073-4441/13/18/2535  

---

### 🔧 Complétion des données manquantes

- https://www.math.univ-toulouse.fr/~besse/Wikistat/pdf/st-m-app-idm.pdf  

---

### 🤖 Complétion via IA / Deep Learning

- https://biblio.univ-annaba.dz/ingeniorat/wp-content/uploads/2025/01/M2-ST-Memoire-HEMICI_MERABET.pdf  
- https://www.fidle.cnrs.fr/w3/parcours/02-avance.html  
- https://youtu.be/Shnhb3hrKn8  
- https://youtu.be/OZ989EvTIBQ  

- https://celene.univ-orleans.fr/pluginfile.php/1798970/mod_resource/content/1/LSTM-explication.pdf  
- https://celene.univ-orleans.fr/pluginfile.php/1797464/mod_resource/content/1/CM-DLmodels_V2.pdf  

- https://www.kaggle.com/code/dungtuan/interpolate-series-prediction-with-lstm  
- https://pmc.ncbi.nlm.nih.gov/articles/PMC7571071/  
- https://anthology-of-data.science/resources/prince2023udl.pdf  
