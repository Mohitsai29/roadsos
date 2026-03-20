import streamlit as st
from streamlit_folium import st_folium
from emergency_finder import find_nearby_services, get_nearest_hospital
from ai_assistant import get_ai_guidance, chat_with_ai
from map_module import create_emergency_map
from geopy.geocoders import Nominatim

st.set_page_config(page_title="RoadSoS", page_icon="🚨", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
#MainMenu, footer, header { visibility: hidden !important; }
.stApp { background: #f5f3ff; }
.block-container { padding: 1.5rem 2rem !important; max-width: 1400px !important; }

.hero { background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); border-radius: 20px; padding: 2rem 2.5rem; margin-bottom: 1.5rem; }
.hero h1 { font-size: 1.9rem; font-weight: 700; color: white !important; margin: 0 0 0.3rem; }
.hero p { color: rgba(255,255,255,0.82) !important; margin: 0; font-size: 0.93rem; }
.hero-badge { display: inline-block; background: rgba(255,255,255,0.18); color: white !important; border-radius: 20px; padding: 3px 14px; font-size: 0.78rem; font-weight: 600; margin-bottom: 0.7rem; }

.card { background: white; border-radius: 16px; padding: 1.5rem; border: 1px solid #ede9fe; margin-bottom: 1.2rem; }
.clabel { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.3px; color: #4f46e5; margin-bottom: 0.8rem; display: block; }

.num-row { display: grid; grid-template-columns: repeat(4,1fr); gap: 10px; margin-bottom: 1.2rem; }
.num-card { background: white; border-radius: 14px; padding: 1rem; text-align: center; border: 1px solid #ede9fe; }
.num-card .ni { font-size: 1.4rem; margin-bottom: 4px; }
.num-card .nn { font-size: 1.6rem; font-weight: 700; color: #4f46e5; line-height: 1; }
.num-card .nl { font-size: 0.72rem; color: #94a3b8; margin-top: 3px; }

.sos-card { background: linear-gradient(135deg, #dc2626, #b91c1c); border-radius: 18px; padding: 1.3rem 1.8rem; margin-bottom: 1.2rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; box-shadow: 0 8px 28px rgba(220,38,38,0.2); }
.sos-title { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; color: rgba(255,255,255,0.7) !important; margin-bottom: 3px; }
.sos-name { font-size: 1.05rem; font-weight: 700; color: white !important; }
.sos-dist { font-size: 0.82rem; color: rgba(255,255,255,0.75) !important; margin-top: 2px; }
.call-now { display: inline-block; background: white; color: #dc2626 !important; border-radius: 50px; padding: 0.7rem 2rem; font-weight: 700; font-size: 1rem; text-decoration: none !important; white-space: nowrap; }

.radius-badge { display: inline-flex; align-items: center; gap: 6px; background: #ede9fe; color: #4f46e5; border: 1px solid #c7d2fe; border-radius: 20px; padding: 4px 14px; font-size: 0.82rem; font-weight: 600; margin: 0.4rem 0; }
.search-progress { background: white; border-radius: 14px; padding: 1rem 1.2rem; border: 1px solid #ede9fe; margin-bottom: 1rem; }
.progress-step { display: flex; align-items: center; gap: 10px; padding: 5px 0; font-size: 0.85rem; color: #1e1b4b; }
.step-done { color: #16a34a; font-weight: 600; }
.step-active { color: #4f46e5; font-weight: 600; }
.step-wait { color: #94a3b8; }

.stTabs [data-baseweb="tab-list"] { background: white !important; border-radius: 14px !important; padding: 5px !important; border: 1px solid #ede9fe !important; gap: 4px !important; }
.stTabs [data-baseweb="tab"] { border-radius: 10px !important; font-size: 0.9rem !important; font-weight: 500 !important; color: #94a3b8 !important; padding: 0.55rem 1.4rem !important; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #4f46e5, #7c3aed) !important; color: white !important; }

.svc { background: white; border-radius: 14px; padding: 1rem 1.2rem; margin: 0.5rem 0; border: 1px solid #ede9fe; border-left: 4px solid #4f46e5; }
.svc .sname { font-weight: 600; color: #1e1b4b; font-size: 0.92rem; }
.svc .sph { color: #64748b; font-size: 0.8rem; margin-top: 2px; }
.svc-dist { display: inline-block; background: #ede9fe; color: #4f46e5; font-size: 0.72rem; font-weight: 600; padding: 2px 10px; border-radius: 20px; margin-top: 5px; }
.call-svc { display: inline-block; background: #dcfce7; color: #16a34a !important; font-size: 0.75rem; font-weight: 700; padding: 2px 12px; border-radius: 20px; margin-top: 5px; margin-left: 6px; text-decoration: none !important; border: 1px solid #bbf7d0; }

.guidance { background: white; border-radius: 16px; padding: 1.8rem; border: 1px solid #ede9fe; border-top: 4px solid #4f46e5; line-height: 1.85; color: #1e1b4b; font-size: 0.93rem; }
.ref { background: white; border-radius: 14px; padding: 1.3rem; border: 1px solid #ede9fe; line-height: 1.9; color: #1e1b4b; font-size: 0.87rem; }
.tip { background: #ede9fe; border-radius: 10px; padding: 0.65rem 1rem; font-size: 0.85rem; color: #4338ca; margin-bottom: 1rem; border: 1px solid #c7d2fe; }
.empty { text-align: center; padding: 3rem 2rem; background: white; border-radius: 18px; border: 1px solid #ede9fe; }

.stButton > button { background: linear-gradient(135deg, #4f46e5, #7c3aed) !important; color: white !important; border: none !important; border-radius: 12px !important; font-weight: 600 !important; padding: 0.65rem 1.5rem !important; font-size: 0.93rem !important; transition: all 0.2s !important; width: 100% !important; }
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stTextInput > div > div > input { border-radius: 12px !important; border: 1.5px solid #ede9fe !important; color: #1e1b4b !important; font-size: 0.93rem !important; padding: 0.65rem 1rem !important; background: white !important; }
.stTextInput > div > div > input:focus { border-color: #4f46e5 !important; box-shadow: 0 0 0 3px rgba(79,70,229,0.1) !important; }
.stTextArea > div > div > textarea { border-radius: 12px !important; border: 1.5px solid #ede9fe !important; color: #1e1b4b !important; font-size: 0.93rem !important; background: white !important; }
div[data-testid="stChatMessage"] { background: white !important; border-radius: 14px !important; border: 1px solid #ede9fe !important; margin: 0.4rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state ──
for key, default in [
    ("chat_history", []),
    ("services", None),
    ("user_location", None),
    ("search_radius_used", None)
]:
    if key not in st.session_state:
        st.session_state[key] = default

def auto_search(lat, lon):
    """Search starting from 0.5 km, incrementing by 0.5 km until services found or 20 km reached."""
    radius = 0.5
    max_radius = 20.0
    step = 0.5

    progress_placeholder = st.empty()

    while radius <= max_radius:
        # Show live progress
        radius_m = radius * 1000
        if radius_m >= 1000:
            radius_label = f"{radius:.1f} km"
        else:
            radius_label = f"{int(radius_m)} m"

        progress_placeholder.markdown(f"""
        <div class="search-progress">
            <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#4f46e5;margin-bottom:0.6rem;">
                🔍 Auto-searching nearby services...
            </div>
            <div class="progress-step step-active">
                ⏳ Searching within <b>{radius_label}</b> of your location...
            </div>
            <div class="progress-step step-wait" style="margin-top:4px;font-size:0.78rem;">
                Will expand up to 20 km automatically if needed
            </div>
        </div>
        """, unsafe_allow_html=True)

        services = find_nearby_services(lat, lon, radius)
        total = sum(len(v) for v in services.values())

        if total > 0:
            progress_placeholder.markdown(f"""
            <div class="search-progress">
                <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#16a34a;margin-bottom:0.6rem;">
                    ✅ Services found!
                </div>
                <div class="progress-step step-done">
                    ✅ Found <b>{total} services</b> within <b>{radius_label}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.search_radius_used = radius
            return services, radius

        radius = round(radius + step, 1)

    # Nothing found even at 20 km
    progress_placeholder.markdown(f"""
    <div class="search-progress">
        <div style="font-size:0.72rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#dc2626;margin-bottom:0.6rem;">
            ⚠️ Search complete
        </div>
        <div class="progress-step" style="color:#dc2626;">
            No services found within 20 km. Please call 112 directly.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.session_state.search_radius_used = max_radius
    return {}, max_radius

# ══════════════════════════════════════
# HERO
# ══════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-badge">🇮🇳 India Road Safety · AI Powered</div>
    <h1>🚨 RoadSoS — Emergency Assistant</h1>
    <p>Instantly locate hospitals, police & ambulances · Get AI first-aid guidance · Chat with emergency AI</p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════
# LOCATION SECTION
# ══════════════════════════════════════
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<span class="clabel">📍 Step 1 — Detect Your Location & Auto-Search</span>', unsafe_allow_html=True)

col_gps, col_dial = st.columns([3, 1])

with col_gps:
    st.components.v1.html("""
    <style>
    body { margin:0; padding:0; background:transparent; }
    #gb { background:#4f46e5; color:white; border:none; border-radius:12px; padding:14px 20px; font-size:15px; font-weight:600; cursor:pointer; width:100%; font-family:Inter,sans-serif; margin-bottom:10px; transition:background 0.2s; }
    #gb:hover { background:#4338ca; }
    #gs { font-size:13px; padding:10px 14px; border-radius:10px; font-family:Inter,sans-serif; background:#ede9fe; color:#4338ca; line-height:1.5; min-height:38px; }
    </style>
    <button id="gb" onclick="go()">📍 Detect My Exact GPS Location</button>
    <div id="gs">Tap above — browser will ask for your location permission</div>
    <script>
    function go() {
        var b=document.getElementById('gb'), s=document.getElementById('gs');
        b.innerText='⏳ Detecting...'; b.disabled=true;
        s.style.background='#fef3c7'; s.style.color='#92400e';
        s.innerText='Requesting GPS permission...';
        if(!navigator.geolocation){
            s.style.background='#fee2e2'; s.style.color='#991b1b';
            s.innerText='❌ GPS not available. Type city below.';
            b.innerText='📍 Detect GPS'; b.disabled=false; return;
        }
        navigator.geolocation.getCurrentPosition(function(p){
            var lat=p.coords.latitude.toFixed(6), lon=p.coords.longitude.toFixed(6);
            var v=lat+', '+lon;
            s.style.background='#dcfce7'; s.style.color='#166534';
            s.innerText='✅ GPS detected: '+v+'\nNow click USE LOCATION & AUTO-SEARCH below ↓';
            b.innerText='✅ GPS Ready — Click the button below!';
            b.style.background='#059669';
            var n=0, t=setInterval(function(){
                n++;
                var ins=window.parent.document.querySelectorAll('input[type=text]');
                for(var i=0;i<ins.length;i++){
                    var ph=(ins[i].getAttribute('placeholder')||'').toLowerCase();
                    if(ph.includes('gps')||ph.includes('city')||ph.includes('enter')){
                        ins[i].value=v;
                        ins[i].dispatchEvent(new Event('input',{bubbles:true}));
                        ins[i].dispatchEvent(new Event('change',{bubbles:true}));
                        clearInterval(t); break;
                    }
                }
                if(n>20) clearInterval(t);
            },400);
        },function(e){
            s.style.background='#fee2e2'; s.style.color='#991b1b';
            s.innerText=e.code===1?'❌ Permission denied. Type city below.':'❌ GPS error. Type city below.';
            b.innerText='📍 Try Again'; b.disabled=false; b.style.background='#4f46e5';
        },{enableHighAccuracy:true,timeout:12000,maximumAge:0});
    }
    </script>
    """, height=120)

    coord_input = st.text_input("",
        placeholder="GPS fills here — or type city: Vijayawada",
        label_visibility="collapsed", key="coord_box")

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button("✅ Use Location & Auto-Search"):
            val = coord_input.strip()
            if not val:
                st.warning("Detect GPS or type a city first")
            else:
                # Parse coordinates or geocode city
                if "," in val:
                    try:
                        p = val.split(",")
                        lat, lon = float(p[0].strip()), float(p[1].strip())
                        if 6.5 <= lat <= 37.5 and 68.0 <= lon <= 97.5:
                            st.session_state.user_location = (lat, lon, f"{lat:.5f}, {lon:.5f}")
                        else:
                            st.error("Outside India bounds"); st.stop()
                    except:
                        st.error("Invalid format"); st.stop()
                else:
                    geo = Nominatim(user_agent="roadsos_v7")
                    loc = geo.geocode(val + ", India", country_codes="IN")
                    if loc and 6.5 <= loc.latitude <= 37.5:
                        st.session_state.user_location = (loc.latitude, loc.longitude, val)
                    else:
                        st.error("Location not found in India"); st.stop()

                # Auto search
                lat, lon, addr = st.session_state.user_location
                services, radius_used = auto_search(lat, lon)
                st.session_state.services = services
                st.rerun()

    with c2:
        if st.button("🗑️ Clear & Reset"):
            st.session_state.user_location = None
            st.session_state.services = None
            st.session_state.search_radius_used = None
            st.rerun()

    # Status display
    if st.session_state.user_location:
        radius_info = ""
        if st.session_state.search_radius_used:
            r = st.session_state.search_radius_used
            r_label = f"{int(r*1000)} m" if r < 1 else f"{r:.1f} km"
            total = sum(len(v) for v in st.session_state.services.values()) if st.session_state.services else 0
            radius_info = f" &nbsp;·&nbsp; 🔍 Found {total} services within {r_label}"
        st.markdown(f"""
        <div style="background:#ede9fe;border:1px solid #c7d2fe;border-radius:10px;
             padding:0.5rem 1rem;font-size:0.85rem;color:#4338ca;margin-top:0.5rem;">
            ✅ <b>{st.session_state.user_location[2]}</b>{radius_info}
        </div>
        """, unsafe_allow_html=True)

with col_dial:
    st.markdown("""
    <div style="background:#1e1b4b;border-radius:14px;padding:1.2rem 1rem;">
        <div style="font-size:0.7rem;font-weight:700;text-transform:uppercase;letter-spacing:1.3px;color:#818cf8;margin-bottom:0.8rem;">☎️ Quick Dial</div>
        <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #312e81;">
            <span style="color:#e0e7ff;font-size:0.9rem;">🚑 Ambulance</span><span style="color:#818cf8;font-weight:700;font-size:1rem;">108</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #312e81;">
            <span style="color:#e0e7ff;font-size:0.9rem;">🚔 Police</span><span style="color:#818cf8;font-weight:700;font-size:1rem;">100</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #312e81;">
            <span style="color:#e0e7ff;font-size:0.9rem;">🔥 Fire</span><span style="color:#818cf8;font-weight:700;font-size:1rem;">101</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #312e81;">
            <span style="color:#e0e7ff;font-size:0.9rem;">🛣️ Highway</span><span style="color:#818cf8;font-weight:700;font-size:1rem;">1033</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:8px 0;">
            <span style="color:#e0e7ff;font-size:0.9rem;">🆘 SOS</span><span style="color:#818cf8;font-weight:700;font-size:1rem;">112</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── NEAREST HOSPITAL CALL CARD ──
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

# ── EMERGENCY NUMBERS ──
st.markdown("""
<div class="num-row">
    <div class="num-card"><div class="ni">🆘</div><div class="nn">112</div><div class="nl">National SOS</div></div>
    <div class="num-card"><div class="ni">🚑</div><div class="nn">108</div><div class="nl">Ambulance</div></div>
    <div class="num-card"><div class="ni">🚔</div><div class="nn">100</div><div class="nl">Police</div></div>
    <div class="num-card"><div class="ni">🛣️</div><div class="nn">1033</div><div class="nl">Highway Help</div></div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──
tab1, tab2, tab3 = st.tabs(["🗺️  Map & Services", "🤖  AI First-Aid Guide", "💬  AI Chat"])

with tab1:
    if st.session_state.user_location and st.session_state.services:
        lat, lon, _ = st.session_state.user_location
        total = sum(len(v) for v in st.session_state.services.values())
        if total == 0:
            st.markdown("""
            <div class="empty">
                <div style="font-size:2.5rem">🔍</div>
                <div style="font-weight:600;color:#1e1b4b;margin:0.8rem 0 0.3rem;">No services found within 20 km</div>
                <div style="color:#94a3b8;font-size:0.88rem;">Please call 112 directly for emergency help</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Show radius badge
            r = st.session_state.search_radius_used or 0
            r_label = f"{int(r*1000)} m" if r < 1 else f"{r:.1f} km"
            st.markdown(f'<div class="radius-badge">🔍 Showing services within <b>&nbsp;{r_label}&nbsp;</b> of your location</div>', unsafe_allow_html=True)

            col1, col2 = st.columns([3, 2])
            with col1:
                st.markdown('<span class="clabel">Live Emergency Map</span>', unsafe_allow_html=True)
                m = create_emergency_map(lat, lon, st.session_state.services)
                st_folium(m, width=None, height=450)
            with col2:
                st.markdown('<span class="clabel">Nearest Services</span>', unsafe_allow_html=True)
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
            <div style="font-weight:600;font-size:1rem;color:#1e1b4b;margin:1rem 0 0.4rem;">
                Detect GPS → Click Use Location & Auto-Search
            </div>
            <div style="color:#94a3b8;font-size:0.88rem;">
                The app will automatically find the nearest services starting from 500 m
            </div>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown('<span class="clabel">Describe the Accident</span>', unsafe_allow_html=True)
        situation = st.text_area("",
            placeholder="e.g. Two vehicles collided on NH65 near Vijayawada. One person unconscious, another has bleeding arm...",
            height=160, label_visibility="collapsed")
        if st.button("⚡  Get AI Emergency Guidance"):
            if situation.strip():
                loc_info = st.session_state.user_location[2] if st.session_state.user_location else "India"
                with st.spinner("AI analyzing situation..."):
                    guidance = get_ai_guidance(situation, loc_info)
                st.markdown('<span class="clabel" style="margin-top:1rem;">AI Guidance</span>', unsafe_allow_html=True)
                st.markdown(f'<div class="guidance">{guidance}</div>', unsafe_allow_html=True)
            else:
                st.warning("Please describe the accident situation first.")
    with col2:
        st.markdown('<span class="clabel">Quick Reference</span>', unsafe_allow_html=True)
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
    st.markdown('<span class="clabel">Chat with RoadSoS AI</span>', unsafe_allow_html=True)
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
