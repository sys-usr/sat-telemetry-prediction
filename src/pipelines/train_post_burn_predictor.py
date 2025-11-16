# src/pipelines/train_post_burn_predictor.py
import joblib
from pathlib import Path

from ingestion.ccsds_loader import load_ccsds_oem
from ingestion.tle_loader import load_tle_file  # optional
from preprocessing.feature_builder import build_post_burn_dataset
from models.ml_regressors import train_baseline_regressor

def main():
    data_dir = Path("data")
    telemetry_path = data_dir / "processed" / "telemetry.parquet"
    maneuvers_path = data_dir / "processed" / "maneuvers.parquet"

    # Load already-processed telemetry & maneuver tables.
    # You can also call raw loaders + cleanup here instead.
    import pandas as pd
    telemetry_df = pd.read_parquet(telemetry_path)
    maneuvers_df = pd.read_parquet(maneuvers_path)

    dataset = build_post_burn_dataset(
        telemetry_df, maneuvers_df, horizon_seconds=600
    )

    model, metrics = train_baseline_regressor(dataset)
    print("Model metrics:", metrics)

    out_path = Path("models") / "post_burn_rf.joblib"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out_path)
    print(f"Saved model to {out_path}")

if __name__ == "__main__":
    main()

