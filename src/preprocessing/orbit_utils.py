# src/preprocessing/orbit_utils.py
import numpy as np
from astropy import units as u
from astropy.time import Time
from poliastro.twobody import Orbit
from poliastro.bodies import Earth

def state_to_orbit_elements(x, y, z, vx, vy, vz, epoch):
    r = np.array([x, y, z]) * u.km
    v = np.array([vx, vy, vz]) * (u.km / u.s)
    t = Time(epoch)
    orb = Orbit.from_vectors(Earth, r, v, epoch=t)
    # Return classical elements in a friendly dict
    return {
        "a": orb.a.to_value(u.km),
        "ecc": orb.ecc.value,
        "inc": orb.inc.to_value(u.deg),
        "raan": orb.raan.to_value(u.deg),
        "argp": orb.argp.to_value(u.deg),
        "nu": orb.nu.to_value(u.deg),
    }

