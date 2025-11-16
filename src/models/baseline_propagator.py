# src/models/baseline_propagator.py
import numpy as np
from astropy import units as u
from astropy.time import Time
from poliastro.twobody import Orbit
from poliastro.bodies import Earth

def apply_delta_v_and_propagate(pre_state, maneuver, dt_seconds):
    """
    pre_state: dict with x,y,z,vx,vy,vz,epoch
    maneuver: dict with dv_x, dv_y, dv_z
    """
    r = np.array([pre_state["x"], pre_state["y"], pre_state["z"]]) * u.km
    v = np.array([pre_state["vx"], pre_state["vy"], pre_state["vz"]]) * (u.km / u.s)
    dv = np.array([maneuver["dv_x"], maneuver["dv_y"], maneuver["dv_z"]]) * (u.km / u.s)

    epoch = Time(pre_state["epoch"])

    orb = Orbit.from_vectors(Earth, r, v, epoch=epoch)
    # Apply instantaneous delta-v in same frame:
    v_new = v + dv
    orb_after_burn = Orbit.from_vectors(Earth, r, v_new, epoch=epoch)

    # Propagate forward dt_seconds
    tof = dt_seconds * u.s
    orb_future = orb_after_burn.propagate(tof)

    r_f, v_f = orb_future.r.to(u.km).value, orb_future.v.to(u.km/u.s).value

    return {
        "x": r_f[0], "y": r_f[1], "z": r_f[2],
        "vx": v_f[0], "vy": v_f[1], "vz": v_f[2],
    }

