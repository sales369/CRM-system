import streamlit as st
import pandas as pd
from datetime import date, timedelta, datetime
import io
import hashlib
import random
import os
import base64
from database import DatabaseManager

# ── 1. CORE CONFIGURATION ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="ClientPulse CRM",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 2. LOGO LOADER UTILITY ─────────────────────────────────────────────────────
def get_logo_html(width="100px", margin_bottom="16px", centered=True):
    align = "margin: 0 auto;" if centered else "margin: 0;"
    try:
        if os.path.exists("logo.png"):
            with open("logo.png", "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
            return f'<img src="data:image/png;base64,{encoded}" style="width: {width}; height: auto; {align} margin-bottom: {margin_bottom}; display: block;">'
    except Exception:
        pass
    return f"""<div style="width: {width}; height: {width}; background: linear-gradient(135deg, #4f46e5, #9333ea); 
               border-radius: 25%; display: flex; align-items: center; justify-content: center; 
               font-size: calc(max(20px, {width}/2.5)); {align} margin-bottom: {margin_bottom}; 
               box-shadow: 0 8px 20px rgba(79, 70, 229, 0.25); color:white;">✨</div>"""

# ── 3. NEW "AURORA" LIVE BACKGROUND ENGINE ─────────────────────────────────────
def generate_live_background():
    html = '<div class="live-bg"><div class="bg-gradient"></div>'
    # 3 Large Organic Morphing Blobs
    html += '<div class="organic-blob blob-1"></div>'
    html += '<div class="organic-blob blob-2"></div>'
    html += '<div class="organic-blob blob-3"></div>'
    # Floating Light Specs
    for i in range(25):
        size = random.randint(3, 8)
        left = random.randint(0, 100)
        top = random.randint(0, 100)
        anim_duration = random.randint(20, 40)
        anim_delay = random.randint(0, 20)
        opacity = random.uniform(0.15, 0.5)
        html += f'<div class="light-spec" style="width:{size}px; height:{size}px; left:{left}vw; top:{top}vh; animation-duration:{anim_duration}s; animation-delay:-{anim_delay}s; opacity:{opacity};"></div>'
    html += '</div>'
    return html

st.markdown(generate_live_background(), unsafe_allow_html=True)

# ── 4. ENTERPRISE CSS ARCHITECTURE (WITH ANIMATIONS) ───────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

.stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6, 
.stApp span, .stApp label, .stApp input, .stApp button, .stApp div, .stApp td, .stApp th {
    font-family: 'Plus Jakarta Sans', sans-serif;
}
.material-icons, .material-symbols-rounded, [data-testid="stIconMaterial"], svg {
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
}

.stApp { background: transparent !important; }

/* ── NEW BACKGROUND CSS ── */
.live-bg { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -9999; overflow: hidden; pointer-events: none; background: #f8fafc; }
.bg-gradient { position: absolute; top: 0; left: 0; width: 200%; height: 200%; background: linear-gradient(120deg, #f0f9ff, #eef2ff, #fdf4ff, #e0f2fe); background-size: 50% 50%; animation: gradientFlow 30s ease infinite alternate; }
@keyframes gradientFlow { 0% { transform: translate(0, 0); } 100% { transform: translate(-20%, -20%); } }

.organic-blob { position: absolute; filter: blur(70px); opacity: 0.65; animation: morphBlob 25s infinite alternate cubic-bezier(0.4, 0, 0.2, 1); }
.blob-1 { width: 55vw; height: 55vw; top: -15vh; left: -15vw; background: #c7d2fe; animation-delay: 0s; }
.blob-2 { width: 60vw; height: 60vw; bottom: -25vh; right: -15vw; background: #fbcfe8; animation-delay: -5s; animation-direction: alternate-reverse; }
.blob-3 { width: 45vw; height: 45vw; top: 30vh; left: 35vw; background: #bae6fd; animation-delay: -10s; }

@keyframes morphBlob {
    0% { transform: translate(0, 0) scale(1) rotate(0deg); border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%; }
    50% { transform: translate(8vw, 12vh) scale(1.05) rotate(15deg); border-radius: 60% 40% 30% 70% / 60% 30% 70% 40%; }
    100% { transform: translate(-5vw, 5vh) scale(0.95) rotate(-10deg); border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%; }
}

.light-spec { position: absolute; background: #ffffff; border-radius: 50%; box-shadow: 0 0 12px rgba(255,255,255,0.9); animation-name: driftSpec; animation-timing-function: linear; animation-iteration-count: infinite; }
@keyframes driftSpec { 0% { transform: translateY(0) translateX(0) scale(0.8); opacity: 0; } 25% { opacity: 1; transform: scale(1); } 75% { opacity: 1; } 100% { transform: translateY(-25vh) translateX(30px) scale(0.5); opacity: 0; } }

/* WIDTH FIX & SLIDE ANIMATION */
.main .block-container { padding: 1.5rem 3rem !important; max-width: 100%; animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
@keyframes slideUpFade { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }

/* ALERT/MESSAGE SLIDE IN ANIMATION */
[data-testid="stAlert"], [data-testid="stException"] {
    animation: slideInRight 0.4s ease-out forwards;
}
@keyframes slideInRight {
    0% { opacity: 0; transform: translateX(30px); }
    100% { opacity: 1; transform: translateX(0); }
}

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(15,23,42,0.15); border-radius: 10px; }

.login-mode header, .login-mode [data-testid="stSidebar"], .login-mode footer { display: none !important; }
header { background: transparent !important; }

[data-testid="stSidebar"] { background: rgba(255, 255, 255, 0.6) !important; backdrop-filter: blur(30px); -webkit-backdrop-filter: blur(30px); border-right: 1px solid rgba(255,255,255,0.8) !important; box-shadow: 4px 0 24px rgba(15, 23, 42, 0.02); }
[data-testid="stSidebarNav"] { padding-top: 0 !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 4px; padding: 0 10px; }
[data-testid="stSidebar"] .stRadio label { background: transparent; border-radius: 10px; padding: 10px 16px !important; font-size: 0.95rem !important; font-weight: 600 !important; color: #475569 !important; transition: all 0.2s ease; cursor: pointer; border: 1px solid transparent; }
[data-testid="stSidebar"] .stRadio label:hover, [data-testid="stSidebar"] .stRadio label[data-checked="true"] { background: rgba(255,255,255,0.9) !important; color: #0f172a !important; transform: translateX(4px); box-shadow: 0 4px 12px rgba(15,23,42,0.03); border: 1px solid rgba(255,255,255,1); }
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] { display: flex; }

.page-title { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin: 0 0 2px; letter-spacing: -0.04em; }
.page-sub   { font-size: 1rem; color: #64748b; font-weight: 500; margin: 0 0 1.5rem; letter-spacing: 0.01em; }

/* DASHBOARD CARDS WITH BOUNCE IN */
.dash-card {
    height: 110px !important; background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.9); border-radius: 16px; padding: 16px 20px; position: relative; overflow: hidden;
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); margin: 0 !important; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03); display: flex; flex-direction: column; justify-content: center; z-index: 1;
    animation: bounceIn 0.6s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
}
@keyframes bounceIn { 0% { transform: scale(0.9); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }

[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card { transform: translateY(-6px) scale(1.02); background: rgba(255, 255, 255, 0.95); box-shadow: 0 12px 30px -5px rgba(15, 23, 42, 0.1), 0 0 15px rgba(255,255,255,0.6); border-color: #ffffff; }
.dash-card::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 4px; background: transparent; transition: background 0.4s ease; }
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card.indigo::after { background: linear-gradient(90deg, #6366f1, #818cf8); }
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card.blue::after   { background: linear-gradient(90deg, #0ea5e9, #38bdf8); }
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card.red::after    { background: linear-gradient(90deg, #ef4444, #f87171); }
.metric-icon { font-size: 1.6rem; margin-bottom: 4px; line-height: 1; text-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.metric-val  { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin: 0 0 2px; line-height: 1; letter-spacing: -0.03em; }
.metric-lbl  { font-size: 0.8rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin: 0; }

@keyframes pulseRed { 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); } }
.pulse-alert { animation: pulseRed 2s infinite; }

.form-section { background: rgba(255, 255, 255, 0.65); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px); border-radius: 16px; padding: 24px 30px; border: 1px solid rgba(255,255,255,0.9); box-shadow: 0 8px 30px rgba(15, 23, 42, 0.03); margin-bottom: 20px; }
.form-section h5 { color: #0f172a; font-weight: 800; margin-bottom: 16px; font-size: 1.1rem; letter-spacing: -0.02em;}

[data-baseweb="input"] > div, [data-baseweb="select"] > div, [data-baseweb="textarea"] > div { border-radius: 10px !important; background-color: rgba(255,255,255,0.7) !important; border: 1px solid rgba(15, 23, 42, 0.08) !important; transition: all 0.2s ease !important; }
[data-baseweb="input"] > div:hover, [data-baseweb="select"] > div:hover { border-color: rgba(15, 23, 42, 0.2) !important; background-color: #ffffff !important; }
[data-baseweb="input"] > div:focus-within, [data-baseweb="select"] > div:focus-within { border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important; background-color: #ffffff !important; }

/* BUTTON HOVER & CLICK ANIMATIONS */
.stButton > button { border-radius: 10px !important; font-weight: 700 !important; font-size: 0.95rem !important; padding: 0.5rem 1.4rem !important; transition: all 0.2s cubic-bezier(0.25, 0.8, 0.25, 1) !important; border: 1px solid rgba(15, 23, 42, 0.05) !important; background: rgba(255,255,255,0.9) !important; color: #1e293b !important; box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03) !important; }
.stButton > button:hover { background: #ffffff !important; transform: translateY(-2px) !important; box-shadow: 0 6px 15px rgba(15, 23, 42, 0.06) !important; border-color: rgba(15, 23, 42, 0.1) !important; }
.stButton > button:active { transform: scale(0.95) translateY(0) !important; box-shadow: 0 1px 3px rgba(15, 23, 42, 0.05) !important; }

.stButton > button[kind="primary"] { background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important; border: none !important; color: white !important; box-shadow: 0 6px 15px rgba(79, 70, 229, 0.25) !important; }
.stButton > button[kind="primary"]:hover { background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%) !important; box-shadow: 0 10px 20px rgba(79, 70, 229, 0.4) !important; transform: translateY(-2px) scale(1.02) !important; }
.stButton > button[kind="primary"]:active { transform: scale(0.95) !important; }

[data-baseweb="tab-list"] { gap: 30px; border-bottom: 2px solid rgba(15, 23, 42, 0.05) !important; padding-bottom: 4px; }
[data-baseweb="tab"] { font-weight: 700 !important; font-size: 1rem !important; color: #64748b !important; background: transparent !important; border: none !important; transition: color 0.2s ease; }
[aria-selected="true"] { color: #4f46e5 !important; border-bottom: 3px solid #4f46e5 !important; }

.streamlit-expanderHeader { font-weight: 700 !important; color: #0f172a !important; background: rgba(255,255,255,0.8) !important; border-radius: 12px !important; border: 1px solid rgba(255,255,255,1) !important; box-shadow: 0 2px 8px rgba(0,0,0,0.02); transition: all 0.2s ease; }
.streamlit-expanderHeader:hover { background: #ffffff !important; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
details { border: none !important; border-radius: 12px !important; background: transparent; overflow: hidden; margin-top: 10px; }

/* Client selector panel */
.client-selector-panel {
    background: rgba(255,255,255,0.75); backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,1); border-radius: 14px;
    padding: 18px 22px; margin-top: 12px;
    box-shadow: 0 4px 20px rgba(15,23,42,0.04);
}
.selector-label {
    font-size: 0.75rem; font-weight: 800; color: #6366f1;
    text-transform: uppercase; letter-spacing: 0.12em; margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  DATABASE & HELPERS
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def get_db():
    db = DatabaseManager()
    db.init_tables()
    db.init_user_tables()
    db.ensure_default_admin()
    return db

db = get_db()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def to_excel(df: pd.DataFrame) -> bytes:
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="Clients")
    return out.getvalue()

def status_label(row) -> str:
    nf_val = row.get("next_followup")
    if pd.isna(nf_val) or not nf_val: return "—"
    try:
        nf  = pd.to_datetime(nf_val)
        now = datetime.now()
        if nf < now:
            diff = now - nf
            if diff.days > 0: return f"🔴 Overdue ({diff.days}d)"
            hrs  = diff.seconds // 3600
            mins = (diff.seconds % 3600) // 60
            if hrs > 0: return f"🔴 Overdue ({hrs}h)"
            return f"🔴 Overdue ({mins}m)"
        else:
            diff = nf - now
            if diff.days > 0: return f"🟢 In {diff.days}d"
            hrs  = diff.seconds // 3600
            mins = (diff.seconds % 3600) // 60
            if hrs > 0: return f"🟡 Today (in {hrs}h)"
            return f"🟡 In {mins}m"
    except:
        return "—"

def highlight_rows(row):
    status = str(row['Status'])
    if '🔴' in status: return ['background-color: rgba(254, 226, 226, 0.7);'] * len(row)
    if '🟡' in status: return ['background-color: rgba(224, 242, 254, 0.7);'] * len(row)
    return [''] * len(row)

def change_user_password(user_id, new_password):
    try:
        db.update_user_password(user_id, hash_password(new_password))
        return True
    except Exception:
        return False


# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN PAGE
# ══════════════════════════════════════════════════════════════════════════════

def show_login():
    st.markdown("""
    <style>
    .main .block-container { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; padding: 0 !important; }
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(30px); -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 1) !important; border-radius: 24px; padding: 32px 40px !important;
        width: 100%; max-width: 400px; margin: 0 auto;
        box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.08), inset 0 0 0 1px rgba(255,255,255,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown(f"""
        <div style="text-align:center; margin-bottom:24px;">
            {get_logo_html(width="100px", margin_bottom="16px")}
            <div style="font-size: 1.5rem; font-weight: 800; color: #0f172a; margin-bottom: 2px;">ClientPulse CRM</div>
            <div style="font-size: 0.85rem; color: #64748b; font-weight: 500;">Please log in to your account</div>
        </div>
        """, unsafe_allow_html=True)

        username  = st.text_input("Username", placeholder="Enter your username")
        password  = st.text_input("Password", type="password", placeholder="Enter your password")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Log In ➜", use_container_width=True, type="primary")

        if submitted:
            if not username or not password:
                st.error("Please enter credentials.")
            else:
                user = db.authenticate_user(username, hash_password(password))
                if user:
                    st.session_state.logged_in = True
                    st.session_state.username  = user["username"]
                    st.session_state.role      = user["role"]
                    st.session_state.full_name = user["full_name"]
                    st.session_state.user_id   = user["id"]
                    
                    # Trigger login animation toast
                    st.session_state.toast_msg = f"Welcome back, {user['full_name']}!"
                    st.session_state.toast_icon = "👋"
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ══════════════════════════════════════════════════════════════════════════════

def show_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="padding: 16px 12px 24px; display: flex; align-items: center; gap: 12px;">
            {get_logo_html(width="54px", margin_bottom="0", centered=False)}
            <div>
                <div style="font-size: 1.2rem; font-weight: 800; color: #0f172a; letter-spacing: -0.02em; line-height: 1;">ClientPulse</div>
                <div style="font-size: 0.6rem; color: #6366f1; text-transform: uppercase; letter-spacing: 0.15em; font-weight: 800; margin-top: 4px;">CRM PLATFORM</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        role      = st.session_state.get("role", "user")
        full_name = st.session_state.get("full_name", "User")
        initials  = "".join(p[0].upper() for p in full_name.split()[:2])

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.9); border: 1px solid rgba(255,255,255,1); border-radius: 12px; padding: 12px 14px; margin: 0 12px 20px; display: flex; align-items: center; gap: 12px; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02);">
            <div style="width: 34px; height: 34px; border-radius: 8px; background: #e0e7ff; border: 1px solid #c7d2fe; display: flex; align-items: center; justify-content: center; font-size: 0.85rem; font-weight: 800; color: #4f46e5; flex-shrink: 0;">{initials}</div>
            <div style="overflow: hidden;">
                <div style="font-size: 0.85rem; font-weight: 800; color: #0f172a; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{full_name}</div>
                <div style="font-size: 0.65rem; color: #64748b; font-weight: 600; margin-top: 2px; text-transform:uppercase; letter-spacing:0.05em;">{'🛡️ Admin' if role == 'admin' else '👤 User'}</div>
            </div>
        </div>
        <div style="padding: 0 12px; font-size: 0.7rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 6px;">Menu</div>
        """, unsafe_allow_html=True)

        nav_options = ["🏠  Dashboard", "➕  Add Client", "⚙️  Settings"]
        page = st.radio("Navigation", nav_options, label_visibility="collapsed")

        st.markdown("<div style='height:1px;background:rgba(15, 23, 42, 0.06);margin:20px 12px 16px;'></div>", unsafe_allow_html=True)

        if st.button("🚪  Sign Out", use_container_width=True):
            for k in ["logged_in","username","role","full_name","user_id"]:
                st.session_state.pop(k, None)
            st.rerun()

    return page


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD & CLIENT DIRECTORY
# ══════════════════════════════════════════════════════════════════════════════

def page_dashboard():
    st.markdown('<p class="page-title">Dashboard</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-sub">Welcome back, {st.session_state.get("full_name","User")}. Use the filters below to manage your workflow.</p>', unsafe_allow_html=True)

    total    = db.get_total_clients()
    today_df = db.get_todays_followups()
    over_df  = db.get_overdue_followups()

    # ── METRIC TILES ──
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="dash-card indigo"><div class="metric-icon">👥</div><p class="metric-val">{total}</p><p class="metric-lbl">Total Clients</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="dash-card blue"><div class="metric-icon">⚡</div><p class="metric-val">{len(today_df)}</p><p class="metric-lbl">Due Today</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="dash-card red pulse-alert"><div class="metric-icon">⚠️</div><p class="metric-val">{len(over_df)}</p><p class="metric-lbl">Overdue Tasks</p></div>', unsafe_allow_html=True)

    st.markdown("<hr style='margin: 25px 0 15px 0; border-top: 1px solid rgba(15,23,42,0.06);'>", unsafe_allow_html=True)

    # ── DIRECTORY HEADER + FILTERS ──
    st.markdown("<h5 style='color:#0f172a; font-weight:800; margin-bottom:12px;'>👥 Client Directory</h5>", unsafe_allow_html=True)

    fc1, fc2, fc3, fc4, fc5 = st.columns([2, 1.5, 1.5, 1.5, 1])
    with fc1: search        = st.text_input("🔍", placeholder="Search by name, company…", label_visibility="collapsed")
    with fc2: status_filter = st.selectbox("Status", ["All","Due Today","Overdue","Upcoming"], label_visibility="collapsed")
    with fc3: cat           = st.selectbox("Category", ["All Categories","Lead","Prospect","Active Client","Partner","VIP","Churned"], label_visibility="collapsed")
    with fc4: srt           = st.selectbox("Sort By", ["Next Follow-up","Name","Company","Deal Value"], label_visibility="collapsed")

    clean_cat = None if cat == "All Categories" else cat
    df = db.get_all_clients(search=search or None, category=clean_cat, sort_by=srt)

    if df.empty:
        st.info("📭 Database is currently empty.")
        return

    df["Status"] = df.apply(status_label, axis=1)

    if status_filter == "Due Today":
        df = df[df["Status"].str.contains("🟡", na=False)]
    elif status_filter == "Overdue":
        df = df[df["Status"].str.contains("🔴", na=False)]
    elif status_filter == "Upcoming":
        df = df[df["Status"].str.contains("🟢", na=False)]

    with fc5:
        st.download_button("📥 Export", data=to_excel(df) if not df.empty else b"", file_name="Export.xlsx", use_container_width=True)

    if df.empty:
        st.info("📭 No clients match the current filters.")
        return

    # ── BULK DELETE & INTERACTIVE TABLE BUILDER ──
    df_display = df.copy()
    
    # Insert a boolean "Select" column at the very front
    df_display.insert(0, "Select", False)
    
    df_display["Deal Value"]  = df_display["deal_value"].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "—")
    df_display["Next Contact"] = pd.to_datetime(df_display["next_followup"]).dt.strftime('%b %d, %I:%M %p')
    df_display["Discussion"] = df_display.get("discussion", pd.Series([""] * len(df_display))).fillna("").apply(
        lambda x: (str(x)[:45] + "…") if len(str(x)) > 45 else str(x)
    )

    show_cols  = ["Select", "name", "company", "phone", "email", "category", "Next Contact", "Status", "Deal Value", "Discussion"]
    rename_map = {"name": "Full Name", "company": "Company", "phone": "Phone", "email": "Email", "category": "Category"}

    styled_df = df_display[show_cols].rename(columns=rename_map).style.apply(highlight_rows, axis=1)
    
    # Disable editing for everything EXCEPT the "Select" column
    disabled_cols = ["Full Name", "Company", "Phone", "Email", "Category", "Next Contact", "Status", "Deal Value", "Discussion"]
    
    edited_df = st.data_editor(
        styled_df,
        column_config={
            "Select": st.column_config.CheckboxColumn("☑", help="Select client(s)", default=False)
        },
        disabled=disabled_cols,
        use_container_width=True, 
        height=650, 
        hide_index=True
    )

    # Grab the index numbers of all rows that the user checked
    selected_indices = edited_df.index[edited_df['Select'] == True].tolist()

    # If ANY checkboxes are checked, show the Bulk Delete option
    if len(selected_indices) > 0:
        st.markdown(f"""
        <div style="padding: 12px 16px; background: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444; border-radius: 4px; margin: 10px 0; animation: slideInRight 0.3s ease-out forwards;">
            <strong style="color: #ef4444;">⚠️ Bulk Action:</strong> {len(selected_indices)} client(s) selected for deletion.
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"🗑️ Delete {len(selected_indices)} Selected Client(s)", type="primary"):
            ids_to_delete = df.iloc[selected_indices]['id'].tolist()
            db.delete_multiple_clients(ids_to_delete)
            
            # Fire animation and success state
            st.session_state.toast_msg = f"Successfully deleted {len(selected_indices)} client(s)."
            st.session_state.toast_icon = "🗑️"
            st.rerun()

    st.markdown("<hr style='margin: 30px 0; border-top: 1px solid rgba(15,23,42,0.06);'>", unsafe_allow_html=True)

    # ════════════════════════════════════════════════════════════
    #  DYNAMIC EDIT PANEL (Depends on Checkbox selection)
    # ════════════════════════════════════════════════════════════

    if len(selected_indices) == 1:
        target_row  = df.iloc[selected_indices[0]]
        cid         = int(target_row["id"])
        client_name = target_row["name"]

        st.markdown(f"""
        <div style="margin-top:10px; padding:10px 18px; background:rgba(99,102,241,0.07); border-left:4px solid #6366f1;
                    border-radius:0 10px 10px 0; font-size:0.9rem; font-weight:700; color:#4f46e5; animation: slideInRight 0.3s ease-out forwards;">
            Selected for Editing: {client_name}
        </div>
        """, unsafe_allow_html=True)

        with st.expander(f"✏️ Manage  ·  {client_name}", expanded=True):
            t1, t2 = st.tabs(["🕒 Reschedule", "📝 Edit Details"]) 

            with t1:
                st.markdown("<br>", unsafe_allow_html=True)
                sc1, sc2, sc3 = st.columns([2, 2, 1.5])
                try:
                    curr_dt = pd.to_datetime(target_row["next_followup"])
                except Exception:
                    curr_dt = datetime.now() + timedelta(hours=4)

                with sc1:
                    new_d = st.date_input("New Date", value=curr_dt.date(), key=f"resched_d_{cid}")
                with sc2:
                    # ── USING STREAMLIT TIME WIDGET ──
                    parsed_time = st.time_input("New Time", value=curr_dt.time(), key=f"resched_t_{cid}")
                with sc3:
                    st.markdown("<br style='line-height:2.3'>", unsafe_allow_html=True)
                    if st.button("✅ Update Timing", type="primary", use_container_width=True, key=f"btn_resched_{cid}"):
                        new_dt = datetime.combine(new_d, parsed_time)
                        db.update_followup(cid, new_dt.strftime("%Y-%m-%d %H:%M:%S"))
                        
                        st.session_state.toast_msg = f"Rescheduled {client_name} to {new_dt.strftime('%b %d')}"
                        st.session_state.toast_icon = "🕒"
                        st.rerun()

            with t2:
                st.markdown("<br>", unsafe_allow_html=True)
                with st.form(key=f"edit_form_{cid}"):
                    ec1, ec2 = st.columns(2)
                    with ec1:
                        e_name  = st.text_input("Full Name",     value=target_row["name"])
                        e_email = st.text_input("Email",         value=target_row.get("email", "") or "")
                        e_val   = st.number_input("Deal Value ($)", value=int(target_row["deal_value"]) if pd.notna(target_row.get("deal_value")) else 0, step=1000)
                    with ec2:
                        e_phone   = st.text_input("Phone",   value=target_row.get("phone", "") or "")
                        e_company = st.text_input("Company", value=target_row.get("company", "") or "")
                        cat_opts  = ["Lead","Prospect","Active Client","Partner","VIP","Churned"]
                        curr_cat  = target_row.get("category", "Lead")
                        e_cat     = st.selectbox("Category", cat_opts, index=cat_opts.index(curr_cat) if curr_cat in cat_opts else 0)

                    e_discussion = st.text_area(
                        "💬 Discussion",
                        value=target_row.get("discussion", "") or "",
                        height=110,
                        placeholder="What was discussed with this client — products, pricing, requirements…"
                    )

                    if st.form_submit_button("💾 Save Details", type="primary", use_container_width=True):
                        try:
                            # Direct database update for the form inputs
                            update_sql = """
                            UPDATE clients 
                            SET name=%(name)s, email=%(email)s, phone=%(phone)s, company=%(company)s, 
                                deal_value=%(deal_value)s, category=%(category)s, discussion=%(discussion)s 
                            WHERE id=%(cid)s
                            """
                            with db._connect() as conn:
                                with conn.cursor() as cur:
                                    cur.execute(update_sql, {
                                        "name": e_name, "email": e_email, "phone": e_phone, "company": e_company, 
                                        "deal_value": e_val, "category": e_cat, "discussion": e_discussion, "cid": cid
                                    })
                                conn.commit()
                            
                            st.session_state.toast_msg = f"{client_name}'s details saved!"
                            st.session_state.toast_icon = "💾"
                            st.rerun()
                        except Exception as e:
                            st.error(f"Database error: {e}")

    elif len(selected_indices) > 1:
        st.info("ℹ️ Multiple clients selected. Please check only one box to edit details or reschedule.")
    else:
        st.info("👆 Check the box next to a single client in the table above to edit their details or reschedule.")


# ══════════════════════════════════════════════════════════════════════════════
#  ADD CLIENT
# ══════════════════════════════════════════════════════════════════════════════

def page_add_client():
    st.markdown('<p class="page-title">Add New Client</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Enter client details and schedule their follow-up.</p>', unsafe_allow_html=True)

    # ── PERSISTENT SUCCESS MESSAGE ──
    if "client_added_success" in st.session_state:
        st.success(st.session_state.client_added_success)
        del st.session_state.client_added_success 

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("##### 👤 Client Information")
    c1, c2 = st.columns(2)
    with c1:
        name    = st.text_input("Full Name *",    key="ac_name", placeholder="e.g. Jane Doe")
        email   = st.text_input("Email Address",  key="ac_email", placeholder="e.g. jane@company.com")
        company = st.text_input("Company Name",   key="ac_comp", placeholder="e.g. Acme Corp")
    with c2:
        phone    = st.text_input("Phone Number", key="ac_phone", placeholder="+1 555-0199")
        category = st.selectbox("Category", ["Lead","Prospect","Active Client","Partner","VIP","Churned"], key="ac_cat")
        source   = st.selectbox("Lead Source", ["Referral","Website","LinkedIn","Cold Outreach","Event","Existing","Other"], key="ac_src")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("##### 📅 Pipeline Scheduling")
    c3, c4 = st.columns(2)

    with c3:
        st.markdown("<div style='font-size:0.85rem; font-weight:600; color:#475569; margin-bottom:8px;'>Next Contact Schedule</div>", unsafe_allow_html=True)
        next_d = st.date_input("Date", value=date.today(), label_visibility="collapsed", key="ac_date")
        
        if "ac_time" not in st.session_state:
            st.session_state.ac_time = (datetime.now() + timedelta(hours=4)).time()
        
        parsed_t = st.time_input("Time", key="ac_time")
        deal_value = st.number_input("Deal Value ($)", min_value=0, value=0, step=5000, key="ac_deal")

    with c4:
        nf_preview  = datetime.combine(next_d, parsed_t)
        date_str    = nf_preview.strftime("%A, %b %d")
        time_str    = nf_preview.strftime("%I:%M %p") 

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.7); border:1px solid rgba(255,255,255,1); border-radius:12px; padding:16px; text-align:center; box-shadow: 0 2px 10px rgba(0,0,0,0.02);">
            <p style="font-size:0.75rem; font-weight:800; color:#6366f1; text-transform:uppercase; letter-spacing:0.1em; margin:0;">Target Execution</p>
            <p style="font-size:1.3rem; font-weight:800; color:#0f172a; margin:4px 0;">{date_str}</p>
            <p style="font-size:1.1rem; color:#4f46e5; font-weight:700; margin:0;">@ {time_str}</p>
        </div>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("##### 💬 Discussion & Notes")
    dn1, dn2 = st.columns(2)
    with dn1:
        discussion = st.text_area(
            "Discussion Topics",
            placeholder="What topics were discussed? Products, requirements, pricing, concerns…",
            height=110,
            key="ac_disc"
        )
    with dn2:
        notes = st.text_area(
            "Additional Notes",
            placeholder="Internal notes, next steps, special requirements…",
            height=110,
            key="ac_notes"
        )
    st.markdown('</div>', unsafe_allow_html=True)

    submitted = st.button("💾 Save Client", type="primary", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("❌ Full Name is required.")
        else:
            nf_datetime = datetime.combine(next_d, parsed_t)
            f_days      = max((nf_datetime.date() - date.today()).days, 0)
            nf_str      = nf_datetime.strftime("%Y-%m-%d %H:%M:%S")
            now_str     = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            ok = db.add_client({
                "name": name, "email": email, "phone": phone, "company": company,
                "category": category, "source": source,
                "last_contacted": now_str, "followup_days": f_days,
                "next_followup": nf_str, "deal_value": deal_value,
                "notes": notes, "discussion": discussion,
                "created_by": st.session_state.get("user_id", 1)
            })
            
            if ok:
                st.session_state.client_added_success = f"✅ **{name}** added successfully! Scheduled for **{nf_datetime.strftime('%b %d @ %I:%M %p')}**."
                st.session_state.toast_msg = "New client added to pipeline!"
                st.session_state.toast_icon = "🎉"
                st.session_state.show_balloons = True
                
                # Manually clear the form inputs
                keys_to_clear = ["ac_name", "ac_email", "ac_comp", "ac_phone", "ac_cat", "ac_src", "ac_date", "ac_time", "ac_deal", "ac_disc", "ac_notes"]
                for k in keys_to_clear:
                    if k in st.session_state:
                        del st.session_state[k]
                
                st.rerun()
            else:
                st.error("❌ Database error.")


# ══════════════════════════════════════════════════════════════════════════════
#  SETTINGS / ACCESS CONTROL
# ══════════════════════════════════════════════════════════════════════════════

def page_settings():
    st.markdown('<p class="page-title">Settings</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Manage your account and workspace preferences.</p>', unsafe_allow_html=True)

    is_admin        = st.session_state.get("role") == "admin"
    current_user_id = st.session_state.get("user_id")

    tabs = st.tabs(["👥 Active Users", "➕ Add User", "🔑 Change Password"]) if is_admin else st.tabs(["🔑 Change Password"])

    if is_admin:
        with tabs[0]:
            st.markdown("<br>", unsafe_allow_html=True)
            users = db.get_all_users()
            if users.empty:
                st.info("No active users found.")
            else:
                for _, u in users.iterrows():
                    role_badge   = "🛡️ Admin" if u["role"] == "admin" else "👤 User"
                    status_badge = "🟢 Active" if u["is_active"] else "🔴 Suspended"
                    c1, c2, c3  = st.columns([4, 1.5, 1.5])
                    with c1:
                        st.markdown(f"""
                        <div style="background: rgba(255,255,255,0.7); backdrop-filter: blur(10px); padding: 12px 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,1); box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                            <div style="font-size: 1rem; font-weight: 800; color: #0f172a; margin-bottom: 2px;">{u['full_name']} <span style="color: #64748b; font-weight: 500; font-size: 0.8rem;">(@{u['username']})</span></div>
                            <div style="font-size: 0.75rem; font-weight: 600; color: #475569;">{role_badge} &nbsp;|&nbsp; {status_badge}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with c2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if u["username"] != st.session_state.get("username"):
                            if st.button("Suspend" if u["is_active"] else "Activate", key=f"tog_{u['id']}", use_container_width=True):
                                db.toggle_user_status(int(u["id"]))
                                st.session_state.toast_msg = f"User status updated."
                                st.session_state.toast_icon = "⚙️"
                                st.rerun()
                        else:
                            st.markdown("<div style='text-align:center; margin-top:10px; font-weight:700; color:#10b981; font-size:0.8rem;'>Current User</div>", unsafe_allow_html=True)
                    with c3:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if u["username"] != st.session_state.get("username"):
                            if st.button("Delete", key=f"del_{u['id']}", use_container_width=True):
                                db.delete_user(int(u["id"]))
                                st.session_state.toast_msg = f"User deleted."
                                st.session_state.toast_icon = "🗑️"
                                st.rerun()
                    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

        with tabs[1]:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.markdown("##### Add New User")
            with st.form("add_user_form", clear_on_submit=True):
                new_fullname = st.text_input("Full Name *",  placeholder="e.g. Alex Smith")
                new_username = st.text_input("Username *",   placeholder="e.g. alex.smith")
                new_password = st.text_input("Password *",   type="password", placeholder="Min 6 characters")
                new_role     = st.selectbox("Role", ["user","admin"])
                st.markdown("<br>", unsafe_allow_html=True)
                add_submitted = st.form_submit_button("➕ Create User", type="primary", use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

            if add_submitted:
                if not new_fullname.strip() or not new_username.strip() or not new_password:
                    st.error("❌ Missing required fields.")
                elif len(new_password) < 6:
                    st.error("❌ Password too short (minimum 6 characters).")
                elif db.username_exists(new_username):
                    st.error("❌ Username already taken.")
                else:
                    db.add_user({"full_name": new_fullname, "username": new_username, "email": "",
                                 "password_hash": hash_password(new_password), "role": new_role})
                    st.session_state.toast_msg = f"User {new_fullname} created!"
                    st.session_state.toast_icon = "🛡️"
                    st.rerun()

    pwd_tab = tabs[2] if is_admin else tabs[0]
    with pwd_tab:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### Security: Update Password")
        with st.form("change_password_form", clear_on_submit=True):
            old_p  = st.text_input("Current Password *", type="password")
            new_p  = st.text_input("New Password *",     type="password", placeholder="Min 6 characters")
            new_p2 = st.text_input("Confirm New Password *", type="password")
            st.markdown("<br>", unsafe_allow_html=True)
            pwd_submitted = st.form_submit_button("Update Password", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if pwd_submitted:
            if not old_p or not new_p or not new_p2:
                st.error("❌ Please fill out all fields.")
            elif new_p != new_p2:
                st.error("❌ New passwords do not match.")
            elif len(new_p) < 6:
                st.error("❌ New password must be at least 6 characters.")
            else:
                if not db.authenticate_user(st.session_state.username, hash_password(old_p)):
                    st.error("❌ Incorrect current password.")
                else:
                    if change_user_password(current_user_id, new_p):
                        st.session_state.toast_msg = "Password updated securely."
                        st.session_state.toast_icon = "🔒"
                        st.rerun()
                    else:
                        st.error("❌ System Error: Failed to update password.")


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN ROUTER WITH GLOBAL NOTIFICATION ENGINE
# ══════════════════════════════════════════════════════════════════════════════

if not st.session_state.get("logged_in"):
    show_login()
else:
    # ── THE GLOBAL NOTIFICATION ENGINE ──
    if "show_balloons" in st.session_state:
        st.balloons()
        del st.session_state.show_balloons

    if "toast_msg" in st.session_state:
        st.toast(st.session_state.toast_msg, icon=st.session_state.get("toast_icon", "✅"))
        del st.session_state.toast_msg
        if "toast_icon" in st.session_state:
            del st.session_state.toast_icon

    page = show_sidebar()
    if   "Dashboard"  in page: page_dashboard()
    elif "Add Client" in page: page_add_client()
    elif "Settings"   in page: page_settings()
