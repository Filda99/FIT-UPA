import json
from tqdm import tqdm
import time
from collections import defaultdict

# Define the input and output file paths
input_geojson_file = "Traffic_accidents.geojson"
output_filtered_json_file = 'accidents.json'

# Define the attributes to remove
attributes_to_remove = ['OBJECTID', 'id', 'd', 'e', 'den', 'cas', 'hodina', 'mesic', 'smrt_dny', 'smrt_po', 'ovlivneni_ridice', 'kategorie_chodce', 'stav_chodce', 'chovani_chodce', 'situace_nehody', 'prvni_pomoc', 'nasledky_chodce', 'id_vozidla', 'id_nehody', 'geometry']  # Add all redundant attributes here

# Load the GeoJSON data
with open(input_geojson_file, 'r', encoding='utf-8') as geojson_file:
    data = json.load(geojson_file)

# Remove specified attributes and create a new filtered JSON
filtered_features = []
for feature in data['features']:
    properties = feature['properties']
    for attribute in attributes_to_remove:
        properties.pop(attribute, None)  # Remove the attribute if it exists
    # Rename 'GlobalID' to '_id'
    if 'GlobalID' in properties:
        properties['_id'] = properties.pop('GlobalID')
     # Lowercase all values (except "ZSJ" and "MC")
    for key, value in properties.items():
        if key != 'ZSJ' and key != 'MC' and value:
            if isinstance(value, str):
                properties[key] = value.lower()
    filtered_features.append(properties)  # Only add the properties, not the geometry

# Save the filtered JSON data to a new file
with open(output_filtered_json_file, 'w', encoding='utf-8') as output_file:
    json.dump(filtered_features, output_file, ensure_ascii=False, indent=4)

######################################################################
######################################################################
# Load the filtered JSON data
input_filtered_json_file = output_filtered_json_file

with open(input_filtered_json_file, 'r', encoding='utf-8') as filtered_json_file:
    data = json.load(filtered_json_file)

# Create a dictionary to store location data
locations = defaultdict(list)

# Iterate through the filtered data and group accidents by location
for accident in data:
    location_name = accident['MC']  # Assuming 'MC' contains the location name
    accident_id = accident['_id']  # Assuming '_id' is the accident ID
    
    # Add the accident ID to the list of accident IDs for this location
    locations[location_name].append(accident_id)

# Convert the dictionary to a list of location objects with "name" and "accident_ids" attributes
locations_list = [{'_id': name, 'accident_ids': accident_ids} for name, accident_ids in locations.items()]

# Save the location data as a JSON file
output_locations_json_file = 'locations.json'

with open(output_locations_json_file, 'w', encoding='utf-8') as locations_json_file:
    json.dump(locations_list, locations_json_file, ensure_ascii=False, indent=4)
