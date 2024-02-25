# Coordinate Conversion

Coordinate Conversion is a Python package that provides functions for converting coordinates between Cartesian, spherical, and cylindrical systems.

## Installation

You can install Coordinate Conversion using pip:

```Bash
pip install coordinate_conversion
```
## Usage

```python
import coordinate_conversion

# Convert Cartesian coordinates to spherical
x, y, z = 1, 1, 1
r, theta, phi = coordinate_conversion.cartesian_to_spherical(x, y, z)
print("Spherical coordinates:", r, theta, phi)

# Convert spherical coordinates to Cartesian
x, y, z = coordinate_conversion.spherical_to_cartesian(r, theta, phi)
print("Back to Cartesian coordinates:", x, y, z)

# Convert Cartesian coordinates to cylindrical
rho, phi, z = coordinate_conversion.cartesian_to_cylindrical(x, y, z)
print("Cylindrical coordinates:", rho, phi, z)

# Convert cylindrical coordinates to Cartesian
x, y, z = coordinate_conversion.cylindrical_to_cartesian(rho, phi, z)
print("Back to Cartesian coordinates:", x, y, z)

# Convert spherical coordinates to cylindrical
rho, phi, z = coordinate_conversion.spherical_to_cylindrical(r, theta, phi)
print("Spherical to Cylindrical:", rho, phi, z)

# Convert cylindrical coordinates to spherical
r, theta, phi = coordinate_conversion.cylindrical_to_spherical(rho, phi, z)
print("Back to Spherical coordinates:", r, theta, phi)
```