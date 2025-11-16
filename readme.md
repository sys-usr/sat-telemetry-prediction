🚀 Satellite Telemetry Prediction

A Python project for ingesting satellite telemetry from multiple sources and training models to predict satellite position and velocity after maneuvers such as orbital burns and station-keeping events.

This repo provides:

A clean ingestion pipeline for CCSDS OEM, TLE, or custom telemetry.

Automatic feature extraction for pre-burn → post-burn prediction.

A physics baseline propagator using poliastro.

Machine-learning models for predicting post-maneuver state vectors.

A modular, expandable architecture designed for real ops workflows.

📦 Project Structure
sat-telemetry-prediction/
├─ data/
│  ├─ raw/          # Incoming unprocessed telemetry files
│  ├─ interim/      # Intermediate transformed data
│  └─ processed/    # Cleaned telemetry & maneuver tables (not versioned)
├─ notebooks/        # Jupyter notebooks for exploration & prototyping
├─ src/
│  ├─ ingestion/     # Loaders for TLE, CCSDS, custom formats
│  ├─ preprocessing/ # State vectors, orbital elements, feature building
│  ├─ models/        # ML models + physics propagator
│  └─ pipelines/     # End-to-end training/evaluation pipelines
├─ scripts/          # Optional run scripts or automation
├─ tests/            # (Future) unit tests
├─ requirements.txt  # Python dependencies
└─ README.md         # You are here

⚙️ Installation

Clone the repo:

git clone https://github.com/<your-username>/sat-telemetry-prediction.git
cd sat-telemetry-prediction


Create a virtual environment:

python -m venv .venv


Activate it:

PowerShell:

. .venv/Scripts/Activate.ps1


Install dependencies:

pip install -r requirements.txt

📡 Data Ingestion

Supported source types (modular):

CCSDS OEM

TLE (using sgp4)

Custom CSV / proprietary telemetry files

Example:

from src.ingestion.ccsds_loader import load_ccsds_oem
df = load_ccsds_oem("data/raw/my_satellite.oem")


All telemetry is normalized into a unified schema:

timestamp

x, y, z (km)

vx, vy, vz (km/s)

frame (default: ECI)

maneuver_flag

maneuver_id

🧠 Feature Engineering

Training samples are built around maneuver events:

pre-burn state + maneuver metadata → post-burn state at +Δt

Example feature builder:

from src.preprocessing.feature_builder import build_post_burn_dataset

dataset = build_post_burn_dataset(
    telemetry_df,
    maneuvers_df,
    horizon_seconds=600
)

🛰 Physics Baseline

The project includes a physics-based baseline model:

Applies instantaneous ΔV

Propagates the orbit forward using poliastro

Produces a “physics-only” prediction

ML models can then learn residuals

Example:

from src.models.baseline_propagator import apply_delta_v_and_propagate

🤖 Machine Learning Models

Initial ML models use scikit-learn:

Random Forest Regressor

Gradient Boosting (optional)

Multi-output regression on:

post_x, post_y, post_z

post_vx, post_vy, post_vz

Later improvements (planned):

Neural networks for ΔV modeling

Sequence models (LSTM/Transformer)

Physics-informed residual learning

🏋️ Training

Run the training pipeline:

python -m src.pipelines.train_post_burn_predictor


This will:

Load telemetry & maneuver tables from data/processed/

Build the feature dataset

Train the Random Forest model

Save the model to models/post_burn_rf.joblib

📊 Future Enhancements

Add CI/CD (GitHub Actions)

Add automated dataset validation

Integrate Kalman filtering for smoothing telemetry noise

Add long-horizon multi-step predictions (1hr, 6hr, 24hr)

Add visualization scripts for:

position error vs time

residual distributions

3-D orbit plots

📄 License

MIT License

🙋 Contributing

PRs and feature requests welcome.

🛰 Contact

Maintained by London.
