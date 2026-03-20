import streamlit as st
from streamlit_folium import st_folium
from emergency_finder import find_nearby_services, get_nearest_hospital
from ai_assistant import get_ai_guidance, chat_with_ai
from map_module import create_emergency_map
from geopy.geocoders import Nominatim

st.set_page_config(
    page_title="RoadSoS",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
.stApp { background: #f5f3ff; }

/* ── Hide Streamlit junk ── */
#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="collapsedControl"] { display: none !important; }
button[kind="header"] { display: none !important; }
.stDeployButton { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #1e1b4b !important;
    min-width: 300px !important;
    max-width: 300px !important;
    width: 300px !important;
}
section[data-testid="stSidebar"] > div:first-child {
    padding: 1.5rem 1.2rem !important;
}
section[data-testid="stSidebar"] * {
    color: #e0e7ff !important;
    font-size: 0.95rem !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: #4f46e5 !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    width: 100% !important;
    padding: 0.75rem 1rem !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    margin-top: 6px !important;
    transition: background 0.2s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #4338ca !important;
}
section[data-testid="stSidebar"] .stTextInput > div > div > input {
    background: #312e81 !important;
    border: 1.5px solid #4f46e5 !important;
    border-radius: 12px !important;
    color: white !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 1rem !important;
    height: 48px !important;
}
section[data-testid="stSidebar"] .stTextInput > div > div > input::placeholder {
    color: #a5b4fc !important;
    font-size: 0.88rem !important;
}
section[data-testid="stSidebar"] .stSlider {
    padding: 0.2rem 0 !important;
}
section[data-testid="stSidebar"] .stSlider > div {
    padding: 0 !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #312e81 !important;
    margin: 0.8rem 0 !important;
}
section[data-testid="stSidebar"] .stCaption {
    font-size: 0.82rem !important;
    color: #a5b4fc !important;
}
section[data-testid="stSidebar"] .stSuccess {
    background: #064e3b !important;
    border-radius: 10px !important;
    font-size: 0.88rem !important;
}
section[data-testid="stSidebar"] .stWarning,
section[data-testid="stSidebar"] .stError {
    border-radius: 10px !important;
    font-size: 0.88rem !important;
}

.slabel {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.4px !important;
    color: #818cf8 !important;
    display: block;
    margin: 1rem 0 0.5rem !important;
}

.loc-pill {
    background: #312e81;
    border: 1px solid #4f46e5;
    border-radius: 12px;
    padding: 0.6rem 1rem;
    font-size: 0.85rem !important;
    color: #a5b4fc !important;
    margin-top: 0.5rem;
    word-break: break-all;
    line-height: 1.5;
}

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
    border-radius: 24px;
    padding: 2.5rem 3rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -60%;
    right: -5%;
    width: 450px;
    height: 450px;
    background: rgba(255,255,255,0.06);
    border-radius: 50%;
    pointer-events: none;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.18);
    color: white !important;
    border-radius: 20px;
    padding: 4px 16px;
    font-size: 0.8rem;
    font-weight: 600;
    margin-bottom: 0.9rem;
}
.hero h1 {
    font-size: 2.1rem;
    font-weight: 700;
    color: white !important;
    margin: 0 0 0.5rem;
    letter-spacing: -0.5px;
}
.hero p { color: rgba(255,255,255,0.82) !important; margin: 0; font-size: 0.97rem; }

/* ── SOS Card ── */
.sos-card {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    border-radius: 20px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
    box-shadow: 0 8px 32px rgba(220,38,38,0.22);
}
.sos-info .sos-title {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    color: rgba(255,255,255,0.7) !important;
    margin-bottom: 4px;
}
.sos-info .sos-name { font-size: 1.1rem; font-weight: 700; color: white !important; }
.sos-info .sos-dist { font-size: 0.83rem; color: rgba(255,255,255,0.75) !important; margin-top: 3px; }
.call-now-btn {
    display: inline-block;
    background: white;
    color: #dc2626 !important;
    border-radius: 50px;
    padding: 0.75rem 2.2rem;
    font-weight: 700;
    font-size: 1.05rem;
    text-decoration: none !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    transition: transform 0.15s, box-shadow 0.15s;
    white-space: nowrap;
}
.call-now-btn:hover {
    transform: scale(1.04);
    box-shadow: 0 6px 24px rgba(0,0,0,0.2);
    color: #dc2626 !important;
}

/* ── Number grid ── */
.num-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 1.5rem;
}
.num-card {
    background: white;
    border-radius: 16px;
    padding: 1.1rem 0.8rem;
    text-align: center;
    border: 1px solid #ede9fe;
    transition: all 0.2s;
}
.num-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(79,70,229,0.12); }
.num-card .ni { font-size: 1.5rem; margin-bottom: 5px; }
.num-card .nn { font-size: 1.75rem; font-weight: 700; color: #4f46e5; line-height: 1; }
.num-card .nl { font-size: 0.73rem; color: #94a3b8; margin-top: 4px; font-weight: 500; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: white !important;
    border-radius: 16px !important;
    padding: 6px !important;
    border: 1px solid #ede9fe !important;
    gap: 4px !important;
    margin-bottom: 1rem !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 12px !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    padding: 0.6rem 1.5rem !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
}

/* ── Service card ── */
.svc {
    background: white;
    border-radius: 14px;
    padding: 1rem 1.2rem;
    margin: 0.5rem 0;
    border: 1px solid #ede9fe;
    border-left: 4px solid #4f46e5;
    transition: box-shadow 0.2s;
}
.svc:hover { box-shadow: 0 4px 16px rgba(79,70,229,0.1); }
.svc .sname { font-weight: 600; color: #1e1b4b; font-size: 0.93rem; }
.svc .sphone { color: #64748b; font-size: 0.82rem; margin-top: 3px; }
.svc-dist {
    display: inline-block;
    background: #ede9fe;
    color: #4f46e5;
    font-size: 0.73rem;
    font-weight: 600;
    padding: 2px 10px;
    border-radius: 20px;
    margin-top: 6px;
}
.call-svc {
    display: inline-block;
    background: #dcfce7;
    color: #16a34a !important;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 2px 12px;
    border-radius: 20px;
    margin-top: 6px;
    margin-left: 6px;
    text-decoration: none !important;
    border: 1px solid #bbf7d0;
}
.call-svc:hover { background: #bbf7d0; }

/* ── Guidance ── */
.guidance {
    background: white;
    border-radius: 16px;
    padding: 1.8rem;
    border: 1px solid #ede9fe;
    border-top: 4px solid #4f46e5;
    line-height: 1.85;
    color: #1e1b4b;
    font-size: 0.93rem;
}
.ref {
    background: white;
    border-radius: 14px;
    padding: 1.3rem;
    border: 1px solid #ede9fe;
    line-height: 1.9;
    color: #1e1b4b;
    font-size: 0.87rem;
}
.empty {
    text-align: center;
    padding: 4rem 2rem;
    background: white;
    border-radius: 20px;
    border: 1px solid #ede9fe;
}
.tip {
    background: #ede9fe;
    border-radius: 10px;
    padding: 0.65rem 1rem;
    font-size: 0.85rem;
    color: #4338ca;
    margin-bottom: 1rem;
    border: 1px solid #c7d2fe;
}

/* ── Main buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.6rem 2rem !important;
    transition: all 0.2s !important;
    font-size: 0.95rem !important;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(79,70,229,0.25) !important;
}

/* ── Inputs main ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border-radius: 12px !important;
    border: 1.5px solid #ede9fe !important;
    color: #1e1b4b !important;
    font-size: 0.93rem !important;
    padding: 0.65rem 1rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 3px rgba(79,70,229,0.1) !important;
}

/* ── Chat ── */
div[data-testid="stChatMessage"] {
    background: white !important;
    border-radius: 14px !important;
    border: 1px solid #ede9fe !important;
    margin: 0.4rem 0 !important;
    padding: 0.3rem !important;
}

.stSlider > div > div > div > div { background: #4f46e5 !important; }
hr { border-color: #ede9fe !important; }
</style>
""", unsafe_allow_html=True)

# Session state
for key, default in [("chat_history",[]),("services",None),("user_location",None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ══════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════
with st.sidebar:
    # Brand
    st.markdown("""
    <div style="margin-bottom:1.2rem;">
        <div style="font-size:1.5rem;font-weight:700;color:white!important;letter-spacing:-0.3px;">
            🚨 RoadSoS
        </div>
        <div style="font-size:0.82rem;color:#a5b4fc!important;margin-top:3px;">
            India Emergency Assistant
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span class="slabel">📍 Your Location</span>', unsafe_allow_html=True)

    # GPS Component
    st.components.v1.html("""
    <style>
    body { margin:0; padding:0; background:transparent; }
    #gps-btn {
        background: #4f46e5;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 16px;
        font-size: 15px;
        font-weight: 600;
        cursor: pointer;
        width: 100%;
        margin-bottom: 8px;
        font-family: Inter, sans-serif;
        transition: background 0.2s;
    }
    #gps-btn:hover { background: #4338ca; }
    #gps-btn:disabled { background: #059669; cursor: default; }
    #gps-status {
        font-size: 12px;
        padding: 8px 10px;
        border-radius: 10px;
        font-family: Inter, sans-serif;
        background: #312e81;
        color: #a5b4fc;
        line-height: 1.5;
        min-height: 36px;
    }
    </style>
    <button id="gps-btn" onclick="getGPS()">📍 Detect My Exact GPS Location</button>
    <div id="gps-status">Tap the button above — your browser will ask for location permission</div>
    <script>
    function getGPS() {
        var btn = document.getElementById('gps-btn');
        var stat = document.getElementById('gps-status');
        btn.innerText = '⏳ Detecting location...';
        btn.disabled = true;
        stat.style.color = '#fbbf24';
        stat.innerText = 'Requesting GPS permission from browser...';
        if (!navigator.geolocation) {
            stat.style.color = '#f87171';
            stat.innerText = '❌ GPS not supported. Type your city name below.';
            btn.innerText = '📍 Detect GPS'; btn.disabled = false; return;
        }
        navigator.geolocation.getCurrentPosition(
            function(pos) {
                var lat = pos.coords.latitude.toFixed(6);
                var lon = pos.coords.longitude.toFixed(6);
                var val = lat + ', ' + lon;
                stat.style.color = '#34d399';
                stat.innerText = '✅ GPS detected!\n' + val + '\n👉 Now click USE LOCATION below';
                btn.innerText = '✅ GPS Ready — Click Use Location ↓';
                btn.style.background = '#059669';
                var tries = 0;
                var fill = setInterval(function() {
                    tries++;
                    var inputs = window.parent.document.querySelectorAll('input[type=text]');
                    for (var i = 0; i < inputs.length; i++) {
                        var ph = (inputs[i].getAttribute('placeholder') || '').toLowerCase();
                        if (ph.includes('gps') || ph.includes('city') || ph.includes('type')) {
                            inputs[i].value = val;
                            inputs[i].dispatchEvent(new Event('input', {bubbles:true}));
                            inputs[i].dispatchEvent(new Event('change', {bubbles:true}));
                            clearInterval(fill); break;
                        }
                    }
                    if (tries > 15) clearInterval(fill);
                }, 400);
            },
            function(err) {
                stat.style.color = '#f87171';
                if (err.code === 1)
                    stat.innerText = '❌ Location permission denied.\nPlease type your city name in the box below.';
                else
                    stat.innerText = '❌ GPS error. Please type your city or area below.';
                btn.innerText = '📍 Try GPS Again';
                btn.disabled = false;
                btn.style.background = '#4f46e5';
            },
            { enableHighAccuracy: true, timeout: 12000, maximumAge: 0 }
        );
    }
    </script>
    """, height=110)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    coord_input = st.text_input("",
        placeholder="GPS fills here — or type city name",
        label_visibility="collapsed",
        key="coord_box")

    c1, c2 = st.columns([3, 2])
    with c1:
        if st.button("✅ Use Location", use_container_width=True):
            val = coord_input.strip()
            if not val:
                st.warning("Enter or detect location first")
            elif "," in val:
                try:
                    p = val.split(",")
                    lat, lon = float(p[0].strip()), float(p[1].strip())
                    if 6.5 <= lat <= 37.5 and 68.0 <= lon <= 97.5:
                        st.session_state.user_location = (lat, lon, f"{lat:.5f}, {lon:.5f}")
                        st.success("✅ GPS location set!")
                    else:
                        st.error("Location outside India")
                except:
                    st.error("Invalid. Format: 16.51, 80.63")
            else:
                geo = Nominatim(user_agent="roadsos_v4")
                loc = geo.geocode(val + ", India", country_codes="IN")
                if loc and 6.5 <= loc.latitude <= 37.5:
                    st.session_state.user_location = (loc.latitude, loc.longitude, val)
                    st.success(f"✅ Found: {val}")
                else:
                    st.error("Not found in India")
    with c2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.user_location = None
            st.session_state.services = None
            st.rerun()

    if st.session_state.user_location:
        st.markdown(f'<div class="loc-pill">📍 Active: {st.session_state.user_location[2]}</div>',
                    unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span class="slabel">🔍 Search Radius</span>', unsafe_allow_html=True)
    radius = st.slider("", 2, 25, 10, label_visibility="collapsed")
    st.caption(f"Within **{radius} km** of your location")

    st.markdown("---")
    if st.session_state.user_location:
        if st.button("🚨  FIND EMERGENCY SERVICES", use_container_width=True):
            lat, lon, _ = st.session_state.user_location
            with st.spinner("Scanning nearby services..."):
                st.session_state.services = find_nearby_services(lat, lon, radius)
            found = sum(len(v) for v in st.session_state.services.values())
            if found > 0:
                st.success(f"✅ Found {found} nearby services!")
            else:
                st.warning("None found. Try 20 km radius.")
    else:
        st.markdown("""
        <div style="background:#312e81;border:1px solid #4f46e5;border-radius:12px;
             padding:0.7rem 1rem;font-size:0.85rem;color:#a5b4fc;text-align:center;line-height:1.5;">
            ☝️ Detect or enter your<br>location first
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span class="slabel">☎️ Quick Dial</span>', unsafe_allow_html=True)
    for emoji, num, name in [("🚑","108","Ambulance"),("🚔","100","Police"),("🔥","101","Fire"),("🛣️","1033","Highway")]:
        st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;
             background:#312e81;border-radius:12px;padding:10px 14px;margin:5px 0;
             border:1px solid #4f46e5;">
            <span style="font-size:0.92rem;">{emoji}&nbsp; {name}</span>
            <span style="font-size:1.05rem;font-weight:700;color:#818cf8!important;">{num}</span>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-badge">🇮🇳 India Road Safety · AI Powered</div>
    <h1>Road Accident Emergency Assistant</h1>
    <p>Instantly locate hospitals, police & ambulances · Get AI first-aid guidance · Chat with emergency AI</p>
</div>
""", unsafe_allow_html=True)

# ── Nearest Hospital Call Card ──
if st.session_state.services:
    nearest = get_nearest_hospital(st.session_state.services)
    if nearest:
        phone = nearest.get("phone","").strip()
        call_href = f"tel:{phone}" if phone else "tel:108"
        call_label = "📞 Call Now" if phone else "📞 Call 108"
        dist_info = f"📏 {nearest['distance_km']} km away"
        phone_info = f" · 📞 {phone}" if phone else " · No phone listed — calling 108"
        st.markdown(f"""
        <div class="sos-card">
            <div class="sos-info">
                <div class="sos-title">🏥 Nearest Hospital — One Tap to Call</div>
                <div class="sos-name">{nearest['name']}</div>
                <div class="sos-dist">{dist_info}{phone_info}</div>
            </div>
            <a href="{call_href}" class="call-now-btn">{call_label}</a>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sos-card">
            <div class="sos-info">
                <div class="sos-title">🏥 Emergency</div>
                <div class="sos-name">Search for services first</div>
                <div class="sos-dist">Or call national ambulance directly</div>
            </div>
            <a href="tel:108" class="call-now-btn">📞 Call 108</a>
        </div>
        """, unsafe_allow_html=True)

# Emergency numbers
st.markdown("""
<div class="num-row">
    <div class="num-card"><div class="ni">🆘</div><div class="nn">112</div><div class="nl">National SOS</div></div>
    <div class="num-card"><div class="ni">🚑</div><div class="nn">108</div><div class="nl">Ambulance</div></div>
    <div class="num-card"><div class="ni">🚔</div><div class="nn">100</div><div class="nl">Police</div></div>
    <div class="num-card"><div class="ni">🛣️</div><div class="nn">1033</div><div class="nl">Highway Help</div></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🗺️  Map & Services", "🤖  AI First-Aid Guide", "💬  AI Chat"])

with tab1:
    if st.session_state.user_location and st.session_state.services:
        lat, lon, _ = st.session_state.user_location
        total = sum(len(v) for v in st.session_state.services.values())
        if total == 0:
            st.markdown("""
            <div class="empty">
                <div style="font-size:2.5rem">🔍</div>
                <div style="font-weight:600;color:#1e1b4b;margin:0.8rem 0 0.3rem;font-size:1rem;">
                    No services found in this area
                </div>
                <div style="color:#94a3b8;font-size:0.88rem;">
                    Increase the search radius to 15–20 km in the left panel and try again
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#4f46e5;margin-bottom:0.6rem;">Live Emergency Map</div>', unsafe_allow_html=True)
                m = create_emergency_map(lat, lon, st.session_state.services)
                st_folium(m, width=None, height=450)
            with col2:
                st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#4f46e5;margin-bottom:0.6rem;">Nearest Services</div>', unsafe_allow_html=True)
                icons = {"hospitals":"🏥","police":"🚔","ambulance":"🚑"}
                colors = {"hospitals":"#dc2626","police":"#2563eb","ambulance":"#d97706"}
                for stype, places in st.session_state.services.items():
                    if places:
                        for p in places[:2]:
                            ph = p.get("phone","")
                            c = colors.get(stype,"#4f46e5")
                            call_html = f'<a href="tel:{ph}" class="call-svc">📞 Call</a>' if ph else '<span style="font-size:0.75rem;color:#94a3b8;margin-left:6px;">No phone</span>'
                            st.markdown(f"""
                            <div class="svc" style="border-left-color:{c}">
                                <div class="sname">{icons.get(stype,'')} {p['name']}</div>
                                <div class="sphone">{"📞 "+ph if ph else "Phone not listed"}</div>
                                <span class="svc-dist">📏 {p['distance_km']} km</span>{call_html}
                            </div>
                            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty">
            <div style="font-size:3rem">🗺️</div>
            <div style="font-weight:600;font-size:1.05rem;color:#1e1b4b;margin:1rem 0 0.4rem;">
                Detect your location to get started
            </div>
            <div style="color:#94a3b8;font-size:0.88rem;">
                Left panel → Detect GPS → Find Emergency Services
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#4f46e5;margin-bottom:0.6rem;">Describe the Accident</div>', unsafe_allow_html=True)
        situation = st.text_area("",
            placeholder="e.g. Two vehicles collided on NH65 near Vijayawada. One person unconscious, another has a bleeding arm...",
            height=160, label_visibility="collapsed")
        if st.button("⚡  Get AI Emergency Guidance"):
            if situation.strip():
                loc_info = st.session_state.user_location[2] if st.session_state.user_location else "India"
                with st.spinner("AI analyzing situation..."):
                    guidance = get_ai_guidance(situation, loc_info)
                st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#4f46e5;margin:1.2rem 0 0.5rem;">AI Emergency Guidance</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="guidance">{guidance}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please describe the accident situation first.")
    with col2:
        st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#4f46e5;margin-bottom:0.6rem;">Quick Reference</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="ref">
            <div style="color:#4f46e5;font-weight:700;margin-bottom:8px;">✅ DO IMMEDIATELY</div>
            ① Call <b>112</b> right away<br>
            ② Switch on hazard lights<br>
            ③ Keep victim still & calm<br>
            ④ Press cloth on wounds<br>
            ⑤ Stay on call with operator<br><br>
            <div style="color:#dc2626;font-weight:700;margin-bottom:8px;">❌ NEVER DO THIS</div>
            ✗ Move unconscious victims<br>
            ✗ Remove helmet yourself<br>
            ✗ Give water/food to victim<br>
            ✗ Leave the victim alone<br>
            ✗ Crowd around the injured
        </div>
        """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#4f46e5;margin-bottom:0.6rem;">Chat with RoadSoS AI</div>', unsafe_allow_html=True)
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
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        loc_info = st.session_state.user_location[2] if st.session_state.user_location else "India"
        with st.spinner(""):
            reply = chat_with_ai(st.session_state.chat_history[:-1], prompt, loc_info)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        st.rerun()
