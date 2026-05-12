from evaluations import grid_search_all
from data.loader import charger_dossier
from data.prepare import train_data_cnn

racine = "./"
dossier_nappe = racine + "data/fusion"
fichier_scaler = racine + "scaler/scaler.save"
window_size = 120



X_train, X_val, y_train, y_val, scaler = train_data_cnn(charger_dossier(dossier_nappe), window_size, fichier_scaler, croissant=True, saine=True)

best_model, best_config, results = grid_search_all(
    X_train, y_train, X_val, y_val,
    n_workers=4  # ajuste selon ton GPU
)

best_model.save("best_model.keras")