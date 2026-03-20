import streamlit as st
from streamlit_folium import st_folium
from emergency_finder import find_nearby_services
from ai_assistant import get_ai_guidance, chat_with_ai
from map_module import create_emergency_map
from geopy.geocoders import Nominatim

st.set_page_config(page_title="RoadSoS — Emergency Assistant", page_icon="🚨", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
*, html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
.stApp { background: #f4f2ff; }
section[data-testid="stSidebar"] { background: #ffffff !important; border-right: 1px solid #ece8ff; }
section[data-testid="stSidebar"] * { color: #1a1a2e !important; }
.sidebar-brand { background: linear-gradient(135deg, #6c47ff, #9b7dff); margin: -1.5rem -1rem 1.2rem -1rem; padding: 1.2rem 1.2rem 1rem; }
.sidebar-brand h2 { font-size: 1.2rem; font-weight: 700; margin: 0; color: white !important; }
.sidebar-brand p { font-size: 0.75rem; margin: 3px 0 0; opacity: 0.85; color: white !important; }
.slabel { font-size: 0.68rem; font-weight: 700; color: #6c47ff !important; text-transform: uppercase; letter-spacing: 1.3px; margin: 1rem 0 0.4rem; display: block; }
.helpline-row { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 0.5rem; }
.helpline-pill { flex: 1; min-width: 70px; background: #f4f2ff; border: 1px solid #ece8ff; border-radius: 10px; padding: 8px 6px; text-align: center; font-size: 0.78rem; color: #1a1a2e !important; }
.helpline-pill .num { font-size: 1.05rem; font-weight: 700; color: #6c47ff !important; display: block; }
.loc-active { background: #f0ecff; border: 1px solid #d4c9ff; border-radius: 10px; padding: 0.55rem 0.8rem; font-size: 0.8rem; color: #5535e0 !important; margin-top: 0.5rem; }
.hero { background: linear-gradient(135deg, #6c47ff 0%, #a78bff 100%); border-radius: 20px; padding: 2.2rem 2.5rem; margin-bottom: 1.5rem; position: relative; overflow: hidden; }
.hero::after { content: "🚨"; position: absolute; right: 2rem; top: 50%; transform: translateY(-50%); font-size: 5rem; opacity: 0.15; }
.hero h1 { font-size: 2.2rem; font-weight: 700; color: white !important; margin: 0; }
.hero p { color: rgba(255,255,255,0.85) !important; font-size: 1rem; margin: 0.5rem 0 0; }
.enum-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 1.5rem; }
.enum-card { background: white; border-radius: 14px; padding: 1.1rem; text-align: center; border: 1px solid #ece8ff; }
.enum-card .en { font-size: 1.9rem; font-weight: 700; color: #6c47ff; line-height: 1; }
.enum-card .el { font-size: 0.75rem; color: #888; margin-top: 4px; }
.enum-card .ei { font-size: 1.5rem; margin-bottom: 4px; }
.stTabs [data-baseweb="tab-list"] { background: white !important; border-radius: 14px !important; padding: 5px !important; border: 1px solid #ece8ff !important; gap: 4px !important; margin-bottom: 1.2rem !important; }
.stTabs [data-baseweb="tab"] { border-radius: 10px !important; font-size: 0.88rem !important; font-weight: 500 !important; color: #888 !important; padding: 0.5rem 1.2rem !important; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #6c47ff, #9b7dff) !important; color: white !important; }
.svc-card { background: white; border-radius: 14px; padding: 1rem 1.2rem; margin: 0.5rem 0; border: 1px solid #ece8ff; border-left: 4px solid #6c47ff; }
.svc-card .sn { font-weight: 600; color: #1a1a2e; font-size: 0.93rem; }
.svc-card .sd { color: #888; font-size: 0.8rem; margin-top: 2px; }
.svc-badge { display: inline-block; background: #f0ecff; color: #6c47ff; font-size: 0.73rem; font-weight: 600; padding: 3px 10px; border-radius: 20px; margin-top: 6px; }
.guidance-box { background: white; border-radius: 16px; padding: 1.8rem; border: 1px solid #ece8ff; border-top: 4px solid #6c47ff; line-height: 1.85; color: #1a1a2e; font-size: 0.93rem; }
.ref-card { background: white; border-radius: 14px; padding: 1.3rem; border: 1px solid #ece8ff; font-size: 0.86rem; line-height: 1.9; color: #1a1a2e; }
.empty-state { text-align: center; padding: 4rem 2rem; background: white; border-radius: 20px; border: 1px solid #ece8ff; }
.stButton > button { background: linear-gradient(135deg, #6c47ff, #9b7dff) !important; color: white !important; border: none !important; border-radius: 10px !important; font-weight: 500 !important; }
.stButton > button:hover { opacity: 0.92 !important; transform: translateY(-1px) !important; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea { border-radius: 10px !important; border: 1.5px solid #ece8ff !important; background: #fafafa !important; color: #1a1a2e !important; }
.stSlider > div > div > div > div { background: linear-gradient(to right, #6c47ff, #9b7dff) !important; }
div[data-testid="stChatMessage"] { background: white !important; border-radius: 14px !important; border: 1px solid #ece8ff !important; }
hr { border-color: #ece8ff !important; }
.india-badge { display:inline-block; background:#e8f5e9; color:#2e7d32; border:1px solid #c8e6c9; border-radius:20px; padding:3px 12px; font-size:0.78rem; font-weight:600; margin-bottom:0.8rem; }
</style>
""", unsafe_allow_html=True)

# Session state
for key in ["chat_history", "services", "user_location", "gps_lat", "gps_lon"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key == "chat_history" else None

# ══════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <h2>🚨 RoadSoS</h2>
        <p>India Emergency Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="slabel">📍 Your Location</span>', unsafe_allow_html=True)
    st.markdown('<span class="india-badge">🇮🇳 India only</span>', unsafe_allow_html=True)

    # GPS auto-detect with persistent storage in session state
    gps_component = st.components.v1.html("""
    <script>
    function sendGPS() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(function(pos) {
                var lat = pos.coords.latitude.toFixed(6);
                var lon = pos.coords.longitude.toFixed(6);
                // Store in sessionStorage so Streamlit can read it
                sessionStorage.setItem('roadsos_lat', lat);
                sessionStorage.setItem('roadsos_lon', lon);
                document.getElementById('gps-display').innerHTML =
                    '<span style="color:#2e7d32">✅ GPS ready: ' + lat + ', ' + lon + '</span>';
                // Fill the hidden input
                var inputs = window.parent.document.querySelectorAll('input[type=text]');
                for (var i=0; i<inputs.length; i++) {
                    if (inputs[i].getAttribute('placeholder') &&
                        inputs[i].getAttribute('placeholder').includes('auto')) {
                        inputs[i].value = lat + ', ' + lon;
                        inputs[i].dispatchEvent(new Event('input', {bubbles:true}));
                        inputs[i].dispatchEvent(new Event('change', {bubbles:true}));
                        break;
                    }
                }
            }, function(err) {
                document.getElementById('gps-display').innerHTML =
                    '<span style="color:#c62828">❌ GPS denied. Use manual entry below.</span>';
            }, {timeout: 8000});
        }
    }
    setTimeout(sendGPS, 500);
    </script>
    <div id="gps-display"
         style="font-size:0.78rem; color:#6c47ff; padding:6px 0; min-height:20px;">
        ⏳ Detecting GPS location...
    </div>
    """, height=35)

    # Input box — GPS fills this automatically
    coord_val = st.text_input("",
        placeholder="GPS fills here auto — or type: Vijayawada",
        label_visibility="collapsed",
        key="coord_input")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📍 Use GPS", use_container_width=True):
            if coord_val and "," in coord_val:
                try:
                    parts = coord_val.strip().split(",")
                    lat, lon = float(parts[0].strip()), float(parts[1].strip())
                    # Verify it's within India bounds
                    if 6.5 <= lat <= 37.5 and 68.0 <= lon <= 97.5:
                        st.session_state.user_location = (lat, lon, f"{lat:.4f}, {lon:.4f}")
                        st.success("✅ GPS location set!")
                    else:
                        st.error("⚠️ Location outside India. This app is for India only.")
                except:
                    st.error("Could not read GPS. Try manual entry.")
            else:
                st.warning("GPS still loading... wait 3 seconds and try again.")

    with col_b:
        if st.button("🔍 Search", use_container_width=True):
            query = coord_val.strip()
            if query:
                geolocator = Nominatim(user_agent="roadsos_india_v2")
                # Force search within India
                loc = geolocator.geocode(query + ", India",
                                          country_codes="IN")
                if loc:
                    lat, lon = loc.latitude, loc.longitude
                    if 6.5 <= lat <= 37.5 and 68.0 <= lon <= 97.5:
                        st.session_state.user_location = (lat, lon, query)
                        st.success(f"✅ Found in India!")
                    else:
                        st.error("Location not in India.")
                else:
                    st.error("Not found. Try: 'Vijayawada' or 'NH48 Gurugram'")
            else:
                st.warning("Type a location first.")

    if st.session_state.user_location:
        st.markdown(f"""
        <div class="loc-active">
            📍 <b>Active:</b> {st.session_state.user_location[2]}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span class="slabel">🔍 Search Radius</span>', unsafe_allow_html=True)
    radius = st.slider("", 2, 20, 5, label_visibility="collapsed")
    st.caption(f"Within **{radius} km**")
    st.markdown("---")

    if st.session_state.user_location:
        if st.button("🚨  FIND EMERGENCY SERVICES", use_container_width=True):
            lat, lon, addr = st.session_state.user_location
            with st.spinner("Scanning nearby services..."):
                st.session_state.services = find_nearby_services(lat, lon, radius)
            st.success("✅ Services loaded! Check Map tab.")
    else:
        st.markdown("""
        <div style="background:#fff8f0; border:1px solid #ffe0b2; border-radius:10px;
             padding:0.6rem 0.8rem; font-size:0.82rem; color:#e65100; text-align:center;">
            ☝️ Set your location first
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span class="slabel">☎️ Emergency Numbers</span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="helpline-row">
        <div class="helpline-pill"><span style="font-size:1.3rem">🚑</span><span class="num">108</span>Ambulance</div>
        <div class="helpline-pill"><span style="font-size:1.3rem">🚔</span><span class="num">100</span>Police</div>
    </div>
    <div class="helpline-row">
        <div class="helpline-pill"><span style="font-size:1.3rem">🔥</span><span class="num">101</span>Fire</div>
        <div class="helpline-pill"><span style="font-size:1.3rem">🛣️</span><span class="num">1033</span>Highway</div>
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════
st.markdown("""
<div class="hero">
    <h1>Road Accident Emergency Assistant</h1>
    <p>🇮🇳 India · Locate hospitals · Get AI first-aid guidance · Chat with emergency AI</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="enum-grid">
    <div class="enum-card"><div class="ei">🆘</div><div class="en">112</div><div class="el">National Emergency</div></div>
    <div class="enum-card"><div class="ei">🚑</div><div class="en">108</div><div class="el">Ambulance</div></div>
    <div class="enum-card"><div class="ei">🚔</div><div class="en">100</div><div class="el">Police</div></div>
    <div class="enum-card"><div class="ei">🛣️</div><div class="en">1033</div><div class="el">Highway Helpline</div></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🗺️  Map & Services", "🤖  AI First-Aid Guide", "💬  AI Chat"])

with tab1:
    if st.session_state.user_location and st.session_state.services:
        lat, lon, addr = st.session_state.user_location
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown('<span class="slabel">Live Emergency Map</span>', unsafe_allow_html=True)
            m = create_emergency_map(lat, lon, st.session_state.services)
            st_folium(m, width=None, height=430)
        with col2:
            st.markdown('<span class="slabel">Nearest Services</span>', unsafe_allow_html=True)
            icons = {"hospitals": "🏥", "police": "🚔", "ambulance": "🚑"}
            colors = {"hospitals": "#e53e3e", "police": "#3182ce", "ambulance": "#e67e22"}
            for stype, places in st.session_state.services.items():
                if places:
                    for p in places[:2]:
                        ph = f"📞 {p['phone']}" if p['phone'] else "Phone not listed"
                        c = colors.get(stype, "#6c47ff")
                        st.markdown(f"""
                        <div class="svc-card" style="border-left-color:{c}">
                            <div class="sn">{icons.get(stype,'')} {p['name']}</div>
                            <div class="sd">{ph}</div>
                            <span class="svc-badge">📏 {p['distance_km']} km away</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class="svc-card" style="border-left-color:#ccc">
                        <div class="sn">{icons.get(stype,'')} No {stype} found nearby</div>
                        <div class="sd">Try increasing search radius</div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:3.5rem">🗺️</div>
            <h3 style="font-size:1.1rem; font-weight:600; color:#1a1a2e; margin:1rem 0 0.4rem">
                No services loaded yet
            </h3>
            <p style="color:#aaa; font-size:0.88rem">
                Set your location in the left panel<br>and click Find Emergency Services
            </p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<span class="slabel">Describe the accident</span>', unsafe_allow_html=True)
        situation = st.text_area("",
            placeholder="e.g. Two vehicles collided on NH65. One person is unconscious, another has a bleeding arm...",
            height=150, label_visibility="collapsed")
        if st.button("⚡  Generate Emergency Guidance"):
            if situation.strip():
                loc_info = st.session_state.user_location[2] if st.session_state.user_location else "India"
                with st.spinner("AI analyzing situation..."):
                    guidance = get_ai_guidance(situation, loc_info)
                st.markdown('<span class="slabel" style="margin-top:1.5rem">AI Guidance</span>', unsafe_allow_html=True)
                st.markdown(f'<div class="guidance-box">{guidance}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please describe the accident situation above.")
    with col2:
        st.markdown('<span class="slabel">First Aid Quick Reference</span>', unsafe_allow_html=True)
        st.markdown("""
        <div class="ref-card">
            <div style="color:#6c47ff; font-weight:700; margin-bottom:6px">✅ DO IMMEDIATELY</div>
            ① Call <b>112</b> right away<br>
            ② Turn on hazard lights<br>
            ③ Keep victim still & calm<br>
            ④ Press cloth on bleeding wounds<br>
            ⑤ Stay on line with operator<br><br>
            <div style="color:#e53e3e; font-weight:700; margin-bottom:6px">❌ NEVER DO THIS</div>
            ✗ Move unconscious victims<br>
            ✗ Remove helmets yourself<br>
            ✗ Give water to unconscious<br>
            ✗ Leave the victim alone<br>
            ✗ Crowd around the injured
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown('<span class="slabel">Chat with RoadSoS AI</span>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#f0ecff; border-radius:10px; padding:0.7rem 1rem;
         font-size:0.83rem; color:#5535e0; border:1px solid #d4c9ff; margin-bottom:1rem;">
        💡 Ask anything — what to do, who to call, how to help an injured person
    </div>
    """, unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    if prompt := st.chat_input("Type your question here..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        loc_info = st.session_state.user_location[2] if st.session_state.user_location else "India"
        with st.spinner(""):
            reply = chat_with_ai(st.session_state.chat_history[:-1], prompt, loc_info)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()
