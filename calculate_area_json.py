import json
import pyproj

# Load GeoJSON from a file
with open('input.json', 'r') as f:
    geojson_file = json.load(f)

# If FeatureCollection, extract first feature
if geojson_file.get('type') == 'FeatureCollection':
    feature = geojson_file['features'][0]
elif geojson_file.get('type') == 'Feature':
    feature = geojson_file
else:
    raise ValueError("Unsupported GeoJSON format")

geometry = feature['geometry']
geom_type = geometry['type']
coords = geometry['coordinates']

# If LineString, convert to closed polygon ring
if geom_type == 'LineString':
    if coords[0] != coords[-1]:
        coords.append(coords[0])
    coords = [coords]  # wrap in list to mimic Polygon exterior ring
elif geom_type == 'Polygon':
    coords = coords
else:
    raise ValueError("Geometry type must be Polygon or LineString")

# Use the outer ring for area calculation
coordinates = coords[0]
geometry['coordinates'] = coords

# --- Area Calculation ---

# 1. Extract the coordinates
# GeoJSON format: [longitude, latitude]
# The coordinates list is nested: geometry -> coordinates -> outer_ring -> points
try:
    # Use the coordinates we already extracted
    # 1. Separate longitude and latitude into lists
    lons = [point[0] for point in coordinates]
    lats = [point[1] for point in coordinates]

    # 2. Define the geodetic reference system (WGS84 ellipsoid)
    # pyproj.Geod handles calculations on the ellipsoid
    geod = pyproj.Geod(ellps='WGS84')

    # 3. Calculate the area
    # polygon_area_perimeter returns area (m^2) and perimeter (m)
    # We only need the area. Use abs() as the sign depends on vertex order.
    area_m2, perimeter_m = geod.polygon_area_perimeter(lons, lats)
    area_m2 = abs(area_m2) # Ensure area is positive

    # 4. Convert area from square meters to square kilometers
    area_km2 = area_m2 / 1_000_000 # 1 km = 1000 m, so 1 km^2 = 1,000,000 m^2

    # 5. Print the result
    print(f"Calculated Area:")  # Green title
    print(f"  {area_m2:.2f} m²")
    print(f"  {area_km2:.2f} km²")  
except KeyError as e:
    print(f"Error: Could not find key {e} in the GeoJSON data. Is it valid?")
except IndexError:
    print("Error: Could not extract coordinates. Check the GeoJSON structure.")
except ImportError:
    print("Error: The 'pyproj' library is required. Please install it (`pip install pyproj`).")
except Exception as e:
    print(f"An unexpected error occurred: {e}")