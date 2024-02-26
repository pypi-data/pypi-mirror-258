import numpy as np

def cylindrical_to_cartesian(rho, phi, z):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y, z

def cylindrical_to_spherical(rho, phi, z):
    r = np.sqrt(rho**2 + z**2)
    theta = np.arctan2(rho, z)
    return r, theta, phi
