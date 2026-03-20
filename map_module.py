import folium

COLOR_MAP = {
    "hospitals": "red",
    "police": "blue",
    "ambulance": "orange"
}

ICON_MAP = {
    "hospitals": "plus-sign",
    "police": "star",
    "ambulance": "heart"
}

def create_emergency_map(user_lat, user_lon, services):
    m = folium.Map(location=[user_lat, user_lon], zoom_start=14)

    folium.Marker(
        [user_lat, user_lon],
        popup="<b>YOU ARE HERE</b>",
        icon=folium.Icon(color="green", icon="home"),
        tooltip="Your Location"
    ).add_to(m)

    for service_type, places in services.items():
        for place in places:
            popup_html = f"""
            <b>{place['name']}</b><br>
            Type: {service_type}<br>
            Distance: {place['distance_km']} km<br>
            {"Phone: " + place['phone'] if place['phone'] else "Phone: Not listed"}
            """
            folium.Marker(
                [place["lat"], place["lon"]],
                popup=folium.Popup(popup_html, max_width=200),
                icon=folium.Icon(
                    color=COLOR_MAP.get(service_type, "gray"),
                    icon=ICON_MAP.get(service_type, "info-sign")
                ),
                tooltip=place["name"]
            ).add_to(m)

    return m
