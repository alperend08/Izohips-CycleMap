
import folium
import requests
import geopandas as gpd
from shapely.geometry import shape

# OpenRouteService API anahtarınızı buraya ekleyin
ORS_API_KEY = 'x'

# Dağlık bölge koordinatları (Sazak Köyü - Gödence Köyü)
start_coords = (38.5115, 27.1091)  # Sazak Köyü
end_coords = (38.5115, 27.1904)    # Gödence Köyü

# OpenRouteService API üzerinden rota hesaplama
def get_route(start_coords, end_coords, profile='cycling-regular'):
    url = f'https://api.openrouteservice.org/v2/directions/{profile}?api_key={ORS_API_KEY}'
    params = {
        'start': f'{start_coords[1]},{start_coords[0]}',
        'end': f'{end_coords[1]},{end_coords[0]}'
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'features' in data:
        return data['features'][0]['geometry']['coordinates']
    else:
        raise Exception("Rota verisi alınamadı.")

# İzohips verilerini çekme
def get_contours():
    query_contours = """
    [out:json];
    area[name="Izmir, Turkey"];
    (
      way["natural"="contour"](area);
    );
    out body;
    """
    response_contours = requests.get('http://overpass-api.de/api/interpreter?data=' + query_contours)
    data_contours = response_contours.json()
    features_contours = [shape(feature['geometry']) for feature in data_contours['elements'] if feature['type'] == 'way']
    return gpd.GeoDataFrame(geometry=features_contours, crs="EPSG:4326")

# Rota ve izohips verilerini al
try:
    route_coords_1 = get_route(start_coords, end_coords, profile='cycling-regular')  # Alternatif 1: Araba Yolu
    route_coords_2 = get_route(start_coords, end_coords, profile='cycling-mountain')  # Alternatif 2: Dağ Yolu
    gdf_contours = get_contours()
except Exception as e:
    print(f"Veri çekme sırasında bir hata oluştu: {e}")
    exit()

# CyclOSM haritasını oluşturma
m = folium.Map(location=[(start_coords[0] + end_coords[0]) / 2, (start_coords[1] + end_coords[1]) / 2], zoom_start=13,
               tiles='https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
               attr='CyclOSM')

# İzohipsleri haritaya ekleme
for _, row in gdf_contours.iterrows():
    if row.geometry.type == 'LineString':
        folium.PolyLine(locations=list(row.geometry.coords), color='blue', weight=2, opacity=0.7).add_to(m)

# Rotaları çizme
folium.PolyLine(locations=[(coord[1], coord[0]) for coord in route_coords_1], color='red', weight=3, opacity=0.7).add_to(m)  # Alternatif 1: Araba Yolu
folium.PolyLine(locations=[(coord[1], coord[0]) for coord in route_coords_2], color='green', weight=3, opacity=0.7).add_to(m)  # Alternatif 2: Dağ Yolu

# Haritayı HTML dosyasına kaydetme
html_file = 'cycleway_map_with_cyclosm.html'
m.save(html_file)
print(f"Harita '{html_file}' dosyasına kaydedildi.")

