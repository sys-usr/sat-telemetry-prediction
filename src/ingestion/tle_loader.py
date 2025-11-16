# src/ingestion/tle_loader.py
from pathlib import Path
import pandas as pd
from sgp4.api import Satrec, jday

def load_tle_file(path: str | Path, sat_id: str) -> pd.DataFrame:
    path = Path(path)
    with path.open() as f:
        lines = [l.strip() for l in f.readlines()]
    line1, line2 = lines[0], lines[1]

    sat = Satrec.twoline2rv(line1, line2)

    # Example: sample at 60-second intervals for N steps from epoch
    # In reality, you'd sync TLE epochs with your telemetry timestamps.
    ts = pd.date_range(start="2025-01-01T00:00:00Z",
                       periods=360,
                       freq="60S")
    records = []
    for t in ts:
        jd, fr = jday(t.year, t.month, t.day, t.hour, t.minute,
                      t.second + t.microsecond / 1e6)
        e, r, v = sat.sgp4(jd, fr)
        if e != 0:
            continue
        x, y, z = (coord / 1000 for coord in r)    # m→km
        vx, vy, vz = (vel / 1000 for vel in v)     # m/s→km/s
        records.append({
            "satellite_id": sat_id,
            "timestamp": t,
            "frame": "ECI",
            "x": x, "y": y, "z": z,
            "vx": vx, "vy": vy, "vz": vz,
            "maneuver_flag": 0,
            "maneuver_id": None,
        })
    return pd.DataFrame.from_records(records)

