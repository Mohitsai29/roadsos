import streamlit as st
from streamlit_folium import st_folium
from emergency_finder import find_nearby_services, get_nearest_hospital
from ai_assistant import get_ai_guidance, chat_with_ai
from map_module import create_emergency_map
from geopy.geocoders import Nominatim

st.set_page_config(page_title="RoadSoS", page_icon="🚨", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
.stApp { background: #f5f3ff; }
section[data-testid="stSidebar"] { background: #1e1b4b !important; border-right: none !important; }
section[data-testid="stSidebar"] * { color: #e0e7ff !important; }
section[data-testid="stSidebar"] .stButton > button { background: #4f46e5 !important; color: white !important; border: none !important; border-radius: 12px !important; width: 100% !important; padding: 0.6rem !important; font-weight: 600 !important; font-size: 0.88rem !important; }
section[data-testid="stSidebar"] .stButton > button:hover { background: #4338ca !important; }
section[data-testid="stSidebar"] .stTextInput > div > div > input { background: #312e81 !important; border: 1px solid #4f46e5 !important; border-radius: 10px !important; color: white !important; font-size: 0.88rem !important; }
section[data-testid="stSidebar"] .stTextInput > div > div > input::placeholder { color: #a5b4fc !important; }
section[data-testid="stSidebar"] hr { border-color: #312e81 !important; }
.hero { background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); border-radius: 24px; padding: 2.5rem 3rem; margin-bottom: 1.5rem; position: relative; overflow: hidden; }
.hero::before { content: ''; position: absolute; top: -50%; right: -10%; width: 400px; height: 400px; background: rgba(255,255,255,0.05); border-radius: 50%; }
.hero h1 { font-size: 2rem; font-weight: 700; color: white !important; margin: 0 0 0.4rem; }
.hero p { color: rgba(255,255,255,0.8) !important; margin: 0; font-size: 0.95rem; }
.hero-badge { display: inline-block; background: rgba(255,255,255,0.15); color: white !important; border-radius: 20px; padding: 4px 14px; font-size: 0.78rem; font-weight: 600; margin-bottom: 0.8rem; }
.num-row { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 1.5rem; }
.num-card { background: white; border-radius: 16px; padding: 1rem; text-align: center; border: 1px solid #ede9fe; transition: all 0.2s; }
.num-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(79,70,229,0.12); }
.num-card .icon { font-size: 1.4rem; margin-bottom: 4px; }
.num-card .num { font-size: 1.7rem; font-weight: 700; color: #4f46e5; line-height: 1; }
.num-card .lbl { font-size: 0.72rem; color: #94a3b8; margin-top: 3px; font-weight: 500; }

/* SOS CALL CARD */
.sos-card {
    background: linear-gradient(135deg, #dc2626, #b91c1c);
    border-radius: 20px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
    box-shadow: 0 8px 32px rgba(220,38,38,0.25);
}
.sos-card .sos-info { flex: 1; }
.sos-card .sos-title { font-size: 0.72rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.3px; color: rgba(255,255,255,0.7) !important; margin-bottom: 4px; }
.sos-card .sos-name { font-size: 1.1rem; font-weight: 700; color: white !important; }
.sos-card .sos-dist { font-size: 0.82rem; color: rgba(255,255,255,0.75) !important; margin-top: 2px; }
.sos-call-btn {
    background: white !important;
    color: #dc2626 !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    transition: all 0.2s;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.sos-call-btn:hover { transform: scale(1.03); box-shadow: 0 6px 20px rgba(0,0,0,0.2); }
.no-phone-btn {
    background: rgba(255,255,255,0.2) !important;
    color: white !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    border-radius: 50px !important;
    padding: 0.7rem 2rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
}

.stTabs [data-baseweb="tab-list"] { background: white !important; border-radius: 16px !important; padding: 6px !important; border: 1px solid #ede9fe !important; gap: 4px !important; }
.stTabs [data-baseweb="tab"] { border-radius: 12px !important; font-size: 0.88rem !important; font-weight: 500 !important; color: #94a3b8 !important; padding: 0.55rem 1.4rem !important; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #4f46e5, #7c3aed) !important; color: white !important; }
.svc { background: white; border-radius: 14px; padding: 1rem 1.2rem; margin: 0.5rem 0; border: 1px solid #ede9fe; border-left: 4px solid #4f46e5; }
.svc .name { font-weight: 600; color: #1e1b4b; font-size: 0.92rem; }
.svc .phone { color: #64748b; font-size: 0.8rem; margin-top: 2px; }
.svc .dist { display: inline-block; background: #ede9fe; color: #4f46e5; font-size: 0.72rem; font-weight: 600; padding: 2px 10px; border-radius: 20px; margin-top: 6px; }
.call-link { display: inline-block; background: #dcfce7; color: #16a34a !important; font-size: 0.75rem; font-weight: 700; padding: 3px 12px; border-radius: 20px; margin-top: 6px; margin-left: 6px; text-decoration: none; border: 1px solid #bbf7d0; }
.call-link:hover { background: #bbf7d0; }
.guidance { background: white; border-radius: 16px; padding: 1.8rem; border: 1px solid #ede9fe; border-top: 4px solid #4f46e5; line-height: 1.85; color: #1e1b4b; font-size: 0.93rem; }
.ref { background: white; border-radius: 14px; padding: 1.3rem; border: 1px solid #ede9fe; line-height: 1.9; color: #1e1b4b; font-size: 0.85rem; }
.empty { text-align: center; padding: 4rem 2rem; background: white; border-radius: 20px; border: 1px solid #ede9fe; }
.stButton > button { background: linear-gradient(135deg, #4f46e5, #7c3aed) !important; color: white !important; border: none !important; border-radius: 12px !important; font-weight: 600 !important; padding: 0.55rem 1.8rem !important; transition: all 0.2s !important; }
.stButton > button:hover { opacity: 0.9 !important; transform: translateY(-1px) !important; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea { border-radius: 12px !important; border: 1.5px solid #ede9fe !important; color: #1e1b4b !important; }
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus { border-color: #4f46e5 !important; box-shadow: 0 0 0 3px rgba(79,70,229,0.1) !important; }
div[data-testid="stChatMessage"] { background: white !important; border-radius: 14px !important; border: 1px solid #ede9fe !important; margin: 0.4rem 0 !important; }
.tip { background: #ede9fe; border-radius: 10px; padding: 0.65rem 1rem; font-size: 0.82rem; color: #4338ca; margin-bottom: 1rem; border: 1px solid #c7d2fe; }
.slabel { font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.3px; color: #a5b4fc !important; display: block; margin: 1rem 0 0.4rem; }
.loc-pill { background: #312e81; border: 1px solid #4f46e5; border-radius: 10px; padding: 0.5rem 0.8rem; font-size: 0.8rem; color: #a5b4fc !important; margin-top: 0.4rem; word-break: break-all; }
.stSlider > div > div > div > div { background: #4f46e5 !important; }
</style>
""", unsafe_allow_html=True)

for key, default in [("chat_history", []), ("services", None), ("user_location", None)]:
    if key not in st.session_state:
        st.session_state[key] = default

# ══════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="padding:0.5rem 0 1rem;">
        <div style="font-size:1.3rem; font-weight:700; color:white !important;">🚨 RoadSoS</div>
        <div style="font-size:0.75rem; color:#a5b4fc !important; margin-top:2px;">India Emergency Assistant</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<span class="slabel">📍 Your Location</span>', unsafe_allow_html=True)

    st.components.v1.html("""
    <style>
        #gps-btn { background:#4f46e5; color:white; border:none; border-radius:10px; padding:8px 16px; font-size:13px; font-weight:600; cursor:pointer; width:100%; margin-bottom:6px; font-family:Inter,sans-serif; }
        #gps-btn:hover { background:#4338ca; }
        #gps-status { font-size:11px; padding:6px 8px; border-radius:8px; font-family:Inter,sans-serif; min-height:28px; background:#312e81; color:#a5b4fc; }
    </style>
    <button id="gps-btn" onclick="getGPS()">📍 Detect My Exact Location</button>
    <div id="gps-status">Tap above to detect your GPS location</div>
    <script>
    function getGPS() {
        var btn = document.getElementById('gps-btn');
        var status = document.getElementById('gps-status');
        btn.innerText = '⏳ Detecting...';
        btn.disabled = true;
        status.style.color = '#fbbf24';
        status.innerText = 'Requesting GPS permission...';
        if (!navigator.geolocation) {
            status.style.color = '#f87171';
            status.innerText = '❌ GPS not supported. Type city below.';
            btn.innerText = '📍 Detect My Location'; btn.disabled = false; return;
        }
        navigator.geolocation.getCurrentPosition(
            function(pos) {
                var lat = pos.coords.latitude.toFixed(6);
                var lon = pos.coords.longitude.toFixed(6);
                var val = lat + ', ' + lon;
                status.style.color = '#34d399';
                status.innerText = '✅ ' + val + ' — now click USE LOCATION ↓';
                btn.innerText = '✅ Detected!'; btn.style.background = '#059669';
                var tryFill = setInterval(function() {
                    var inputs = window.parent.document.querySelectorAll('input[type=text]');
                    for (var i=0; i<inputs.length; i++) {
                        var ph = inputs[i].getAttribute('placeholder') || '';
                        if (ph.includes('GPS') || ph.includes('city') || ph.includes('16.')) {
                            inputs[i].value = val;
                            inputs[i].dispatchEvent(new Event('input', {bubbles:true}));
                            inputs[i].dispatchEvent(new Event('change', {bubbles:true}));
                            clearInterval(tryFill); break;
                        }
                    }
                }, 300);
                setTimeout(function(){ clearInterval(tryFill); }, 5000);
            },
            function(err) {
                status.style.color = '#f87171';
                status.innerText = err.code===1 ? '❌ Permission denied. Type city below.' : '❌ GPS failed. Type city manually.';
                btn.innerText = '📍 Try Again'; btn.disabled = false; btn.style.background = '#4f46e5';
            },
            {enableHighAccuracy:true, timeout:10000, maximumAge:0}
        );
    }
    </script>
    """, height=90)

    coord_input = st.text_input("",
        placeholder="GPS fills here — or type city: Vijayawada",
        label_visibility="collapsed", key="coord_box")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("✅ Use Location", use_container_width=True):
            val = coord_input.strip()
            if "," in val:
                try:
                    parts = val.split(",")
                    lat, lon = float(parts[0].strip()), float(parts[1].strip())
                    if 6.5 <= lat <= 37.5 and 68.0 <= lon <= 97.5:
                        st.session_state.user_location = (lat, lon, f"{lat:.5f}, {lon:.5f}")
                        st.success("✅ Location set!")
                    else:
                        st.error("Outside India bounds")
                except:
                    st.error("Invalid format")
            elif val:
                geolocator = Nominatim(user_agent="roadsos_v3")
                loc = geolocator.geocode(val + ", India", country_codes="IN")
                if loc and 6.5 <= loc.latitude <= 37.5:
                    st.session_state.user_location = (loc.latitude, loc.longitude, val)
                    st.success("✅ Found!")
                else:
                    st.error("Not found in India")
            else:
                st.warning("Enter location first")
    with c2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.user_location = None
            st.session_state.services = None
            st.rerun()

    if st.session_state.user_location:
        st.markdown(f'<div class="loc-pill">📍 {st.session_state.user_location[2]}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span class="slabel">🔍 Search Radius</span>', unsafe_allow_html=True)
    radius = st.slider("", 2, 25, 10, label_visibility="collapsed")
    st.caption(f"Within **{radius} km**")
    st.markdown("---")

    if st.session_state.user_location:
        if st.button("🚨  FIND EMERGENCY SERVICES", use_container_width=True):
            lat, lon, addr = st.session_state.user_location
            with st.spinner("Scanning nearby services..."):
                st.session_state.services = find_nearby_services(lat, lon, radius)
            found = sum(len(v) for v in st.session_state.services.values())
            if found > 0:
                st.success(f"✅ Found {found} services!")
            else:
                st.warning("None found. Try 20km radius.")
    else:
        st.markdown("""
        <div style="background:#312e81; border:1px solid #4f46e5; border-radius:10px;
             padding:0.6rem; font-size:0.8rem; color:#a5b4fc; text-align:center;">
            ☝️ Detect or enter location first
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<span class="slabel">☎️ Quick Dial</span>', unsafe_allow_html=True)
    for emoji, num, name in [("🚑","108","Ambulance"),("🚔","100","Police"),("🔥","101","Fire"),("🛣️","1033","Highway")]:
        st.markdown(f"""
        <div style="display:flex; justify-content:space-between; align-items:center;
             background:#312e81; border-radius:10px; padding:8px 12px; margin:4px 0;
             border:1px solid #4f46e5;">
            <span style="font-size:0.85rem;">{emoji} {name}</span>
            <span style="font-size:1rem; font-weight:700; color:#818cf8 !important;">{num}</span>
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

# ── NEAREST HOSPITAL CALL CARD ──
if st.session_state.services:
    nearest = get_nearest_hospital(st.session_state.services)
    if nearest:
        if nearest.get("phone"):
            phone_clean = nearest["phone"].replace(" ","").replace("-","")
            st.markdown(f"""
            <div class="sos-card">
                <div class="sos-info">
                    <div class="sos-title">🏥 Nearest Hospital — Tap to Call Now</div>
                    <div class="sos-name">{nearest['name']}</div>
                    <div class="sos-dist">📏 {nearest['distance_km']} km away &nbsp;·&nbsp; 📞 {nearest['phone']}</div>
                </div>
                <a href="tel:{phone_clean}" class="sos-call-btn">📞 Call Now</a>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="sos-card">
                <div class="sos-info">
                    <div class="sos-title">🏥 Nearest Hospital</div>
                    <div class="sos-name">{nearest['name']}</div>
                    <div class="sos-dist">📏 {nearest['distance_km']} km away &nbsp;·&nbsp; No phone listed</div>
                </div>
                <a href="tel:108" class="sos-call-btn">📞 Call 108</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="sos-card">
            <div class="sos-info">
                <div class="sos-title">🏥 Emergency</div>
                <div class="sos-name">No nearby hospital found</div>
                <div class="sos-dist">Call national ambulance directly</div>
            </div>
            <a href="tel:108" class="sos-call-btn">📞 Call 108</a>
        </div>
        """, unsafe_allow_html=True)

# Emergency numbers
st.markdown("""
<div class="num-row">
    <div class="num-card"><div class="icon">🆘</div><div class="num">112</div><div class="lbl">National SOS</div></div>
    <div class="num-card"><div class="icon">🚑</div><div class="num">108</div><div class="lbl">Ambulance</div></div>
    <div class="num-card"><div class="icon">🚔</div><div class="num">100</div><div class="lbl">Police</div></div>
    <div class="num-card"><div class="icon">🛣️</div><div class="num">1033</div><div class="lbl">Highway Help</div></div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🗺️  Map & Services", "🤖  AI First-Aid Guide", "💬  AI Chat"])

with tab1:
    if st.session_state.user_location and st.session_state.services:
        lat, lon, addr = st.session_state.user_location
        total = sum(len(v) for v in st.session_state.services.values())
        if total == 0:
            st.markdown("""
            <div class="empty">
                <div style="font-size:2.5rem">🔍</div>
                <div style="font-weight:600; color:#1e1b4b; margin:0.8rem 0 0.3rem">No services found</div>
                <div style="color:#94a3b8; font-size:0.88rem">Increase radius to 15–20 km in the left panel</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#4f46e5;margin-bottom:0.5rem;">Live Emergency Map</div>', unsafe_allow_html=True)
                m = create_emergency_map(lat, lon, st.session_state.services)
                st_folium(m, width=None, height=440)
            with col2:
                st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#4f46e5;margin-bottom:0.5rem;">Nearest Services</div>', unsafe_allow_html=True)
                icons = {"hospitals": "🏥", "police": "🚔", "ambulance": "🚑"}
                colors = {"hospitals": "#dc2626", "police": "#2563eb", "ambulance": "#d97706"}
                for stype, places in st.session_state.services.items():
                    if places:
                        for p in places[:2]:
                            ph = p['phone'] if p['phone'] else ""
                            c = colors.get(stype, "#4f46e5")
                            call_btn = f'<a href="tel:{ph}" class="call-link">📞 Call</a>' if ph else '<span style="font-size:0.75rem;color:#94a3b8;margin-left:6px;">No phone</span>'
                            st.markdown(f"""
                            <div class="svc" style="border-left-color:{c}">
                                <div class="name">{icons.get(stype,'')} {p['name']}</div>
                                <div class="phone">{"📞 " + ph if ph else "Phone not listed"}</div>
                                <span class="dist">📏 {p['distance_km']} km</span>
                                {call_btn}
                            </div>
                            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty">
            <div style="font-size:3rem">🗺️</div>
            <div style="font-weight:600;font-size:1.05rem;color:#1e1b4b;margin:1rem 0 0.4rem">Detect your location to get started</div>
            <div style="color:#94a3b8;font-size:0.88rem">Left panel → Detect GPS → Find Emergency Services</div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#4f46e5;margin-bottom:0.5rem;">Describe the Accident</div>', unsafe_allow_html=True)
        situation = st.text_area("",
            placeholder="e.g. Two vehicles collided on NH65 near Vijayawada. One person unconscious, another bleeding...",
            height=160, label_visibility="collapsed")
        if st.button("⚡  Get AI Emergency Guidance"):
            if situation.strip():
                loc_info = st.session_state.user_location[2] if st.session_state.user_location else "India"
                with st.spinner("AI analyzing situation..."):
                    guidance = get_ai_guidance(situation, loc_info)
                st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#4f46e5;margin:1.2rem 0 0.5rem;">AI Emergency Guidance</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="guidance">{guidance}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please describe the accident situation above.")
    with col2:
        st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#4f46e5;margin-bottom:0.5rem;">Quick Reference</div>', unsafe_allow_html=True)
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
    st.markdown('<div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#4f46e5;margin-bottom:0.5rem;">Chat with RoadSoS AI</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="tip">
        💡 Ask anything — "What do I do if someone is unconscious?", "How to stop bleeding?", "Is it safe to move the victim?"
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
