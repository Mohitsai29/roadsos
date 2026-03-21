st.components.v1.html("""
<!DOCTYPE html>
<html>
<head>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; font-family: Inter, sans-serif; }
body { background: transparent; }
#btn {
    width: 100%; padding: 14px 20px; font-size: 15px; font-weight: 700;
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white; border: none; border-radius: 14px; cursor: pointer;
    transition: opacity 0.2s;
}
#btn:hover { opacity: 0.88; }
#status {
    margin-top: 10px; padding: 10px 14px; border-radius: 10px;
    font-size: 13px; line-height: 1.6;
    background: #1e1a3f; color: #a5b4fc;
    border: 1px solid #2a2660; display: none;
    white-space: pre-line;
}
</style>
</head>
<body>
<button id="btn" onclick="detect()">📍 Detect My Exact GPS Location</button>
<div id="status"></div>
<script>
function fillInput(val) {
    var attempts = 0;
    var timer = setInterval(function() {
        attempts++;
        var inputs = window.parent.document.querySelectorAll('input[type="text"]');
        for (var i = 0; i < inputs.length; i++) {
            var ph = (inputs[i].placeholder || '').toLowerCase();
            if (ph.indexOf('gps') !== -1 ||
                ph.indexOf('vijayawada') !== -1 ||
                ph.indexOf('city') !== -1 ||
                ph.indexOf('fills') !== -1) {
                inputs[i].value = val;
                inputs[i].dispatchEvent(new Event('input', { bubbles: true }));
                inputs[i].dispatchEvent(new Event('change', { bubbles: true }));
                clearInterval(timer);
                return;
            }
        }
        if (attempts > 40) clearInterval(timer);
    }, 250);
}

function detect() {
    var btn = document.getElementById('btn');
    var st = document.getElementById('status');
    st.style.display = 'block';

    if (!navigator.geolocation) {
        st.style.background = '#450a0a';
        st.style.color = '#f87171';
        st.style.borderColor = '#991b1b';
        st.innerText = '❌ GPS not supported by this browser.\nPlease type your city name in the box below.';
        return;
    }

    btn.disabled = true;
    btn.innerText = '⏳ Detecting location...';
    st.style.background = '#1e1a3f';
    st.style.color = '#fbbf24';
    st.style.borderColor = '#2a2660';
    st.innerText = 'Requesting GPS permission...\nIf a popup appears, click Allow.';

    navigator.geolocation.getCurrentPosition(
        function(pos) {
            var lat = pos.coords.latitude.toFixed(6);
            var lon = pos.coords.longitude.toFixed(6);
            var val = lat + ', ' + lon;
            var acc = Math.round(pos.coords.accuracy);

            st.style.background = '#052e16';
            st.style.color = '#34d399';
            st.style.borderColor = '#166534';
            st.innerText = '✅ Detected: ' + val + '\nAccuracy: ±' + acc + ' m\nNow click USE LOCATION & AUTO-SEARCH ↓';

            btn.innerText = '✅ GPS Ready!';
            btn.style.background = '#059669';

            fillInput(val);
        },
        function(err) {
            st.style.background = '#450a0a';
            st.style.color = '#f87171';
            st.style.borderColor = '#991b1b';
            btn.disabled = false;
            btn.innerText = '📍 Try GPS Again';
            btn.style.background = 'linear-gradient(135deg, #4f46e5, #7c3aed)';

            var msg = '';
            if (err.code === 1) {
                msg = '❌ Location permission DENIED.\n\nTo fix this:\n1. Click the 🔒 lock icon in your browser address bar\n2. Set Location to Allow\n3. Refresh the page and try again\n\nOR type your city name in the box below.';
            } else if (err.code === 2) {
                msg = '❌ GPS signal not available.\nPlease type your city name below.';
            } else {
                msg = '❌ GPS timed out.\nPlease type your city name below.';
            }
            st.innerText = msg;
        },
        {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 0
        }
    );
}
</script>
</body>
</html>
""", height=160)
