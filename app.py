import streamlit as st
from streamlit_folium import st_folium
from emergency_finder import find_nearby_services
from ai_assistant import get_ai_guidance, chat_with_ai
from map_module import create_emergency_map
from geopy.geocoders import Nominatim

st.set_page_config(page_title="RoadSoS", page_icon="🚨", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f8f7ff; }

    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e8e4f3;
    }
    section[data-testid="stSidebar"] * {
        color: #2d2d2d !important;
    }
    section[data-testid="stSidebar"] .sidebar-header {
        color: #6c47ff !important;
    }

    .hero-banner {
        background: linear-gradient(135deg, #6c47ff 0%, #9b7dff 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        color: white;
    }
    .hero-banner h1 { font-size: 2rem; font-weight: 600; margin: 0; color: white !important; }
    .hero-banner p { font-size: 0.95rem; opacity: 0.85; margin: 0.4rem 0 0 0; color: white !important; }

    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        border: 1px solid #e8e4f3;
        text-align: center;
    }
    .stat-card .number { font-size: 1.8rem; font-weight: 600; color: #6c47ff; }
    .stat-card .label { font-size: 0.8rem; color: #888; margin-top: 2px; }

    .service-card {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        border: 1px solid #e8e4f3;
        border-left: 4px solid #6c47ff;
    }
    .service-card .name { font-weight: 600; color: #2d2d2d; font-size: 0.95rem; }
    .service-card .detail { color: #888; font-size: 0.82rem; margin-top: 3px; }
    .service-card .distance {
        display: inline-block;
        background: #f0ecff;
        color: #6c47ff;
        font-size: 0.78rem;
        font-weight: 500;
        padding: 2px 10px;
        border-radius: 20px;
        margin-top: 6px;
    }

    .guidance-box {
        background: white;
        border-radius: 16px;
        padding: 1.8rem;
        border: 1px solid #e8e4f3;
        line-height: 1.8;
        color: #2d2d2d;
        font-size: 0.95rem;
    }

    .section-label {
        font-size: 0.75rem;
        font-weight: 600;
        color: #6c47ff;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }

    .stButton > button {
        background: #6c47ff !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
    }
    .stButton > button:hover {
        background: #5535e0 !important;
        transform: translateY(-1px) !important;
    }

    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 1px solid #e8e4f3 !important;
        background: #fafafa !important;
        color: #2d2d2d !important;
    }
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 1px solid #e8e4f3 !important;
        background: #fafafa !important;
        color: #2d2d2d !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: white;
        border-radius: 12px;
        padding: 4px;
        border: 1px solid #e8e4f3;
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        color: #888 !important;
    }
    .stTabs [aria-selected="true"] {
        background: #6c47ff !important;
        color: white !important;
    }

    .hotline-card {
        background: #f8f7ff;
        border-radius: 10px;
        padding: 0.7rem 1rem;
        margin: 0.3rem 0;
        border: 1px solid #e8e4f3;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #2d2d2d !important;
        font-size: 0.88rem;
    }
    .hotline-card b { color: #6c47ff !important; font-size: 1rem; }

    .sidebar-header {
        font-size: 0.72rem;
        font-weight: 700;
        color: #6c47ff !important;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 0.6rem;
        display: block;
    }

    .location-detected {
        background: #f0ecff;
        border-radius: 10px;
        padding: 0.6rem 0.9rem;
        font-size: 0.82rem;
        color: #6c47ff !important;
        border: 1px solid #d4c9ff;
        margin-bottom: 0.5rem;
    }
</style>

<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var lat = position.coords.latitude;
            var lon = position.coords.longitude;
            var input = window.parent.document.querySelector('input[aria-label="lat_input"]');
            if (input) {
                input.value = lat + "," + lon;
                input.dispatchEvent(new Event('input', { bubbles: true }));
            }
        });
    }
}
</script>
""", unsafe_allow_html=True)

# Hero Banner
st.markdown("""
<div class="hero-banner">
    <h1>🚨 RoadSoS</h1>
    <p>AI-powered emergency assistant · Find help instantly after a road accident</p>
</div>
""", unsafe_allow_html=True)

# Quick stats
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown('<div class="stat-card"><div class="number">112</div><div class="label">National Emergency</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="stat-card"><div class="number">108</div><div class="label">Ambulance</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="stat-card"><div class="number">100</div><div class="label">Police</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="stat-card"><div class="number">1033</div><div class="label">Highway Helpline</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "services" not in st.session_state:
    st.session_state.services = None
if "user_location" not in st.session_state:
    st.session_state.user_location = None

# Sidebar
with st.sidebar:
    st.markdown('<span class="sidebar-header">📍 Your Location</span>', unsafe_allow_html=True)

    # Auto-detect location using browser
    loc_method = st.radio("", ["📍 Auto-detect my location", "🔤 Enter address", "🔢 Enter coordinates"],
                           label_visibility="collapsed")

    if loc_method == "📍 Auto-detect my location":
        st.markdown("""
        <div class="location-detected">
            ℹ️ Click the button below — your browser will ask for location permission. Allow it!
        </div>
        """, unsafe_allow_html=True)

        # We use a text input trick to receive coordinates
        coords_input = st.text_input("Paste your coordinates here:",
                                      placeholder="e.g. 16.5062, 80.6480",
                                      help="Go to maps.google.com → right click your location → copy the coordinates shown")

        st.markdown("""
        <div style="background:#f0ecff; border-radius:10px; padding:0.8rem; font-size:0.82rem; color:#2d2d2d; border:1px solid #d4c9ff;">
            <b style="color:#6c47ff">How to get your coordinates:</b><br>
            1. Open <b>Google Maps</b><br>
            2. Right-click on your location<br>
            3. Click the coordinates at the top<br>
            4. Paste them above
        </div>
        """, unsafe_allow_html=True)

        if coords_input and st.button("✅  Use This Location", use_container_width=True):
            try:
                parts = coords_input.replace(" ", "").split(",")
                lat, lon = float(parts[0]), float(parts[1])
                st.session_state.user_location = (lat, lon, f"{lat:.4f}, {lon:.4f}")
                st.success("✅ Location set!")
            except:
                st.error("Invalid format. Try: 16.5062, 80.6480")

    elif loc_method == "🔤 Enter address":
        address = st.text_input("", placeholder="e.g. Vijayawada, Andhra Pradesh",
                                 label_visibility="collapsed")
        if st.button("🔍  Find Location", use_container_width=True):
            geolocator = Nominatim(user_agent="roadsos_app")
            loc = geolocator.geocode(address + ", India")
            if loc:
                st.session_state.user_location = (loc.latitude, loc.longitude, address)
                st.success("✅ Location found!")
            else:
                st.error("Not found. Try a more specific address.")

    else:
        lat = st.number_input("Latitude", value=16.5062, format="%.4f")
        lon = st.number_input("Longitude", value=80.6480, format="%.4f")
        if st.button("✅  Use These Coordinates", use_container_width=True):
            st.session_state.user_location = (lat, lon, f"{lat:.4f}, {lon:.4f}")
            st.success("✅ Location set!")

    # Show current location
    if st.session_state.user_location:
        st.markdown(f"""
        <div class="location-detected">
            📍 <b>Location set:</b> {st.session_state.user_location[2]}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span class="sidebar-header">🔍 Search Radius</span>', unsafe_allow_html=True)
    radius = st.slider("", 2, 20, 5, label_visibility="collapsed")
    st.caption(f"Searching within **{radius} km**")

    st.markdown("---")
    if st.session_state.user_location:
        if st.button("🚨  FIND EMERGENCY SERVICES", use_container_width=True, type="primary"):
            lat, lon, addr = st.session_state.user_location
            with st.spinner("Locating nearby services..."):
                st.session_state.services = find_nearby_services(lat, lon, radius)
            st.success("✅ Services found!")
    else:
        st.info("👆 Set your location first")

    st.markdown("---")
    st.markdown('<span class="sidebar-header">☎️ Quick Helplines</span>', unsafe_allow_html=True)
    st.markdown('<div class="hotline-card"><span>🚑 Ambulance</span><b>108</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="hotline-card"><span>🚔 Police</span><b>100</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="hotline-card"><span>🔥 Fire</span><b>101</b></div>', unsafe_allow_html=True)
    st.markdown('<div class="hotline-card"><span>🛣️ Highway</span><b>1033</b></div>', unsafe_allow_html=True)

# Main Tabs
tab1, tab2, tab3 = st.tabs(["🗺️  Map & Services", "🤖  AI First-Aid Guide", "💬  AI Chat"])

with tab1:
    if st.session_state.user_location and st.session_state.services:
        lat, lon, addr = st.session_state.user_location
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown('<div class="section-label">Live Emergency Map</div>', unsafe_allow_html=True)
            m = create_emergency_map(lat, lon, st.session_state.services)
            st_folium(m, width=None, height=420)
        with col2:
            st.markdown('<div class="section-label">Nearest Services</div>', unsafe_allow_html=True)
            icons = {"hospitals": "🏥", "police": "🚔", "ambulance": "🚑"}
            colors = {"hospitals": "#e53e3e", "police": "#3182ce", "ambulance": "#dd6b20"}
            for service_type, places in st.session_state.services.items():
                if places:
                    for p in places[:2]:
                        phone_str = f"📞 {p['phone']}" if p['phone'] else ""
                        color = colors.get(service_type, "#6c47ff")
                        st.markdown(f"""
                        <div class="service-card" style="border-left-color:{color}">
                            <div class="name">{icons.get(service_type,'')} {p['name']}</div>
                            <div class="detail">{phone_str}</div>
                            <span class="distance">📏 {p['distance_km']} km away</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="service-card">
                        <div class="name">{icons.get(service_type,'')} No {service_type} found nearby</div>
                        <div class="detail">Try increasing search radius</div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align:center; padding:4rem 2rem; background:white;
             border-radius:16px; border:1px solid #e8e4f3;">
            <div style="font-size:3rem">📍</div>
            <div style="font-size:1.1rem; font-weight:600; color:#2d2d2d; margin-top:1rem">
                Enter your location to get started
            </div>
            <div style="color:#888; margin-top:0.5rem; font-size:0.9rem">
                Use the left panel to set your location and find emergency services
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div class="section-label">Describe the Situation</div>', unsafe_allow_html=True)
        situation = st.text_area("", placeholder="e.g. Two vehicles collided on NH65, one person unconscious...",
                                  height=140, label_visibility="collapsed")
        if st.button("⚡  Get AI Guidance", use_container_width=False):
            if situation:
                loc_info = st.session_state.user_location[2] if st.session_state.user_location else "India"
                with st.spinner("Generating emergency guidance..."):
                    guidance = get_ai_guidance(situation, loc_info)
                st.markdown('<div class="section-label" style="margin-top:1.5rem">Emergency Guidance</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="guidance-box">{guidance}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please describe the situation first.")
    with col2:
        st.markdown('<div class="section-label">Quick Reference</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="background:white; border-radius:12px; padding:1.2rem;
             border:1px solid #e8e4f3; font-size:0.88rem; line-height:2; color:#2d2d2d;">
            <b style="color:#6c47ff">✅ DO</b><br>
            • Call 112 immediately<br>
            • Turn on hazard lights<br>
            • Keep victim conscious<br>
            • Apply pressure to wounds<br><br>
            <b style="color:#e53e3e">❌ DON'T</b><br>
            • Move unconscious victims<br>
            • Remove helmets yourself<br>
            • Give water to unconscious<br>
            • Leave the scene
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-label">Chat with RoadSoS AI</div>', unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    if prompt := st.chat_input("Ask anything... e.g. What do I do if someone is unconscious?"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        loc_info = st.session_state.user_location[2] if st.session_state.user_location else "India"
        with st.spinner(""):
            reply = chat_with_ai(st.session_state.chat_history[:-1], prompt, loc_info)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()
