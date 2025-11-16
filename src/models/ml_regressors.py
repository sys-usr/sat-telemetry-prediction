# src/models/ml_regressors.py
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

FEATURE_COLS = [
    "pre_x", "pre_y", "pre_z",
    "pre_vx", "pre_vy", "pre_vz",
    "dv_x", "dv_y", "dv_z", "dv_mag",
    "dt_horizon",
]

TARGET_COLS = ["post_x", "post_y", "post_z", "post_vx", "post_vy", "post_vz"]

def train_baseline_regressor(df):
    X = df[FEATURE_COLS].values
    y = df[TARGET_COLS].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(
        n_estimators=200,
        max_depth=20,
        n_jobs=-1,
        random_state=42
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    return model, {"rmse": rmse}

