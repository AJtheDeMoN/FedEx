import pulp
import pandas as pd
from io import StringIO
import os
from pulp import LpVariable


# ULD Data
uld_data = """ULD Identifier,Length (cm),Width (cm),Height (cm),Weight Limit (kg)
U1,224,318,162,2500
U2,244,318,244,2800"""

# Parse ULD Data
uld_df = pd.read_csv(StringIO(uld_data))
uld_df['Volume'] = uld_df['Length (cm)'] * uld_df['Width (cm)'] * uld_df['Height (cm)']

# Package Data
package_data = """Package Identifier,Length (cm),Width (cm),Height (cm),Weight (kg),Type (P/E),Cost of Delay
P-1,99,53,55,61,Economy,176
P-2,56,99,81,53,Priority,-
P-3,42,101,51,17,Priority,-
P-4,108,75,56,73,Economy,138
P-5,88,58,64,93,Economy,139
P-6,91,56,84,47,Priority,-
P-7,88,78,93,117,Economy,102
P-8,108,105,76,142,Economy,108
P-9,73,71,88,50,Priority,-
P-10,88,70,85,81,Priority,-
P-11,55,80,81,23,Economy,96
P-12,48,80,88,27,Economy,117
P-13,55,94,87,41,Economy,73
P-14,45,46,81,27,Economy,68
P-15,84,49,60,57,Priority,-
P-16,48,93,63,82,Priority,-
P-17,83,63,57,29,Priority,-
P-18,68,101,95,96,Economy,65
P-19,51,87,69,73,Economy,107
P-20,88,106,56,71,Priority,-
P-21,105,71,105,223,Economy,116
P-22,100,92,99,191,Economy,86
P-23,51,50,110,59,Priority,-
P-24,81,109,55,123,Economy,69
P-25,44,77,53,37,Economy,108
P-26,69,56,73,56,Economy,130
P-27,93,62,49,18,Economy,122
P-28,81,64,95,70,Economy,139
P-29,62,86,53,23,Economy,122
P-30,88,85,102,164,Economy,70
P-31,71,49,76,67,Economy,76
P-32,70,44,98,53,Economy,124
P-33,90,89,73,132,Economy,136
P-34,87,45,81,45,Economy,77
P-35,83,72,63,96,Economy,103
P-36,86,80,78,146,Priority,-
P-37,59,76,51,33,Economy,131
P-38,84,96,48,21,Economy,60
P-39,96,64,61,61,Economy,111
P-40,70,45,90,78,Economy,106
P-41,104,90,68,72,Priority,-
P-42,62,109,41,46,Priority,-
P-43,51,86,108,87,Economy,109
P-44,84,40,49,28,Economy,87
P-45,91,72,81,92,Priority,-
P-46,71,62,94,39,Priority,-
P-47,86,58,104,149,Economy,67
P-48,53,65,48,33,Economy,67
P-49,69,40,100,55,Priority,-
P-50,73,104,64,75,Priority,-
P-51,57,86,97,65,Economy,67
P-52,104,88,102,96,Economy,121
P-53,44,53,106,14,Economy,74
P-54,106,51,59,20,Economy,98
P-55,95,93,77,71,Economy,78
P-56,65,68,109,77,Economy,85
P-57,83,64,59,32,Economy,137
P-58,95,102,55,126,Economy,134
P-59,85,79,49,26,Economy,111
P-60,60,85,87,23,Economy,84
P-61,57,109,95,130,Economy,136
P-62,43,92,88,25,Economy,84
P-63,75,69,85,111,Economy,116
P-64,100,56,104,123,Economy,62
P-65,50,78,110,56,Economy,121
P-66,50,47,86,53,Economy,72
P-67,76,57,101,34,Economy,65
P-68,92,46,81,62,Priority,-
P-69,84,47,54,57,Priority,-
P-70,108,101,77,158,Economy,102
P-71,99,43,60,41,Priority,-
P-72,89,83,44,79,Economy,66
P-73,104,86,63,79,Priority,-
P-74,73,87,69,115,Economy,61
P-75,74,43,85,42,Economy,128
P-76,40,92,96,81,Economy,123
P-77,96,50,65,57,Economy,88
P-78,74,104,42,85,Economy,116
P-79,86,62,75,61,Economy,91
P-80,43,85,44,20,Economy,127
P-81,110,101,93,94,Economy,116
P-82,66,71,97,130,Priority,-
P-83,106,105,99,168,Economy,97
P-84,94,66,78,41,Economy,82
P-85,47,68,44,42,Economy,74
P-86,65,63,41,50,Priority,-
P-87,54,53,107,84,Economy,116
P-88,70,106,62,106,Economy,74
P-89,68,109,108,60,Economy,117
P-90,44,98,102,119,Economy,60
P-91,91,92,50,89,Economy,76
P-92,58,58,65,59,Economy,138
P-93,88,68,92,100,Economy,133
P-94,67,98,66,95,Priority,-
P-95,91,69,89,68,Economy,73
P-96,50,65,84,40,Economy,68
P-97,53,53,93,54,Economy,120
P-98,108,63,94,139,Economy,76
P-99,71,70,68,28,Economy,108
P-100,100,62,87,104,Economy,79
P-101,102,82,76,154,Economy,109
P-102,70,106,64,70,Economy,135
P-103,44,78,102,84,Priority,-
P-104,90,95,95,110,Economy,108
P-105,80,95,103,225,Priority,-
P-106,90,54,92,100,Priority,-
P-107,99,100,100,252,Economy,134
P-108,47,109,70,95,Economy,90
P-109,98,79,44,53,Priority,-
P-110,86,88,100,158,Economy,89
P-111,62,103,65,27,Economy,60
P-112,63,79,67,20,Priority,-
P-113,55,86,75,88,Economy,87
P-114,80,93,104,175,Economy,124
P-115,46,105,102,112,Economy,105
P-116,106,109,83,132,Economy,128
P-117,52,49,65,33,Priority,-
P-118,90,82,75,55,Economy,114
P-119,41,79,104,25,Economy,61
P-120,48,91,74,82,Economy,105
"""

# Parse Package Data
package_df = pd.read_csv(StringIO(package_data))
package_df = package_df.fillna({'Cost of Delay': 0})  # Replace NaN with 0 for Priority packages
package_df['Volume'] = package_df['Length (cm)'] * package_df['Width (cm)'] * package_df['Height (cm)']

# Identify Priority and Economy packages
priority_packages = package_df[package_df['Type (P/E)'] == 'Priority']
economy_packages = package_df[package_df['Type (P/E)'] == 'Economy']

# Create mappings for efficiency
package_df['Cost of Delay'] = pd.to_numeric(package_df['Cost of Delay'], errors='coerce').fillna(0)
cost_delay_dict = dict(zip(package_df['Package Identifier'], package_df['Cost of Delay']))
package_type_dict = dict(zip(package_df['Package Identifier'], package_df['Type (P/E)']))

# Function to check if a package fits in a ULD
def fits(uld, pkg):
    return (pkg['Length (cm)'] <= uld['Length (cm)']) and \
           (pkg['Width (cm)'] <= uld['Width (cm)']) and \
           (pkg['Height (cm)'] <= uld['Height (cm)'])

# Create a list of feasible assignments
feasible_assignments = []

for idx_p, pkg in package_df.iterrows():
    for idx_u, uld in uld_df.iterrows():
        if fits(uld, pkg):
            feasible_assignments.append((pkg['Package Identifier'], uld['ULD Identifier']))

# Convert to DataFrame for easier handling
feasible_df = pd.DataFrame(feasible_assignments, columns=['Package', 'ULD'])

# Initialize the problem
prob = pulp.LpProblem("FedEx_ULD_Packing", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("assign",
                          ((pkg, uld) for pkg, uld in feasible_assignments),
                          cat='Binary')

z = pulp.LpVariable.dicts("not_assign",
                          (pkg for pkg in economy_packages['Package Identifier']),
                          cat='Binary')

s = pulp.LpVariable.dicts("ULD_has_Priority",
                          (uld for uld in uld_df['ULD Identifier']),
                          cat='Binary')

# Initialize LpVariable for coordinates (x, y, z) for each package and ULD
package_coords = {}

for uld in uld_df['ULD Identifier']:
    for i, pkg in package_df.iterrows():
        # Initialize the LpVariables for x, y, z coordinates for each package
        x_var = LpVariable(f"x_{pkg['Package Identifier']}_{uld}", lowBound=0)  # LpVariable for x-coordinate
        y_var = LpVariable(f"y_{pkg['Package Identifier']}_{uld}", lowBound=0)  # LpVariable for y-coordinate
        z_var = LpVariable(f"z_{pkg['Package Identifier']}_{uld}", lowBound=0)  # LpVariable for z-coordinate
        
        # Store the coordinates for each package in the dictionary
        package_coords[(pkg['Package Identifier'], uld)] = (x_var, y_var, z_var)


# Objective Function
K = 5000  # Cost per ULD carrying Priority packages

prob += (
    pulp.lpSum([
        z[pkg] * cost_delay_dict.get(pkg, 0)  # Cost of Delay for Economy packages
        for pkg in economy_packages['Package Identifier']
    ]) +
    K * pulp.lpSum([s[uld] for uld in uld_df['ULD Identifier']])
, "Total Cost")

# Assignment Constraints
for pkg in package_df['Package Identifier']:
    if package_type_dict.get(pkg) == 'Economy':
        prob += (
            pulp.lpSum([x[(pkg, uld)] for uld in uld_df['ULD Identifier'] if (pkg, uld) in feasible_assignments]) + z[pkg] == 1,
            f"Assignment_{pkg}"
        )
    elif package_type_dict.get(pkg) == 'Priority':
        prob += (
            pulp.lpSum([x[(pkg, uld)] for uld in uld_df['ULD Identifier'] if (pkg, uld) in feasible_assignments]) == 1,
            f"Assignment_Priority_{pkg}"
        )

# ULD Weight Limit Constraints
for idx_u, uld in uld_df.iterrows():
    uld_id = uld['ULD Identifier']
    prob += (
        pulp.lpSum([
            x[(pkg, uld_id)] * package_df.loc[package_df['Package Identifier'] == pkg, 'Weight (kg)'].values[0]
            for pkg in package_df['Package Identifier'] if (pkg, uld_id) in feasible_assignments
        ]) <= uld['Weight Limit (kg)'],
        f"Weight_Limit_{uld_id}"
    )

# ULD Volume Limit Constraints
for idx_u, uld in uld_df.iterrows():
    uld_id = uld['ULD Identifier']
    uld_volume = uld['Volume']
    prob += (
        pulp.lpSum([
            x[(pkg, uld_id)] * package_df.loc[package_df['Package Identifier'] == pkg, 'Volume'].values[0]
            for pkg in package_df['Package Identifier'] if (pkg, uld_id) in feasible_assignments
        ]) <= uld_volume,
        f"Volume_Limit_{uld_id}"
    )

# Assuming package_coords stores coordinates as LpVariables for each package and ULD
# for uld in uld_df['ULD Identifier']:
#     for i, pkg1 in package_df.iterrows():
#         for j, pkg2 in package_df.iterrows():
#             if i < j:  # Avoid redundant checks
#                 if (pkg1['Package Identifier'], uld) in feasible_assignments and (pkg2['Package Identifier'], uld) in feasible_assignments:
#                     # Create unique constraint names for the overlap constraints
#                     constraint_name = f"Overlap_{pkg1['Package Identifier']}_{pkg2['Package Identifier']}_{uld}"
                    
#                     # Coordinates of package 1
#                     x1 = package_coords[(pkg1['Package Identifier'], uld)][0]
#                     y1 = package_coords[(pkg1['Package Identifier'], uld)][1]
#                     z1 = package_coords[(pkg1['Package Identifier'], uld)][2]

#                     # Coordinates of package 2
#                     x2 = package_coords[(pkg2['Package Identifier'], uld)][0]
#                     y2 = package_coords[(pkg2['Package Identifier'], uld)][1]
#                     z2 = package_coords[(pkg2['Package Identifier'], uld)][2]

#                     # Ensure no overlap along the x, y, and z axes
#                     prob += (
#                         x1 + pkg1['Length (cm)'] <= x2 + 10000 * (1 - x[(pkg1['Package Identifier'], uld)] - x[(pkg2['Package Identifier'], uld)]),
#                         constraint_name + "_x"
#                     )

#                     prob += (
#                         x2 + pkg2['Length (cm)'] <= x1 + 10000 * (1 - x[(pkg1['Package Identifier'], uld)] - x[(pkg2['Package Identifier'], uld)]),
#                         constraint_name + "_x_reverse"
#                     )

#                     prob += (
#                         y1 + pkg1['Width (cm)'] <= y2 + 10000 * (1 - x[(pkg1['Package Identifier'], uld)] - x[(pkg2['Package Identifier'], uld)]),
#                         constraint_name + "_y"
#                     )

#                     prob += (
#                         y2 + pkg2['Width (cm)'] <= y1 + 10000 * (1 - x[(pkg1['Package Identifier'], uld)] - x[(pkg2['Package Identifier'], uld)]),
#                         constraint_name + "_y_reverse"
#                     )

#                     prob += (
#                         z1 + pkg1['Height (cm)'] <= z2 + 10000 * (1 - x[(pkg1['Package Identifier'], uld)] - x[(pkg2['Package Identifier'], uld)]),
#                         constraint_name + "_z"
#                     )

#                     prob += (
#                         z2 + pkg2['Height (cm)'] <= z1 + 10000 * (1 - x[(pkg1['Package Identifier'], uld)] - x[(pkg2['Package Identifier'], uld)]),
#                         constraint_name + "_z_reverse"
#                     )

# Create constraints for non-overlapping packages
for uld in uld_df['ULD Identifier']:
    for i, pkg1 in package_df.iterrows():
        for j, pkg2 in package_df.iterrows():
            if i < j:  # Avoid redundant checks
                if (pkg1['Package Identifier'], uld) in package_coords and (pkg2['Package Identifier'], uld) in package_coords:
                    # Extract the coordinates (x, y, z) for each package
                    x1, y1, z1 = package_coords[(pkg1['Package Identifier'], uld)]
                    x2, y2, z2 = package_coords[(pkg2['Package Identifier'], uld)]

                    # Create unique constraint names for the overlap constraints
                    constraint_name = f"Overlap_{pkg1['Package Identifier']}_{pkg2['Package Identifier']}_{uld}"

                    # Ensure no overlap along the x, y, and z axes
                    prob += (x1 + pkg1['Length (cm)'] <= x2 + 10000 * (1 - x[(pkg1['Package Identifier'], uld)] - x[(pkg2['Package Identifier'], uld)]), f"{constraint_name}_x")
                    prob += (x2 + pkg2['Length (cm)'] <= x1 + 10000 * (1 - x[(pkg1['Package Identifier'], uld)] - x[(pkg2['Package Identifier'], uld)]), f"{constraint_name}_x_reverse")

                    prob += (y1 + pkg1['Width (cm)'] <= y2 + 10000 * (1 - x[(pkg1['Package Identifier'], uld)] - x[(pkg2['Package Identifier'], uld)]), f"{constraint_name}_y")
                    prob += (y2 + pkg2['Width (cm)'] <= y1 + 10000 * (1 - x[(pkg1['Package Identifier'], uld)] - x[(pkg2['Package Identifier'], uld)]), f"{constraint_name}_y_reverse")

                    prob += (z1 + pkg1['Height (cm)'] <= z2 + 10000 * (1 - x[(pkg1['Package Identifier'], uld)] - x[(pkg2['Package Identifier'], uld)]), f"{constraint_name}_z")
                    prob += (z2 + pkg2['Height (cm)'] <= z1 + 10000 * (1 - x[(pkg1['Package Identifier'], uld)] - x[(pkg2['Package Identifier'], uld)]), f"{constraint_name}_z_reverse")


# Solve the problem
prob.solve()

# Prepare the output
if pulp.LpStatus[prob.status] != 'Optimal':
    print("No optimal solution found.")
else:
    # Total Cost
    total_cost = pulp.value(prob.objective)

    # Count packed packages and ULDs with Priority Packages
    packed_packages = []
    priority_uld_ids = set()

    for (pkg, uld) in feasible_assignments:
        if pulp.value(x[(pkg, uld)]) == 1:
            packed_packages.append(pkg)
            if package_type_dict[pkg] == 'Priority':
                priority_uld_ids.add(uld)

    # First line of output
    total_packed = len(packed_packages)
    total_priority_uld = len(priority_uld_ids)
    output = f"{total_cost},{total_packed},{total_priority_uld}\n"

    # Subsequent lines: Package details
    for pkg in package_df['Package Identifier']:
        uld_id = 'NONE'
        if package_type_dict[pkg] == 'Economy' and pulp.value(z[pkg]) == 1:
            uld_id = 'NONE'
            coordinates = '-1,-1,-1,-1,-1,-1'
        else:
            for uld in uld_df['ULD Identifier']:
                if pulp.value(x[(pkg, uld)]) == 1:
                    uld_id = uld
                    package = package_df[package_df['Package Identifier'] == pkg].iloc[0]
                    length, width, height = package['Length (cm)'], package['Width (cm)'], package['Height (cm)']
                    coordinates = f"0,0,0,{length},{width},{height}"
                    break

        # Add package line to the output
        output += f"{pkg},{uld_id},{coordinates}\n"

    # Save to output file
    with open("output2.txt", "w") as f:
        f.write(output)
    
    print("Output written to output2.txt")

# Parse Package Data
package_df = pd.read_csv(StringIO(package_data))
package_df = package_df.fillna({'Cost of Delay': 0})  # Replace NaN with 0 for Priority packages
package_df['Volume'] = package_df['Length (cm)'] * package_df['Width (cm)'] * package_df['Height (cm)']

# Identify Priority and Economy packages
priority_packages = package_df[package_df['Type (P/E)'] == 'Priority']
economy_packages = package_df[package_df['Type (P/E)'] == 'Economy']

# Create mappings for efficiency
package_df['Cost of Delay'] = pd.to_numeric(package_df['Cost of Delay'], errors='coerce').fillna(0)
cost_delay_dict = dict(zip(package_df['Package Identifier'], package_df['Cost of Delay']))
package_type_dict = dict(zip(package_df['Package Identifier'], package_df['Type (P/E)']))

# Function to check if a package fits in a ULD
def fits(uld, pkg):
    return (pkg['Length (cm)'] <= uld['Length (cm)']) and \
           (pkg['Width (cm)'] <= uld['Width (cm)']) and \
           (pkg['Height (cm)'] <= uld['Height (cm)'])

# Create a list of feasible assignments
feasible_assignments = []

for idx_p, pkg in package_df.iterrows():
    for idx_u, uld in uld_df.iterrows():
        if fits(uld, pkg):
            feasible_assignments.append((pkg['Package Identifier'], uld['ULD Identifier']))

# Convert to DataFrame for easier handling
feasible_df = pd.DataFrame(feasible_assignments, columns=['Package', 'ULD'])

# Initialize the problem
prob = pulp.LpProblem("FedEx_ULD_Packing", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("assign",
                          ((pkg, uld) for pkg, uld in feasible_assignments),
                          cat='Binary')

z = pulp.LpVariable.dicts("not_assign",
                          (pkg for pkg in economy_packages['Package Identifier']),
                          cat='Binary')

s = pulp.LpVariable.dicts("ULD_has_Priority",
                          (uld for uld in uld_df['ULD Identifier']),
                          cat='Binary')

# Objective Function
K = 5000  # Cost per ULD carrying Priority packages

prob += (
    pulp.lpSum([
        z[pkg] * cost_delay_dict.get(pkg, 0)  # Cost of Delay for Economy packages
        for pkg in economy_packages['Package Identifier']
    ]) +
    K * pulp.lpSum([s[uld] for uld in uld_df['ULD Identifier']])
, "Total Cost")

# Assignment Constraints
for pkg in package_df['Package Identifier']:
    if package_type_dict.get(pkg) == 'Economy':
        prob += (
            pulp.lpSum([x[(pkg, uld)] for uld in uld_df['ULD Identifier'] if (pkg, uld) in feasible_assignments]) + z[pkg] == 1,
            f"Assignment_{pkg}"
        )
    elif package_type_dict.get(pkg) == 'Priority':
        # Priority packages must be assigned to exactly one ULD
        prob += (
            pulp.lpSum([x[(pkg, uld)] for uld in uld_df['ULD Identifier'] if (pkg, uld) in feasible_assignments]) == 1,
            f"Assignment_Priority_{pkg}"
        )

# ULD Weight Limit Constraints
for idx_u, uld in uld_df.iterrows():
    uld_id = uld['ULD Identifier']
    prob += (
        pulp.lpSum([
            x[(pkg, uld_id)] * package_df.loc[package_df['Package Identifier'] == pkg, 'Weight (kg)'].values[0]
            for pkg in package_df['Package Identifier'] if (pkg, uld_id) in feasible_assignments
        ]) <= uld['Weight Limit (kg)'],
        f"Weight_Limit_{uld_id}"
    )

# ULD Volume Limit Constraints
for idx_u, uld in uld_df.iterrows():
    uld_id = uld['ULD Identifier']
    uld_volume = uld['Volume']
    prob += (
        pulp.lpSum([
            x[(pkg, uld_id)] * package_df.loc[package_df['Package Identifier'] == pkg, 'Volume'].values[0]
            for pkg in package_df['Package Identifier'] if (pkg, uld_id) in feasible_assignments
        ]) <= uld_volume,
        f"Volume_Limit_{uld_id}"
    )

# Solve the problem
prob.solve()

# Prepare the output
if pulp.LpStatus[prob.status] != 'Optimal':
    print("No optimal solution found.")
else:
    # Total Cost
    total_cost = pulp.value(prob.objective)

    # Count packed packages and ULDs with Priority Packages
    packed_packages = []
    priority_uld_ids = set()

    for (pkg, uld) in feasible_assignments:
        if pulp.value(x[(pkg, uld)]) == 1:
            packed_packages.append(pkg)
            if package_type_dict[pkg] == 'Priority':
                priority_uld_ids.add(uld)

    # First line of output
    total_packed = len(packed_packages)
    total_priority_uld = len(priority_uld_ids)
    output = f"{total_cost},{total_packed},{total_priority_uld}\n"

    # Subsequent lines: Package details
    for pkg in package_df['Package Identifier']:
        uld_id = 'NONE'
        if package_type_dict[pkg] == 'Economy' and pulp.value(z[pkg]) == 1:
            uld_id = 'NONE'
            coordinates = '-1,-1,-1,-1,-1,-1'
        else:
            for uld in uld_df['ULD Identifier']:
                if pulp.value(x[(pkg, uld)]) == 1:
                    uld_id = uld
                    package = package_df[package_df['Package Identifier'] == pkg].iloc[0]
                    length, width, height = package['Length (cm)'], package['Width (cm)'], package['Height (cm)']
                    coordinates = f"0,0,0,{length},{width},{height}"
                    break

        # Add package line to the output
        output += f"{pkg},{uld_id},{coordinates}\n"

    # Save to output file
    with open("output2.txt", "w") as f:
        f.write(output)
    
    print("Output written to output2.txt")


'''
# Parse Package Data
package_df = pd.read_csv(StringIO(package_data))
package_df = package_df.fillna({'Cost of Delay': 0})  # Replace NaN with 0 for Priority packages
package_df['Volume'] = package_df['Length (cm)'] * package_df['Width (cm)'] * package_df['Height (cm)']

# Identify Priority and Economy packages
priority_packages = package_df[package_df['Type (P/E)'] == 'Priority']
economy_packages = package_df[package_df['Type (P/E)'] == 'Economy']

# Create mappings for efficiency
package_df['Cost of Delay'] = pd.to_numeric(package_df['Cost of Delay'], errors='coerce').fillna(0)
cost_delay_dict = dict(zip(package_df['Package Identifier'], package_df['Cost of Delay']))
package_type_dict = dict(zip(package_df['Package Identifier'], package_df['Type (P/E)']))

# Function to check if a package fits in a ULD
def fits(uld, pkg):
    return (pkg['Length (cm)'] <= uld['Length (cm)']) and \
           (pkg['Width (cm)'] <= uld['Width (cm)']) and \
           (pkg['Height (cm)'] <= uld['Height (cm)'])

# Create a list of feasible assignments
feasible_assignments = []

for idx_p, pkg in package_df.iterrows():
    for idx_u, uld in uld_df.iterrows():
        if fits(uld, pkg):
            feasible_assignments.append((pkg['Package Identifier'], uld['ULD Identifier']))

# Convert to DataFrame for easier handling
feasible_df = pd.DataFrame(feasible_assignments, columns=['Package', 'ULD'])

# Initialize the problem
prob = pulp.LpProblem("FedEx_ULD_Packing", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("assign",
                          ((pkg, uld) for pkg, uld in feasible_assignments),
                          cat='Binary')

z = pulp.LpVariable.dicts("not_assign",
                          (pkg for pkg in economy_packages['Package Identifier']),
                          cat='Binary')

s = pulp.LpVariable.dicts("ULD_has_Priority",
                          (uld for uld in uld_df['ULD Identifier']),
                          cat='Binary')

# Objective Function
K = 5000  # Cost per ULD carrying Priority packages

prob += (
    pulp.lpSum([
        z[pkg] * cost_delay_dict.get(pkg, 0)  # Cost of Delay for Economy packages
        for pkg in economy_packages['Package Identifier']
    ]) +
    K * pulp.lpSum([s[u] for u in uld_df['ULD Identifier']])
, "Total Cost")

# Assignment Constraints
for pkg in package_df['Package Identifier']:
    if package_type_dict.get(pkg) == 'Economy':
        prob += (
            pulp.lpSum([x[(pkg, uld)] for uld in uld_df['ULD Identifier'] if (pkg, uld) in feasible_assignments]) + z[pkg] == 1,
            f"Assignment_{pkg}"
        )
    elif package_type_dict.get(pkg) == 'Priority':
        # Priority packages must be assigned to exactly one ULD
        prob += (
            pulp.lpSum([x[(pkg, uld)] for uld in uld_df['ULD Identifier'] if (pkg, uld) in feasible_assignments]) == 1,
            f"Assignment_Priority_{pkg}"
        )

# ULD Weight Limit Constraints
for idx_u, uld in uld_df.iterrows():
    uld_id = uld['ULD Identifier']
    prob += (
        pulp.lpSum([
            x[(pkg, uld_id)] * package_df.loc[package_df['Package Identifier'] == pkg, 'Weight (kg)'].values[0]
            for pkg in package_df['Package Identifier'] if (pkg, uld_id) in feasible_assignments
        ]) <= uld['Weight Limit (kg)'],
        f"Weight_Limit_{uld_id}"
    )

# ULD Volume Limit Constraints
for idx_u, uld in uld_df.iterrows():
    uld_id = uld['ULD Identifier']
    uld_volume = uld['Volume']
    prob += (
        pulp.lpSum([
            x[(pkg, uld_id)] * package_df.loc[package_df['Package Identifier'] == pkg, 'Volume'].values[0]
            for pkg in package_df['Package Identifier'] if (pkg, uld_id) in feasible_assignments
        ]) <= uld_volume,
        f"Volume_Limit_{uld_id}"
    )

# Solve the problem
prob.solve()

# Status of the solution
print(f"Status: {pulp.LpStatus[prob.status]}")

# Check if the solution is optimal
if pulp.LpStatus[prob.status] != 'Optimal':
    print("No optimal solution found.")
else:
    # Total Cost
    total_cost = pulp.value(prob.objective)
    print(f"Total Cost: {total_cost}")

    # Package Assignments
    assignments = []

    # Assigned Packages
    for (pkg, uld) in feasible_assignments:
        if pulp.value(x[(pkg, uld)]) == 1:
            assignments.append((pkg, uld, 'Assigned'))

    # Not Assigned Economy Packages
    for pkg in economy_packages['Package Identifier']:
        if pulp.value(z[pkg]) == 1:
            assignments.append((pkg, 'NONE', 'Not Assigned'))

    # Convert to DataFrame
    assignments_df = pd.DataFrame(assignments, columns=['Package', 'ULD', 'Status'])

    # Display a summary instead of printing all 400 entries
    print("\nPackage Assignments Summary:")
    print(assignments_df.groupby(['ULD', 'Status']).size().unstack(fill_value=0))

    # ULDs Carrying Priority Packages
    priority_uld = [uld for uld in uld_df['ULD Identifier'] if pulp.value(s[uld]) == 1]
    print(f"\nULDs carrying Priority Packages: {priority_uld}")

    # Packing Fractions
    packing_fractions = []

    # Improved: Packing with No Overlaps
    uld_weights = {uld: 0 for uld in uld_df['ULD Identifier']}
    uld_coordinates = {uld: [] for uld in uld_df['ULD Identifier']}
    package_coords = {}

    # Track used positions to avoid overlaps
    used_positions = {uld: [] for uld in uld_df['ULD Identifier']}

    for (pkg, uld) in feasible_assignments:
        if pulp.value(x[(pkg, uld)]) == 1:
            package = package_df[package_df['Package Identifier'] == pkg].iloc[0]
            length, width, height = package['Length (cm)'], package['Width (cm)'], package['Height (cm)']
            weight = package['Weight (kg)']

            # Search for a valid position in the ULD
            placed = False
            for start_x in range(0, uld_df[uld_df['ULD Identifier'] == uld]['Length (cm)'].values[0] - length, length):
                for start_y in range(0, uld_df[uld_df['ULD Identifier'] == uld]['Width (cm)'].values[0] - width, width):
                    if (start_x, start_y) not in used_positions[uld]:
                        # Check if package fits within the ULD space
                        uld_weights[uld] += weight
                        uld_coordinates[uld].append((start_x, start_y, start_x + length, start_y + width))
                        used_positions[uld].append((start_x, start_y))
                        package_coords[pkg] = (start_x, start_y, start_x + length, start_y + width)
                        placed = True
                        break
                if placed:
                    break

            if not placed:
                print(f"Package {pkg} could not be placed in ULD {uld}")
    
    # Displaying the updated packing information
    print("\nPacking Coordinates for each Package:")
    for pkg, coord in package_coords.items():
        print(f"Package {pkg} placed at {coord}")
'''