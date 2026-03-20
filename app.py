import streamlit as st
from streamlit_folium import st_folium
from emergency_finder import find_nearby_services
from ai_assistant import get_ai_guidance, chat_with_ai
from map_module import create_emergency_map
from geopy.geocoders import Nominatim

st.set_page_config(page_title="RoadSoS", page_icon="🚨", layout="wide")

st.markdown("""
<style>
.sos-header {background:#CC0000;color:white;padding:1rem;border-radius:8px;text-align:center;font-size:1.8rem;font-weight:bold;}
.service-card {border:1px solid #ddd;border-radius:8px;padding:1rem;margin:0.5rem 0;}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="sos-header">🚨 RoadSoS — Emergency Assistant</div>', unsafe_allow_html=True)
st.markdown("**AI-powered road accident emergency tool | Find help instantly**")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "services" not in st.session_state:
    st.session_state.services = None
if "user_location" not in st.session_state:
    st.session_state.user_location = None

with st.sidebar:
    st.header("📍 Your Location")
    location_method = st.radio("How to get location:", ["Enter address/city", "Enter coordinates"])

    if location_method == "Enter address/city":
        address = st.text_input("Enter location:", placeholder="e.g. Vijayawada, Andhra Pradesh")
        if st.button("🔍 Find Location"):
            geolocator = Nominatim(user_agent="roadsos")
            loc = geolocator.geocode(address + ", India")
            if loc:
                st.session_state.user_location = (loc.latitude, loc.longitude, address)
                st.success(f"Found: {loc.latitude:.4f}, {loc.longitude:.4f}")
            else:
                st.error("Location not found. Try a more specific address.")
    else:
        lat = st.number_input("Latitude", value=16.5062, format="%.4f")
        lon = st.number_input("Longitude", value=80.6480, format="%.4f")
        if st.button("Use These Coordinates"):
            st.session_state.user_location = (lat, lon, f"{lat:.4f}, {lon:.4f}")

    st.markdown("---")
    radius = st.slider("Search radius (km)", 2, 20, 5)

    if st.session_state.user_location and st.button("🚨 FIND EMERGENCY SERVICES", type="primary"):
        lat, lon, addr = st.session_state.user_location
        with st.spinner("Locating nearby services..."):
            st.session_state.services = find_nearby_services(lat, lon, radius)
        st.success("Services found!")

tab1, tab2, tab3 = st.tabs(["🗺️ Map & Services", "🤖 AI First-Aid Guide", "💬 AI Chat"])

with tab1:
    if st.session_state.user_location and st.session_state.services:
        lat, lon, addr = st.session_state.user_location
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Emergency Services Map")
            m = create_emergency_map(lat, lon, st.session_state.services)
            st_folium(m, width=None, height=450)
        with col2:
            st.subheader("Nearby Services")
            for service_type, places in st.session_state.services.items():
                icon = {"hospitals": "🏥", "police": "🚔", "ambulance": "🚑"}.get(service_type, "📍")
                st.markdown(f"**{icon} {service_type.capitalize()}**")
                if places:
                    for p in places[:3]:
                        st.markdown(f"""
                        <div class="service-card">
                        <b>{p['name']}</b><br>
                        📏 {p['distance_km']} km away<br>
                        {"📞 " + p['phone'] if p['phone'] else ""}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info(f"No {service_type} found nearby")
    else:
        st.info("👈 Enter your location in the left panel and click Find Emergency Services")

with tab2:
    st.subheader("🤖 AI First-Aid Guidance")
    situation = st.text_area("Describe the accident situation:",
        placeholder="e.g. Two vehicles collided, one person is unconscious...")
    if st.button("Get AI Guidance") and situation:
        loc_info = st.session_state.user_location[2] if st.session_state.user_location else "unknown location"
        with st.spinner("AI is generating guidance..."):
            guidance = get_ai_guidance(situation, loc_info)
        st.markdown("### 📋 Emergency Guidance")
        st.markdown(guidance)

with tab3:
    st.subheader("💬 Chat with RoadSoS AI")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    if prompt := st.chat_input("Ask anything about the emergency..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        loc_info = st.session_state.user_location[2] if st.session_state.user_location else "unknown"
        with st.spinner("..."):
            reply = chat_with_ai(st.session_state.chat_history[:-1], prompt, loc_info)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()
