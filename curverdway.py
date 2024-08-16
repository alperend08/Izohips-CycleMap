import folium
import numpy as np
from h3 import h3

# Bangkok ve Ho Chi Minh City (500 km uzaklıkta) koordinatları
start_coords = (13.7563, 100.5018)  # Bangkok, Tayland
end_coords = (10.7626, 106.6602)     # Ho Chi Minh City, Vietnam

# Kıvrımlı rota oluşturma
def generate_curved_route(start, end, num_points=10):
    latitudes = np.linspace(start[0], end[0], num_points)
    longitudes = np.linspace(start[1], end[1], num_points)
    # Küresel koordinatlar üzerinde rastgele bir kıvrım ekliyoruz
    latitudes += np.sin(np.linspace(0, np.pi, num_points)) * 0.5
    longitudes += np.cos(np.linspace(0, np.pi, num_points)) * 0.5
    return list(zip(latitudes, longitudes))

# Kıvrımlı rota verisi
route_coords = generate_curved_route(start_coords, end_coords)

# CyclOSM haritasını oluşturma
m = folium.Map(location=[(start_coords[0] + end_coords[0]) / 2, (start_coords[1] + end_coords[1]) / 2], zoom_start=6,
               tiles='https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
               attr='CyclOSM')

# Uçuş rotasını haritaya ekleme
folium.PolyLine(locations=route_coords, color='blue', weight=4, opacity=0.7).add_to(m)

# H3 hücrelerini haritaya ekleme
def add_h3_grid(m, bbox, resolution):
    min_lat, min_lon, max_lat, max_lon = bbox
    hexes = h3.polyfill({
        "type": "Polygon",
        "coordinates": [[
            [min_lon, min_lat],
            [max_lon, min_lat],
            [max_lon, max_lat],
            [min_lon, max_lat],
            [min_lon, min_lat]
        ]]
    }, resolution, geo_json_conformant=True)
    
    for hex_id in hexes:
        coords = h3.h3_to_geo_boundary(hex_id, geo_json=True)
        folium.Polygon(
            locations=[(coord[1], coord[0]) for coord in coords],
            color='purple',
            weight=1,
            fill_color='none',
            fill_opacity=0.1
        ).add_to(m)

# Harita için sınırlar belirleme
bbox = [min([coord[0] for coord in route_coords]) - 1,
        min([coord[1] for coord in route_coords]) - 1,
        max([coord[0] for coord in route_coords]) + 1,
        max([coord[1] for coord in route_coords]) + 1]

# H3 gridini haritaya ekleme (örneğin çözünürlük 6)
add_h3_grid(m, bbox, resolution=6)

# Haritayı HTML dosyasına kaydetme
html_file = 'bangkok_to_ho_chi_minh_flight_route_with_h3_map.html'
m.save(html_file)
print(f"Harita '{html_file}' dosyasına kaydedildi.")
