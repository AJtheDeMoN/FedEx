import pulp
import pandas as pd
from io import StringIO
import os

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