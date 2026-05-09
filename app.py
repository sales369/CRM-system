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
    """Loads logo.png if it exists, otherwise falls back to a default CSS icon."""
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

# ── 3. LIVE BACKGROUND ENGINE ──────────────────────────────────────────────────
def generate_particles():
    html = '<div class="mesh-engine"><div class="gradient-bg"></div>'
    html += '<div class="orb orb-1"></div><div class="orb orb-2"></div><div class="orb orb-3"></div>'
    for i in range(35):
        size = random.randint(4, 9)
        left = random.randint(0, 100)
        anim_duration = random.randint(15, 35)
        anim_delay = random.randint(0, 20)
        opacity = random.uniform(0.2, 0.6)
        html += f'<div class="particle" style="width:{size}px; height:{size}px; left:{left}vw; animation-duration:{anim_duration}s; animation-delay:-{anim_delay}s; opacity:{opacity};"></div>'
    html += '</div>'
    return html

st.markdown(generate_particles(), unsafe_allow_html=True)


# ── 4. ENTERPRISE CSS ARCHITECTURE ─────────────────────────────────────────────
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

/* ── LIVE THEME BACKGROUND ── */
.stApp { background: transparent !important; }
.mesh-engine { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; z-index: -9999; overflow: hidden; pointer-events: none; background: #f8fafc; }
.gradient-bg { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(-45deg, #f0f9ff, #eef2ff, #fdf4ff, #e0f2fe); background-size: 400% 400%; animation: liveThemeShift 20s ease infinite alternate; }
@keyframes liveThemeShift { 0% { background-position: 0% 50%; filter: hue-rotate(0deg); } 50% { background-position: 100% 50%; filter: hue-rotate(15deg); } 100% { background-position: 0% 50%; filter: hue-rotate(30deg); } }

.orb { position: absolute; border-radius: 50%; filter: blur(90px); opacity: 0.6; animation: auraFloat 25s infinite alternate ease-in-out; }
.orb-1 { width: 45vw; height: 45vw; top: -10vw; left: -10vw; background: #c7d2fe; }
.orb-2 { width: 40vw; height: 40vw; bottom: -5vw; right: -5vw; background: #fbcfe8; animation-delay: -5s; }
.orb-3 { width: 35vw; height: 35vw; top: 30vh; left: 40vw; background: #bae6fd; animation-delay: -10s; }
@keyframes auraFloat { 0% { transform: translate(0,0) scale(1); } 100% { transform: translate(60px,-60px) scale(1.1); } }

.particle { position: absolute; bottom: -10px; background: rgba(99, 102, 241, 0.4); border-radius: 50%; animation-name: floatUp; animation-timing-function: linear; animation-iteration-count: infinite; }
@keyframes floatUp { 0% { transform: translateY(0) translateX(0); opacity: 0; } 10% { opacity: 1; } 90% { opacity: 1; } 100% { transform: translateY(-100vh) translateX(20px); opacity: 0; } }

/* ── COMPACT LAYOUT (NO SCROLLING) ── */
.main .block-container { padding: 1.5rem 3rem !important; max-width: 1440px; animation: slideUpFade 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
@keyframes slideUpFade { 0% { opacity: 0; transform: translateY(15px); } 100% { opacity: 1; transform: translateY(0); } }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(15,23,42,0.15); border-radius: 10px; }

/* ── HIDE CHROME ON LOGIN ── */
.login-mode header, .login-mode [data-testid="stSidebar"], .login-mode footer { display: none !important; }
header { background: transparent !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] { background: rgba(255, 255, 255, 0.6) !important; backdrop-filter: blur(30px); -webkit-backdrop-filter: blur(30px); border-right: 1px solid rgba(255,255,255,0.8) !important; box-shadow: 4px 0 24px rgba(15, 23, 42, 0.02); }
[data-testid="stSidebarNav"] { padding-top: 0 !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 4px; padding: 0 10px; }
[data-testid="stSidebar"] .stRadio label { background: transparent; border-radius: 10px; padding: 10px 16px !important; font-size: 0.95rem !important; font-weight: 600 !important; color: #475569 !important; transition: all 0.2s ease; cursor: pointer; border: 1px solid transparent; }
[data-testid="stSidebar"] .stRadio label:hover, [data-testid="stSidebar"] .stRadio label[data-checked="true"] { background: rgba(255,255,255,0.9) !important; color: #0f172a !important; transform: translateX(4px); box-shadow: 0 4px 12px rgba(15,23,42,0.03); border: 1px solid rgba(255,255,255,1); }
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] { display: flex; }

/* ── TYPOGRAPHY ── */
.page-title { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin: 0 0 2px; letter-spacing: -0.04em; }
.page-sub   { font-size: 1rem; color: #64748b; font-weight: 500; margin: 0 0 1.5rem; letter-spacing: 0.01em; }


/* ══════════════════════════════════════════════════════════════════════════
   🚀 BULLETPROOF DASHBOARD TILE ENGINE
   ══════════════════════════════════════════════════════════════════════════ */
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] { position: relative !important; }

.dash-card {
    height: 110px !important; background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.9); border-radius: 16px; padding: 16px 20px; position: relative; overflow: hidden;
    transition: all 0.3s ease; margin: 0 !important; box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03); display: flex; flex-direction: column; justify-content: center; z-index: 1;
}

[data-testid="stHorizontalBlock"]:first-of-type [data-testid="stButton"] { position: absolute !important; top: 0 !important; left: 0 !important; width: 100% !important; height: 100% !important; margin: 0 !important; padding: 0 !important; z-index: 10 !important; }
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="stButton"] button { width: 100% !important; height: 100% !important; opacity: 0 !important; cursor: pointer !important; background: transparent !important; border: none !important; box-shadow: none !important; color: transparent !important; }
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card { transform: translateY(-4px); background: rgba(255, 255, 255, 0.95); box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08), 0 0 15px rgba(255,255,255,0.6); border-color: #ffffff; }

.dash-card::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 4px; background: transparent; transition: background 0.3s ease; }
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card.indigo::after { background: linear-gradient(90deg, #6366f1, #818cf8); }
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card.blue::after   { background: linear-gradient(90deg, #0ea5e9, #38bdf8); }
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card.red::after    { background: linear-gradient(90deg, #ef4444, #f87171); }
[data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card.purple::after { background: linear-gradient(90deg, #8b5cf6, #c084fc); }

.metric-icon { font-size: 1.6rem; margin-bottom: 4px; line-height: 1; text-shadow: 0 2px 8px rgba(0,0,0,0.06); }
.metric-val  { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin: 0 0 2px; line-height: 1; letter-spacing: -0.03em; }
.metric-lbl  { font-size: 0.8rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin: 0; }

@keyframes pulseRed { 0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); } 70% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); } 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); } }
.pulse-alert { animation: pulseRed 2s infinite; }

/* ── FORMS & CONTAINERS ── */
.form-section {
    background: rgba(255, 255, 255, 0.65); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    border-radius: 16px; padding: 24px 30px; border: 1px solid rgba(255,255,255,0.9);
    box-shadow: 0 8px 30px rgba(15, 23, 42, 0.03); margin-bottom: 20px;
}
.form-section h5 { color: #0f172a; font-weight: 800; margin-bottom: 16px; font-size: 1.1rem; letter-spacing: -0.02em;}

[data-baseweb="input"] > div, [data-baseweb="select"] > div, [data-baseweb="textarea"] > div {
    border-radius: 10px !important; background-color: rgba(255,255,255,0.7) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important; transition: all 0.2s ease !important;
}
[data-baseweb="input"] > div:hover, [data-baseweb="select"] > div:hover { border-color: rgba(15, 23, 42, 0.2) !important; background-color: #ffffff !important; }
[data-baseweb="input"] > div:focus-within, [data-baseweb="select"] > div:focus-within { border-color: #6366f1 !important; box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important; background-color: #ffffff !important; }

/* ── BUTTONS ── */
.stButton > button {
    border-radius: 10px !important; font-weight: 700 !important; font-size: 0.95rem !important;
    padding: 0.5rem 1.4rem !important; transition: all 0.2s ease !important;
    border: 1px solid rgba(15, 23, 42, 0.05) !important; background: rgba(255,255,255,0.9) !important; color: #1e293b !important;
    box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03) !important;
}
.stButton > button:hover { background: #ffffff !important; transform: translateY(-2px) !important; box-shadow: 0 6px 15px rgba(15, 23, 42, 0.06) !important; border-color: rgba(15, 23, 42, 0.1) !important; }
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important; border: none !important;
    color: white !important; box-shadow: 0 6px 15px rgba(79, 70, 229, 0.25) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%) !important; box-shadow: 0 10px 20px rgba(79, 70, 229, 0.4) !important; transform: translateY(-2px) scale(1.02) !important;
}

/* ── LIST STRIPS ── */
.strip { 
    background: rgba(255, 255, 255, 0.85); backdrop-filter: blur(16px); border-radius: 16px; padding: 16px 24px; margin-bottom: 12px; 
    border: 1px solid rgba(255,255,255,1); border-left-width: 5px; display: flex; flex-direction: column; gap: 6px; transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02);
}
.strip:hover { transform: translateX(6px); background: #ffffff; box-shadow: 0 8px 25px rgba(15, 23, 42, 0.05); }
.strip-today { border-left-color: #3b82f6; }
.strip-overdue { border-left-color: #ef4444; }
.strip-ok { border-left-color: #10b981; align-items: center; text-align: center; }

.strip-header { display: flex; justify-content: space-between; align-items: center; }
.strip-title { font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0; }
.strip-badge { font-size: 0.7rem; font-weight: 800; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em;}
.badge-blue { background: rgba(56, 189, 248, 0.15); color: #0284c7; border: 1px solid rgba(56, 189, 248, 0.3); }
.badge-red { background: rgba(248, 113, 113, 0.15); color: #b91c1c; border: 1px solid rgba(248, 113, 113, 0.3); }
.strip-meta { display: flex; gap: 16px; font-size: 0.85rem; color: #475569; font-weight: 600; margin: 0; }

/* ── TABS ── */
[data-baseweb="tab-list"] { gap: 30px; border-bottom: 2px solid rgba(15, 23, 42, 0.05) !important; padding-bottom: 4px; }
[data-baseweb="tab"] { font-weight: 700 !important; font-size: 1rem !important; color: #64748b !important; background: transparent !important; border: none !important; transition: color 0.2s ease; }
[aria-selected="true"] { color: #4f46e5 !important; border-bottom: 3px solid #4f46e5 !important; }
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

def hash_password(password: str) -> str: return hashlib.sha256(password.encode()).hexdigest()
def to_excel(df: pd.DataFrame) -> bytes:
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w: df.to_excel(w, index=False, sheet_name="Clients")
    return out.getvalue()

def status_label(row) -> str:
    """Calculates status dynamically up to the minute to support precise Time pickers"""
    nf_val = row.get("next_followup")
    if pd.isna(nf_val) or not nf_val: return "—"
    try:
        nf = pd.to_datetime(nf_val)
        now = datetime.now()
        if nf < now:
            diff = now - nf
            if diff.days > 0: return f"🔴 Overdue ({diff.days}d)"
            hrs = diff.seconds // 3600
            mins = (diff.seconds % 3600) // 60
            if hrs > 0: return f"🔴 Overdue ({hrs}h)"
            return f"🔴 Overdue ({mins}m)"
        else:
            diff = nf - now
            if diff.days > 0: return f"🟢 In {diff.days}d"
            hrs = diff.seconds // 3600
            mins = (diff.seconds % 3600) // 60
            if hrs > 0: return f"🟡 Today (in {hrs}h)"
            return f"🟡 In {mins}m"
    except:
        return "—"

def change_user_password(user_id, new_password):
    try:
        new_hash = hash_password(new_password)
        db.c.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_hash, user_id))
        db.conn.commit()
        return True
    except Exception as e:
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
        border: 1px solid rgba(255, 255, 255, 1) !important; border-radius: 24px; padding: 32px 40px !important; width: 100%; max-width: 400px; margin: 0 auto;
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

        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Log In ➜", use_container_width=True, type="primary")

        if submitted:
            if not username or not password: st.error("Please enter credentials.")
            else:
                user = db.authenticate_user(username, hash_password(password))
                if user:
                    st.session_state.logged_in  = True
                    st.session_state.username   = user["username"]
                    st.session_state.role       = user["role"]
                    st.session_state.full_name  = user["full_name"]
                    st.session_state.user_id    = user["id"]
                    st.rerun()
                else: st.error("❌ Invalid username or password.")


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

        role = st.session_state.get("role", "user")
        full_name = st.session_state.get("full_name", "User")
        initials = "".join(p[0].upper() for p in full_name.split()[:2])

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

        nav_options = ["🏠  Dashboard", "➕  Add Client", "👥  Client Directory", "⚙️  Settings"]
        page = st.radio("Navigation", nav_options, label_visibility="collapsed")
        
        st.markdown("<div style='height:1px;background:rgba(15, 23, 42, 0.06);margin:20px 12px 16px;'></div>", unsafe_allow_html=True)
        
        if st.button("🚪  Sign Out", use_container_width=True):
            for k in ["logged_in","username","role","full_name","user_id","dash_view"]: st.session_state.pop(k, None)
            st.rerun()

    return page


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def page_dashboard():
    st.markdown('<p class="page-title">Dashboard</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-sub">Welcome back, {st.session_state.get("full_name","User")}. Here is your overview.</p>', unsafe_allow_html=True)

    total = db.get_total_clients()
    today_df  = db.get_todays_followups()
    over_df   = db.get_overdue_followups()

    if "dash_view" not in st.session_state: st.session_state.dash_view = "today"

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f'<div class="dash-card indigo"><div class="metric-icon">👥</div><p class="metric-val">{total}</p><p class="metric-lbl">Total Clients</p></div>', unsafe_allow_html=True)
        if st.button("\u200B", key="t_tot", use_container_width=True): st.session_state.dash_view = "total"

    with c2:
        st.markdown(f'<div class="dash-card blue"><div class="metric-icon">⚡</div><p class="metric-val">{len(today_df)}</p><p class="metric-lbl">Due Today</p></div>', unsafe_allow_html=True)
        if st.button("\u200B\u200B", key="t_tod", use_container_width=True): st.session_state.dash_view = "today"

    with c3:
        st.markdown(f'<div class="dash-card red pulse-alert"><div class="metric-icon">⚠️</div><p class="metric-val">{len(over_df)}</p><p class="metric-lbl">Overdue Tasks</p></div>', unsafe_allow_html=True)
        if st.button("\u200B\u200B\u200B", key="t_ovr", use_container_width=True): st.session_state.dash_view = "overdue"


    st.markdown("<hr style='margin: 15px 0 15px 0; border-top: 1px solid rgba(15,23,42,0.06);'>", unsafe_allow_html=True)

    view = st.session_state.dash_view

    if view == "today":
        st.markdown("<h5 style='color:#0f172a; font-weight:800; margin-bottom:12px;'>⚡ Due Today</h5>", unsafe_allow_html=True)
        if today_df.empty: st.markdown('<div class="strip strip-ok"><div style="font-size:1.5rem;margin-bottom:2px;opacity:0.9;">☕</div><p class="strip-title">All caught up</p><p class="strip-meta">No tasks due today.</p></div>', unsafe_allow_html=True)
        else:
            for _, r in today_df.iterrows():
                time_str = pd.to_datetime(r['next_followup']).strftime('%I:%M %p')
                st.markdown(f"""
                <div class="strip strip-today">
                    <div class="strip-header"><p class="strip-title">{r['name']} <span style="color:#64748b; font-weight:500;">· {r['company']}</span></p><span class="strip-badge badge-blue">{r['category']}</span></div>
                    <div class="strip-meta"><span>📞 {r['phone'] or 'N/A'}</span><span>✉️ {r['email'] or 'N/A'}</span><span>⏰ {time_str}</span></div>
                </div>""", unsafe_allow_html=True)

    elif view == "overdue":
        st.markdown("<h5 style='color:#0f172a; font-weight:800; margin-bottom:12px;'>⚠️ Overdue Tasks</h5>", unsafe_allow_html=True)
        if over_df.empty: st.markdown('<div class="strip strip-ok"><div style="font-size:1.5rem;margin-bottom:2px;opacity:0.9;">✅</div><p class="strip-title">Zero Overdue</p><p class="strip-meta">You are completely up to date.</p></div>', unsafe_allow_html=True)
        else:
            for _, r in over_df.iterrows():
                time_str = pd.to_datetime(r['next_followup']).strftime('%b %d, %I:%M %p')
                st.markdown(f"""
                <div class="strip strip-overdue">
                    <div class="strip-header"><p class="strip-title">{r['name']} <span style="color:#64748b; font-weight:500;">· {r['company']}</span></p><span class="strip-badge badge-red">LATE</span></div>
                    <div class="strip-meta"><span>📞 {r['phone'] or 'N/A'}</span><span>✉️ {r['email'] or 'N/A'}</span><span>⏰ Was Due: {time_str}</span></div>
                </div>""", unsafe_allow_html=True)

    elif view == "total":
        st.markdown("<h5 style='color:#0f172a; font-weight:800; margin-bottom:12px;'>👥 All Clients</h5>", unsafe_allow_html=True)
        df = db.get_all_clients()
        if df.empty: st.info("No clients added yet.")
        else:
            df["Status"] = df.apply(status_label, axis=1)
            st.dataframe(df[["name", "company", "category", "Status", "next_followup", "deal_value"]], use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ADD CLIENT
# ══════════════════════════════════════════════════════════════════════════════

def page_add_client():
    st.markdown('<p class="page-title">Add New Client</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Enter client details and schedule their follow-up.</p>', unsafe_allow_html=True)

    with st.form("add_client_form", clear_on_submit=True):
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 👤 Client Information")
        c1, c2 = st.columns(2)
        with c1:
            name    = st.text_input("Full Name *", placeholder="e.g. Jane Doe")
            email   = st.text_input("Email Address", placeholder="e.g. jane@company.com")
            company = st.text_input("Company Name", placeholder="e.g. Acme Corp")
        with c2:
            phone    = st.text_input("Phone Number", placeholder="+1 555-0199")
            category = st.selectbox("Category", ["Lead", "Prospect", "Active Client", "Partner", "VIP", "Churned"])
            source   = st.selectbox("Lead Source", ["Referral", "Website", "LinkedIn", "Cold Outreach", "Event", "Other"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 📅 Pipeline Scheduling")
        c3, c4 = st.columns(2)
        
        with c3:
            st.markdown("<div style='font-size:0.85rem; font-weight:600; color:#475569; margin-bottom:8px;'>Next Contact Schedule</div>", unsafe_allow_html=True)
            sc1, sc2 = st.columns(2)
            with sc1:
                next_d = st.date_input("Date", value=date.today(), label_visibility="collapsed")
            with sc2:
                default_time = (datetime.now() + timedelta(hours=4)).time()
                next_t = st.time_input("Time", value=default_time, label_visibility="collapsed")
            
            deal_value = st.number_input("Deal Value ($)", min_value=0, value=0, step=5000)
            
        with c4:
            nf_datetime = datetime.combine(next_d, next_t)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.7); border:1px solid rgba(255,255,255,1); border-radius:12px; padding:16px; text-align:center; box-shadow: 0 2px 10px rgba(0,0,0,0.02);">
                <p style="font-size:0.75rem; font-weight:800; color:#6366f1; text-transform:uppercase; letter-spacing:0.1em; margin:0;">Target Execution</p>
                <p style="font-size:1.3rem; font-weight:800; color:#0f172a; margin:4px 0;">{nf_datetime.strftime("%A, %b %d")}</p>
                <p style="font-size:1.1rem; color:#4f46e5; font-weight:700; margin:0;">@ {nf_datetime.strftime("%I:%M %p")}</p>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 📝 Additional Notes")
        notes = st.text_area("Notes", placeholder="Enter specific requirements, meeting notes...", height=80)
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("💾 Save Client", type="primary", use_container_width=True)

    if submitted:
        if not name.strip(): st.error("❌ Full Name is required.")
        else:
            f_days = (nf_datetime.date() - date.today()).days
            f_days = f_days if f_days > 0 else 0
            
            ok = db.add_client({
                "name": name, "email": email, "phone": phone, "company": company, "category": category, "source": source, 
                "last_contacted": str(datetime.now()), "followup_days": f_days, "next_followup": str(nf_datetime), 
                "deal_value": deal_value, "notes": notes, "created_by": st.session_state.get("user_id", 1)
            })
            if ok: st.success(f"✅ Success! **{name}** added. Scheduled for **{nf_datetime.strftime('%b %d @ %I:%M %p')}**.")
            else: st.error("❌ Database error.")


# ══════════════════════════════════════════════════════════════════════════════
#  CLIENT DIRECTORY (With Edit Console)
# ══════════════════════════════════════════════════════════════════════════════

def page_all_clients():
    st.markdown('<p class="page-title">Client Directory</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">View and manage all your clients.</p>', unsafe_allow_html=True)

    st.markdown('<div class="form-section" style="padding: 20px 24px;">', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns([3, 1, 1])
    with fc1: search = st.text_input("🔍 Search Clients", placeholder="Search by name, company, or email...", label_visibility="collapsed")
    with fc2: cat    = st.selectbox("Filter", ["All","Lead","Prospect","Active Client","Partner","VIP","Churned"], label_visibility="collapsed")
    with fc3: srt    = st.selectbox("Sort By", ["Next Follow-up","Name","Company","Deal Value"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    df = db.get_all_clients(search=search or None, category=cat if cat != "All" else None, sort_by=srt)

    if df.empty: 
        st.info("📭 No clients found.")
        return

    hc1, hc2 = st.columns([5, 1])
    with hc1: st.markdown(f"<p style='color:#64748b; font-size:0.9rem; font-weight:600; padding-top:10px;'>{len(df)} Clients found</p>", unsafe_allow_html=True)
    with hc2: st.download_button("📥 Export to Excel", data=to_excel(df), file_name=f"CRM_Export_{date.today()}.xlsx", use_container_width=True)

    # Format dataframe for display safely without overriding DB data
    df_display = df.copy()
    df_display["Status"] = df_display.apply(status_label, axis=1)
    df_display["Deal Value"] = df_display["deal_value"].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "—")
    df_display["next_contact_fmt"] = pd.to_datetime(df_display["next_followup"]).dt.strftime('%b %d, %I:%M %p')

    show_cols = ["name","company","phone","email","category","next_contact_fmt","Status","Deal Value"]
    rename    = {"name":"Full Name","company":"Company","phone":"Phone","email":"Email", "category":"Category","next_contact_fmt":"Next Contact"}

    st.dataframe(df_display[show_cols].rename(columns=rename), use_container_width=True, height=350, hide_index=True)

    st.markdown("<hr style='margin: 20px 0;'>", unsafe_allow_html=True)
    st.markdown("<h5 style='color:#0f172a; font-weight:800; margin-bottom:12px;'>⚙️ Client Management Console</h5>", unsafe_allow_html=True)
    
    st.markdown('<div class="form-section" style="padding: 24px 30px;">', unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.85rem; font-weight:700; color:#0f172a; margin-bottom:8px;'>Select Client to Manage</div>", unsafe_allow_html=True)
    sel = st.selectbox("Target", df["name"].tolist(), label_visibility="collapsed")
    
    if sel:
        target_row = df[df["name"] == sel].iloc[0]
        cid = int(target_row["id"])
        
        t1, t2, t3 = st.tabs(["🕒 Reschedule Time", "📝 Edit Details", "🗑️ Delete"])
        
        with t1:
            st.markdown("<br>", unsafe_allow_html=True)
            sc1, sc2, sc3 = st.columns([2, 2, 1])
            
            try:
                curr_dt = pd.to_datetime(target_row["next_followup"])
            except:
                curr_dt = datetime.now() + timedelta(hours=4)
                
            with sc1: new_d = st.date_input("New Date", value=curr_dt.date(), key=f"d_{cid}")
            with sc2: new_t = st.time_input("New Time", value=curr_dt.time(), key=f"t_{cid}")
            with sc3:
                st.markdown("<br style='line-height:1.2'>", unsafe_allow_html=True)
                if st.button("Update Time/Date", type="primary", use_container_width=True, key=f"btn_resched_{cid}"):
                    new_dt = datetime.combine(new_d, new_t)
                    db.update_followup(cid, str(new_dt))
                    st.rerun()
                    
        with t2:
            st.markdown("<br>", unsafe_allow_html=True)
            with st.form(key=f"edit_form_{cid}"):
                ec1, ec2 = st.columns(2)
                with ec1:
                    e_name = st.text_input("Full Name", value=target_row["name"])
                    e_email = st.text_input("Email", value=target_row["email"] if pd.notna(target_row["email"]) else "")
                    e_val = st.number_input("Deal Value ($)", value=int(target_row["deal_value"]) if pd.notna(target_row["deal_value"]) else 0, step=1000)
                with ec2:
                    e_phone = st.text_input("Phone", value=target_row["phone"] if pd.notna(target_row["phone"]) else "")
                    e_company = st.text_input("Company", value=target_row["company"] if pd.notna(target_row["company"]) else "")
                    
                    cat_opts = ["Lead", "Prospect", "Active Client", "Partner", "VIP", "Churned"]
                    curr_cat = target_row["category"]
                    cat_idx = cat_opts.index(curr_cat) if curr_cat in cat_opts else 0
                    e_cat = st.selectbox("Category", cat_opts, index=cat_idx)
                
                if st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True):
                    try:
                        db.c.execute('''UPDATE clients SET name=?, email=?, phone=?, company=?, deal_value=?, category=? WHERE id=?''', 
                                     (e_name, e_email, e_phone, e_company, e_val, e_cat, cid))
                        db.conn.commit()
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating database: {e}")
                        
        with t3:
            st.markdown("<br>", unsafe_allow_html=True)
            st.error(f"Warning: Deleting **{sel}** is permanent and cannot be undone.")
            if st.button("🗑 Confirm Delete", use_container_width=True, key=f"btn_del_{cid}"):
                db.delete_client(cid)
                st.rerun()
                
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SETTINGS / ACCESS CONTROL
# ══════════════════════════════════════════════════════════════════════════════

def page_settings():
    st.markdown('<p class="page-title">Settings</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Manage your account and workspace preferences.</p>', unsafe_allow_html=True)

    is_admin = st.session_state.get("role") == "admin"
    current_user_id = st.session_state.get("user_id")

    if is_admin:
        tabs = st.tabs(["👥 Active Users", "➕ Add User", "🔑 Change Password"])
    else:
        tabs = st.tabs(["🔑 Change Password"])

    if is_admin:
        with tabs[0]:
            st.markdown("<br>", unsafe_allow_html=True)
            users = db.get_all_users()
            if users.empty: st.info("No active users found.")
            else:
                for _, u in users.iterrows():
                    role_badge = "🛡️ Admin" if u["role"] == "admin" else "👤 User"
                    status_badge = "🟢 Active" if u["is_active"] else "🔴 Suspended"
                    
                    c1, c2, c3 = st.columns([4, 1.5, 1.5])
                    with c1:
                        st.markdown(f"""
                        <div style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); padding: 12px 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,1); box-shadow: 0 2px 8px rgba(0,0,0,0.02);">
                            <div style="font-size: 1rem; font-weight: 800; color: #0f172a; margin-bottom: 2px;">{u['full_name']} <span style="color: #64748b; font-weight: 500; font-size: 0.8rem;">(@{u['username']})</span></div>
                            <div style="font-size: 0.75rem; font-weight: 600; color: #475569;">{role_badge} &nbsp;|&nbsp; {status_badge}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with c2:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if u["username"] != st.session_state.get("username"):
                            if st.button("Suspend" if u["is_active"] else "Activate", key=f"tog_{u['id']}", use_container_width=True): 
                                db.toggle_user_status(int(u["id"])); st.rerun()
                        else:
                            st.markdown("<div style='text-align: center; margin-top: 10px; font-weight: 700; color: #10b981; font-size: 0.8rem;'>Current User</div>", unsafe_allow_html=True)
                            
                    with c3:
                        st.markdown("<br>", unsafe_allow_html=True)
                        if u["username"] != st.session_state.get("username"):
                            if st.button("Delete", key=f"del_{u['id']}", use_container_width=True): 
                                db.delete_user(int(u["id"])); st.rerun()
                    st.markdown("<div style='height:4px;'></div>", unsafe_allow_html=True)

        with tabs[1]:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="form-section">', unsafe_allow_html=True)
            st.markdown("##### Add New User")
            with st.form("add_user_form", clear_on_submit=True):
                new_fullname = st.text_input("Full Name *", placeholder="e.g. Alex Smith")
                new_username = st.text_input("Username *", placeholder="e.g. alex.smith")
                new_password  = st.text_input("Password *", type="password", placeholder="Min 6 characters")
                new_role      = st.selectbox("Role", ["user", "admin"])

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
                    db.add_user({"full_name": new_fullname, "username": new_username, "email": "", "password_hash": hash_password(new_password), "role": new_role})
                    st.success(f"✅ Success! {new_fullname} added."); st.rerun()

    pwd_tab = tabs[2] if is_admin else tabs[0]
    with pwd_tab:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### Security: Update Password")
        with st.form("change_password_form", clear_on_submit=True):
            old_p = st.text_input("Current Password *", type="password")
            new_p = st.text_input("New Password *", type="password", placeholder="Min 6 characters")
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
                user_check = db.authenticate_user(st.session_state.username, hash_password(old_p))
                if not user_check:
                    st.error("❌ Incorrect current password.")
                else:
                    success = change_user_password(current_user_id, new_p)
                    if success: st.success("✅ Password updated successfully!")
                    else: st.error("❌ System Error: Failed to update password.")


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════

if not st.session_state.get("logged_in"): show_login()
else:
    page = show_sidebar()
    
    if   "Dashboard"        in page: page_dashboard()
    elif "Add Client"       in page: page_add_client()
    elif "Client Directory" in page: page_all_clients()
    elif "Settings"         in page: page_settings()
