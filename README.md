# Project Progress: CoastSat Shoreline Extraction for Skåne County

**1. Define and Segment Region of Interest (ROI):**
- [x] Define overall Skåne region boundary (`Skane/input.json`)
- [x] Subdivide Skåne coast into manageable segments (`Skane/segment_polygon.py`)
- [x] Obtain coordinates for each segment (`Skane/segments/segment_*.json`)
- [x] Define `sitename` for *each* segment (`FID`)

**2. Define Parameters:**
- [x] Define `sat_list` (`S2`)
- [x] Define `dates` (`['2024-06-01', '2024-10-31']`)

> Late Spring to Early Fall (May-September): 
>    - Lower and more stable Baltic Sea water levels
>    - Reduced cloud cover and better illumination conditions
>    - Calmer sea states with less wave interference
>    - Optimal vegetation conditions for accurate shoreline delineation
>    - More practical field validation possibilities

- [x] Define `output_epsg` (`EPSG:3006`)
- [x] Define `filepath` ((`Skane/segments/results/`)

**3. Retrieve Sentinel-2 Imagery (for each segment):**
- [X] Assemble `inputs` dictionary for each segment

```python
inputs = {
    'polygon': polygon,           
    'dates': ['2024-06-01', '2024-10-31'],  
    'sat_list': ['S2'],           
    'sitename': 'FID_X',         
    'filepath': 'Skane/segments/results/', 
    'output_epsg': 3006        
}
```

- [ ] Download images (`coastsat/SDS_download.py`).

**4. FES2022 Tide Model Setup:**
- [ ] Install `pyfes`, and download `FES2022 netcdf`, and `fes2022.yaml` files.
- [ ] Configure `fes2022.yaml` absolute file path.
- [ ] Clip FES2022 Model to Skåne county (`Skane/input.json`, `examples/tide_model_clipping/clip_tide_files.py`).

**5. Collection of Training Data & Custom Classifier Preparation:**

- [ ] **Define Class Mapping:**
  - [ ] Map `/ Sand or gravel` soil polygons → `sand` (Label=1)
  - [ ] Map all other soil types (peat, clay, moraine, stone block, rock, fill, etc.) → `other land features` (Label=0)
  - [ ] Use water index thresholding → `water` (Label=3)
  - [ ] Manually identify breaking waves → `white-water` (Label=2)

- [ ] **Rasterize Soil Type Vectors:**
  - [ ] Convert SGU soil polygons/lines to raster grids
  - [ ] Match CRS, resolution, and extent of satellite images
  - [ ] Assign pixel values based on mapped classes (sand=1, other land=0)

- [ ] **Calculate Water Index:**
  - [ ] Compute water index (e.g., MNDWI, NDWI) on satellite images
  - [ ] Apply threshold to generate water mask (Label=3)

- [ ] **Generate Initial Label Masks:**
  - [ ] Assign pixels as:
    - `sand` where soil raster = 1
    - `water` where water index mask = 3
    - `other land` where soil raster = 0
  - [ ] Resolve potential overlaps

- [ ] **Manual Labeling & Verification:**
  - [ ] Load satellite images with initial label masks
  - [ ] Visually inspect and correct mislabels
  - [ ] Manually label `white-water` (Label=2) in breaking wave zones
  - [ ] Save finalized label masks

- [ ] **Train Custom Classifier:**
  - [ ] Extract pixel features and labels from finalized masks
  - [ ] Format data (`X`, `y`) with 4 classes: sand(1), white-water(2), water(3), other land(0)
  - [ ] Train MLPClassifier
  - [ ] Evaluate accuracy and confusion matrix
  - [ ] Save trained model (`joblib.dump`)

- [ ] **Integrate Classifier:**
  - [ ] Modify `SDS_shoreline.py` to load the custom .pkl file.

**6. Configure Shoreline Extraction Settings:**
- [ ] Create `settings` dictionary for each segment
- [ ] Define/Adjust parameters (`cloud_thresh`, etc.)
- [ ] Enable QC (`check_detection`, `save_figure`)
- [ ] Define Reference Shoreline (`get_reference_sl`) for *each* segment

**7. Extract Shorelines (for each segment)**
- [ ] Run `extract_shorelines`
- [ ] Perform manual QC (if `check_detection` is True)
- [ ] Check output files (.pkl, .geojson)
- [ ] Remove duplicate date images (`SDS_tools.remove_duplicates`)
- [ ] Remove images with poor georeferencing (`SDS_tools.remove_inaccurate_georef`)

**8. Compute intersections between the extracted shorelines**

**9. Segment the shoreline to smaller parts (~100 m)**

**10. Define Shore-Normal Transects (For each shoreline part)**

**11. Tidal Correction**

**12. Beach slope (For each shoreline part)**

**13. Time-Series Post-Processing**

```