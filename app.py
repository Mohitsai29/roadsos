import streamlit as st
from streamlit_folium import st_folium
from emergency_finder import find_nearby_services, get_nearest_hospital
from ai_assistant import get_ai_guidance, chat_with_ai
from map_module import create_emergency_map
from geopy.geocoders import Nominatim
import base64
import os

st.set_page_config(page_title="RoadSoS", page_icon="🚨", layout="wide")

def get_logo_b64():
    try:
        with open("logo.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return None

logo_b64 = get_logo_b64()

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; margin: 0; padding: 0; }
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
.stApp { background: #f0f4ff; }
.block-container { padding: 1rem !important; max-width: 100% !important; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #c62828 0%, #1a237e 100%);
    border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;
    display: flex; align-items: center; gap: 1rem;
    position: relative; overflow: hidden;
}
.hero::before {
    content: ''; position: absolute; top: -50%; right: -10%;
    width: 200px; height: 200px;
    background: rgba(255,255,255,0.05); border-radius: 50%;
}
.hero-logo { width: 60px; height: 60px; object-fit: contain; flex-shrink: 0; border-radius: 10px; }
.hero-badge {
    display: inline-block; background: rgba(255,255,255,0.15);
    color: white !important; border-radius: 20px; padding: 2px 10px;
    font-size: 0.7rem; font-weight: 600; margin-bottom: 0.4rem;
}
.hero h1 { font-size: clamp(1.1rem, 4vw, 1.8rem); font-weight: 800; color: white !important; margin: 0 0 0.2rem; line-height: 1.2; }
.hero p { color: rgba(255,255,255,0.85) !important; font-size: clamp(0.72rem, 2.5vw, 0.9rem); margin: 0; line-height: 1.4; }

/* ── Emergency numbers ── */
.num-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 8px; margin-bottom: 1rem; }
.num-card {
    background: white; border-radius: 12px; padding: 0.8rem 0.4rem;
    text-align: center; border: 2px solid #e8eaf6;
    text-decoration: none !important; display: block; transition: all 0.2s;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.num-card:hover { transform: translateY(-2px); border-color: #c62828; box-shadow: 0 6px 20px rgba(198,40,40,0.15); }
.num-card .ni { font-size: clamp(1rem, 3vw, 1.4rem); margin-bottom: 4px; }
.num-card .nn { font-size: clamp(1rem, 3.5vw, 1.5rem); font-weight: 800; color: #c62828; line-height: 1; }
.num-card .nl { font-size: clamp(0.55rem, 1.8vw, 0.7rem); color: #546e7a; margin-top: 3px; font-weight: 600; }
.num-card .nc { font-size: clamp(0.5rem, 1.5vw, 0.62rem); color: #1a237e; margin-top: 1px; font-weight: 500; }

/* ── Section card ── */
.section-card {
    background: white; border-radius: 14px; padding: 1.2rem;
    border: 1px solid #e8eaf6; margin-bottom: 1rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.05);
}
.sec-label {
    font-size: 0.65rem; font-weight: 700; text-transform: uppercase;
    letter-spacing: 1.3px; color: #1a237e; margin-bottom: 0.8rem; display: block;
}

/* ── SOS Card ── */
.sos-card {
    background: linear-gradient(135deg, #c62828, #b71c1c);
    border-radius: 14px; padding: 1rem 1.2rem; margin-bottom: 1rem;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 0.8rem;
    box-shadow: 0 6px 24px rgba(198,40,40,0.3);
    animation: pulse-red 2s infinite;
}
@keyframes pulse-red {
    0%,100% { box-shadow: 0 6px 24px rgba(198,40,40,0.3); }
    50% { box-shadow: 0 6px 32px rgba(198,40,40,0.5); }
}
.sos-title { font-size: 0.62rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.75) !important; margin-bottom: 2px; }
.sos-name { font-size: clamp(0.88rem, 3vw, 1rem); font-weight: 700; color: white !important; }
.sos-dist { font-size: 0.78rem; color: rgba(255,255,255,0.8) !important; margin-top: 2px; }
.call-now {
    display: inline-block; background: white; color: #c62828 !important;
    border-radius: 50px; padding: 0.6rem 1.5rem; font-weight: 800;
    font-size: clamp(0.82rem, 2.5vw, 0.95rem); text-decoration: none !important;
    white-space: nowrap; transition: all 0.15s;
    box-shadow: 0 3px 12px rgba(0,0,0,0.2);
}
.call-now:hover { transform: scale(1.04); }

/* ── Quick dial ── */
.dial-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
.dial-btn {
    display: flex; justify-content: space-between; align-items: center;
    background: #f8f9ff; border: 1px solid #e8eaf6; border-radius: 10px;
    padding: 8px 12px; text-decoration: none !important; transition: all 0.15s;
}
.dial-btn:hover { background: #e8eaf6; border-color: #1a237e; }
.dial-btn span { font-size: clamp(0.72rem, 2vw, 0.85rem); color: #37474f; }
.dial-btn b { font-size: clamp(0.82rem, 2.5vw, 0.95rem); color: #c62828 !important; font-weight: 700; }
.dial-sos {
    display: flex; justify-content: space-between; align-items: center;
    background: #1a237e; border-radius: 10px; padding: 8px 12px;
    text-decoration: none !important; margin-top: 6px;
}
.dial-sos span { font-size: clamp(0.72rem, 2vw, 0.85rem); color: white; font-weight: 600; }
.dial-sos b { font-size: clamp(0.82rem, 2.5vw, 0.95rem); color: white !important; font-weight: 700; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: white !important; border-radius: 12px !important;
    padding: 4px !important; border: 1px solid #e8eaf6 !important;
    gap: 3px !important; margin-bottom: 1rem !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px !important; font-size: clamp(0.72rem, 2vw, 0.88rem) !important;
    font-weight: 600 !important; color: #546e7a !important;
    padding: 0.5rem 0.8rem !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #c62828, #1a237e) !important; color: white !important;
}

/* ── Service cards ── */
.svc {
    background: #f8f9ff; border-radius: 12px; padding: 0.9rem 1rem;
    margin: 0.4rem 0; border: 1px solid #e8eaf6; border-left: 4px solid #1a237e;
    transition: all 0.15s;
}
.svc:hover { border-left-color: #c62828; box-shadow: 0 3px 12px rgba(0,0,0,0.08); }
.svc .sname { font-weight: 700; color: #1a237e; font-size: clamp(0.8rem, 2.5vw, 0.92rem); }
.svc .sph { color: #546e7a; font-size: clamp(0.7rem, 2vw, 0.8rem); margin-top: 2px; }
.svc-dist {
    display: inline-block; background: #e8eaf6; color: #1a237e;
    font-size: 0.68rem; font-weight: 700; padding: 2px 8px;
    border-radius: 20px; margin-top: 4px;
}
.call-svc {
    display: inline-block; background: #e8f5e9; color: #2e7d32 !important;
    font-size: 0.68rem; font-weight: 700; padding: 2px 10px;
    border-radius: 20px; margin-top: 4px; margin-left: 5px;
    text-decoration: none !important; border: 1px solid #a5d6a7;
}

/* ── GPS button ── */
.gps-btn {
    display: block; width: 100%; padding: 14px 20px;
    font-size: clamp(0.88rem, 2.5vw, 1rem); font-weight: 700;
    background: linear-gradient(135deg, #c62828, #1a237e);
    color: white; border-radius: 12px; text-align: center;
    text-decoration: none !important; margin-bottom: 8px;
    box-shadow: 0 4px 16px rgba(198,40,40,0.3); transition: all 0.2s;
}
.gps-btn:hover { opacity: 0.92; transform: translateY(-1px); color: white !important; }
.gps-info {
    background: #e8eaf6; border-radius: 10px; padding: 8px 12px;
    font-size: 0.72rem; color: #1a237e; margin-bottom: 10px; line-height: 1.5;
}

/* ── Guidance ── */
.guidance {
    background: #f8f9ff; border-radius: 14px; padding: 1.2rem;
    border: 1px solid #e8eaf6; border-top: 4px solid #c62828;
    line-height: 1.8; color: #263238; font-size: clamp(0.82rem, 2.5vw, 0.93rem);
}
.ref {
    background: #f8f9ff; border-radius: 12px; padding: 1rem;
    border: 1px solid #e8eaf6; border-left: 4px solid #1a237e;
    line-height: 1.85; color: #263238; font-size: clamp(0.78rem, 2.2vw, 0.87rem);
}
.tip {
    background: #e8eaf6; border-radius: 10px; padding: 0.6rem 0.9rem;
    font-size: clamp(0.78rem, 2.2vw, 0.85rem); color: #1a237e;
    margin-bottom: 0.8rem; border: 1px solid #c5cae9;
}
.empty {
    text-align: center; padding: 2.5rem 1.5rem;
    background: #f8f9ff; border-radius: 14px; border: 1px solid #e8eaf6;
}
.radius-badge {
    display: inline-flex; align-items: center; gap: 5px;
    background: #e8eaf6; color: #1a237e; border: 1px solid #c5cae9;
    border-radius: 20px; padding: 3px 12px;
    font-size: clamp(0.72rem, 2vw, 0.82rem); font-weight: 600; margin-bottom: 0.8rem;
}
.loc-found {
    background: #e8f5e9; border: 1px solid #a5d6a7; border-radius: 10px;
    padding: 0.5rem 0.9rem; font-size: clamp(0.75rem, 2vw, 0.85rem);
    color: #1b5e20; margin-top: 0.5rem;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #c62828, #1a237e) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    font-weight: 600 !important; padding: 0.6rem 1.2rem !important;
    font-size: clamp(0.8rem, 2.5vw, 0.93rem) !important;
    transition: all 0.2s !important; width: 100% !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }

/* ── Inputs ── */
.stTextInput > div > div > input {
    border-radius: 10px !important; border: 1.5px solid #e8eaf6 !important;
    color: #263238 !important; font-size: clamp(0.82rem, 2.5vw, 0.93rem) !important;
    padding: 0.6rem 0.9rem !important; background: #f8f9ff !important;
}
.stTextInput > div > div > input::placeholder { color: #90a4ae !important; }
.stTextInput > div > div > input:focus { border-color: #c62828 !important; }
.stTextArea > div > div > textarea {
    border-radius: 10px !important; border: 1.5px solid #e8eaf6 !important;
    color: #263238 !important; font-size: clamp(0.82rem, 2.5vw, 0.93rem) !important;
    background: #f8f9ff !important;
}
.stTextArea > div > div > textarea:focus { border-color: #c62828 !important; }
.stSlider > div > div > div > div { background: #c62828 !important; }
div[data-testid="stChatMessage"] {
    background: #f8f9ff !important; border-radius: 12px !important;
    border: 1px solid #e8eaf6 !important; margin: 0.4rem 0 !important;
}

/* ── Mobile responsive ── */
@media (max-width: 768px) {
    .block-container { padding: 0.6rem !important; }
    .hero { padding: 1rem; border-radius: 12px; }
    .num-row { gap: 5px; }
    .num-card { padding: 0.6rem 0.2rem; border-radius: 10px; }
    .section-card { padding: 0.9rem; border-radius: 12px; }
    .sos-card { padding: 0.9rem 1rem; }
    .dial-grid { grid-template-columns: 1fr 1fr; gap: 5px; }
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──
for key, default in [
    ("chat_history",[]), ("services",None),
    ("user_location",None), ("search_radius_used",None), ("gps_auto",False)
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ── Read GPS from URL query params ──
params = st.query_params
if "lat" in params and "lon" in params:
    try:
        lat_q = float(params["lat"])
        lon_q = float(params["lon"])
        if 6.5 <= lat_q <= 37.5 and 68.0 <= lon_q <= 97.5:
            if not st.session_state.user_location:
                st.session_state.user_location = (lat_q, lon_q, f"{lat_q:.5f}, {lon_q:.5f}")
                st.session_state.gps_auto = True
        st.query_params.clear()
    except:
        pass

def auto_search(lat, lon, max_radius=20.0):
    radius = 0.5
    ph = st.empty()
    while radius <= max_radius:
        r_label = f"{int(radius*1000)} m" if radius < 1 else f"{radius:.1f} km"
        ph.markdown(f"""
        <div style="background:#e8eaf6;border:1px solid #c5cae9;border-radius:12px;padding:0.9rem 1.2rem;margin-bottom:0.8rem;">
            <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#1a237e;margin-bottom:0.4rem;">🔍 Auto-scanning nearby services</div>
            <div style="font-size:0.9rem;color:#c62828;font-weight:600;">⏳ Searching within <b>{r_label}</b>...</div>
            <div style="font-size:0.72rem;color:#546e7a;margin-top:3px;">Expands automatically up to {max_radius} km</div>
        </div>
        """, unsafe_allow_html=True)
        services = find_nearby_services(lat, lon, radius)
        total = sum(len(v) for v in services.values())
        if total > 0:
            ph.markdown(f"""
            <div style="background:#e8f5e9;border:1px solid #a5d6a7;border-radius:12px;padding:0.9rem 1.2rem;margin-bottom:0.8rem;">
                <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#1b5e20;margin-bottom:0.4rem;">✅ Services found!</div>
                <div style="font-size:0.9rem;color:#2e7d32;font-weight:600;">Found <b>{total} services</b> within <b>{r_label}</b></div>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.search_radius_used = radius
            return services, radius
        radius = round(radius + 0.5, 1)
    ph.markdown(f"""
    <div style="background:#ffebee;border:1px solid #ffcdd2;border-radius:12px;padding:0.9rem 1.2rem;margin-bottom:0.8rem;">
        <div style="font-size:0.9rem;color:#c62828;font-weight:600;">⚠️ No services within {max_radius} km. Call 112.</div>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.search_radius_used = max_radius
    return {}, max_radius

# ── Auto-search after GPS redirect ──
if st.session_state.gps_auto and st.session_state.user_location and not st.session_state.services:
    st.session_state.gps_auto = False
    lat_a, lon_a, _ = st.session_state.user_location
    svcs, _ = auto_search(lat_a, lon_a)
    st.session_state.services = svcs
    st.rerun()

# ── HERO ──
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="hero-logo"/>' if logo_b64 else '<div style="font-size:2.5rem;flex-shrink:0;">🚨</div>'
st.markdown(f"""
<div class="hero">
    {logo_html}
    <div>
        <div class="hero-badge">🇮🇳 India Road Safety · AI Powered</div>
        <h1>RoadSoS Emergency Assistant</h1>
        <p>Locate hospitals · AI first-aid guidance · One-tap emergency calling</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── EMERGENCY NUMBERS ──
st.markdown("""
<div class="num-row">
    <a href="tel:112" class="num-card"><div class="ni">🆘</div><div class="nn">112</div><div class="nl">National SOS</div><div class="nc">Tap to call</div></a>
    <a href="tel:108" class="num-card"><div class="ni">🚑</div><div class="nn">108</div><div class="nl">Ambulance</div><div class="nc">Tap to call</div></a>
    <a href="tel:100" class="num-card"><div class="ni">🚔</div><div class="nn">100</div><div class="nl">Police</div><div class="nc">Tap to call</div></a>
    <a href="tel:1033" class="num-card"><div class="ni">🛣️</div><div class="nn">1033</div><div class="nl">Highway</div><div class="nc">Tap to call</div></a>
</div>
""", unsafe_allow_html=True)

# ── LOCATION SECTION ──
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<span class="sec-label">📍 Detect Location & Auto-Search Services</span>', unsafe_allow_html=True)

left, right = st.columns([3, 2])

with left:
    GPS_URL = "https://mohitsai29.github.io/roadsos/gps.html"
    st.markdown(f"""
    <a href="{GPS_URL}" class="gps-btn">📍 Detect My Exact GPS Location</a>
    <div class="gps-info">
        ℹ️ Opens GPS page → detects your exact location → returns here automatically
    </div>
    """, unsafe_allow_html=True)

    coord_input = st.text_input("",
        placeholder="GPS auto-fills here — or type city: Vijayawada",
        label_visibility="collapsed", key="coord_box")

    st.markdown('<span style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#1a237e;margin-bottom:0.3rem;display:block;">🔍 Max Search Radius</span>', unsafe_allow_html=True)
    max_radius = st.slider("", 5, 50, 20, format="%d km", label_visibility="collapsed")
    st.caption(f"Auto-searches from 500 m up to **{max_radius} km**")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Use Location & Search"):
            val = coord_input.strip()
            if not val:
                st.warning("⚠️ Detect GPS or type a city")
            elif "," in val:
                try:
                    p = val.split(",")
                    lat, lon = float(p[0].strip()), float(p[1].strip())
                    if 6.5 <= lat <= 37.5 and 68.0 <= lon <= 97.5:
                        st.session_state.user_location = (lat, lon, f"{lat:.5f}, {lon:.5f}")
                        services, radius = auto_search(lat, lon, max_radius)
                        st.session_state.services = services
                        st.rerun()
                    else:
                        st.error("⚠️ Outside India")
                except:
                    st.error("⚠️ Invalid format")
            else:
                with st.spinner("Finding..."):
                    geo = Nominatim(user_agent="roadsos_v11")
                    loc = geo.geocode(val + ", India", country_codes="IN")
                if loc and 6.5 <= loc.latitude <= 37.5:
                    st.session_state.user_location = (loc.latitude, loc.longitude, val)
                    services, radius = auto_search(loc.latitude, loc.longitude, max_radius)
                    st.session_state.services = services
                    st.rerun()
                else:
                    st.error("⚠️ Not found in India")
    with c2:
        if st.button("🗑️ Clear"):
            for k in ["user_location","services","search_radius_used"]:
                st.session_state[k] = None
            st.rerun()

    if st.session_state.user_location:
        r = st.session_state.search_radius_used
        r_label = f"{int(r*1000)} m" if r and r<1 else (f"{r:.1f} km" if r else "")
        total = sum(len(v) for v in st.session_state.services.values()) if st.session_state.services else 0
        st.markdown(f"""
        <div class="loc-found">
            ✅ <b>{st.session_state.user_location[2]}</b>
            {"&nbsp;·&nbsp; 🔍 "+str(total)+" services within "+r_label if r_label else ""}
        </div>
        """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div style="background:#f8f9ff;border-radius:12px;padding:1rem;border:1px solid #e8eaf6;border-top:3px solid #1a237e;">
        <div style="font-size:0.65rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#1a237e;margin-bottom:0.7rem;">☎️ Tap to Call</div>
        <div class="dial-grid">
            <a href="tel:108" class="dial-btn"><span>🚑 Ambulance</span><b>108</b></a>
            <a href="tel:100" class="dial-btn"><span>🚔 Police</span><b>100</b></a>
            <a href="tel:101" class="dial-btn"><span>🔥 Fire</span><b>101</b></a>
            <a href="tel:1033" class="dial-btn"><span>🛣️ Highway</span><b>1033</b></a>
        </div>
        <a href="tel:112" class="dial-sos"><span>🆘 National SOS</span><b>112</b></a>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── NEAREST HOSPITAL SOS CARD ──
if st.session_state.services:
    nearest = get_nearest_hospital(st.session_state.services)
    if nearest:
        phone = nearest.get("phone","").strip()
        href  = f"tel:{phone}" if phone else "tel:108"
        label = "📞 Call Now" if phone else "📞 Call 108"
        phone_txt = f"📞 {phone}" if phone else "No phone — tap calls 108"
        st.markdown(f"""
        <div class="sos-card">
            <div>
                <div class="sos-title">🏥 Nearest Hospital — Tap to Call</div>
                <div class="sos-name">{nearest['name']}</div>
                <div class="sos-dist">📏 {nearest['distance_km']} km &nbsp;·&nbsp; {phone_txt}</div>
            </div>
            <a href="{href}" class="call-now">{label}</a>
        </div>
        """, unsafe_allow_html=True)

# ── TABS ──
tab1, tab2, tab3 = st.tabs(["🗺️ Map & Services","🤖 AI First-Aid","💬 AI Chat"])

with tab1:
    if st.session_state.user_location and st.session_state.services:
        lat, lon, _ = st.session_state.user_location
        total = sum(len(v) for v in st.session_state.services.values())
        if total == 0:
            st.markdown("""
            <div class="empty">
                <div style="font-size:2rem">🔍</div>
                <div style="font-weight:700;color:#1a237e;margin:0.6rem 0 0.3rem;font-size:0.95rem;">No services found</div>
                <div style="color:#546e7a;font-size:0.82rem;">Increase radius and search again</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            r = st.session_state.search_radius_used or 0
            r_label = f"{int(r*1000)} m" if r<1 else f"{r:.1f} km"
            st.markdown(f'<div class="radius-badge">🔍 Services within <b>&nbsp;{r_label}&nbsp;</b></div>', unsafe_allow_html=True)
            col1, col2 = st.columns([3,2])
            with col1:
                st.markdown('<span class="sec-label">Live Emergency Map</span>', unsafe_allow_html=True)
                m = create_emergency_map(lat, lon, st.session_state.services)
                st_folium(m, width=None, height=400)
            with col2:
                st.markdown('<span class="sec-label">Nearest Services</span>', unsafe_allow_html=True)
                icons  = {"hospitals":"🏥","police":"🚔","ambulance":"🚑"}
                colors = {"hospitals":"#c62828","police":"#1a237e","ambulance":"#e65100"}
                for stype, places in st.session_state.services.items():
                    if places:
                        for p in places[:2]:
                            ph = p.get("phone","")
                            c  = colors.get(stype,"#1a237e")
                            call_html = f'<a href="tel:{ph}" class="call-svc">📞 Call</a>' if ph else ''
                            st.markdown(f"""
                            <div class="svc" style="border-left-color:{c}">
                                <div class="sname">{icons.get(stype,'')} {p['name']}</div>
                                <div class="sph">{"📞 "+ph if ph else "Phone not listed"}</div>
                                <span class="svc-dist">📏 {p['distance_km']} km</span>{call_html}
                            </div>
                            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty">
            <div style="font-size:2.5rem">🗺️</div>
            <div style="font-weight:700;font-size:0.95rem;color:#1a237e;margin:0.8rem 0 0.3rem;">
                Detect GPS → Use Location → Map loads here
            </div>
            <div style="color:#546e7a;font-size:0.82rem;">Searches from 500 m and expands until services found</div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown('<span class="sec-label">Describe the Accident</span>', unsafe_allow_html=True)
        situation = st.text_area("",
            placeholder="e.g. Two vehicles collided on NH65. One person unconscious, another bleeding...",
            height=140, label_visibility="collapsed")
        if st.button("⚡ Get AI Emergency Guidance"):
            if situation.strip():
                loc_info = st.session_state.user_location[2] if st.session_state.user_location else "India"
                with st.spinner("AI analyzing..."):
                    guidance = get_ai_guidance(situation, loc_info)
                st.markdown('<span class="sec-label" style="margin-top:0.8rem;">AI Guidance</span>', unsafe_allow_html=True)
                st.markdown(f'<div class="guidance">{guidance}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please describe the accident situation first.")
    with col2:
        st.markdown('<span class="sec-label">Quick Reference</span>', unsafe_allow_html=True)
        st.markdown("""
        <div class="ref">
            <div style="color:#c62828;font-weight:700;margin-bottom:6px;">✅ DO IMMEDIATELY</div>
            ① Call <b>112</b> right away<br>
            ② Switch on hazard lights<br>
            ③ Keep victim still &amp; calm<br>
            ④ Press cloth on wounds<br>
            ⑤ Stay on call with operator<br><br>
            <div style="color:#1a237e;font-weight:700;margin-bottom:6px;">❌ NEVER DO THIS</div>
            ✗ Move unconscious victims<br>
            ✗ Remove helmet yourself<br>
            ✗ Give water/food to victim<br>
            ✗ Leave the victim alone<br>
            ✗ Crowd around the injured
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown('<span class="sec-label">Chat with RoadSoS AI</span>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tip">
        💡 Ask anything — "What if someone is unconscious?", "How to stop bleeding?", "Is it safe to move them?"
    </div>
    """, unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    if prompt := st.chat_input("Ask your emergency question..."):
        st.session_state.chat_history.append({"role":"user","content":prompt})
        loc_info = st.session_state.user_location[2] if st.session_state.user_location else "India"
        with st.spinner("Thinking..."):
            reply = chat_with_ai(st.session_state.chat_history[:-1], prompt, loc_info)
        st.session_state.chat_history.append({"role":"assistant","content":reply})
        st.rerun()
