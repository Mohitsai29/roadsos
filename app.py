import streamlit as st
from streamlit_folium import st_folium
from emergency_finder import find_nearby_services, get_nearest_hospital
from ai_assistant import get_ai_guidance, chat_with_ai
from map_module import create_emergency_map
from geopy.geocoders import Nominatim

st.set_page_config(page_title="RoadSoS", page_icon="🚨", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] { display: none !important; }
.stApp { background: #0f0e1a; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px !important; }
.hero { background: linear-gradient(135deg,#4f46e5 0%,#7c3aed 60%,#9333ea 100%); border-radius:24px; padding:2.2rem 3rem; margin-bottom:1.5rem; position:relative; overflow:hidden; }
.hero::after { content:'🚨'; position:absolute; right:2.5rem; top:50%; transform:translateY(-50%); font-size:7rem; opacity:0.08; }
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
.guidance { background:#1e1a3f; border-radius:16px; padding:1.8rem; border:1px solid #2a2660; border-top:4px solid #4f46e5; line-height:1.85; color:#e0e7ff; font-size:0.93rem; }
.ref { background:#1e1a3f; border-radius:14px; padding:1.3rem; border:1px solid #2a2660; line-height:1.9; color:#e0e7ff; font-size:0.87rem; }
.tip { background:#1e1a3f; border-radius:10px; padding:0.65rem 1rem; font-size:0.85rem; color:#a5b4fc; margin-bottom:1rem; border:1px solid #2a2660; }
.empty { text-align:center; padding:3rem 2rem; background:#13112b; border-radius:18px; border:1px solid #2a2260; }
.radius-badge { display:inline-flex; align-items:center; gap:6px; background:#1e1a3f; color:#818cf8; border:1px solid #2a2660; border-radius:20px; padding:4px 14px; font-size:0.82rem; font-weight:600; margin-bottom:0.8rem; }
.loc-found { background:#1e1a3f; border:1px solid #4f46e5; border-radius:10px; padding:0.5rem 1rem; font-size:0.85rem; color:#a5b4fc; margin-top:0.5rem; }
.stButton > button { background:linear-gradient(135deg,#4f46e5,#7c3aed) !important; color:white !important; border:none !important; border-radius:12px !important; font-weight:600 !important; padding:0.65rem 1.5rem !important; font-size:0.93rem !important; transition:all 0.2s !important; width:100% !important; }
.stButton > button:hover { opacity:0.88 !important; transform:translateY(-1px) !important; }
.stTextInput > div > div > input { border-radius:12px !important; border:1.5px solid #2a2660 !important; color:#e0e7ff !important; font-size:0.93rem !important; padding:0.65rem 1rem !important; background:#1e1a3f !important; }
.stTextInput > div > div > input::placeholder { color:#6366f1 !important; }
.stTextInput > div > div > input:focus { border-color:#4f46e5 !important; }
.stTextArea > div > div > textarea { border-radius:12px !important; border:1.5px solid #2a2660 !important; color:#e0e7ff !important; font-size:0.93rem !important; background:#1e1a3f !important; }
div[data-testid="stChatMessage"] { background:#13112b !important; border-radius:14px !important; border:1px solid #2a2660 !important; margin:0.4rem 0 !important; }
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

def auto_search(lat, lon):
    radius = 0.5
    ph = st.empty()
    while radius <= 20.0:
        r_label = f"{int(radius*1000)} m" if radius < 1 else f"{radius:.1f} km"
        ph.markdown(f"""
        <div style="background:#1e1a3f;border:1px solid #2a2660;border-radius:14px;padding:1rem 1.5rem;margin-bottom:1rem;">
            <div style="font-size:0.68rem;font-weight:700;text-transform:uppercase;letter-spacing:1.4px;color:#6366f1;margin-bottom:0.5rem;">🔍 Auto-scanning</div>
            <div style="font-size:0.9rem;color:#fbbf24;font-weight:600;">⏳ Searching within <b>{r_label}</b>...</div>
            <div style="font-size:0.75rem;color:#4f46e5;margin-top:4px;">Expands automatically up to 20 km</div>
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
        <div style="font-size:0.9rem;color:#f87171;font-weight:600;">⚠️ No services found within 20 km. Please call 112.</div>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.search_radius_used = 20.0
    return {}, 20.0

# ── Auto-search after GPS redirect ──
if st.session_state.gps_auto and st.session_state.user_location and not st.session_state.services:
    st.session_state.gps_auto = False
    lat_a, lon_a, _ = st.session_state.user_location
    svcs, _ = auto_search(lat_a, lon_a)
    st.session_state.services = svcs
    st.rerun()

# ── HERO ──
st.markdown("""
<div class="hero">
    <div class="hero-badge">🇮🇳 India Road Safety · AI Powered</div>
    <h1>Road Accident Emergency Assistant</h1>
    <p>Instantly locate hospitals · Get AI first-aid guidance · One-tap emergency calling</p>
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
    st.components.v1.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { box-sizing:border-box; margin:0; padding:0; font-family:Inter,sans-serif; }
body { background:transparent; }
#btn {
    width:100%; padding:14px 20px; font-size:15px; font-weight:700;
    background:linear-gradient(135deg,#4f46e5,#7c3aed);
    color:white; border:none; border-radius:14px; cursor:pointer; margin-bottom:10px;
}
#btn:hover { opacity:0.88; }
#st {
    padding:12px 16px; border-radius:12px; font-size:13px; line-height:1.6;
    white-space:pre-line; display:none;
    background:#1e1a3f; color:#fbbf24; border:1px solid #2a2660;
    margin-bottom:10px;
}
#confirm {
    display:none; width:100%; padding:14px 20px; font-size:14px; font-weight:700;
    background:#059669; color:white; border:none; border-radius:14px;
    cursor:pointer; text-align:center; margin-top:8px;
}
#confirm:hover { opacity:0.88; }
</style>
</head>
<body>
<button id="btn" onclick="go()">📍 Detect My Exact GPS Location</button>
<div id="st"></div>
<button id="confirm" onclick="useLocation()"></button>
<script>
var detLat = '', detLon = '';

function go() {
    var b  = document.getElementById('btn');
    var s  = document.getElementById('st');
    var cf = document.getElementById('confirm');
    cf.style.display = 'none';
    s.style.display  = 'block';
    b.disabled       = true;
    b.innerText      = '⏳ Detecting...';
    s.style.background  = '#1e1a3f';
    s.style.color       = '#fbbf24';
    s.style.borderColor = '#2a2660';
    s.innerText = 'Requesting GPS permission...\nIf browser asks, tap Allow.';

    if (!navigator.geolocation) {
        s.style.background  = '#450a0a';
        s.style.color       = '#f87171';
        s.style.borderColor = '#991b1b';
        s.innerText  = 'GPS not supported. Type your city below.';
        b.disabled   = false;
        b.innerText  = '📍 Detect GPS';
        return;
    }

    navigator.geolocation.getCurrentPosition(
        function(pos) {
            detLat = pos.coords.latitude.toFixed(6);
            detLon = pos.coords.longitude.toFixed(6);
            var acc = Math.round(pos.coords.accuracy);
            s.style.background  = '#052e16';
            s.style.color       = '#34d399';
            s.style.borderColor = '#166534';
            s.innerText = '✅ ' + detLat + ', ' + detLon + ' (±' + acc + 'm)\nClick the green button below to load your location!';
            b.innerText         = '✅ GPS Detected!';
            b.style.background  = '#374151';
            cf.style.display    = 'block';
            cf.innerText        = '🚀 Use My Location & Find Services → ' + detLat + ', ' + detLon;
        },
        function(err) {
            s.style.background  = '#450a0a';
            s.style.color       = '#f87171';
            s.style.borderColor = '#991b1b';
            b.disabled  = false;
            b.innerText = '📍 Try Again';
            b.style.background = 'linear-gradient(135deg,#4f46e5,#7c3aed)';
            if (err.code === 1)
                s.innerText = '❌ Permission denied.\n\nFix:\n1. Click 🔒 in address bar\n2. Location → Allow\n3. Refresh & try again\n\nOR type your city below.';
            else
                s.innerText = '❌ GPS failed. Type your city below.';
        },
        { enableHighAccuracy:true, timeout:15000, maximumAge:0 }
    );
}

function useLocation() {
    if (!detLat || !detLon) return;
    var url = window.top.location.href.split('?')[0] + '?lat=' + detLat + '&lon=' + detLon;
    window.top.location.replace(url);
}
</script>
</body>
</html>
""", height=210)

    coord_input = st.text_input("",
        placeholder="GPS auto-fills here — or type city: Vijayawada",
        label_visibility="collapsed", key="coord_box")

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
                    if 6.5 <= lat <= 37.5 and 68.0 <= lon <= 97.5:
                        st.session_state.user_location = (lat, lon, f"{lat:.5f}, {lon:.5f}")
                        services, radius = auto_search(lat, lon)
                        st.session_state.services = services
                        st.rerun()
                    else:
                        st.error("⚠️ Outside India")
                except:
                    st.error("⚠️ Invalid. Try: 16.514445, 80.679274")
            else:
                with st.spinner("Finding..."):
                    geo = Nominatim(user_agent="roadsos_v10")
                    loc = geo.geocode(val + ", India", country_codes="IN")
                if loc and 6.5 <= loc.latitude <= 37.5:
                    st.session_state.user_location = (loc.latitude, loc.longitude, val)
                    services, radius = auto_search(loc.latitude, loc.longitude)
                    st.session_state.services = services
                    st.rerun()
                else:
                    st.error("⚠️ Not found in India")
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
        href  = f"tel:{phone}" if phone else "tel:108"
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
tab1, tab2, tab3 = st.tabs(["🗺️  Map & Services","🤖  AI First-Aid Guide","💬  AI Chat"])

with tab1:
    if st.session_state.user_location and st.session_state.services:
        lat, lon, _ = st.session_state.user_location
        total = sum(len(v) for v in st.session_state.services.values())
        if total == 0:
            st.markdown("""
            <div class="empty">
                <div style="font-size:2.5rem">🔍</div>
                <div style="font-weight:600;color:#e0e7ff;margin:0.8rem 0 0.3rem;">No services found within 20 km</div>
                <div style="color:#6366f1;font-size:0.88rem;">Please call 112 directly</div>
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
                icons  = {"hospitals":"🏥","police":"🚔","ambulance":"🚑"}
                colors = {"hospitals":"#dc2626","police":"#2563eb","ambulance":"#d97706"}
                for stype, places in st.session_state.services.items():
                    if places:
                        for p in places[:2]:
                            ph = p.get("phone","")
                            c  = colors.get(stype,"#4f46e5")
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
            <div style="font-size:3rem">🗺️</div>
            <div style="font-weight:600;font-size:1rem;color:#e0e7ff;margin:1rem 0 0.4rem;">
                Click GPS → Allow → Click green button → Done!
            </div>
            <div style="color:#6366f1;font-size:0.88rem;">
                Searches from 500 m and expands until services found
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([3,2])
    with col1:
        st.markdown('<span class="sec-label">Describe the Accident</span>', unsafe_allow_html=True)
        situation = st.text_area("",
            placeholder="e.g. Two vehicles collided on NH65. One person unconscious, another bleeding...",
            height=160, label_visibility="collapsed")
        if st.button("⚡  Get AI Emergency Guidance"):
            if situation.strip():
                loc_info = st.session_state.user_location[2] if st.session_state.user_location else "India"
                with st.spinner("AI analyzing..."):
                    guidance = get_ai_guidance(situation, loc_info)
                st.markdown('<span class="sec-label" style="margin-top:1rem;">AI Guidance</span>', unsafe_allow_html=True)
                st.markdown(f'<div class="guidance">{guidance}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please describe the accident situation first.")
    with col2:
        st.markdown('<span class="sec-label">Quick Reference</span>', unsafe_allow_html=True)
        st.markdown("""
        <div class="ref">
            <div style="color:#818cf8;font-weight:700;margin-bottom:8px;">✅ DO IMMEDIATELY</div>
            ① Call <b>112</b> right away<br>
            ② Switch on hazard lights<br>
            ③ Keep victim still &amp; calm<br>
            ④ Press cloth on wounds<br>
            ⑤ Stay on call with operator<br><br>
            <div style="color:#f87171;font-weight:700;margin-bottom:8px;">❌ NEVER DO THIS</div>
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
        💡 Ask anything — "What do I do if someone is unconscious?",
        "How to stop bleeding?", "Is it safe to move the victim?"
    </div>
    """, unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])
    if prompt := st.chat_input("Ask your emergency question..."):
        st.session_state.chat_history.append({"role":"user","content":prompt})
        loc_info = st.session_state.user_location[2] if st.session_state.user_location else "India"
        with st.spinner(""):
            reply = chat_with_ai(st.session_state.chat_history[:-1], prompt, loc_info)
        st.session_state.chat_history.append({"role":"assistant","content":reply})
        st.rerun()
