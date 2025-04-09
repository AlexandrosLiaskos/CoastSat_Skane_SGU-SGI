# Progress Report #01

**Author:** Alexandros P. Liaskos  
**Date:** 04/09/2025  
**Recipients:** SGU & SGI

---

## Overview

The initial phase focused on segmenting the Region of Interest (RoI) polygon; ensuring compatibility with processing constraints of GEE (< 100 km² RoIs), and preparing the plan for the Shoreline Extraction with the CoastSat software and a custom Classifier; addressing the multiple beach soil types of the Skåne's coastline zone.

---

## 1. RoI Polygon Creation

- The full Skåne coastline was **drawn interactively on [geojson.io](https://geojson.io/)**.
- Saved as `Skane/input.json`.
- Visualization and area calculation scripts (`visualize_geojson.py`, `calculate_area_json.py`) confirm the polygon's integrity and size.

---

## 2. Segmentation for GEE & CoastSat Compatibility

- **Reason:** GEE and CoastSat have limitations with very large polygons; processing is more reliable with polygons **< 100 km²**.
- **Method:**  
  - Implemented in `Skane/Skane_CoastSat_Prep.ipynb` and `Skane/segment_polygon.py`.
  - Uses `shapely` and `pyproj` for accurate geodetic calculations and geometry operations.
  - **Recursive splitting**:  
    - The large polygon is bisected vertically until all parts are < 100 km².  
    - Each segment is saved as `Skane/segments/segment_*.json` with properties:  
      - `FID` (unique ID)  
      - `area_km2` (precise area)
- **Verification:**  
  - `combine_segments.py` merges all segments into `combined_segments.json`.  
  - `visualize_geojson.py` generates an interactive HTML map for visual confirmation.
- **Outcome:**  
  - Over 30 segments created, all < 100 km², ready for batch processing.

---

## 3. Project Planning Status (from `Skane/README.md`)

- **Completed:**  
  - RoI definition and segmentation  
  - Parameter setup (dates, satellites, EPSG, paths)  
  - Input preparation for image retrieval
- **Next Steps:**  
  - Download Sentinel-2 imagery  
  - Setup FES2022 tide model  
  - Develop a custom classifier  
  - Extract shorelines and post-process

---

## 4. Need for Soil Type Data & Custom Classifier

- **Challenge:**  
  - The default CoastSat classifier is optimized for **sandy beaches only**.  
  - Skåne's coastline includes **peat, clay, moraine, stone block, rock, fill**, etc.
- **Solution:**  
  - **Acquire detailed soil/substrate data** (ideally from SGU).  
  - **Rasterize** these data to match satellite imagery.  
  - **Map classes:**  
    - Sand/gravel → `sand` (Label=1)  
    - Other soils → `other land features` (Label=0)  
    - Water (via spectral indices) → `water` (Label=3)  
    - White-water (manual labeling) → `white-water` (Label=2)
  - **Train a custom classifier** (e.g., MLPClassifier) on these multi-class labels.  
  - **Integrate** the trained model into CoastSat.
- **Request:**  
  - **If existing/possible, I would need the beach soil type dataset for Skåne County, as visualized in the map of [Produkt: Stränders jordart och eroderbarhet](https://resource.sgu.se/dokument/produkter/stranders-jordart-eroderbarhet-beskrivning.pdf).**  
  - This is **critical** for accurate shoreline detection across diverse coastal soil types.

---