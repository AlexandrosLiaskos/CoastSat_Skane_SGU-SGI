import json
import os
from shapely.geometry import Polygon, LineString, box, mapping
from shapely.ops import split
from shapely import affinity
from pyproj import Geod

INPUT_FILE = "input.json"  # Input polygon GeoJSON file
OUTPUT_DIR = "segments"    # Output directory for polygon segments
TARGET_AREA_KM2 = 100
geod = Geod(ellps="WGS84")

def calculate_area_km2(poly):
    lon, lat = poly.exterior.coords.xy
    area, _ = geod.polygon_area_perimeter(lon, lat)
    return abs(area) / 1_000_000

def recursive_split(polygon, fid_counter):
    """
    Recursively split polygon into parts < TARGET_AREA_KM2.
    fid_counter: list with one int element, incremented for each saved segment.
    Returns list of (fid, polygon, area).
    """
    queue = [polygon]
    segments = []

    while queue:
        poly = queue.pop(0)
        area = calculate_area_km2(poly)
        if area <= TARGET_AREA_KM2:
            fid = fid_counter[0]
            fid_counter[0] += 1
            segments.append((fid, poly, area))
        else:
            # Split polygon vertically at center
            minx, miny, maxx, maxy = poly.bounds
            midx = (minx + maxx) / 2
            splitter = LineString([(midx, miny - 1), (midx, maxy + 1)])
            parts = split(poly, splitter)
            # Normalize parts to list of polygons
            if parts.geom_type == 'GeometryCollection':
                parts = [g for g in parts.geoms if g.geom_type == 'Polygon']
            elif parts.geom_type == 'Polygon':
                parts = [parts]
            elif parts.geom_type == 'MultiPolygon':
                parts = list(parts.geoms)
            else:
                parts = []

            # If split failed (1 part), try horizontal split
            if len(parts) <= 1:
                midy = (miny + maxy) / 2
                splitter = LineString([(minx - 1, midy), (maxx + 1, midy)])
                parts = split(poly, splitter)
                if parts.geom_type == 'GeometryCollection':
                    parts = [g for g in parts.geoms if g.geom_type == 'Polygon']
                elif parts.geom_type == 'Polygon':
                    parts = [parts]
                elif parts.geom_type == 'MultiPolygon':
                    parts = list(parts.geoms)
                else:
                    parts = []

            # If still 1 part, stop splitting
            if len(parts) <= 1:
                fid = fid_counter[0]
                fid_counter[0] += 1
                segments.append((fid, poly, area))
            else:
                queue.extend(parts)
    return segments

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(INPUT_FILE) as f:
        data = json.load(f)

    coords = data['features'][0]['geometry']['coordinates']
    # Close polygon if not closed
    if coords[0] != coords[-1]:
        coords.append(coords[0])

    polygon = Polygon(coords)

    fid_counter = [0]
    segments = recursive_split(polygon, fid_counter)

    for fid, poly, area in segments:
        feature = {
            "type": "Feature",
            "properties": {"FID": fid, "area_km2": area},
            "geometry": mapping(poly)
        }
        out_path = os.path.join(OUTPUT_DIR, f"segment_{fid}.json")
        with open(out_path, "w") as f_out:
            json.dump({
                "type": "FeatureCollection",
                "features": [feature]
            }, f_out, indent=2)
        print(f"Saved segment {fid} with area {area:.2f} km²")

    print(f"Total segments created: {len(segments)}")

if __name__ == "__main__":
    main()