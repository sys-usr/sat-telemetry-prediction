# src/ingestion/ccsds_loader.py
import pandas as pd
from pathlib import Path

def load_ccsds_oem(path: str | Path) -> pd.DataFrame:
    """
    Load a CCSDS OEM-like file into a canonical telemetry DataFrame.
    This assumes you've parsed out epochs, position, velocity, etc.
    """
    path = Path(path)
    # TODO: replace this pseudo-parser with a real CCSDS OEM parser
    # depending on your actual file format.
    records = []

    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('C'):
                continue
            # Example: epoch x y z vx vy vz
            parts = line.split()
            # You will need to adapt this to your real file layout.
            epoch = parts[0]
            x, y, z, vx, vy, vz = map(float, parts[1:7])

            records.append({
                "satellite_id": path.stem,
                "timestamp": pd.to_datetime(epoch),
                "frame": "ECI",
                "x": x,
                "y": y,
                "z": z,
                "vx": vx,
                "vy": vy,
                "vz": vz,
                "maneuver_flag": 0,
                "maneuver_id": None,
            })

    df = pd.DataFrame.from_records(records)
    df.sort_values("timestamp", inplace=True)
    return df

