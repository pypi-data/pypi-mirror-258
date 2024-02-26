import math

# Constants for WGS84 ellipsoid
a = 6378137.0  # semi-major axis in meters
f_inv = 298.257223563  # inverse flattening

def gps_to_cartesian(latitude, longitude, altitude=0):
    # Convert latitude and longitude from degrees to radians
    lat_rad = math.radians(latitude)
    lon_rad = math.radians(longitude)

    # Calculate auxiliary parameters
    e2 = 1 - (1 - 1/f_inv) ** 2
    N = a / math.sqrt(1 - e2 * math.sin(lat_rad) ** 2)

    # Calculate Cartesian coordinates
    x = (N + altitude) * math.cos(lat_rad) * math.cos(lon_rad)
    y = (N + altitude) * math.cos(lat_rad) * math.sin(lon_rad)
    z = ((1 - e2) * N + altitude) * math.sin(lat_rad)

    return x, y, z

def cartesian_to_gps(x, y, z):
    # Calculate longitude
    lon_rad = math.atan2(y, x)
    
    # Calculate auxiliary parameters
    p = math.sqrt(x**2 + y**2)
    theta = math.atan2(z * a, p * b)

    # Iteratively calculate latitude using an approximation
    lat_rad = math.atan2(z + (e2 * b * math.sin(theta) ** 3), p - (e2 * a * math.cos(theta) ** 3))
    N = a / math.sqrt(1 - e2 * math.sin(lat_rad) ** 2)

    # Calculate altitude
    alt = p / math.cos(lat_rad) - N

    # Convert latitude and longitude from radians to degrees
    latitude = math.degrees(lat_rad)
    longitude = math.degrees(lon_rad)

    return latitude, longitude, alt
