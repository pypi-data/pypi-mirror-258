import numpy as np

def spherical_to_cartesian(r, theta, phi):
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)
    return x, y, z

def spherical_to_cylindrical(r, theta, phi):
    rho = r * np.sin(theta)
    return rho, phi, r * np.cos(theta)
