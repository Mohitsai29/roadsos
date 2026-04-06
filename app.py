import streamlit as st
from streamlit_folium import st_folium
from emergency_finder import find_nearby_services, get_nearest_hospital, OFFLINE_CONTACTS
from map_module import create_emergency_map
from geopy.geocoders import Nominatim
import base64

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
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
.stApp { background: #0f0e1a; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px !important; }
.hero { background: linear-gradient(135deg,#4f46e5 0%,#7c3aed 60%,#9333ea 100%); border-radius:24px; padding:2.2rem 3rem; margin-bottom:1.5rem; position:relative; overflow:hidden; display:flex; align-items:center; gap:2rem; }
.hero-text { flex:1; }
.hero-logo { width:100px; height:100px; object-fit:contain; filter:drop-shadow(0 0 20px rgba(255,255,255,0.3)); flex-shrink:0; }
.hero-badge { display:inline-block; background:rgba(255,255,255,0.15); color:white !important; border-radius:20px; padding:4px 16px; font-size:0.78rem; font-weight:600; margin-bottom:0.8rem; }
.hero h1 { font-size:2.1rem; font-weight:800; color:white !important; margin:0 0 0.4rem; }
.hero p { color:rgba(255,255,255,0.8) !important; margin:0; font-size:0.95rem; }
.section-card { background:#13112b; border-radius:20px; padding:1.5rem 1.8rem; border:1px solid #2a2660; margin-bottom:1.2rem; }
.sec-label { font-size:0.68rem; font-weight:700; text-transform:uppercase; letter-spacing:1.4px; color:#6366f1; margin-bottom:1rem; display:block; }
.num-row { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:1.2rem; }
.num-card { background:#13112b; border-radius:18px; padding:1.2rem 1rem; text-align:center; border:1px solid #2a2660; transition:all 0.2s; text-decoration:none !important; display:block; }
.num-card:hover { transform:translateY(-3px); border-color:#4f46e5; box-shadow:0 8px 28px rgba(79,70,229,0.3); }
.num-card .ni { font-size:1.6rem; margin-bottom:6px; }
.num-card .nn { font-size:1.8rem; font-weight:800; color:#818cf8; line-height:1; }
.num-card .nl { font-size:0.73rem; color:#6366f1; margin-top:4px; }
.num-card .nc { font-size:0.68rem; color:#4f46e5; margin-top:2px; }
.sos-card { background:linear-gradient(135deg,#dc2626,#b91c1c); border-radius:20px; padding:1.4rem 2rem; margin-bottom:1.2rem; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:1rem; animation:pulse-red 2s infinite; }
@keyframes pulse-red { 0%,100% { box-shadow:0 8px 32px rgba(220,38,38,0.3); } 50% { box-shadow:0 8px 40px rgba(220,38,38,0.55); } }
.sos-title { font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:rgba(255,255,255,0.7) !important; margin-bottom:3px; }
.sos-name { font-size:1.1rem; font-weight:700; color:white !important; }
.sos-dist { font-size:0.83rem; color:rgba(255,255,255,0.75) !important; margin-top:2px; }
.call-now { display:inline-block; background:white; color:#dc2626 !important; border-radius:50px; padding:0.75rem 2.2rem; font-weight:800; font-size:1.05rem; text-decoration:none !important; white-space:nowrap; transition:all 0.15s; }
.call-now:hover { transform:scale(1.05); }
.stTabs [data-baseweb="tab-list"] { background:#13112b !important; border-radius:16px !important; padding:6px !important; border:1px solid #2a2660 !important; gap:4px !important; margin-bottom:1.2rem !important; }
.stTabs [data-baseweb="tab"] { border-radius:12px !important; font-size:0.9rem !important; font-weight:500 !important; color:#6366f1 !important; padding:0.6rem 1.5rem !important; }
.stTabs [aria-selected="true"] { background:linear-gradient(135deg,#4f46e5,#7c3aed) !important; color:white !important; }
.svc { background:#1e1a3f; border-radius:14px; padding:1rem 1.2rem; margin:0.5rem 0; border:1px solid #2a2660; border-left:4px solid #4f46e5; }
.svc .sname { font-weight:600; color:#e0e7ff; font-size:0.92rem; }
.svc .sph { color:#6366f1; font-size:0.8rem; margin-top:2px; }
.svc-dist { display:inline-block; background:#13112b; color:#818cf8; font-size:0.72rem; font-weight:600; padding:2px 10px; border-radius:20px; margin-top:5px; border:1px solid #2a2660; }
.call-svc { display:inline-block; background:#052e16; color:#34d399 !important; font-size:0.75rem; font-weight:700; padding:2px 12px; border-radius:20px; margin-top:5px; margin-left:6px; text-decoration:none !important; border:1px solid #166534; }
.empty { text-align:center; padding:3rem 2rem; background:#13112b; border-radius:18px; border:1px solid #2a2260; }
.radius-badge { display:inline-flex; align-items:center; gap:6px; background:#1e1a3f; color:#818cf8; border:1px solid #2a2660; border-radius:20px; padding:4px 14px; font-size:0.82rem; font-weight:600; margin-bottom:0.8rem; }
.loc-found { background:#1e1a3f; border:1px solid #4f46e5; border-radius:10px; padding:0.5rem 1rem; font-size:0.85rem; color:#a5b4fc; margin-top:0.5rem; }
.stButton > button { background:linear-gradient(135deg,#4f46e5,#7c3aed) !important; color:white !important; border:none !important; border-radius:12px !important; font-weight:600 !important; padding:0.65rem 1.5rem !important; font-size:0.93rem !important; transition:all 0.2s !important; width:100% !important; }
.stButton > button:hover { opacity:0.88 !important; transform:translateY(-1px) !important; }
.stTextInput > div > div > input { border-radius:12px !important; border:1.5px solid #2a2660 !important; color:#e0e7ff !important; font-size:0.93rem !important; padding:0.65rem 1rem !important; background:#1e1a3f !important; }
.stTextInput > div > div > input::placeholder { color:#6366f1 !important; }
.stSlider > div > div > div > div { background:#4f46e5 !important; }
</style>
""", unsafe_allow_html=True)

for key, default in [
    ("chat_history",[]), ("services",None),
    ("user_location",None), ("search_radius_used",None), ("gps_auto",False)
]:
    if key not in st.session_state:
        st.session_state[key] = default

params = st.query_params
if "lat" in params and "lon" in params:
    try:
        lat_q = float(params["lat"])
        lon_q = float(params["lon"])
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
        <div style="background:#1e1a3f;border:1px solid #2a2660;border-radius:14px;padding:1rem 1.5rem;margin-bottom:1rem;">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:1.4px;color:#6366f1;margin-bottom:0.5rem;">🔍 Auto-scanning</div>
            <div style="font-size:0.9rem;color:#fbbf24;font-weight:600;">⏳ Searching within <b>{r_label}</b>...</div>
            <div style="font-size:0.75rem;color:#4f46e5;margin-top:4px;">Expands automatically up to {max_radius} km</div>
        </div>
        """, unsafe_allow_html=True)
        services = find_nearby_services(lat, lon, radius)
        total = sum(len(v) for v in services.values())
        if total > 0:
            ph.markdown(f"""
            <div style="background:#052e16;border:1px solid #166534;border-radius:14px;padding:1rem 1.5rem;margin-bottom:1rem;">
                <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:1.4px;color:#34d399;margin-bottom:0.5rem;">✅ Services found!</div>
                <div style="font-size:0.9rem;color:#34d399;font-weight:600;">Found <b>{total} services</b> within <b>{r_label}</b></div>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.search_radius_used = radius
            return services, radius
        radius = round(radius + 0.5, 1)
    ph.markdown("""
    <div style="background:#450a0a;border:1px solid #991b1b;border-radius:14px;padding:1rem 1.5rem;margin-bottom:1rem;">
        <div style="font-size:0.9rem;color:#f87171;font-weight:600;">⚠️ No live services found. Check Offline Contacts tab.</div>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.search_radius_used = max_radius
    return {}, max_radius

if st.session_state.gps_auto and st.session_state.user_location and not st.session_state.services:
    st.session_state.gps_auto = False
    lat_a, lon_a, _ = st.session_state.user_location
    svcs, _ = auto_search(lat_a, lon_a)
    st.session_state.services = svcs
    st.rerun()

# ── HERO ──
logo_html = f'<img src="data:image/png;base64,{logo_b64}" class="hero-logo"/>' if logo_b64 else '<div style="font-size:4rem">🚨</div>'
st.markdown(f"""
<div class="hero">
    {logo_html}
    <div class="hero-text">
        <div class="hero-badge">🌍 Global Road Safety · AI Powered</div>
        <h1>RoadSoS — Emergency Assistant</h1>
        <p>Hospitals · Police · Ambulance · Towing · Fuel · Showrooms · Offline Support</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── EMERGENCY NUMBERS ──
st.markdown("""
<div class="num-row">
    <a href="tel:112" class="num-card"><div class="ni">🆘</div><div class="nn">112</div><div class="nl">National SOS</div><div class="nc">Tap to call</div></a>
    <a href="tel:108" class="num-card"><div class="ni">🚑</div><div class="nn">108</div><div class="nl">Ambulance</div><div class="nc">Tap to call</div></a>
    <a href="tel:100" class="num-card"><div class="ni">🚔</div><div class="nn">100</div><div class="nl">Police</div><div class="nc">Tap to call</div></a>
    <a href="tel:1033" class="num-card"><div class="ni">🛣️</div><div class="nn">1033</div><div class="nl">Highway Help</div><div class="nc">Tap to call</div></a>
</div>
""", unsafe_allow_html=True)

# ── LOCATION SECTION ──
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<span class="sec-label">📍 Step 1 — Detect Location & Auto-Search Services</span>', unsafe_allow_html=True)

left, right = st.columns([2, 1])

with left:
    GPS_URL = "https://mohitsai29.github.io/roadsos/gps.html"
    st.markdown(f"""
    <a href="{GPS_URL}" target="_blank" style="
        display:block; width:100%; padding:16px 20px; font-size:16px; font-weight:700;
        background:linear-gradient(135deg,#4f46e5,#7c3aed); color:white;
        border-radius:14px; cursor:pointer; text-align:center;
        text-decoration:none; margin-bottom:10px;">
        📍 Detect My Exact GPS Location
    </a>
    <div style="background:#1e1a3f;border:1px solid #2a2660;border-radius:10px;
         padding:10px 14px;font-size:12px;color:#6366f1;margin-bottom:12px;line-height:1.6;">
        ℹ️ Opens GPS page → detects your exact location → automatically returns here
    </div>
    """, unsafe_allow_html=True)

    coord_input = st.text_input("",
        placeholder="GPS auto-fills here — or type city: Vijayawada",
        label_visibility="collapsed", key="coord_box")

    st.markdown('<span style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:1.4px;color:#6366f1;margin-bottom:0.3rem;display:block;">🔍 Max Search Radius</span>', unsafe_allow_html=True)
    max_radius = st.slider("", 5, 50, 20, format="%d km",
        label_visibility="collapsed", key="radius_slider")
    st.caption(f"Auto-searches from 500 m up to **{max_radius} km**")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Use Location & Auto-Search"):
            val = coord_input.strip()
            if not val:
                st.warning("⚠️ Detect GPS or type a city name")
            elif "," in val:
                try:
                    p = val.split(",")
                    lat, lon = float(p[0].strip()), float(p[1].strip())
                    st.session_state.user_location = (lat, lon, f"{lat:.5f}, {lon:.5f}")
                    services, radius = auto_search(lat, lon, max_radius)
                    st.session_state.services = services
                    st.rerun()
                except:
                    st.error("⚠️ Invalid. Try: 16.514445, 80.679274")
            else:
                with st.spinner("Finding..."):
                    geo = Nominatim(user_agent="roadsos_v11")
                    loc = geo.geocode(val)
                if loc:
                    st.session_state.user_location = (loc.latitude, loc.longitude, val)
                    services, radius = auto_search(loc.latitude, loc.longitude, max_radius)
                    st.session_state.services = services
                    st.rerun()
                else:
                    st.error("⚠️ Location not found.")
    with col2:
        if st.button("🗑️ Clear & Reset"):
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
    <div style="background:#1e1a3f;border-radius:16px;padding:1.2rem;border:1px solid #2a2660;">
        <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:1.4px;color:#6366f1;margin-bottom:0.8rem;">☎️ Tap to Call</div>
        <a href="tel:108" style="display:flex;justify-content:space-between;align-items:center;background:#13112b;border:1px solid #2a2660;border-radius:10px;padding:10px 14px;margin:5px 0;text-decoration:none;">
            <span style="color:#e0e7ff;font-size:0.9rem;">🚑 Ambulance</span><b style="color:#818cf8;font-size:1.05rem;">108</b></a>
        <a href="tel:100" style="display:flex;justify-content:space-between;align-items:center;background:#13112b;border:1px solid #2a2660;border-radius:10px;padding:10px 14px;margin:5px 0;text-decoration:none;">
            <span style="color:#e0e7ff;font-size:0.9rem;">🚔 Police</span><b style="color:#818cf8;font-size:1.05rem;">100</b></a>
        <a href="tel:101" style="display:flex;justify-content:space-between;align-items:center;background:#13112b;border:1px solid #2a2660;border-radius:10px;padding:10px 14px;margin:5px 0;text-decoration:none;">
            <span style="color:#e0e7ff;font-size:0.9rem;">🔥 Fire</span><b style="color:#818cf8;font-size:1.05rem;">101</b></a>
        <a href="tel:1033" style="display:flex;justify-content:space-between;align-items:center;background:#13112b;border:1px solid #2a2660;border-radius:10px;padding:10px 14px;margin:5px 0;text-decoration:none;">
            <span style="color:#e0e7ff;font-size:0.9rem;">🛣️ Highway</span><b style="color:#818cf8;font-size:1.05rem;">1033</b></a>
        <a href="tel:112" style="display:flex;justify-content:space-between;align-items:center;background:#4f46e5;border:1px solid #6366f1;border-radius:10px;padding:10px 14px;margin:5px 0;text-decoration:none;">
            <span style="color:white;font-size:0.9rem;font-weight:700;">🆘 National SOS</span><b style="color:white;font-size:1.05rem;">112</b></a>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── NEAREST HOSPITAL SOS CARD ──
if st.session_state.services:
    nearest = get_nearest_hospital(st.session_state.services)
    if nearest:
        phone = nearest.get("phone","").strip()
        href = f"tel:{phone}" if phone else "tel:108"
        label = "📞 Call Now" if phone else "📞 Call 108"
        phone_txt = f"📞 {phone}" if phone else "No phone — tap calls 108"
        st.markdown(f"""
        <div class="sos-card">
            <div>
                <div class="sos-title">🏥 Nearest Hospital — Tap to Call Instantly</div>
                <div class="sos-name">{nearest['name']}</div>
                <div class="sos-dist">📏 {nearest['distance_km']} km away &nbsp;·&nbsp; {phone_txt}</div>
            </div>
            <a href="{href}" class="call-now">{label}</a>
        </div>
        """, unsafe_allow_html=True)

# ── TABS ──
tab1, tab2 = st.tabs(["🗺️  Map & Services", "📵  Offline Emergency Contacts"])

with tab1:
    if st.session_state.user_location and st.session_state.services:
        lat, lon, _ = st.session_state.user_location
        total = sum(len(v) for v in st.session_state.services.values())
        if total == 0:
            st.markdown("""
            <div class="empty">
                <div style="font-size:2.5rem">📵</div>
                <div style="font-weight:600;color:#e0e7ff;margin:0.8rem 0 0.3rem;">No live services found</div>
                <div style="color:#6366f1;font-size:0.88rem;">Check Offline Contacts tab · Try increasing radius</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            r = st.session_state.search_radius_used or 0
            r_label = f"{int(r*1000)} m" if r<1 else f"{r:.1f} km"
            st.markdown(f'<div class="radius-badge">🔍 Services within <b>&nbsp;{r_label}&nbsp;</b> of your location</div>', unsafe_allow_html=True)
            col1, col2 = st.columns([3,2])
            with col1:
                st.markdown('<span class="sec-label">Live Emergency Map</span>', unsafe_allow_html=True)
                m = create_emergency_map(lat, lon, st.session_state.services)
                st_folium(m, width=None, height=450)
            with col2:
                st.markdown('<span class="sec-label">Nearest Services</span>', unsafe_allow_html=True)
                icons = {
                    "hospitals":"🏥","police":"🚔","ambulance":"🚑",
                    "towing":"🔧","fuel":"⛽","showrooms":"🚗"
                }
                colors = {
                    "hospitals":"#dc2626","police":"#2563eb",
                    "ambulance":"#d97706","towing":"#7c3aed",
                    "fuel":"#059669","showrooms":"#0891b2"
                }
                labels = {
                    "hospitals":"Hospital","police":"Police Station",
                    "ambulance":"Ambulance","towing":"Towing/Repair",
                    "fuel":"Fuel Station","showrooms":"Showroom"
                }
                for stype, places in st.session_state.services.items():
                    if places:
                        for p in places[:2]:
                            ph = p.get("phone","")
                            c = colors.get(stype,"#4f46e5")
                            call_html = f'<a href="tel:{ph}" class="call-svc">📞 Call</a>' if ph else ''
                            st.markdown(f"""
                            <div class="svc" style="border-left-color:{c}">
                                <div class="sname">{icons.get(stype,'')} {p['name']}</div>
                                <div style="font-size:0.72rem;color:{c};font-weight:600;margin-top:1px;">{labels.get(stype,'')}</div>
                                <div class="sph">{"📞 "+ph if ph else "Phone not listed"}</div>
                                <span class="svc-dist">📏 {p['distance_km']} km</span>{call_html}
                            </div>
                            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty">
            <div style="font-size:3rem">🗺️</div>
            <div style="font-weight:600;font-size:1rem;color:#e0e7ff;margin:1rem 0 0.4rem;">
                Click GPS → Allow → Open RoadSoS → Map loads here
            </div>
            <div style="color:#6366f1;font-size:0.88rem;">
                Finds hospitals, police, ambulance, towing, fuel & showrooms
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown('<span class="sec-label">📵 Offline Emergency Contacts — Works Without Internet</span>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#052e16;border:1px solid #166534;border-radius:12px;
         padding:0.8rem 1rem;margin-bottom:1rem;font-size:0.85rem;color:#34d399;">
        ℹ️ These contacts work even without internet. Save them on your phone!
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="background:#1e1a3f;border-radius:14px;padding:1rem;border:1px solid #2a2660;margin-bottom:0.8rem;">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:1.4px;color:#6366f1;margin-bottom:0.8rem;">🆘 Emergency</div>
            <a href="tel:112" style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #2a2660;text-decoration:none;">
                <span style="color:#e0e7ff;font-size:0.88rem;">🆘 National SOS</span><b style="color:#818cf8;">112</b></a>
            <a href="tel:108" style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #2a2660;text-decoration:none;">
                <span style="color:#e0e7ff;font-size:0.88rem;">🚑 Ambulance</span><b style="color:#818cf8;">108</b></a>
            <a href="tel:100" style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #2a2660;text-decoration:none;">
                <span style="color:#e0e7ff;font-size:0.88rem;">🚔 Police</span><b style="color:#818cf8;">100</b></a>
            <a href="tel:101" style="display:flex;justify-content:space-between;padding:8px 0;text-decoration:none;">
                <span style="color:#e0e7ff;font-size:0.88rem;">🔥 Fire</span><b style="color:#818cf8;">101</b></a>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style="background:#1e1a3f;border-radius:14px;padding:1rem;border:1px solid #2a2660;margin-bottom:0.8rem;">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:1.4px;color:#6366f1;margin-bottom:0.8rem;">🛣️ Road Help</div>
            <a href="tel:1033" style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #2a2660;text-decoration:none;">
                <span style="color:#e0e7ff;font-size:0.88rem;">🛣️ Highway Help</span><b style="color:#818cf8;">1033</b></a>
            <a href="tel:1073" style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #2a2660;text-decoration:none;">
                <span style="color:#e0e7ff;font-size:0.88rem;">🚦 Road Accident</span><b style="color:#818cf8;">1073</b></a>
            <a href="tel:104" style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #2a2660;text-decoration:none;">
                <span style="color:#e0e7ff;font-size:0.88rem;">🏥 Health Line</span><b style="color:#818cf8;">104</b></a>
            <a href="tel:1070" style="display:flex;justify-content:space-between;padding:8px 0;text-decoration:none;">
                <span style="color:#e0e7ff;font-size:0.88rem;">🌊 Disaster</span><b style="color:#818cf8;">1070</b></a>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div style="background:#1e1a3f;border-radius:14px;padding:1rem;border:1px solid #2a2660;margin-bottom:0.8rem;">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:1.4px;color:#6366f1;margin-bottom:0.8rem;">👨‍👩‍👧 Other Help</div>
            <a href="tel:1091" style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #2a2660;text-decoration:none;">
                <span style="color:#e0e7ff;font-size:0.88rem;">👩 Women Help</span><b style="color:#818cf8;">1091</b></a>
            <a href="tel:1098" style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #2a2660;text-decoration:none;">
                <span style="color:#e0e7ff;font-size:0.88rem;">👦 Child Help</span><b style="color:#818cf8;">1098</b></a>
            <a href="tel:1800111363" style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #2a2660;text-decoration:none;">
                <span style="color:#e0e7ff;font-size:0.88rem;">👴 Senior Help</span><b style="color:#818cf8;">1800-111-363</b></a>
            <a href="tel:9152987821" style="display:flex;justify-content:space-between;padding:8px 0;text-decoration:none;">
                <span style="color:#e0e7ff;font-size:0.88rem;">🧠 Mental Health</span><b style="color:#818cf8;">iCall</b></a>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:#1e1a3f;border-radius:14px;padding:1rem 1.2rem;border:1px solid #2a2660;margin-top:0.5rem;">
        <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:1.4px;color:#6366f1;margin-bottom:0.8rem;">🌍 International Emergency Numbers</div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;">
            <div style="background:#13112b;border-radius:10px;padding:8px;text-align:center;">
                <div style="color:#6366f1;font-size:0.72rem;">🇮🇳 India</div>
                <div style="color:#818cf8;font-weight:700;font-size:1rem;">112</div>
            </div>
            <div style="background:#13112b;border-radius:10px;padding:8px;text-align:center;">
                <div style="color:#6366f1;font-size:0.72rem;">🇺🇸 USA</div>
                <div style="color:#818cf8;font-weight:700;font-size:1rem;">911</div>
            </div>
            <div style="background:#13112b;border-radius:10px;padding:8px;text-align:center;">
                <div style="color:#6366f1;font-size:0.72rem;">🇬🇧 UK</div>
                <div style="color:#818cf8;font-weight:700;font-size:1rem;">999</div>
            </div>
            <div style="background:#13112b;border-radius:10px;padding:8px;text-align:center;">
                <div style="color:#6366f1;font-size:0.72rem;">🇪🇺 Europe</div>
                <div style="color:#818cf8;font-weight:700;font-size:1rem;">112</div>
            </div>
            <div style="background:#13112b;border-radius:10px;padding:8px;text-align:center;">
                <div style="color:#6366f1;font-size:0.72rem;">🇦🇺 Australia</div>
                <div style="color:#818cf8;font-weight:700;font-size:1rem;">000</div>
            </div>
            <div style="background:#13112b;border-radius:10px;padding:8px;text-align:center;">
                <div style="color:#6366f1;font-size:0.72rem;">🇨🇦 Canada</div>
                <div style="color:#818cf8;font-weight:700;font-size:1rem;">911</div>
            </div>
            <div style="background:#13112b;border-radius:10px;padding:8px;text-align:center;">
                <div style="color:#6366f1;font-size:0.72rem;">🇦🇪 UAE</div>
                <div style="color:#818cf8;font-weight:700;font-size:1rem;">999</div>
            </div>
            <div style="background:#13112b;border-radius:10px;padding:8px;text-align:center;">
                <div style="color:#6366f1;font-size:0.72rem;">🇸🇬 Singapore</div>
                <div style="color:#818cf8;font-weight:700;font-size:1rem;">995</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
