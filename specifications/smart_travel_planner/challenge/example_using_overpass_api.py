from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import overpass
import math
import os
import json

app = FastAPI()
api = overpass.API()

CACHE_DIR = "cache/cities"
os.makedirs(CACHE_DIR, exist_ok=True)

# Basic country list for the POC
COUNTRIES = [
    "United Kingdom", "United States", "Germany", "France", 
    "South Africa", "Netherlands", "Italy", "Spain", "Canada", "Australia"
]

@app.get("/api/countries")
def get_countries():
    return COUNTRIES

@app.get("/api/cities/{country}")
def get_cities(country: str):
    cache_file = os.path.join(CACHE_DIR, f"{country.lower().replace(' ', '_')}.json")
    
    if os.path.exists(cache_file):
        print(f"Using cached cities for: {country}")
        with open(cache_file, "r") as f:
            return json.load(f)

    print(f"Fetching cities for: {country} from API")
    # Query overpass for cities in the given country
    # We search for the area by name and then find nodes tagged as city or town within it.
    # We use a union of name and name:en to be more robust.
    query = f'''
    (
      area["name"="{country}"];
      area["name:en"="{country}"];
    )->.searchArea;
    (
      node["place"~"city|town"](area.searchArea);
    );
    out body;
    '''
    try:
        response = api.get(query)
        print(f"Overpass returned {len(response.get('features', []))} features")
        cities = []
        for feature in response.get("features", []):
            tags = feature.get("properties", {}).get("tags", {})
            name = tags.get("name")
            if name:
                cities.append({
                    "name": name,
                    "lat": feature.get("geometry", {}).get("coordinates", [0, 0])[1],
                    "lon": feature.get("geometry", {}).get("coordinates", [0, 0])[0]
                })
        # Sort and remove duplicates
        unique_cities = sorted({v['name']: v for v in cities}.values(), key=lambda x: x['name'])
        
        # Cache the results
        with open(cache_file, "w") as f:
            json.dump(unique_cities, f)
            
        return unique_cities
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/poi/{lat}/{lon}")
def get_poi(lat: float, lon: float, amenity: str = "fuel"):
    print(f"Fetching {amenity} near {lat}, {lon}")
    # Search for nodes with the given amenity within 5000m of the center
    query = f'''
    (
      node["amenity"="{amenity}"](around:5000, {lat}, {lon});
    );
    out body;
    '''
    try:
        response = api.get(query)
        print(f"Overpass returned {len(response.get('features', []))} POIs")
        pois = []
        for feature in response.get("features", []):
            tags = feature.get("properties", {}).get("tags", {})
            name = tags.get("name", "Unknown")
            pois.append({
                "name": name,
                "lat": feature.get("geometry", {}).get("coordinates", [0, 0])[1],
                "lon": feature.get("geometry", {}).get("coordinates", [0, 0])[0],
                "amenity": tags.get("amenity")
            })
        return pois
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r") as f:
        return f.read()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
