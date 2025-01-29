import pulp
import pandas as pd
from io import StringIO
import os
import threading
import time


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
P-121,79,108,80,99,Economy,124
P-122,77,104,46,67,Economy,105
P-123,43,62,40,7,Economy,75
P-124,54,104,72,96,Priority,-
P-125,68,85,91,139,Priority,-
P-126,85,64,60,94,Priority,-
P-127,71,78,67,79,Economy,66
P-128,79,102,66,44,Economy,92
P-129,110,59,85,64,Priority,-
P-130,78,45,40,18,Economy,79
P-131,82,80,79,84,Economy,109
P-132,92,102,42,115,Economy,77
P-133,63,109,91,174,Priority,-
P-134,80,88,97,150,Priority,-
P-135,108,66,45,56,Economy,132
P-136,47,66,102,36,Priority,-
P-137,59,110,96,108,Economy,120
P-138,85,80,89,142,Economy,87
P-139,96,84,75,123,Priority,-
P-140,84,106,65,60,Economy,119
P-141,70,43,87,34,Economy,70
P-142,92,74,83,169,Priority,-
P-143,82,100,106,206,Economy,76
P-144,59,72,106,120,Economy,111
P-145,75,106,79,66,Priority,-
P-146,100,45,56,46,Economy,92
P-147,65,46,55,36,Priority,-
P-148,67,100,49,50,Priority,-
P-149,63,45,104,76,Economy,84
P-150,54,42,58,12,Priority,-
P-151,44,106,79,23,Economy,89
P-152,67,57,49,39,Economy,73
P-153,62,64,51,59,Economy,62
P-154,64,103,91,47,Economy,118
P-155,95,87,47,95,Economy,99
P-156,47,73,110,57,Economy,124
P-157,88,88,54,30,Priority,-
P-158,72,107,95,135,Economy,61
P-159,50,92,52,15,Economy,66
P-160,108,82,99,232,Economy,84
P-161,78,97,62,127,Economy,67
P-162,46,104,65,36,Priority,-
P-163,49,83,83,45,Priority,-
P-164,102,40,87,99,Economy,124
P-165,103,96,93,267,Priority,-
P-166,84,62,103,142,Economy,134
P-167,47,50,100,33,Economy,124
P-168,68,87,88,109,Priority,-
P-169,48,87,94,102,Economy,136
P-170,100,81,44,39,Economy,120
P-171,50,55,93,55,Economy,110
P-172,51,71,76,22,Economy,112
P-173,92,81,89,130,Economy,81
P-174,107,101,47,107,Economy,127
P-175,66,88,96,127,Economy,121
P-176,60,62,102,42,Economy,87
P-177,44,41,99,17,Economy,77
P-178,78,69,96,97,Economy,98
P-179,62,73,63,38,Economy,84
P-180,80,71,59,43,Priority,-
P-181,98,58,57,93,Priority,-
P-182,45,70,78,42,Economy,65
P-183,105,72,57,37,Priority,-
P-184,88,96,74,129,Economy,84
P-185,42,67,100,52,Economy,133
P-186,47,84,93,60,Economy,118
P-187,54,84,78,97,Priority,-
P-188,86,51,51,12,Priority,-
P-189,56,63,87,66,Economy,121
P-190,108,101,52,143,Economy,128
P-191,100,71,94,123,Economy,64
P-192,54,76,74,33,Economy,106
P-193,72,87,67,113,Economy,75
P-194,71,48,109,97,Economy,116
P-195,102,57,72,62,Economy,90
P-196,64,107,66,85,Economy,60
P-197,109,82,99,68,Economy,85
P-198,74,59,84,68,Economy,113
P-199,58,67,73,59,Priority,-
P-200,74,74,83,81,Economy,95
P-201,80,106,76,159,Economy,139
P-202,52,94,40,57,Economy,105
P-203,68,106,93,52,Economy,63
P-204,55,88,103,150,Economy,101
P-205,47,40,109,24,Economy,107
P-206,60,47,41,29,Economy,85
P-207,70,45,95,46,Priority,-
P-208,89,50,102,117,Economy,127
P-209,75,44,72,57,Economy,74
P-210,45,93,88,64,Economy,67
P-211,96,95,81,142,Priority,-
P-212,105,74,48,96,Priority,-
P-213,71,50,105,94,Economy,66
P-214,58,81,61,40,Priority,-
P-215,87,89,80,126,Priority,-
P-216,44,64,83,57,Priority,-
P-217,78,74,72,97,Priority,-
P-218,90,77,59,63,Economy,134
P-219,94,61,76,57,Priority,-
P-220,44,104,71,80,Economy,137
P-221,68,44,49,13,Economy,86
P-222,88,73,41,59,Priority,-
P-223,83,92,109,145,Economy,66
P-224,68,99,56,103,Priority,-
P-225,54,68,93,52,Economy,98
P-226,60,72,74,27,Priority,-
P-227,59,73,96,58,Economy,118
P-228,98,92,51,128,Economy,75
P-229,69,81,104,171,Economy,116
P-230,46,48,86,44,Economy,82
P-231,96,68,49,48,Economy,91
P-232,67,84,47,38,Priority,-
P-233,71,59,101,120,Economy,63
P-234,43,65,104,60,Economy,101
P-235,80,105,84,61,Economy,95
P-236,91,56,56,57,Priority,-
P-237,97,74,101,193,Economy,97
P-238,50,69,102,74,Priority,-
P-239,79,85,71,94,Economy,93
P-240,101,88,65,84,Economy,127
P-241,71,74,91,25,Economy,115
P-242,89,69,53,48,Economy,118
P-243,69,77,105,98,Economy,76
P-244,76,62,75,24,Economy,111
P-245,53,105,80,61,Economy,67
P-246,60,102,61,58,Economy,106
P-247,98,62,79,61,Economy,136
P-248,77,67,52,70,Economy,139
P-249,89,67,55,66,Economy,88
P-250,65,59,102,105,Economy,89
P-251,78,44,106,106,Economy,71
P-252,48,110,95,139,Priority,-
P-253,91,49,99,99,Economy,98
P-254,99,51,79,101,Economy,72
P-255,64,98,96,78,Priority,-
P-256,92,64,66,117,Economy,99
P-257,67,51,54,40,Economy,103
P-258,71,55,82,43,Economy,138
P-259,84,72,86,55,Economy,98
P-260,43,49,99,20,Economy,65
P-261,100,77,42,80,Economy,114
P-262,103,92,109,99,Economy,65
P-263,56,83,98,33,Economy,107
P-264,60,68,108,35,Priority,-
P-265,47,60,58,37,Priority,-
P-266,61,88,53,37,Priority,-
P-267,54,97,98,130,Economy,116
P-268,84,63,100,99,Economy,95
P-269,58,56,74,25,Economy,85
P-270,52,70,47,12,Priority,-
P-271,41,44,92,30,Economy,63
P-272,75,64,40,54,Economy,133
P-273,85,79,71,127,Priority,-
P-274,75,88,110,114,Priority,-
P-275,74,77,45,31,Priority,-
P-276,46,69,62,29,Economy,70
P-277,54,108,105,93,Priority,-
P-278,73,44,80,60,Economy,96
P-279,85,99,52,118,Economy,101
P-280,90,61,53,75,Priority,-
P-281,55,84,105,57,Economy,95
P-282,107,92,54,147,Priority,-
P-283,100,97,66,79,Priority,-
P-284,70,110,52,86,Priority,-
P-285,81,108,54,78,Priority,-
P-286,93,75,73,133,Economy,102
P-287,99,86,84,94,Economy,110
P-288,61,101,94,36,Economy,122
P-289,70,43,66,28,Economy,79
P-290,80,69,46,23,Economy,64
P-291,74,81,40,42,Economy,124
P-292,63,100,93,46,Economy,66
P-293,56,104,56,78,Economy,81
P-294,88,93,44,30,Economy,69
P-295,49,109,69,32,Priority,-
P-296,92,81,93,50,Economy,60
P-297,103,101,68,149,Priority,-
P-298,44,91,86,57,Economy,83
P-299,83,87,80,55,Priority,-
P-300,97,69,101,57,Priority,-
P-301,61,72,69,76,Economy,72
P-302,64,106,65,98,Economy,84
P-303,57,62,106,75,Economy,85
P-304,51,68,89,31,Priority,-
P-305,53,58,63,22,Economy,104
P-306,88,91,90,57,Economy,106
P-307,43,82,96,100,Economy,123
P-308,57,64,110,62,Economy,87
P-309,104,91,60,135,Economy,66
P-310,65,59,43,15,Priority,-
P-311,79,101,43,26,Economy,69
P-312,90,97,56,121,Economy,120
P-313,91,54,54,73,Economy,120
P-314,84,53,93,48,Economy,93
P-315,50,75,53,14,Economy,104
P-316,105,103,71,201,Economy,123
P-317,53,86,50,44,Economy,89
P-318,86,75,99,47,Economy,89
P-319,48,102,101,144,Priority,-
P-320,64,53,57,55,Priority,-
P-321,71,78,98,92,Economy,91
P-322,45,66,102,72,Economy,104
P-323,72,98,97,183,Economy,129
P-324,68,40,41,27,Economy,122
P-325,80,63,77,93,Economy,74
P-326,84,51,45,17,Economy,136
P-327,58,96,44,18,Economy,119
P-328,50,78,82,57,Economy,72
P-329,94,65,58,26,Priority,-
P-330,105,106,97,271,Economy,75
P-331,71,43,88,64,Economy,91
P-332,57,103,79,63,Economy,108
P-333,100,85,72,59,Priority,-
P-334,65,99,54,103,Economy,102
P-335,91,57,95,47,Economy,140
P-336,49,68,72,33,Economy,114
P-337,40,77,102,52,Economy,102
P-338,46,88,87,75,Economy,70
P-339,54,76,76,80,Economy,94
P-340,103,90,49,66,Economy,98
P-341,72,87,57,50,Economy,109
P-342,63,66,78,83,Economy,85
P-343,107,67,77,98,Economy,130
P-344,55,89,92,111,Economy,95
P-345,43,78,47,43,Priority,-
P-346,83,95,110,54,Priority,-
P-347,53,105,102,96,Economy,116
P-348,89,77,56,60,Economy,89
P-349,99,104,68,70,Economy,80
P-350,85,60,69,52,Priority,-
P-351,107,41,92,42,Economy,112
P-352,89,43,66,32,Priority,-
P-353,66,61,70,33,Priority,-
P-354,52,70,70,47,Economy,78
P-355,45,60,52,42,Economy,72
P-356,77,99,95,133,Priority,-
P-357,40,58,56,15,Economy,110
P-358,81,60,74,55,Economy,93
P-359,101,86,98,188,Economy,103
P-360,80,76,53,23,Priority,-
P-361,65,61,51,55,Economy,68
P-362,75,61,86,99,Economy,92
P-363,67,72,79,29,Economy,136
P-364,68,53,110,29,Economy,94
P-365,88,110,95,217,Priority,-
P-366,56,71,105,112,Priority,-
P-367,54,69,106,74,Economy,106
P-368,71,99,97,178,Economy,85
P-369,84,75,58,92,Economy,110
P-370,106,47,100,95,Economy,68
P-371,91,52,48,50,Economy,106
P-372,110,84,79,182,Economy,96
P-373,62,84,72,108,Economy,105
P-374,81,71,101,169,Economy,96
P-375,48,67,97,35,Economy,99
P-376,101,101,89,73,Economy,96
P-377,101,88,105,118,Economy,80
P-378,59,53,89,61,Economy,131
P-379,68,89,98,58,Economy,77
P-380,41,56,62,22,Economy,102
P-381,64,48,69,60,Economy,87
P-382,102,106,43,41,Economy,130
P-383,85,103,60,61,Economy,83
P-384,69,73,60,16,Economy,97
P-385,64,48,40,23,Economy,113
P-386,63,110,65,88,Economy,120
P-387,42,47,96,37,Economy,140
P-388,99,89,97,88,Economy,134
P-389,49,95,72,55,Economy,61
P-390,82,106,96,244,Economy,114
P-391,65,87,73,71,Economy,122
P-392,87,63,40,59,Economy,74
P-393,44,47,65,23,Economy,133
P-394,109,90,81,68,Priority,-
P-395,60,108,73,112,Economy,107
P-396,102,109,42,118,Economy,120
P-397,80,51,59,51,Economy,81
P-398,52,103,85,68,Economy,130
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
