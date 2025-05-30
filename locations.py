from collections import defaultdict

def normalize_device(name: str) -> str:
    return name.strip().upper()

device_locations = defaultdict(set)
device_first_seen = {}

input_file = "fiber_connections.txt"
output_file = "device_location_summary.txt"

with open(input_file, "r", encoding="utf-8") as file:
    current_location = ""
    current_device = ""

    for line_number, line in enumerate(file, start=1):
        line = line.strip()

        if line.startswith("Location: "):
            current_location = line.replace("Location: ", "").strip()

        elif line.startswith("Device: "):
            raw_device = line.replace("Device: ", "").strip()
            device = normalize_device(raw_device)
            device_locations[device].add(current_location)

            if device not in device_first_seen:
                device_first_seen[device] = line_number

# Sort devices by first appearance
sorted_devices = sorted(device_first_seen.items(), key=lambda x: x[1])

# Output to terminal and file
with open(output_file, "w", encoding="utf-8") as out:
    print("\n📡 Device appearances across locations (standardized):\n")
    out.write("📡 Device appearances across locations (standardized):\n\n")

    for device, _ in sorted_devices:
        locations = sorted(device_locations[device])
        print(f"Device: {device}")
        out.write(f"Device: {device}\n")
        for loc in locations:
            print(f"  - {loc}")
            out.write(f"  - {loc}\n")
        print()
        out.write("\n")
