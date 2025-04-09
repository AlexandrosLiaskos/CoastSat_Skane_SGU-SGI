import json
import glob
import os

SEGMENTS_DIR = "segments"  # Directory containing segment GeoJSON files
OUTPUT_FILE = "combined_segments.json"  # Output combined GeoJSON file

def main():
    features = []

    # Find all segment files
    segment_files = sorted(glob.glob(os.path.join(SEGMENTS_DIR, "segment_*.json")))

    for seg_file in segment_files:
        with open(seg_file) as f:
            data = json.load(f)
            for feature in data.get("features", []):
                features.append(feature)

    # Sort features by FID
    features.sort(key=lambda f: f.get("properties", {}).get("FID", 0))

    combined = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(combined, f, indent=2)

    print(f"Combined {len(features)} segments into '{OUTPUT_FILE}'")

if __name__ == "__main__":
    main()