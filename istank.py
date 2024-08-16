import folium
from h3 import h3

# Uçuş rotası noktaları: İstanbul ve Antalya
route_coords = [
    (41.0082, 28.9784),  # İstanbul
    (37.0662, 35.2156)   # Antalya
]

# CyclOSM haritasını oluşturma
m = folium.Map(location=[(route_coords[0][0] + route_coords[-1][0]) / 2, (route_coords[0][1] + route_coords[-1][1]) / 2], zoom_start=7,
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
bbox = [min([coord[0] for coord in route_coords]) - 0.5,
        min([coord[1] for coord in route_coords]) - 0.5,
        max([coord[0] for coord in route_coords]) + 0.5,
        max([coord[1] for coord in route_coords]) + 0.5]

# H3 gridini haritaya ekleme (örneğin çözünürlük 6)
add_h3_grid(m, bbox, resolution=6)

# Haritayı HTML dosyasına kaydetme
html_file = 'istanbul_to_antalya_flight_route_with_h3_map.html'
m.save(html_file)
print(f"Harita '{html_file}' dosyasına kaydedildi.")
