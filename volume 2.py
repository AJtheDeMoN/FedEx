# Open the text file and read the data
file_path = 'Package.txt'  # Replace with your file path

with open(file_path, 'r') as file:
    lines = file.readlines()

# Parse the data
packages = []
for line in lines[1:]:  # Skip the first line (assumes it's a count)
    parts = line.strip().split(',')
    if len(parts) == 7:
        name, l, b, h, weight, priority, cost = parts
        packages.append({
            "name": name,
            "length": int(l),
            "breadth": int(b),
            "height": int(h),
            "weight": int(weight),
            "priority": priority,
            "cost": int(cost) if cost != '-' else None
        })

# Separate into Economy and Priority
economy_packages = [pkg for pkg in packages if pkg["priority"] == "Economy"]
priority_packages = [pkg for pkg in packages if pkg["priority"] == "Priority"]

# Calculate volume and sort packages
for pkg in packages:
    pkg["volume"] = pkg["length"] * pkg["breadth"] * pkg["height"]

economy_packages = sorted(
    economy_packages,
    key=lambda pkg: (pkg["length"] * pkg["breadth"] * pkg["height"]) / pkg["cost"],
    reverse=False  # Higher ratio first
)
priority_packages.sort(key=lambda x: x["name"])

TotalVolume = 105171504

volPriority = 0
print("\nPriority Packages:")
for pkg in priority_packages:
    volPriority += pkg['volume']

print(volPriority)
TotalVolume -= volPriority

# Display the results
print("Economy Packages:")
print(TotalVolume)
areaEco = 0
cost = 0
cnt =0
for pkg in economy_packages:
    if TotalVolume-pkg['volume'] < 0:
        cost += pkg['cost']
        print(cnt,":",cost)
        cnt +=1
    else:
        TotalVolume -= pkg['volume']
        areaEco += pkg['volume']
print(areaEco)
print("cnt",cnt)
cost += 3*5000
print(cost)
