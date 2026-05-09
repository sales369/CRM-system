import streamlit as st
import pandas as pd
from datetime import date, timedelta
import io
import hashlib
from database import DatabaseManager

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ClientPulse | Enterprise",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 🌌 FUTURISTIC ANIMATED BACKGROUND ──────────────────────────────────────────
# This injects the floating glowing orbs into the background
st.markdown("""
<div class="bg-blobs">
    <div class="blob blob-1"></div>
    <div class="blob blob-2"></div>
    <div class="blob blob-3"></div>
</div>
""", unsafe_allow_html=True)

# ── 💎 ULTRA-PREMIUM DARK GLASSMORPHISM CSS ────────────────────────────────────
st.markdown("""
<style>
/* ── Premium Font ── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&display=swap');

*, html, body, [class*="css"], [class*="st-"] {
    font-family: 'Outfit', sans-serif !important;
}

/* ── Base Theme & Background ── */
.stApp {
    background-color: #060814 !important; /* Deep space dark */
    color: #e2e8f0;
}
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.3); }

/* ── Live Animated Glowing Blobs ── */
.bg-blobs {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: -999; overflow: hidden; pointer-events: none;
    background: #060814;
}
.blob {
    position: absolute; border-radius: 50%; filter: blur(100px);
    opacity: 0.5; animation: floatBlob 15s infinite alternate ease-in-out;
}
.blob-1 {
    width: 60vw; height: 60vw; top: -10vw; left: -10vw;
    background: radial-gradient(circle, rgba(99,102,241,0.15) 0%, transparent 60%);
    animation-delay: 0s;
}
.blob-2 {
    width: 50vw; height: 50vw; bottom: -10vw; right: -5vw;
    background: radial-gradient(circle, rgba(236,72,153,0.15) 0%, transparent 60%);
    animation-delay: -5s;
}
.blob-3 {
    width: 40vw; height: 40vw; top: 40vh; left: 30vw;
    background: radial-gradient(circle, rgba(14,165,233,0.1) 0%, transparent 60%);
    animation-delay: -10s;
}
@keyframes floatBlob {
    0% { transform: translate(0, 0) scale(1); }
    100% { transform: translate(50px, -50px) scale(1.1); }
}

/* ── Animations ── */
@keyframes slideUpFade {
    0% { opacity: 0; transform: translateY(20px); filter: blur(5px); }
    100% { opacity: 1; transform: translateY(0); filter: blur(0); }
}

/* ── Hide Chrome on Login ── */
.login-mode header, .login-mode [data-testid="stSidebar"], .login-mode footer { display: none !important; }

/* ── Glassmorphic Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(10, 12, 24, 0.4) !important;
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.05) !important;
}
[data-testid="stSidebarNav"] { padding-top: 0 !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 8px; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: transparent; border-radius: 12px; padding: 12px 18px !important;
    font-size: 0.95rem !important; font-weight: 500 !important; color: #94a3b8 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); border: 1px solid transparent; cursor: pointer;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.03) !important; color: #ffffff !important;
    transform: translateX(6px); border: 1px solid rgba(255,255,255,0.05);
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-baseweb="radio"] { display: flex; }

/* ── Main Area ── */
.main .block-container { 
    padding: 3rem 4rem !important; max-width: 1440px; 
    animation: slideUpFade 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* ── Premium Typography ── */
.page-title { font-size: 2.5rem; font-weight: 800; color: #ffffff; margin: 0 0 4px; letter-spacing: -0.04em; 
              background: linear-gradient(to right, #fff, #94a3b8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.page-sub   { font-size: 1.05rem; color: #94a3b8; font-weight: 400; margin: 0 0 2.5rem; letter-spacing: 0.01em; }

/* ── Interactive Glass Dashboard Tiles ── */
div[data-testid="stHorizontalBlock"]:has(.dash-card) div[data-testid="column"] { position: relative; }
div[data-testid="stHorizontalBlock"]:has(.dash-card) [data-testid="stButton"] {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 999;
}
div[data-testid="stHorizontalBlock"]:has(.dash-card) [data-testid="stButton"] button {
    width: 100%; height: 100%; opacity: 0; cursor: pointer; background: transparent; border: none;
}

.dash-card {
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-top: 1px solid rgba(255, 255, 255, 0.12); /* Light reflection */
    border-radius: 20px;
    padding: 28px 24px;
    position: relative; overflow: hidden;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    margin-bottom: 12px;
}
.dash-card::after { /* Glow effect under the card */
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 3px;
    background: transparent; transition: background 0.4s ease;
}
div[data-testid="column"]:has(button:hover) .dash-card {
    transform: translateY(-6px);
    background: rgba(255, 255, 255, 0.04);
    box-shadow: 0 20px 40px -10px rgba(0,0,0,0.5), 0 0 20px rgba(99, 102, 241, 0.15);
    border-color: rgba(255, 255, 255, 0.1);
}
div[data-testid="column"]:has(button:hover) .dash-card.indigo::after { background: linear-gradient(90deg, #6366f1, #a855f7); box-shadow: 0 -5px 15px rgba(99,102,241,0.5); }
div[data-testid="column"]:has(button:hover) .dash-card.blue::after   { background: linear-gradient(90deg, #0ea5e9, #38bdf8); box-shadow: 0 -5px 15px rgba(14,165,233,0.5); }
div[data-testid="column"]:has(button:hover) .dash-card.red::after    { background: linear-gradient(90deg, #ef4444, #f87171); box-shadow: 0 -5px 15px rgba(239,68,68,0.5); }
div[data-testid="column"]:has(button:hover) .dash-card.purple::after { background: linear-gradient(90deg, #8b5cf6, #c084fc); box-shadow: 0 -5px 15px rgba(139,92,246,0.5); }

.metric-icon { font-size: 2rem; margin-bottom: 16px; filter: drop-shadow(0 0 8px rgba(255,255,255,0.2)); }
.metric-val  { font-size: 2.6rem; font-weight: 800; color: #ffffff; margin: 0 0 4px; line-height: 1; }
.metric-lbl  { font-size: 0.85rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; margin: 0; }

/* ── Modern Form Cards (Glassmorphism) ── */
.form-section {
    background: rgba(20, 24, 39, 0.5);
    backdrop-filter: blur(12px);
    border-radius: 20px;
    padding: 32px 36px;
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    margin-bottom: 24px;
}
.form-section h5 { color: #ffffff; font-weight: 700; margin-bottom: 20px; font-size: 1.15rem; letter-spacing: 0.02em;}

/* ── Native Streamlit Input Overrides (Dark Glass) ── */
[data-baseweb="input"] > div, [data-baseweb="select"] > div, [data-baseweb="textarea"] > div {
    border-radius: 12px !important; background-color: rgba(0,0,0,0.3) !important;
    border: 1px solid rgba(255,255,255,0.1) !important; color: white !important; transition: all 0.3s ease !important;
}
[data-baseweb="input"] > div:hover, [data-baseweb="select"] > div:hover { border-color: rgba(255,255,255,0.2) !important; }
[data-baseweb="input"] > div:focus-within, [data-baseweb="select"] > div:focus-within {
    border-color: #6366f1 !important; box-shadow: 0 0 0 2px rgba(99,102,241,0.2), inset 0 0 10px rgba(99,102,241,0.1) !important;
}
input, textarea { font-size: 0.95rem !important; color: #ffffff !important; }
.stSelectbox label, .stTextInput label, .stNumberInput label, .stDateInput label { color: #cbd5e1 !important; font-weight: 500 !important; }

/* ── Cinematic Buttons ── */
.stButton > button {
    border-radius: 12px !important; font-weight: 600 !important; font-size: 0.95rem !important;
    padding: 0.6rem 1.4rem !important; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    border: 1px solid rgba(255,255,255,0.1) !important; background: rgba(255,255,255,0.03) !important; color: #ffffff !important;
}
.stButton > button:hover { 
    background: rgba(255,255,255,0.08) !important; transform: translateY(-2px) !important; 
    box-shadow: 0 8px 20px rgba(0,0,0,0.3) !important; border-color: rgba(255,255,255,0.2) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4f46e5 0%, #d946ef 100%) !important; border: none !important;
    color: white !important; box-shadow: 0 4px 15px rgba(217, 70, 239, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4338ca 0%, #c026d3 100%) !important;
    box-shadow: 0 8px 25px rgba(217, 70, 239, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}

/* ── Alert Strips (Dark Neumorphic) ── */
.strip { 
    background: rgba(20, 25, 40, 0.6); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px 24px; margin-bottom: 16px; 
    border: 1px solid rgba(255,255,255,0.05); border-left-width: 4px; display: flex; flex-direction: column; gap: 8px; transition: all 0.3s ease;
}
.strip:hover { transform: translateX(6px); background: rgba(30, 35, 55, 0.8); }
.strip-today { border-left-color: #0ea5e9; box-shadow: inset 20px 0 30px -20px rgba(14,165,233,0.1); }
.strip-overdue { border-left-color: #ef4444; box-shadow: inset 20px 0 30px -20px rgba(239,68,68,0.1); }
.strip-ok { border-left-color: #10b981; align-items: center; text-align: center; }

.strip-header { display: flex; justify-content: space-between; align-items: center; }
.strip-title { font-size: 1.1rem; font-weight: 700; color: #ffffff; margin: 0; }
.strip-badge { font-size: 0.75rem; font-weight: 700; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em;}
.badge-blue { background: rgba(14,165,233,0.2); color: #38bdf8; border: 1px solid rgba(14,165,233,0.3); }
.badge-red { background: rgba(239,68,68,0.2); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }

.strip-meta { display: flex; gap: 16px; font-size: 0.85rem; color: #cbd5e1; font-weight: 500; margin: 0; }
.strip-notes { margin: 6px 0 0; padding-top: 12px; border-top: 1px solid rgba(255,255,255,0.05); font-size: 0.85rem; color: #94a3b8; }

/* ── Expanders & Dividers ── */
.streamlit-expanderHeader {
    font-weight: 600 !important; color: #ffffff !important;
    background: rgba(255,255,255,0.03) !important; border-radius: 12px !important; border: 1px solid rgba(255,255,255,0.05) !important;
}
details { border: none !important; border-radius: 12px !important; background: transparent; overflow: hidden; }
hr { border: none; border-top: 1px solid rgba(255,255,255,0.08); margin: 2rem 0; }

/* ── Tabs ── */
[data-baseweb="tab-list"] { gap: 30px; border-bottom: 2px solid rgba(255,255,255,0.05) !important; padding-bottom: 4px; }
[data-baseweb="tab"] { font-weight: 600 !important; font-size: 1.05rem !important; color: #64748b !important; background: transparent !important; border: none !important; padding: 8px 4px !important; transition: color 0.3s ease; }
[aria-selected="true"] { color: #ffffff !important; border-bottom: 2px solid #a855f7 !important; text-shadow: 0 0 10px rgba(168,85,247,0.5); }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  DB + Auth helpers
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
    nf = pd.to_datetime(row["next_followup"]).date() if pd.notna(row["next_followup"]) else None
    if not nf: return "—"
    d = date.today()
    if nf < d:  return f"🔴 Overdue ({(d - nf).days}d)"
    if nf == d: return "🟡 Due Today"
    return f"🟢 In {(nf - d).days}d"


# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN PAGE (Cinematic Portal)
# ══════════════════════════════════════════════════════════════════════════════

def show_login():
    st.markdown("""
    <style>
    .main .block-container {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        min-height: 100vh; padding: 0 !important;
    }
    header { visibility: hidden !important; }
    
    [data-testid="stForm"] {
        background: rgba(10, 15, 30, 0.6); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.08) !important; border-top: 1px solid rgba(255,255,255,0.15) !important;
        border-radius: 28px; padding: 56px 48px !important; width: 100%; max-width: 460px; margin: 0 auto;
        box-shadow: 0 30px 60px rgba(0,0,0,0.5), inset 0 0 40px rgba(255,255,255,0.02);
        animation: slideUpFade 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }
    </style>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown("""
        <div style="text-align:center; margin-bottom:40px;">
            <div style="width: 72px; height: 72px; background: linear-gradient(135deg, #4f46e5, #d946ef); 
                        border-radius: 22px; display: flex; align-items: center; justify-content: center; 
                        font-size: 32px; margin: 0 auto 24px; box-shadow: 0 10px 30px rgba(217, 70, 239, 0.4);
                        border: 1px solid rgba(255,255,255,0.2);">✨</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em; margin-bottom: 8px;">ClientPulse OS</div>
            <div style="font-size: 0.95rem; color: #94a3b8; font-weight: 400; letter-spacing: 0.02em;">Authenticate to enter workspace</div>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("System Identity", placeholder="Enter your username")
        password = st.text_input("Access Protocol", type="password", placeholder="Enter your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Initialize Session ➜", use_container_width=True, type="primary")

        if submitted:
            if not username or not password:
                st.error("Please enter credentials.")
            else:
                user = db.authenticate_user(username, hash_password(password))
                if user:
                    st.session_state.logged_in  = True
                    st.session_state.username   = user["username"]
                    st.session_state.role       = user["role"]
                    st.session_state.full_name  = user["full_name"]
                    st.session_state.user_id    = user["id"]
                    st.rerun()
                else:
                    st.error("❌ Authentication Failed.")

        st.markdown("""
        <div style="text-align:center; margin-top:32px; font-size:0.8rem; color:#475569; font-weight:500; text-transform:uppercase; letter-spacing:0.1em;">
            End-to-End Encrypted Node
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

def show_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding: 32px 16px 40px; display: flex; align-items: center; gap: 14px;">
            <div style="width: 44px; height: 44px; background: linear-gradient(135deg, #4f46e5, #d946ef); 
                        border-radius: 14px; display: flex; align-items: center; justify-content: center; 
                        font-size: 22px; box-shadow: 0 4px 15px rgba(217, 70, 239, 0.4); border: 1px solid rgba(255,255,255,0.2);">✨</div>
            <div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #ffffff; letter-spacing: -0.02em; line-height: 1;">ClientPulse</div>
                <div style="font-size: 0.65rem; color: #a855f7; text-transform: uppercase; letter-spacing: 0.2em; font-weight: 700; margin-top: 6px;">Operating System</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        role = st.session_state.get("role", "user")
        full_name = st.session_state.get("full_name", "User")
        username  = st.session_state.get("username", "")

        initials = "".join(p[0].upper() for p in full_name.split()[:2])
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); border-radius: 16px; padding: 16px; margin: 0 16px 32px; display: flex; align-items: center; gap: 14px;">
            <div style="width: 46px; height: 46px; border-radius: 12px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1);
                        display: flex; align-items: center; justify-content: center; font-size: 1rem; font-weight: 800; color: #e2e8f0; flex-shrink: 0;">
                {initials}
            </div>
            <div style="overflow: hidden;">
                <div style="font-size: 0.95rem; font-weight: 700; color: #ffffff; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{full_name}</div>
                <div style="font-size: 0.75rem; color: #a855f7; font-weight: 600; margin-top: 4px; text-transform:uppercase; letter-spacing:0.05em;">
                    {'Admin Protocol' if role == 'admin' else 'User Node'}
                </div>
            </div>
        </div>
        <div style="padding: 0 16px; font-size: 0.7rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px;">Main Directory</div>
        """, unsafe_allow_html=True)

        nav_options = ["🏠  Command Center", "➕  Initialize Client", "👥  Database Grid", "📅  Action Pipeline", "📊  Telemetry"]
        if role == "admin":
            nav_options.append("⚙️  System Config")

        page = st.radio("Navigation", nav_options, label_visibility="collapsed")

        st.markdown("<div style='height:1px;background:rgba(255,255,255,0.05);margin:32px 16px 24px;'></div>", unsafe_allow_html=True)
        
        if st.button("🔌  Terminate Session", use_container_width=True):
            for k in ["logged_in","username","role","full_name","user_id","show_today","dash_view"]:
                st.session_state.pop(k, None)
            st.rerun()

    return page


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD (Interactive Holographic Tiles)
# ══════════════════════════════════════════════════════════════════════════════

def page_dashboard():
    st.markdown('<p class="page-title">Command Center</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-sub">System authenticated. Welcome back, <b>{st.session_state.get("full_name","User")}</b>. Awaiting input.</p>', unsafe_allow_html=True)

    total = db.get_total_clients()
    today_df  = db.get_todays_followups()
    over_df   = db.get_overdue_followups()
    upc_df    = db.get_upcoming_followups(7)

    if "dash_view" not in st.session_state:
        st.session_state.dash_view = "today"

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f'<div class="metric-card dash-card indigo"><div class="metric-icon">👥</div><p class="metric-val">{total}</p><p class="metric-lbl">Total Network</p></div>', unsafe_allow_html=True)
        if st.button(" ", key="btn_tot", use_container_width=True): st.session_state.dash_view = "total"

    with c2:
        st.markdown(f'<div class="metric-card dash-card blue"><div class="metric-icon">⚡</div><p class="metric-val">{len(today_df)}</p><p class="metric-lbl">Active Today</p></div>', unsafe_allow_html=True)
        if st.button("  ", key="btn_tod", use_container_width=True): st.session_state.dash_view = "today"

    with c3:
        st.markdown(f'<div class="metric-card dash-card red"><div class="metric-icon">⚠️</div><p class="metric-val">{len(over_df)}</p><p class="metric-lbl">Critical Overdue</p></div>', unsafe_allow_html=True)
        if st.button("   ", key="btn_ovr", use_container_width=True): st.session_state.dash_view = "overdue"

    with c4:
        st.markdown(f'<div class="metric-card dash-card purple"><div class="metric-icon">🔭</div><p class="metric-val">{len(upc_df)}</p><p class="metric-lbl">7-Day Forecast</p></div>', unsafe_allow_html=True)
        if st.button("    ", key="btn_upc", use_container_width=True): st.session_state.dash_view = "upcoming"

    st.markdown("<hr>", unsafe_allow_html=True)

    view = st.session_state.dash_view

    if view == "today":
        st.markdown("<h4 style='color:#ffffff; font-weight:700; margin-bottom:20px; letter-spacing:0.02em;'>⚡ Priority Execution: Today</h4>", unsafe_allow_html=True)
        if today_df.empty:
            st.markdown('<div class="strip strip-ok"><div style="font-size:2rem;margin-bottom:8px;opacity:0.8;">🌐</div><p class="strip-title">Systems Nominal</p><p class="strip-meta">No actions required today.</p></div>', unsafe_allow_html=True)
        else:
            for _, r in today_df.iterrows():
                st.markdown(f"""
                <div class="strip strip-today">
                    <div class="strip-header">
                        <p class="strip-title">{r['name']} <span style="color:#64748b; font-weight:400;">// {r['company']}</span></p>
                        <span class="strip-badge badge-blue">{r['category']}</span>
                    </div>
                    <div class="strip-meta">
                        <span>📞 {r['phone'] or 'NULL'}</span>
                        <span>✉️ {r['email'] or 'NULL'}</span>
                    </div>
                    <p class="strip-notes">📝 {r['notes'] or 'No supplemental data.'}</p>
                </div>""", unsafe_allow_html=True)

    elif view == "overdue":
        st.markdown("<h4 style='color:#ffffff; font-weight:700; margin-bottom:20px; letter-spacing:0.02em;'>⚠️ Critical Backlog</h4>", unsafe_allow_html=True)
        if over_df.empty:
            st.markdown('<div class="strip strip-ok"><div style="font-size:2rem;margin-bottom:8px;opacity:0.8;">✅</div><p class="strip-title">Zero Anomalies</p><p class="strip-meta">No overdue actions detected.</p></div>', unsafe_allow_html=True)
        else:
            for _, r in over_df.iterrows():
                d = (date.today() - pd.to_datetime(r['next_followup']).date()).days
                st.markdown(f"""
                <div class="strip strip-overdue">
                    <div class="strip-header">
                        <p class="strip-title">{r['name']} <span style="color:#64748b; font-weight:400;">// {r['company']}</span></p>
                        <span class="strip-badge badge-red">-{d} CYCLES</span>
                    </div>
                    <div class="strip-meta">
                        <span>📞 {r['phone'] or 'NULL'}</span>
                        <span>✉️ {r['email'] or 'NULL'}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    elif view == "total":
        st.markdown("<h4 style='color:#ffffff; font-weight:700; margin-bottom:20px; letter-spacing:0.02em;'>👥 Complete Data Grid</h4>", unsafe_allow_html=True)
        df = db.get_all_clients()
        if df.empty:
            st.info("Database is currently empty.")
        else:
            df["Status"] = df.apply(status_label, axis=1)
            show_cols = ["name", "company", "category", "Status", "next_followup", "deal_value"]
            st.dataframe(df[show_cols], use_container_width=True, hide_index=True)

    elif view == "upcoming":
        st.markdown("<h4 style='color:#ffffff; font-weight:700; margin-bottom:20px; letter-spacing:0.02em;'>🔭 Predictive Pipeline (7 Days)</h4>", unsafe_allow_html=True)
        if upc_df.empty:
            st.info("No anomalies detected in the upcoming 7-day window.")
        else:
            upc_df["Days Until"] = upc_df["next_followup"].apply(lambda x: (pd.to_datetime(x).date() - date.today()).days)
            st.dataframe(upc_df[["name", "company", "category", "next_followup", "Days Until"]], use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ADD CLIENT
# ══════════════════════════════════════════════════════════════════════════════

def page_add_client():
    st.markdown('<p class="page-title">Initialize Node</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Input parameters to establish a new entity within the database.</p>', unsafe_allow_html=True)

    with st.form("add_client_form", clear_on_submit=True):
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 👤 Entity Specifications")
        c1, c2 = st.columns(2)
        with c1:
            name    = st.text_input("Designation (Name) *", placeholder="e.g. John Doe")
            email   = st.text_input("Comms Relay (Email)", placeholder="e.g. user@domain.com")
            company = st.text_input("Affiliation (Company)", placeholder="e.g. Acme Corp")
        with c2:
            phone    = st.text_input("Frequency (Phone)", placeholder="+1 555-0199")
            category = st.selectbox("Classification", ["Lead", "Prospect", "Active Client", "Partner", "VIP", "Churned"])
            source   = st.selectbox("Origin Source", ["Referral", "Website", "LinkedIn", "Cold Outreach", "Event", "Other"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 📅 Temporal Parameters")
        c3, c4 = st.columns(2)
        with c3:
            last_contacted = st.date_input("Last Sync Date", value=date.today())
            followup_days  = st.number_input("Cadence Interval (Days) *", min_value=1, max_value=365, value=5)
            deal_value     = st.number_input("Projected Value ($)", min_value=0, value=0, step=5000)
        with c4:
            nf = last_contacted + timedelta(days=int(followup_days))
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:rgba(14,165,233,0.1); border:1px dashed rgba(14,165,233,0.4); border-radius:16px; padding:24px; text-align:center;">
                <p style="font-size:0.75rem; font-weight:700; color:#38bdf8; text-transform:uppercase; letter-spacing:0.1em; margin:0;">Computed Execution Date</p>
                <p style="font-size:1.6rem; font-weight:800; color:#ffffff; margin:8px 0;">{nf.strftime("%A, %B %d, %Y")}</p>
                <p style="font-size:0.85rem; color:#94a3b8; font-weight:500; margin:0;">
                    Automated sequence queued in <span style="color:#ffffff; font-weight:700;">{int(followup_days)} cycles</span>
                </p>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 📝 Supplemental Data")
        notes = st.text_area("Encrypted Notes", placeholder="Input mission critical data here...", height=120)
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("💾 Committ to Database", type="primary", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("❌ Designation is a mandatory parameter.")
        else:
            ok = db.add_client({
                "name": name, "email": email, "phone": phone,
                "company": company, "category": category, "source": source,
                "last_contacted": str(last_contacted), "followup_days": int(followup_days),
                "next_followup": str(nf), "deal_value": deal_value, "notes": notes,
                "created_by": st.session_state.get("user_id", 1)
            })
            if ok:
                st.success(f"✅ Protocol accepted. **{name}** assimilated. Sequence scheduled for **{nf.strftime('%b %d')}**.")
            else:
                st.error("❌ Database connection failed. Aborting.")


# ══════════════════════════════════════════════════════════════════════════════
#  ALL CLIENTS 
# ══════════════════════════════════════════════════════════════════════════════

def page_all_clients():
    st.markdown('<p class="page-title">Database Grid</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Global view of all registered entities and their current operational status.</p>', unsafe_allow_html=True)

    st.markdown('<div class="form-section" style="padding: 24px;">', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns([3, 1, 1])
    with fc1: search = st.text_input("🔍 Query Matrix", placeholder="Search parameters...", label_visibility="collapsed")
    with fc2: cat    = st.selectbox("Filter", ["All","Lead","Prospect","Active Client","Partner","VIP","Churned"], label_visibility="collapsed")
    with fc3: srt    = st.selectbox("Sort", ["Next Follow-up","Name","Company","Deal Value"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    df = db.get_all_clients(search=search or None, category=cat if cat != "All" else None, sort_by=srt)

    if df.empty:
        st.info("📭 Query returned zero results.")
        return

    hc1, hc2 = st.columns([5, 1])
    with hc1: st.markdown(f"<p style='color:#94a3b8; font-size:0.95rem; font-weight:500; padding-top:10px;'>{len(df)} Entities Located</p>", unsafe_allow_html=True)
    with hc2:
        st.download_button("📥 Extract JSON/CSV", data=to_excel(df), file_name=f"Data_Export_{date.today()}.xlsx", use_container_width=True)

    df["Status"]     = df.apply(status_label, axis=1)
    df["Deal Value"] = df["deal_value"].apply(lambda x: f"${x:,.0f}" if x else "—")

    show_cols = ["name","company","phone","email","category","next_followup","Status","Deal Value"]
    rename    = {"name":"Designation","company":"Affiliation","phone":"Comms","email":"Email",
                 "category":"Class","next_followup":"Execution Date"}

    st.dataframe(df[show_cols].rename(columns=rename), use_container_width=True, height=500, hide_index=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#ffffff; font-weight:700; margin-bottom:16px;'>⚡ Override Protocols</h4>", unsafe_allow_html=True)
    
    st.markdown('<div class="form-section" style="padding: 24px;">', unsafe_allow_html=True)
    rc1, rc2, rc3, rc4 = st.columns([3, 1, 1, 1])
    with rc1: 
        st.markdown("<div style='font-size:0.8rem; font-weight:600; color:#94a3b8; margin-bottom:4px;'>Target Entity</div>", unsafe_allow_html=True)
        sel = st.selectbox("Target", df["name"].tolist(), label_visibility="collapsed")
    with rc2: 
        st.markdown("<div style='font-size:0.8rem; font-weight:600; color:#94a3b8; margin-bottom:4px;'>New Temporal Coordinate</div>", unsafe_allow_html=True)
        new_d = st.date_input("Date", value=date.today() + timedelta(days=7), label_visibility="collapsed")
    with rc3:
        st.markdown("<br style='line-height:1.2'>", unsafe_allow_html=True)
        if st.button("Shift Timeline", type="primary", use_container_width=True):
            cid = int(df[df["name"] == sel]["id"].values[0])
            db.update_followup(cid, str(new_d))
            st.rerun()
    with rc4:
        st.markdown("<br style='line-height:1.2'>", unsafe_allow_html=True)
        if st.button("🗑 Terminate", use_container_width=True):
            cid = int(df[df["name"] == sel]["id"].values[0])
            db.delete_client(cid)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  FOLLOW-UPS
# ══════════════════════════════════════════════════════════════════════════════

def page_followups():
    st.markdown('<p class="page-title">Action Pipeline</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Categorized view of pending, active, and predictive tasks.</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔴 CRITICAL OVERDUE", "⚡ ACTIVE CYCLE", "🔭 PREDICTIVE QUEUE"])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        ov = db.get_overdue_followups()
        if ov.empty: st.success("🎉 Optimization Complete. No critical delays.")
        else:
            for _, r in ov.iterrows():
                days_over = (date.today() - pd.to_datetime(r["next_followup"]).date()).days
                with st.expander(f"🔴 {r['name']} // {r['company']} [-{days_over} CYCLES]"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.markdown(f"**📞 Comms:** {r['phone'] or '—'}")
                        st.markdown(f"**✉️ Routing:** {r['email'] or '—'}")
                    with cc2:
                        st.markdown(f"**💰 Projected Value:** {'${:,.0f}'.format(r['deal_value']) if r['deal_value'] else '—'}")
                        st.markdown(f"**📅 Original Target:** {pd.to_datetime(r['next_followup']).strftime('%b %d, %Y')}")
                    st.markdown(f"**📝 Data:**<br> <span style='color:#94a3b8;'>{r['notes'] or 'NULL'}</span>", unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
                    nd = st.number_input("Recalibrate (Days)", min_value=1, value=7, key=f"ov_{r['id']}")
                    if st.button("✅ Execute & Recalibrate", type="primary", key=f"ovb_{r['id']}"):
                        db.update_followup(int(r["id"]), str(date.today() + timedelta(days=nd)), update_last_contacted=True)
                        st.rerun()

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        td = db.get_todays_followups()
        if td.empty: st.info("📭 Active cycle is empty.")
        else:
            for _, r in td.iterrows():
                with st.expander(f"⚡ {r['name']} // {r['company']}"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.markdown(f"**📞 Comms:** {r['phone'] or '—'}")
                        st.markdown(f"**✉️ Routing:** {r['email'] or '—'}")
                    with cc2:
                        st.markdown(f"**🏷 Class:** {r['category']}")
                        st.markdown(f"**💰 Value:** {'${:,.0f}'.format(r['deal_value']) if r['deal_value'] else '—'}")
                    st.markdown(f"**📝 Data:**<br> <span style='color:#94a3b8;'>{r['notes'] or 'NULL'}</span>", unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
                    nd = st.number_input("Next Cycle In (Days)", min_value=1, value=int(r["followup_days"]), key=f"td_{r['id']}")
                    if st.button("✅ Complete Sequence", type="primary", key=f"tdb_{r['id']}"):
                        db.update_followup(int(r["id"]), str(date.today() + timedelta(days=nd)), update_last_contacted=True)
                        st.rerun()

    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        days_ahead = st.slider("Forecast Resolution (Days)", 1, 90, 30)
        up = db.get_upcoming_followups(days_ahead)
        if up.empty: st.info(f"No events detected in the T+{days_ahead} window.")
        else:
            up["T-Minus"] = up["next_followup"].apply(lambda x: (pd.to_datetime(x).date() - date.today()).days)
            st.dataframe(up[["name","company","phone","category","next_followup","T-Minus"]], use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  REPORTS
# ══════════════════════════════════════════════════════════════════════════════

def page_reports():
    st.markdown('<p class="page-title">Telemetry & Metrics</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Real-time analytical breakdown of network health.</p>', unsafe_allow_html=True)

    df = db.get_all_clients()
    if df.empty: return st.info("Insufficient telemetry data.")

    today_d = date.today()
    total_deal = df["deal_value"].sum()
    avg_deal   = df["deal_value"].mean()
    active     = len(df[df["category"] == "Active Client"])
    overdue_n  = len(df[df["next_followup"].apply(lambda x: pd.to_datetime(x).date() < today_d if pd.notna(x) else False)])

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, val, lbl, theme in [
        (c1, "💰", f"${total_deal:,.0f}",  "Total Capital",    "green"),
        (c2, "📊", f"${avg_deal:,.0f}",    "Mean Value",       "blue"),
        (c3, "✅", active,                  "Active Nodes",     "indigo"),
        (c4, "⚠️", overdue_n,              "System Errors",    "red"),
    ]:
        col.markdown(f'<div class="metric-card {theme}"><div class="metric-icon">{icon}</div><p class="metric-val">{val}</p><p class="metric-lbl">{lbl}</p></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown("<div class='form-section'><h5 style='margin-top:0;'>Class Distribution</h5>", unsafe_allow_html=True)
        st.bar_chart(df["category"].value_counts(), height=280)
        st.markdown("</div>", unsafe_allow_html=True)
    with r1c2:
        st.markdown("<div class='form-section'><h5 style='margin-top:0;'>Acquisition Vectors</h5>", unsafe_allow_html=True)
        st.bar_chart(df["source"].value_counts(), height=280)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='form-section'><h5 style='margin-top:0;'>Capital Density by Class ($)</h5>", unsafe_allow_html=True)
    st.bar_chart(df.groupby("category")["deal_value"].sum(), height=320)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  USER MANAGEMENT  (admin only)
# ══════════════════════════════════════════════════════════════════════════════

def page_user_management():
    st.markdown('<p class="page-title">System Config</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Manage network operators and authorization protocols.</p>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👥 Operator Matrix", "➕ Provision Node"])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        users = db.get_all_users()
        if users.empty: st.info("No operators found.")
        else:
            for _, u in users.iterrows():
                initials = "".join(p[0].upper() for p in str(u["full_name"]).split()[:2])
                role_bg, role_text = ("rgba(99,102,241,0.2)", "#a855f7") if u["role"] == "admin" else ("rgba(255,255,255,0.05)", "#94a3b8")
                status_bg, status_color, status_text = ("rgba(16,185,129,0.2)", "#10b981", "ONLINE") if u["is_active"] else ("rgba(239,68,68,0.2)", "#ef4444", "OFFLINE")

                uc1, uc2, uc3 = st.columns([5, 1.2, 1.2])
                with uc1:
                    st.markdown(f"""
                    <div style="background:rgba(20, 24, 39, 0.5); backdrop-filter:blur(10px); border:1px solid rgba(255,255,255,0.05); border-radius:16px; padding:20px 24px; display:flex; align-items:center; gap:20px;">
                        <div style="width:52px; height:52px; border-radius:12px; background:{role_bg}; display:flex; align-items:center; justify-content:center; font-size:1.1rem; font-weight:800; color:{role_text};">{initials}</div>
                        <div style="flex:1;">
                            <div style="font-size:1.05rem; font-weight:800; color:#ffffff;">{u['full_name']}</div>
                            <div style="font-size:0.85rem; color:#94a3b8; margin-top:6px; display:flex; gap:10px; align-items:center;">
                                <span>@{u['username']}</span> • 
                                <span style="background:{role_bg}; color:{role_text}; padding:2px 8px; border-radius:6px; font-weight:700; font-size:0.7rem;">{u['role'].upper()}</span> • 
                                <span style="background:{status_bg}; color:{status_color}; padding:2px 8px; border-radius:6px; font-weight:700; font-size:0.7rem;">{status_text}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                with uc2:
                    st.markdown("<br style='line-height:0.8'>", unsafe_allow_html=True)
                    if u["username"] != st.session_state.get("username"):
                        if st.button("Toggle Power" if u["is_active"] else "Restore Power", key=f"tog_{u['id']}", use_container_width=True):
                            db.toggle_user_status(int(u["id"])); st.rerun()
                with uc3:
                    st.markdown("<br style='line-height:0.8'>", unsafe_allow_html=True)
                    if u["username"] != st.session_state.get("username"):
                        if st.button("🗑 Erase", key=f"del_{u['id']}", use_container_width=True):
                            db.delete_user(int(u["id"])); st.rerun()
                st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### Configuration Wizard")
        with st.form("add_user_form", clear_on_submit=True):
            ac1, ac2 = st.columns(2)
            with ac1:
                new_fullname = st.text_input("Identity Tag *", placeholder="e.g. Neo")
                new_username = st.text_input("System Handle *", placeholder="e.g. the_one")
                new_email    = st.text_input("Comms Relay", placeholder="neo@matrix.io")
            with ac2:
                new_password  = st.text_input("Access Key *", type="password", placeholder="Min 6 characters")
                new_password2 = st.text_input("Verify Key *", type="password")
                new_role      = st.selectbox("Clearance Level", ["user", "admin"])

            st.markdown("<br>", unsafe_allow_html=True)
            add_submitted = st.form_submit_button("➕ Provision Identity", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if add_submitted:
            errors = []
            if not new_fullname.strip() or not new_username.strip() or not new_password: errors.append("Missing required fields.")
            if len(new_password) < 6: errors.append("Access Key too weak.")
            if new_password != new_password2: errors.append("Keys mismatch.")
            if db.username_exists(new_username): errors.append("Handle already active.")

            if errors:
                for e in errors: st.error(f"❌ {e}")
            else:
                db.add_user({"full_name": new_fullname, "username": new_username, "email": new_email, "password_hash": hash_password(new_password), "role": new_role})
                st.success(f"✅ Protocol successful. {new_fullname} is online."); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════

if not st.session_state.get("logged_in"):
    show_login()
else:
    page = show_sidebar()
    if   "Command Center"   in page: page_dashboard()
    elif "Initialize"       in page: page_add_client()
    elif "Database"         in page: page_all_clients()
    elif "Pipeline"         in page: page_followups()
    elif "Telemetry"        in page: page_reports()
    elif "Config"           in page:
        if st.session_state.get("role") == "admin": page_user_management()
        else: st.error("🔒 ACCESS DENIED. INSUFFICIENT CLEARANCE.")
