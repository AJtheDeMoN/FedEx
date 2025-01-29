import pulp
import pandas as pd
from io import StringIO
import os

# ULD Data
uld_data = """ULD Identifier,Length (cm),Width (cm),Height (cm),Weight Limit (kg)
U1,224,318,162,2500
U2,224,318,162,2500
U3,244,318,244,2800
U4,244,318,244,2800
U5,244,318,285,3500
U6,244,318,285,3500"""

# Parse ULD Data
uld_df = pd.read_csv(StringIO(uld_data))
uld_df['Volume'] = uld_df['Length (cm)'] * uld_df['Width (cm)'] * uld_df['Height (cm)']

# Package Data (Ensure all 400 packages are included here)
package_data = """Package Identifier,Length (cm),Width (cm),Height (cm),Weight (kg),Type (P/E),Cost of Delay
P-1,99,53,55,61,Economy,176
P-2,56,99,81,53,Priority,-
P-3,42,101,51,17,Priority,-
...
P-399,45,44,89,22,Economy,63
P-400,52,50,64,37,Economy,71
"""

# Replace '...' with actual package data or ensure the full data is included
# For this example, we'll use the complete package_data as provided earlier.

# Parse Package Data
package_df = pd.read_csv(StringIO(package_data))
package_df = package_df.fillna({'Cost of Delay': 0})  # Replace NaN with 0 for Priority packages
package_df['Volume'] = package_df['Length (cm)'] * package_df['Width (cm)'] * package_df['Height (cm)']

# Identify Priority and Economy packages
priority_packages = package_df[package_df['Type (P/E)'] == 'Priority']
economy_packages = package_df[package_df['Type (P/E)'] == 'Economy']

# Create mappings for efficiency

# cost_delay_dict = dict(zip(package_df['Package Identifier'], package_df['Cost of Delay']))

# Change
package_df['Cost of Delay'] = pd.to_numeric(package_df['Cost of Delay'], errors='coerce').fillna(0)
cost_delay_dict = dict(zip(package_df['Package Identifier'], package_df['Cost of Delay']))


package_type_dict = dict(zip(package_df['Package Identifier'], package_df['Type (P/E)']))

# Verify that all Economy packages have a Cost of Delay
missing_cost_delay = [pkg for pkg in economy_packages['Package Identifier'] if pkg not in cost_delay_dict]
if missing_cost_delay:
    print(f"Warning: The following Economy packages are missing Cost of Delay and will be assigned 0: {missing_cost_delay}")
    for pkg in missing_cost_delay:
        cost_delay_dict[pkg] = 0

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

# ULD Carrying Priority Packages Constraints
for idx_u, uld in uld_df.iterrows():
    uld_id = uld['ULD Identifier']
    priority_pkgs = priority_packages['Package Identifier'].tolist()
    
    # Constraint: If any Priority package is assigned to ULD u, then s[u] = 1
    prob += (
        pulp.lpSum([x[(pkg, uld_id)] for pkg in priority_pkgs if (pkg, uld_id) in feasible_assignments]) <= len(priority_pkgs) * s[uld_id],
        f"Priority_Definition_{uld_id}"
    )
    
    # Constraint: If s[u] = 1, at least one Priority package must be assigned
    prob += (
        pulp.lpSum([x[(pkg, uld_id)] for pkg in priority_pkgs if (pkg, uld_id) in feasible_assignments]) >= s[uld_id],
        f"Priority_Assignment_{uld_id}"
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

# # Solve the problem
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

    for idx_u, uld in uld_df.iterrows():
        uld_id = uld['ULD Identifier']
        uld_volume = uld['Volume']
        assigned_volume = sum([
            package_df.loc[package_df['Package Identifier'] == pkg, 'Volume'].values[0]
            for (pkg, uld_assigned) in feasible_assignments
            if uld_assigned == uld_id and pulp.value(x.get((pkg, uld_id), 0)) == 1
        ])
        fraction = assigned_volume / uld_volume if uld_volume > 0 else 0
        packing_fractions.append((uld_id, round(fraction, 4)))  # Rounded to 4 decimal places

    packing_df = pd.DataFrame(packing_fractions, columns=['ULD', 'Packing Fraction'])
    print("\nPacking Fractions:")
    print(packing_df)

    # Optional: Detailed Package Assignments
    # Uncomment the following lines to see detailed assignments
    print("\nDetailed Package Assignments:")
    print(assignments_df.sort_values(by=['ULD', 'Package']))


# Initialize weights and coordinates for ULDs
uld_weights = {uld: 0 for uld in uld_df['ULD Identifier']}
uld_coordinates = {uld: [] for uld in uld_df['ULD Identifier']}
package_coords = {}

# Define the starting coordinates (assumes packages are packed systematically starting at one corner)
start_x, start_y, start_z = 0, 0, 0

# Process the assignments
for (pkg, uld) in feasible_assignments:
    if pulp.value(x[(pkg, uld)]) == 1:
        package = package_df[package_df['Package Identifier'] == pkg].iloc[0]
        length, width, height = package['Length (cm)'], package['Width (cm)'], package['Height (cm)']
        weight = package['Weight (kg)']
        
        # Assign coordinates within the ULD
        x0, y0, z0 = start_x, start_y, start_z
        x1, y1, z1 = x0 + length, y0 + width, z0 + height
        
        # Update ULD weights and coordinates
        uld_weights[uld] += weight
        uld_coordinates[uld].append((pkg, (x0, y0, z0, x1, y1, z1)))
        
        # Track package coordinates
        package_coords[pkg] = (uld, x0, y0, z0, x1, y1, z1)
        
        # Update starting position for the next package (simple heuristic, can be improved for better packing)
        start_x = x1  # Move along x-axis
        if start_x >= uld_df[uld_df['ULD Identifier'] == uld]['Length (cm)'].values[0]:
            start_x = 0
            start_y = y1
        if start_y >= uld_df[uld_df['ULD Identifier'] == uld]['Width (cm)'].values[0]:
            start_y = 0
            start_z = z1

# Output Format
output_lines = []

# Total Cost
total_cost = pulp.value(prob.objective)
total_packed = sum([1 for pkg, uld in feasible_assignments if pulp.value(x[(pkg, uld)]) == 1])
priority_uld_count = sum([1 for uld in uld_df['ULD Identifier'] if pulp.value(s[uld]) == 1])

output_lines.append(f"{int(total_cost)},{total_packed},{priority_uld_count}")

# Package Details
for pkg in package_df['Package Identifier']:
    if pkg in package_coords:
        uld, x0, y0, z0, x1, y1, z1 = package_coords[pkg]
        output_lines.append(f"{pkg},{uld},{x0},{y0},{z0},{x1},{y1},{z1}")
    else:
        # Not assigned packages
        output_lines.append(f"{pkg},NONE,-1,-1,-1,-1,-1,-1")

# Save to a text file
output_file = "output2.txt"
with open(output_file, "w") as file:
    file.write("\n".join(output_lines))

# Packing Efficiency and Weights
print("\nPacking Efficiency and Weights:")
for uld in uld_df['ULD Identifier']:
    assigned_volume = sum([
        package_df.loc[package_df['Package Identifier'] == pkg, 'Volume'].values[0]
        for (pkg, uld_assigned) in feasible_assignments
        if uld_assigned == uld and pulp.value(x.get((pkg, uld), 0)) == 1
    ])
    uld_volume = uld_df[uld_df['ULD Identifier'] == uld]['Volume'].values[0]
    efficiency = assigned_volume / uld_volume if uld_volume > 0 else 0
    weight = uld_weights[uld]
    print(f"ULD {uld}: Efficiency = {efficiency:.4f}, Total Weight = {weight} kg")

# Notify about the output
print(f"\nResults written to {output_file}.")
