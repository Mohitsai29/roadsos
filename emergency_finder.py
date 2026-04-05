import requests
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))

def find_nearby_services(lat, lon, radius_km=10):
    radius_m = radius_km * 1000
    overpass_url = "https://overpass-api.de/api/interpreter"

    queries = {
        "hospitals": f"""
            [out:json][timeout:25];
            (
              node["amenity"~"hospital|clinic|doctors"](around:{radius_m},{lat},{lon});
              way["amenity"~"hospital|clinic|doctors"](around:{radius_m},{lat},{lon});
              node["healthcare"~"hospital|clinic"](around:{radius_m},{lat},{lon});
            );
            out center;
        """,
        "police": f"""
            [out:json][timeout:25];
            (
              node["amenity"="police"](around:{radius_m},{lat},{lon});
              way["amenity"="police"](around:{radius_m},{lat},{lon});
            );
            out center;
        """,
        "ambulance": f"""
            [out:json][timeout:25];
            (
              node["emergency"~"ambulance_station"](around:{radius_m},{lat},{lon});
              node["amenity"="hospital"]["emergency"="yes"](around:{radius_m},{lat},{lon});
            );
            out center;
        """,
        "towing": f"""
            [out:json][timeout:25];
            (
              node["amenity"~"car_repair|vehicle_inspection"](around:{radius_m},{lat},{lon});
              node["shop"~"car_repair|tyres|vehicle"](around:{radius_m},{lat},{lon});
              way["shop"~"car_repair|tyres|vehicle"](around:{radius_m},{lat},{lon});
            );
            out center;
        """,
        "fuel": f"""
            [out:json][timeout:25];
            (
              node["amenity"="fuel"](around:{radius_m},{lat},{lon});
            );
            out center;
        """,
        "showrooms": f"""
            [out:json][timeout:25];
            (
              node["shop"~"car|motorcycle|bicycle"](around:{radius_m},{lat},{lon});
              way["shop"~"car|motorcycle"](around:{radius_m},{lat},{lon});
            );
            out center;
        """
    }

    results = {}
    for service_type, query in queries.items():
        try:
            response = requests.post(
                overpass_url,
                data={"data": query},
                timeout=20
            )
            data = response.json()
            places = []
            for element in data.get("elements", []):
                if element["type"] == "node":
                    place_lat = element["lat"]
                    place_lon = element["lon"]
                elif element["type"] == "way":
                    place_lat = element.get("center", {}).get("lat")
                    place_lon = element.get("center", {}).get("lon")
                    if not place_lat:
                        continue
                else:
                    continue

                tags = element.get("tags", {})
                name = (tags.get("name") or
                        tags.get("name:en") or
                        f"Unnamed {service_type}")
                phone = (tags.get("phone") or
                         tags.get("contact:phone") or
                         tags.get("telephone") or "")
                dist = haversine_distance(lat, lon, place_lat, place_lon)

                places.append({
                    "name": name,
                    "lat": place_lat,
                    "lon": place_lon,
                    "phone": phone,
                    "distance_km": round(dist, 2),
                    "type": service_type
                })

            places.sort(key=lambda x: x["distance_km"])
            results[service_type] = places[:5]
        except Exception:
            results[service_type] = []

    return results

def get_nearest_hospital(services):
    hospitals = services.get("hospitals", [])
    if hospitals:
        return hospitals[0]
    return None

# Offline fallback data for major Indian cities
OFFLINE_CONTACTS = {
    "national": {
        "emergency": "112",
        "ambulance": "108",
        "police": "100",
        "fire": "101",
        "highway": "1033",
        "women": "1091",
        "child": "1098"
    },
    "state_contacts": {
        "Andhra Pradesh": {"disaster": "1070", "health": "104"},
        "Telangana": {"disaster": "1070", "health": "104"},
        "Karnataka": {"disaster": "1070", "health": "104"},
        "Tamil Nadu": {"disaster": "1070", "health": "104"},
        "Maharashtra": {"disaster": "1070", "health": "104"},
        "Delhi": {"disaster": "1070", "health": "104"},
    }
}
