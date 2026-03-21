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
.stApp { background: #0f0e1a; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #13112b !important;
    border-right: 1px solid #2a2660 !important;
    min-width: 280px !important;
}
section[data-testid="stSidebar"] > div { padding: 1.5rem 1.2rem !important; }
section[data-testid="stSidebar"] * { color: #e0e7ff !important; }
section[data-testid="stSidebar"] hr { border-color: #2a2660 !important; margin: 0.8rem 0 !important; }

.sb-brand {
    background: linear-gradient(135deg,#4f46e5,#7c3aed);
    border-radius:14px; padding:1rem 1.2rem; margin-bottom:1.2rem;
}
.sb-brand h2 { font-size:1.2rem; font-weight:800; color:white !important; margin:0; }
.sb-brand p { font-size:0.75rem; color:rgba(255,255,255,0.75) !important; margin:3px 0 0; }

.slabel {
    font-size:0.68rem; font-weight:700; text-transform:uppercase;
    letter-spacing:1.4px; color:#6366f1 !important; display:block; margin:1rem 0 0.5rem;
}

.dial-card {
    background:#1e1a3f; border:1px solid #2a2660; border-radius:12px;
    padding:10px 14px; margin:4px 0; display:flex;
    justify-content:space-between; align-items:center;
    text-decoration:none !important; transition:background 0.15s;
}
.dial-card:hover { background:#2a2660; }
.dial-card span { font-size:0.9rem; color:#e0e7ff !important; }
.dial-card b { font-size:1.05rem; color:#818cf8 !important; font-weight:700; }

.loc-active {
    background:#1e1a3f; border:1px solid #4f46e5; border-radius:10px;
    padding:0.55rem 0.9rem; font-size:0.82rem; color:#a5b4fc !important; margin-top:0.5rem;
}

section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg,#4f46e5,#7c3aed) !important;
    color:white !important; border:none !important; border-radius:12px !important;
    font-weight:600 !important; font-size:0.9rem !important;
    padding:0.65rem 1rem !important; width:100% !important; margin-top:4px !important;
}
section[data-testid="stSidebar"] .stTextInput > div > div > input {
    background:#1e1a3f !important; border:1.5px solid #4f46e5 !important;
    border-radius:12px !important; color:white !important;
    font-size:0.9rem !important; padding:0.65rem 1rem !important;
}
section[data-testid="stSidebar"] .stTextInput > div > div > input::placeholder {
    color:#6366f1 !important;
}

/* ── Main ── */
.hero {
    background: linear-gradient(135deg,#4f46e5 0%,#7c3aed 60%,#9333ea 100%);
    border-radius:24px; padding:2.5rem 3rem; margin-bottom:1.5rem;
    position:relative; overflow:hidden;
}
.hero::after {
    content:'🚨'; position:absolute; right:2.5rem; top:50%;
    transform:translateY(-50%); font-size:7rem; opacity:0.08; pointer-events:none;
}
.hero-badge {
    display:inline-block; background:rgba(255,255,255,0.15);
    color:white !important; border-radius:20px; padding:4px 16px;
    font-size:0.78rem; font-weight:600; margin-bottom:0.8rem;
    backdrop-filter:blur(10px);
}
.hero h1 { font-size:2.2rem; font-weight:800; color:white !important; margin:0 0 0.4rem; letter-spacing:-0.5px; }
.hero p { color:rgba(255,255,255,0.8) !important; margin:0; font-size:0.97rem; }

/* ── Number grid ── */
.num-row { display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-bottom:1.5rem; }
.num-card {
    background:#13112b; border-radius:18px; padding:1.2rem 1rem;
    text-align:center; border:1px solid #2a2660; transition:all 0.2s;
    text-decoration:none !important; display:block;
}
.num-card:hover { transform:translateY(-3px); border-color:#4f46e5; box-shadow:0 8px 28px rgba(79,70,229,0.25); }
.num-card .ni { font-size:1.6rem; margin-bottom:6px; }
.num-card .nn { font-size:1.8rem; font-weight:800; color:#818cf8; line-height:1; }
.num-card .nl { font-size:0.73rem; color:#6366f1; margin-top:4px; font-weight:500; }
.num-card .nc { font-size:0.7rem; color:#4f46e5; margin-top:2px; }

/* ── SOS Card ── */
.sos-card {
    background:linear-gradient(135deg,#dc2626,#b91c1c);
    border-radius:20px; padding:1.4rem 2rem; margin-bottom:1.5rem;
    display:flex; align-items:center; justify-content:space-between;
    flex-wrap:wrap; gap:1rem; box-shadow:0 8px 32px rgba(220,38,38,0.3);
    animation: pulse-red 2s infinite;
}
@keyframes pulse-red {
    0%,100% { box-shadow:0 8px 32px rgba(220,38,38,0.3); }
    50% { box-shadow:0 8px 40px rgba(220,38,38,0.5); }
}
.sos-title { font-size:0.7rem; font-weight:700; text-transform:uppercase; letter-spacing:1.2px; color:rgba(255,255,255,0.7) !important; margin-bottom:3px; }
.sos-name { font-size:1.1rem; font-weight:700; color:white !important; }
.sos-dist { font-size:0.83rem; color:rgba(255,255,255,0.75) !important; margin-top:2px; }
.call-now {
    display:inline-block; background:white; color:#dc2626 !important;
    border-radius:50px; padding:0.75rem 2.2rem; font-weight:800;
    font-size:1.05rem; text-decoration:none !important; white-space:nowrap;
    transition:all 0.15s; box-shadow:0 4px 16px rgba(0,0,0,0.2);
}
.call-now:hover { transform:scale(1.05); color:#dc2626 !important; }

/* ── Search Progress ── */
.search-box {
    background:#13112b; border:1px solid #2a2660; border-radius:16px;
    padding:1.2rem 1.5rem; margin-bottom:1.2rem;
}
.search-step { font-size:0.87rem; color:#a5b4fc; padding:4px 0; }
.search-step.done { color:#34d399; }
.search-step.active { color:#fbbf24; font-weight:600; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background:#13112b !important; border-radius:16px !important;
    padding:6px !important; border:1px solid #2a2660 !important;
    gap:4px !important; margin-bottom:1.2rem !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius:12px !important; font-size:0.9rem !important;
    font-weight:500 !important; color:#6366f1 !important; padding:0.6rem 1.5rem !important;
}
.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#4f46e5,#7c3aed) !important; color:white !important;
}

/* ── Service cards ── */
.svc {
    background:#13112b; border-radius:14px; padding:1rem 1.2rem;
    margin:0.5rem 0; border:1px solid #2a2660; border-left:4px solid #4f46e5;
    transition:border-color 0.2s;
}
.svc:hover { border-color:#7c3aed; }
.svc .sname { font-weight:600; color:#e0e7ff; font-size:0.92rem; }
.svc .sph { color:#6366f1; font-size:0.8rem; margin-top:2px; }
.svc-dist { display:inline-block; background:#1e1a3f; color:#818cf8; font-size:0.72rem; font-weight:600; padding:2px 10px; border-radius:20px; margin-top:5px; border:1px solid #2a2660; }
.call-svc { display:inline-block; background:#052e16; color:#34d399 !important; font-size:0.75rem; font-weight:700; padding:2px 12px; border-radius:20px; margin-top:5px; margin-left:6px; text-decoration:none !important; border:1px solid #166534; }

/* ── Guidance ── */
.guidance { background:#13112b; border-radius:16px; padding:1.8rem; border:1px solid #2a2660; border-top:4px solid #4f46e5; line-height:1.85; color:#e0e7ff; font-size:0.93rem; }
.ref { background:#13112b; border-radius:14px; padding:1.3rem; border:1px solid #2a2660; line-height:1.9; color:#e0e7ff; font-size:0.87rem; }
.tip { background:#1e1a3f; border-radius:10px; padding:0.65rem 1rem; font-size:0.85rem; color:#a5b4fc; margin-bottom:1rem; border:1px solid #2a2660; }
.empty { text-align:center; padding:3rem 2rem; background:#13112b; border-radius:18px; border:1px solid #2a2260; }

/* ── Radius badge ── */
.radius-badge { display:inline-flex; align-items:center; gap:6px; background:#1e1a3f; color:#818cf8; border:1px solid #2a2660; border-radius:20px; padding:4px 14px; font-size:0.82rem; font-weight:600; margin-bottom:0.8rem; }

/* ── Buttons ── */
.stButton > button {
    background:linear-gradient(135deg,#4f46e5,#7c3aed) !important;
    color:white !important; border:none !important; border-radius:12px !important;
    font-weight:600 !important; padding:0.65rem 1.5rem !important;
    font-size:0.93rem !important; transition:all 0.2s !important; width:100% !important;
}
.stButton > button:hover { opacity:0.88 !important; transform:translateY(-1px) !important; }

/* ── Inputs ── */
.stTextInput > div > div > input {
    border-radius:12px !important; border:1.5px solid #2a2660 !important;
    color:#e0e7ff !important; font-size:0.93rem !important;
    padding:0.65rem 1rem !important; background:#13112b !important;
}
.stTextInput > div > div > input:focus { border-color:#4f46e5 !important; }
.stTextArea > div > div > textarea {
    border-radius:12px !important; border:1.5px solid #2a2660 !important;
    color:#e0e7ff !important; font-size:0.93rem !important; background:#13112b !important;
}
div[data-testid="stChatMessage"] {
    background:#13112b !important; border-radius:14px !important;
    border:1px solid #2a2660 !important; margin:0.4rem 0 !important;
}
.stSlider > div > div > div > div { background:#4f46e5 !important; }
</style>
""", unsafe_allow_html=True)

for key, default in [
    ("chat_history",[]), ("services",None),
    ("user_location",None), ("search_radius_used",None)
]:
    if key not in st.session_state:
        st.session_state[key] = default

def auto_search(lat, lon):
    radius = 0.5
    max_radius = 20.0
    step = 0.5
    ph = st.empty()
    while radius <= max_radius:
        r_label = f"{int(radius*1000)} m" if radius < 1 else f"{radius:.1f} km"
        ph.markdown(f"""
        <div class="search-box">
            <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#6366f1;margin-bottom:0.6rem;">🔍 Auto-scanning for services</div>
            <div class="search-step active">⏳ Searching within <b>{r_label}</b>...</div>
            <div class="search-step" style="color:#2a2660;font-size:0.78rem;margin-top:4px;">Expands automatically up to 20 km</div>
        </div>
        """, unsafe_allow_html=True)
        services = find_nearby_services(lat, lon, radius)
        total = sum(len(v) for v in services.values())
        if total > 0:
            ph.markdown(f"""
            <div class="search-box">
                <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#34d399;margin-bottom:0.6rem;">✅ Services found!</div>
                <div class="search-step done">✅ Found <b>{total} services</b> within <b>{r_label}</b></div>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.search_radius_used = radius
            return services, radius
        radius = round(radius + step, 1)
    ph.markdown("""
    <div class="search-box">
        <div class="search-step" style="color:#f87171;">⚠️ No services found within 20 km. Please call 112 directly.</div>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.search_radius_used = max_radius
    return {}, max_radius

# ══════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <h2>🚨 RoadSoS</h2>
        <p>India Emergency Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="slabel">📍 Your Location</span>', unsafe_allow_html=True)

    # Clean GPS component — no redundant text
    st.components.v1.html("""
    <style>
    body{margin:0;padding:0;background:transparent;}
    #gb{
        background:linear-gradient(135deg,#4f46e5,#7c3aed);
        color:white;border:none;border-radius:12px;
        padding:14px 18px;font-size:15px;font-weight:700;
        cursor:pointer;width:100%;font-family:Inter,sans-serif;
        transition:opacity 0.2s; letter-spacing:-0.2px;
    }
    #gb:hover{opacity:0.88;}
    #gb:disabled{background:#059669;cursor:default;}
    #gs{
        font-size:12px;padding:8px 12px;border-radius:10px;
        font-family:Inter,sans-serif;background:#1e1a3f;
        color:#a5b4fc;line-height:1.5;margin-top:8px;
        min-height:32px; display:none;
    }
    </style>
    <button id="gb" onclick="go()">📍 Detect My GPS Location</button>
    <div id="gs"></div>
    <script>
    function go(){
        var b=document.getElementById('gb'),s=document.getElementById('gs');
        b.innerText='⏳ Detecting location...'; b.disabled=true;
        s.style.display='block';
        s.style.background='#1e1a3f'; s.style.color='#fbbf24';
        s.innerText='Requesting GPS permission...';
        if(!navigator.geolocation){
            s.style.color='#f87171';
            s.innerText='❌ GPS unavailable. Type city below.';
            b.innerText='📍 Detect GPS'; b.disabled=false; return;
        }
        navigator.geolocation.getCurrentPosition(function(p){
            var lat=p.coords.latitude.toFixed(6),lon=p.coords.longitude.toFixed(6);
            var v=lat+', '+lon;
            s.style.color='#34d399';
            s.innerText='✅ '+v+'\nClick USE LOCATION below ↓';
            b.innerText='✅ GPS Detected!';
            var n=0,t=setInterval(function(){
                n++;
                var ins=window.parent.document.querySelectorAll('input[type=text]');
                for(var i=0;i<ins.length;i++){
                    var ph=(ins[i].getAttribute('placeholder')||'').toLowerCase();
                    if(ph.includes('gps')||ph.includes('city')||ph.includes('vijayawada')){
                        ins[i].value=v;
                        ins[i].dispatchEvent(new Event('input',{bubbles:true}));
                        ins[i].dispatchEvent(new Event('change',{bubbles:true}));
                        clearInterval(t);break;
                    }
                }
                if(n>25)clearInterval(t);
            },400);
        },function(e){
            s.style.color='#f87171';
            s.innerText=e.code===1?'❌ Permission denied. Type city below.':'❌ GPS failed. Type city below.';
            b.innerText='📍 Try Again'; b.disabled=false;
        },{enableHighAccuracy:true,timeout:12000,maximumAge:0});
    }
    </script>
    """, height=60)

    coord_input = st.text_input("",
        placeholder="Type city: Vijayawada or GPS auto-fills",
        label_visibility="collapsed", key="coord_box")

    if st.button("✅ Use Location & Auto-Search", use_container_width=True):
        val = coord_input.strip()
        if not val:
            st.warning("Detect GPS or type a city")
        elif "," in val:
            try:
                p = val.split(",")
                lat, lon = float(p[0].strip()), float(p[1].strip())
                if 6.5 <= lat <= 37.5 and 68.0 <= lon <= 97.5:
                    st.session_state.user_location = (lat, lon, f"{lat:.5f}, {lon:.5f}")
                else:
                    st.error("Outside India"); st.stop()
            except:
                st.error("Invalid format"); st.stop()
        else:
            geo = Nominatim(user_agent="roadsos_v8")
            loc = geo.geocode(val + ", India", country_codes="IN")
            if loc and 6.5 <= loc.latitude <= 37.5:
                st.session_state.user_location = (loc.latitude, loc.longitude, val)
            else:
                st.error("Not found in India"); st.stop()

        lat, lon, _ = st.session_state.user_location
        services, radius = auto_search(lat, lon)
        st.session_state.services = services
        st.rerun()

    if st.session_state.user_location:
        r = st.session_state.search_radius_used
        r_label = f"{int(r*1000)} m" if r and r < 1 else (f"{r:.1f} km" if r else "")
        total = sum(len(v) for v in st.session_state.services.values()) if st.session_state.services else 0
        st.markdown(f"""
        <div class="loc-active">
            📍 <b>{st.session_state.user_location[2]}</b><br>
            <span style="font-size:0.78rem;color:#6366f1;">
                {"✅ "+str(total)+" services within "+r_label if r_label else ""}
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🗑️ Clear & Reset", use_container_width=True):
        st.session_state.user_location = None
        st.session_state.services = None
        st.session_state.search_radius_used = None
        st.rerun()

    st.markdown("---")
    st.markdown('<span class="slabel">☎️ Tap to Call</span>', unsafe_allow_html=True)
    for emoji, num, name in [("🚑","108","Ambulance"),("🚔","100","Police"),("🔥","101","Fire"),("🛣️","1033","Highway"),("🆘","112","National SOS")]:
        st.markdown(f"""
        <a href="tel:{num}" class="dial-card">
            <span>{emoji}&nbsp; {name}</span><b>{num}</b>
        </a>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════
# MAIN
# ══════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-badge">🇮🇳 India Road Safety · AI Powered</div>
    <h1>Road Accident Emergency Assistant</h1>
    <p>Instantly locate hospitals · Get AI first-aid guidance · One-tap emergency calling</p>
</div>
""", unsafe_allow_html=True)

# Tappable emergency numbers
st.markdown("""
<div class="num-row">
    <a href="tel:112" class="num-card">
        <div class="ni">🆘</div><div class="nn">112</div>
        <div class="nl">National SOS</div><div class="nc">Tap to call</div>
    </a>
    <a href="tel:108" class="num-card">
        <div class="ni">🚑</div><div class="nn">108</div>
        <div class="nl">Ambulance</div><div class="nc">Tap to call</div>
    </a>
    <a href="tel:100" class="num-card">
        <div class="ni">🚔</div><div class="nn">100</div>
        <div class="nl">Police</div><div class="nc">Tap to call</div>
    </a>
    <a href="tel:1033" class="num-card">
        <div class="ni">🛣️</div><div class="nn">1033</div>
        <div class="nl">Highway Help</div><div class="nc">Tap to call</div>
    </a>
</div>
""", unsafe_allow_html=True)

# Nearest hospital SOS card
if st.session_state.services:
    nearest = get_nearest_hospital(st.session_state.services)
    if nearest:
        phone = nearest.get("phone","").strip()
        href = f"tel:{phone}" if phone else "tel:108"
        label = "📞 Call Now" if phone else "📞 Call 108"
        phone_txt = f"📞 {phone}" if phone else "No phone — tap to call 108"
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

# Tabs
tab1, tab2, tab3 = st.tabs(["🗺️  Map & Services", "🤖  AI First-Aid Guide", "💬  AI Chat"])

with tab1:
    if st.session_state.user_location and st.session_state.services:
        lat, lon, _ = st.session_state.user_location
        total = sum(len(v) for v in st.session_state.services.values())
        if total == 0:
            st.markdown("""
            <div class="empty">
                <div style="font-size:2.5rem">🔍</div>
                <div style="font-weight:600;color:#e0e7ff;margin:0.8rem 0 0.3rem;">No services found within 20 km</div>
                <div style="color:#6366f1;font-size:0.88rem;">Please call 112 directly for emergency help</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            r = st.session_state.search_radius_used or 0
            r_label = f"{int(r*1000)} m" if r < 1 else f"{r:.1f} km"
            st.markdown(f'<div class="radius-badge">🔍 Showing services within <b>&nbsp;{r_label}&nbsp;</b></div>', unsafe_allow_html=True)
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown('<span style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#6366f1;margin-bottom:0.5rem;display:block;">Live Emergency Map</span>', unsafe_allow_html=True)
                m = create_emergency_map(lat, lon, st.session_state.services)
                st_folium(m, width=None, height=450)
            with col2:
                st.markdown('<span style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#6366f1;margin-bottom:0.5rem;display:block;">Nearest Services</span>', unsafe_allow_html=True)
                icons = {"hospitals":"🏥","police":"🚔","ambulance":"🚑"}
                colors = {"hospitals":"#dc2626","police":"#2563eb","ambulance":"#d97706"}
                for stype, places in st.session_state.services.items():
                    if places:
                        for p in places[:2]:
                            ph = p.get("phone","")
                            c = colors.get(stype,"#4f46e5")
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
                Detect GPS → Click Use Location & Auto-Search
            </div>
            <div style="color:#6366f1;font-size:0.88rem;">
                Auto-searches from 500 m and expands until services are found
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<span style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#6366f1;margin-bottom:0.5rem;display:block;">Describe the Accident</span>', unsafe_allow_html=True)
        situation = st.text_area("",
            placeholder="e.g. Two vehicles collided on NH65. One person unconscious, another bleeding...",
            height=160, label_visibility="collapsed")
        if st.button("⚡  Get AI Emergency Guidance"):
            if situation.strip():
                loc_info = st.session_state.user_location[2] if st.session_state.user_location else "India"
                with st.spinner("AI analyzing situation..."):
                    guidance = get_ai_guidance(situation, loc_info)
                st.markdown('<span style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#6366f1;margin:1rem 0 0.5rem;display:block;">AI Guidance</span>', unsafe_allow_html=True)
                st.markdown(f'<div class="guidance">{guidance}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please describe the situation first.")
    with col2:
        st.markdown('<span style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#6366f1;margin-bottom:0.5rem;display:block;">Quick Reference</span>', unsafe_allow_html=True)
        st.markdown("""
        <div class="ref">
            <div style="color:#818cf8;font-weight:700;margin-bottom:8px;">✅ DO IMMEDIATELY</div>
            ① Call <b>112</b> right away<br>
            ② Switch on hazard lights<br>
            ③ Keep victim still & calm<br>
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
    st.markdown('<span style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#6366f1;margin-bottom:0.5rem;display:block;">Chat with RoadSoS AI</span>', unsafe_allow_html=True)
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
