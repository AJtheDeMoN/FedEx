import numpy as np

# Parse ULD and package data
def parse_uld_data(uld_data):
    uld_dimensions = {}
    lines = uld_data.strip().split('\n')
    for line in lines[1:]:
        identifier, length, width, height, _ = line.split(',')
        uld_dimensions[identifier] = (int(length), int(width), int(height))
    return uld_dimensions

def parse_package_data(package_data):
    packages = []
    lines = package_data.strip().split('\n')
    for line in lines:
        fields = line.split(',')
        identifier = fields[0]
        uld = fields[1]
        x1, y1, z1 = map(int, fields[2:5])
        x2, y2, z2 = map(int, fields[5:])
        packages.append((identifier, uld, x1, y1, z1, x2, y2, z2))
    return packages

# Check for overlapping packages
def check_overlaps(uld_dimensions, packages):
    uld_spaces = {uld: np.zeros(dimensions, dtype=bool) for uld, dimensions in uld_dimensions.items()}
    overlaps = []

    for package in packages:
        identifier, uld, x1, y1, z1, x2, y2, z2 = package
        if uld == "NONE":
            continue  # Skip packages not assigned to any ULD
        
        # Get the ULD's 3D space
        space = uld_spaces[uld]
        
        # Check if the space is already occupied
        x_range, y_range, z_range = slice(x1, x2-1), slice(y1, y2-1), slice(z1, z2-1)
        if np.any(space[x_range, y_range, z_range]):
            overlaps.append(identifier)
        else:
            # Mark the space as occupied
            space[x_range, y_range, z_range] = True

    return overlaps

# Read ULD and package data from files
def main():
    uld_data = """ULD Identifier,Length (cm),Width (cm),Height (cm),Weight Limit (kg)
U1,224,318,162,2500
U3,244,318,244,2800
U6,244,318,285,3500"""
    
    package_data = """P-1,U6,0,0,0,99,53,55
P-2,U3,99,0,0,155,99,81
P-3,U3,155,0,0,197,101,51
P-4,U6,197,0,0,305,75,56
P-5,U1,0,75,0,88,133,64
P-6,U3,88,75,0,179,131,84
P-7,U6,179,75,0,267,153,93
P-8,U6,0,153,0,108,258,76
P-9,U3,108,153,0,181,224,88
P-10,U3,181,153,0,269,223,85
P-11,U3,0,223,0,55,303,81
P-12,U3,55,223,0,103,303,88
P-13,U6,103,223,0,158,317,87
P-14,U6,158,223,0,203,269,81
P-15,U3,203,223,0,287,272,60
P-16,U3,0,272,0,48,365,63
P-17,U3,48,272,0,131,335,57
P-18,U6,131,272,0,199,373,95
P-19,U1,199,272,0,250,359,69
P-20,U3,0,0,69,88,106,125
P-21,U1,88,0,69,193,71,174
P-22,NONE,-1,-1,-1,-1,-1,-1
P-23,U3,193,0,69,244,50,179
P-24,U1,0,50,69,81,159,124
P-25,U6,81,50,69,125,127,122
P-26,U1,125,50,69,194,106,142
P-27,U3,194,50,69,287,112,118"""
    
# P-6,U3,88,75,0,179,131,84
# P-13,U6,103,223,0,158,317,87
# P-16,U3,0,272,0,48,365,63
# P-17,U3,48,272,0,131,335,57
# P-26,U1,125,50,69,194,106,142


    uld_dimensions = parse_uld_data(uld_data)
    packages = parse_package_data(package_data)
    overlaps = check_overlaps(uld_dimensions, packages)

    if overlaps:
        print("Overlapping packages found:", overlaps)
    else:
        print("No overlapping packages found.")

if __name__ == "__main__":
    main()
