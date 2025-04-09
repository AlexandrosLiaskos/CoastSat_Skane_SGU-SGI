import folium
import json
import geopandas as gpd

# Load GeoJSON as GeoDataFrame for easy bounds calculation
gdf = gpd.read_file('input.json')

# Calculate bounds: (minx, miny, maxx, maxy)
bounds = gdf.total_bounds
minx, miny, maxx, maxy = bounds

# Create map object
m = folium.Map()

# Add GeoJSON overlay
folium.GeoJson(
    gdf,
    name='geojson',
    style_function=lambda feature: {
        'fillColor': 'blue',
        'color': 'black',
        'weight': 2,
        'fillOpacity': 0.5,
    }
).add_to(m)


# Automatically fit map to GeoJSON bounds
m.fit_bounds([[miny, minx], [maxy, maxx]])

# Add layer control
folium.LayerControl().add_to(m)

# Save to HTML
m.save('interactive_map.html')

# Display the map
display(m)