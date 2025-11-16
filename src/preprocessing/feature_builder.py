# src/preprocessing/feature_builder.py
import pandas as pd

def build_post_burn_dataset(telemetry_df: pd.DataFrame,
                            maneuvers_df: pd.DataFrame,
                            horizon_seconds: int = 600) -> pd.DataFrame:
    """
    For each maneuver, build a feature row:
      X: state just before burn + maneuver description
      y: state horizon_seconds after end_time
    """
    telemetry_df = telemetry_df.sort_values("timestamp")
    maneuvers_df = maneuvers_df.sort_values("start_time")

    samples = []

    for _, m in maneuvers_df.iterrows():
        sat_id = m["satellite_id"]
        start_t = m["start_time"]
        end_t = m["end_time"]
        target_t = end_t + pd.Timedelta(seconds=horizon_seconds)

        sat_hist = telemetry_df[telemetry_df["satellite_id"] == sat_id]

        # State just before burn
        pre_state = sat_hist[sat_hist["timestamp"] <= start_t].tail(1)
        if pre_state.empty:
            continue

        # State horizon_seconds after burn
        post_state = sat_hist[sat_hist["timestamp"] >= target_t].head(1)
        if post_state.empty:
            continue

        pre = pre_state.iloc[0]
        post = post_state.iloc[0]

        sample = {
            # Inputs
            "satellite_id": sat_id,
            "dt_horizon": horizon_seconds,
            "pre_x": pre["x"],
            "pre_y": pre["y"],
            "pre_z": pre["z"],
            "pre_vx": pre["vx"],
            "pre_vy": pre["vy"],
            "pre_vz": pre["vz"],
            "dv_x": m.get("delta_v_x", 0.0),
            "dv_y": m.get("delta_v_y", 0.0),
            "dv_z": m.get("delta_v_z", 0.0),
            "dv_mag": m.get("delta_v_mag", 0.0),
            # Outputs / labels
            "post_x": post["x"],
            "post_y": post["y"],
            "post_z": post["z"],
            "post_vx": post["vx"],
            "post_vy": post["vy"],
            "post_vz": post["vz"],
        }

        samples.append(sample)

    return pd.DataFrame(samples)
