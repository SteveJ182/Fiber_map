import pandas as pd

# Load the CSV and skip to the correct header row
df = pd.read_csv("Fiber Map(Fiber Mapping Table).csv", encoding='ISO-8859-1', skiprows=8)

# Select relevant columns: df_links = df[headers].copy()
df_links = df[
    ['Physical Location', 'Device Hostname (Logical)', 'Panel (Physical)', 'Port',
     'Device Hostname (Logical).1', 'Panel (Physical).1', 'Port.1']
].copy()

# Rename for consistency
df_links.columns = [
    'Location', 'Source Hostname', 'Source Panel', 'Source Port',
    'Dest Hostname', 'Dest Panel', 'Dest Port'
]

#replaces non data or null value with a space character to improve visual output
df_links.fillna('', inplace=True)

# Prepare Source and Destination entries
source_data = df_links[['Location', 'Source Hostname', 'Source Panel', 'Source Port']].copy()
source_data.columns = ['Location', 'Hostname', 'Panel', 'Port']
source_data['Role'] = 'Source'

dest_data = df_links[['Location', 'Dest Hostname', 'Dest Panel', 'Dest Port']].copy()
dest_data.columns = ['Location', 'Hostname', 'Panel', 'Port']
dest_data['Role'] = 'Destination'

# Combine and remove empty hostnames
combined = pd.concat([source_data, dest_data])
combined = combined[combined['Hostname'].str.strip() != '']

# Group by location and hostname
grouped = combined.groupby(['Location', 'Hostname', 'Role'])

# Collect output lines
output_lines = []
current_location = None
current_device = None

for (location, hostname, role), group in grouped:
    if location != current_location:
        #if not previous location
        #print location area
        line = f"\nLocation: {location}"
        print(line)
        #append location to output_lines []
        output_lines.append(line)
        #sets current location
        current_location = location
        current_device = None
    if hostname != current_device:
        #checks if hostname was seen in prior position
        #print hostname
        line = f"\n  Device: {hostname}"
        print(line)
        #adds hostname name to output_lines[]
        output_lines.append(line)
        current_device = hostname
    for _, row in group.iterrows():
        #.iterrows() is a method that lets you loop over the rows of a DataFrame as (index, row) pairs.
        #Each row is a pandas Series containing the data in that row.
        #The first value returned is the row's index — but in this case, it's not needed.
        #So _ is used as a conventional way to say: “I'm ignoring this value.”
        #row holds the actual row data you're interested in (like row['Panel'] and row['Port']).

        line = f"    - As {role}: Panel: {row['Panel']}, Port: {row['Port']}"
        print(line)
        output_lines.append(line)

# Save to file
with open("fiber_connections.txt", "w", encoding='utf-8') as f:
    f.write('\n'.join(output_lines))

print("\n✅ Data printed to terminal and saved to 'fiber_connections.txt'")
