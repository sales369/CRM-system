import streamlit as st
import pandas as pd
from datetime import date, timedelta
import io
import hashlib
from database import DatabaseManager

# ── 1. CORE SETUP ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ClientPulse OS | Premium",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 2. GLOBAL LIVE THEME BACKGROUND ENGINE ─────────────────────────────────────
st.markdown("""
<div class="mesh-engine">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
</div>
""", unsafe_allow_html=True)

# ── 3. ENTERPRISE CSS ARCHITECTURE ─────────────────────────────────────────────
st.markdown("""
<style>
/* --- FONT ISOLATION --- */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css-"], p, span, h1, h2, h3, h4, h5, h6, div, label, input, button, select, textarea, table, th, td {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* Force Streamlit icons to keep their native font */
.material-icons, .material-symbols-rounded, [class*="stIcon"], svg, [data-testid="stIconMaterial"] {
    font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
}

/* --- LIVE THEME BACKGROUND SYSTEM --- */
.stApp { background: transparent !important; }
.mesh-engine {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: -9999; overflow: hidden; pointer-events: none;
    /* Beautiful shifting live gradient */
    background: linear-gradient(120deg, #f8fafc, #eef2ff, #fdf4ff, #e0f2fe);
    background-size: 300% 300%;
    animation: liveThemeShift 15s ease infinite alternate;
}

@keyframes liveThemeShift { 
    0% { background-position: 0% 50%; filter: hue-rotate(0deg); } 
    50% { background-position: 100% 50%; filter: hue-rotate(15deg); } 
    100% { background-position: 0% 50%; filter: hue-rotate(30deg); } 
}

.orb {
    position: absolute; border-radius: 50%; filter: blur(90px);
    opacity: 0.6; animation: auraFloat 20s infinite alternate cubic-bezier(0.4, 0, 0.2, 1);
}
.orb-1 { width: 50vw; height: 50vw; top: -10vw; left: -10vw; background: #c7d2fe; }
.orb-2 { width: 40vw; height: 40vw; bottom: -5vw; right: -5vw; background: #fbcfe8; animation-delay: -5s; }
.orb-3 { width: 45vw; height: 45vw; top: 30vh; left: 35vw; background: #bae6fd; animation-delay: -10s; }
@keyframes auraFloat { 0% { transform: translate(0,0) scale(1); } 100% { transform: translate(30px,-30px) scale(1.05); } }

/* --- GLOBAL LAYOUT & SCROLLBAR --- */
/* Reduced padding so everything fits on one screen without scrolling */
.main .block-container { 
    padding: 1.5rem 3rem !important; max-width: 1440px; 
    animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
@keyframes slideUpFade { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }

::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(15,23,42,0.15); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(15,23,42,0.3); }

/* --- HIDE CHROME ON LOGIN --- */
.login-mode header, .login-mode [data-testid="stSidebar"], .login-mode footer { display: none !important; }
header { background: transparent !important; }

/* --- GLASSMORPHIC SIDEBAR --- */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.5) !important;
    backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    border-right: 1px solid rgba(255,255,255,0.7) !important;
    box-shadow: 4px 0 24px rgba(15, 23, 42, 0.02);
}
[data-testid="stSidebarNav"] { padding-top: 0 !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 6px; padding: 0 10px; }
[data-testid="stSidebar"] .stRadio label {
    background: transparent; border-radius: 12px; padding: 12px 16px !important;
    font-size: 0.95rem !important; font-weight: 600 !important; color: #475569 !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); cursor: pointer; border: 1px solid transparent;
}
[data-testid="stSidebar"] .stRadio label:hover, [data-testid="stSidebar"] .stRadio label[data-checked="true"] {
    background: rgba(255,255,255,0.9) !important; color: #0f172a !important;
    transform: translateX(4px); box-shadow: 0 4px 12px rgba(15,23,42,0.03); border: 1px solid rgba(255,255,255,1);
}
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] { display: flex; }

/* --- TYPOGRAPHY --- */
.page-title { font-size: 2rem; font-weight: 800; color: #0f172a; margin: 0 0 4px; letter-spacing: -0.04em; }
.page-sub   { font-size: 1rem; color: #475569; font-weight: 500; margin: 0 0 1rem; letter-spacing: 0.01em; }


/* ══════════════════════════════════════════════════════════════════════════
   🚀 THE FLAWLESS UNIFIED BUTTON-TILE ENGINE (NO WHITE BOXES)
   ══════════════════════════════════════════════════════════════════════════ */

/* 1. Make the column relative to anchor the button */
.main [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] { 
    position: relative !important; 
}

/* 2. Visual Card Styling (Normal document flow so it sets the height automatically) */
.dash-card {
    height: 110px !important; /* Smaller height to prevent scrolling */
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.9); border-radius: 16px; 
    padding: 16px 20px; position: relative; overflow: hidden;
    transition: all 0.3s ease; margin: 0 !important;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.03);
    display: flex; flex-direction: column; justify-content: center;
    z-index: 1;
}

/* 3. The Absolute Button Overlay Hack */
/* This targets Streamlit's button wrapper and stretches it perfectly over the card */
.main [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] div[data-testid="stButton"] {
    position: absolute !important; 
    top: 0 !important; left: 0 !important; 
    width: 100% !important; height: 100% !important; 
    z-index: 10 !important; margin: 0 !important; padding: 0 !important;
}

/* 4. Make the button itself completely invisible but clickable */
.main [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"] div[data-testid="stButton"] button {
    width: 100% !important; height: 100% !important; 
    opacity: 0 !important; cursor: pointer !important; 
    background: transparent !important; border: none !important; 
    color: transparent !important; box-shadow: none !important;
}

/* Bottom Glow Indicator */
.dash-card::after { 
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 4px;
    background: transparent; transition: background 0.3s ease;
}

/* Card Hover Interactions (Triggered by hovering the invisible button!) */
.main [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card {
    transform: translateY(-4px); background: rgba(255, 255, 255, 0.95);
    box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.08), 0 0 15px rgba(255,255,255,0.6);
    border: 1px solid rgba(255, 255, 255, 1);
}
.main [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card.indigo::after { background: linear-gradient(90deg, #6366f1, #818cf8); }
.main [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card.blue::after   { background: linear-gradient(90deg, #0ea5e9, #38bdf8); }
.main [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card.red::after    { background: linear-gradient(90deg, #ef4444, #f87171); }
.main [data-testid="stHorizontalBlock"]:first-of-type [data-testid="column"]:hover .dash-card.purple::after { background: linear-gradient(90deg, #8b5cf6, #c084fc); }

/* Tile Typography */
.metric-icon { font-size: 1.8rem; margin-bottom: 6px; line-height: 1; text-shadow: 0 2px 8px rgba(0,0,0,0.05); }
.metric-val  { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin: 0 0 2px; line-height: 1; letter-spacing: -0.03em; }
.metric-lbl  { font-size: 0.75rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin: 0; }

/* ── MODERN GLASS FORMS ── */
.form-section {
    background: rgba(255, 255, 255, 0.6); backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    border-radius: 20px; padding: 28px 32px; border: 1px solid rgba(255,255,255,0.9);
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.04); margin-bottom: 20px;
}
.form-section h5 { color: #0f172a; font-weight: 800; margin-bottom: 20px; font-size: 1.1rem; letter-spacing: -0.02em;}

/* Inputs */
[data-baseweb="input"] > div, [data-baseweb="select"] > div, [data-baseweb="textarea"] > div {
    border-radius: 12px !important; background-color: rgba(255,255,255,0.6) !important;
    border: 1px solid rgba(15, 23, 42, 0.08) !important; transition: all 0.2s ease !important;
}
[data-baseweb="input"] > div:hover, [data-baseweb="select"] > div:hover { border-color: rgba(15, 23, 42, 0.15) !important; background-color: rgba(255,255,255,0.9) !important;}
[data-baseweb="input"] > div:focus-within, [data-baseweb="select"] > div:focus-within { border-color: #6366f1 !important; box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.15) !important; background-color: #ffffff !important; }

/* ── PREMIUM BUTTONS ── */
.stButton > button {
    border-radius: 12px !important; font-weight: 700 !important; font-size: 0.9rem !important;
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
    border: 1px solid rgba(255,255,255,1); border-left-width: 5px; display: flex; flex-direction: column; gap: 8px; transition: all 0.2s ease;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02);
}
.strip:hover { transform: translateX(6px); background: #ffffff; box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04); }
.strip-today { border-left-color: #3b82f6; }
.strip-overdue { border-left-color: #ef4444; }
.strip-ok { border-left-color: #10b981; align-items: center; text-align: center; }

.strip-header { display: flex; justify-content: space-between; align-items: center; }
.strip-title { font-size: 1.05rem; font-weight: 800; color: #0f172a; margin: 0; }
.strip-badge { font-size: 0.7rem; font-weight: 800; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em;}
.badge-blue { background: #e0f2fe; color: #0284c7; }
.badge-red { background: #fee2e2; color: #b91c1c; }
.strip-meta { display: flex; gap: 18px; font-size: 0.85rem; color: #475569; font-weight: 600; margin: 0; }

/* ── TABS & TABLES ── */
[data-baseweb="tab-list"] { gap: 30px; border-bottom: 2px solid rgba(15, 23, 42, 0.05) !important; padding-bottom: 4px; }
[data-baseweb="tab"] { font-weight: 700 !important; font-size: 1rem !important; color: #64748b !important; background: transparent !important; border: none !important; transition: color 0.2s ease; }
[aria-selected="true"] { color: #4f46e5 !important; border-bottom: 3px solid #4f46e5 !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  DB + AUTH
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
    nf = pd.to_datetime(row["next_followup"]).date() if pd.notna(row["next_followup"]) else None
    if not nf: return "—"
    d = date.today()
    if nf < d:  return f"🔴 Overdue ({(d - nf).days}d)"
    if nf == d: return "🟡 Due Today"
    return f"🟢 In {(nf - d).days}d"


# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN PORTAL
# ══════════════════════════════════════════════════════════════════════════════

def show_login():
    st.markdown("""
    <style>
    .main .block-container { display: flex; flex-direction: column; align-items: center; justify-content: center; min-height: 100vh; padding: 0 !important; }
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.75); backdrop-filter: blur(30px); -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 1) !important; border-radius: 28px; padding: 48px 44px !important; width: 100%; max-width: 420px; margin: 0 auto;
        box-shadow: 0 25px 50px -12px rgba(15, 23, 42, 0.08), inset 0 0 0 1px rgba(255,255,255,0.5);
    }
    </style>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown("""
        <div style="text-align:center; margin-bottom:32px;">
            <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #4f46e5, #9333ea); 
                        border-radius: 18px; display: flex; align-items: center; justify-content: center; 
                        font-size: 28px; margin: 0 auto 20px; box-shadow: 0 8px 20px rgba(79, 70, 229, 0.3); color:white;">✨</div>
            <div style="font-size: 1.6rem; font-weight: 800; color: #0f172a; letter-spacing: -0.02em; margin-bottom: 6px;">ClientPulse OS</div>
            <div style="font-size: 0.9rem; color: #64748b; font-weight: 500;">Sign in to your workspace</div>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Handle", placeholder="Enter your username")
        password = st.text_input("Access Key", type="password", placeholder="Enter your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Authenticate ➜", use_container_width=True, type="primary")

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
                else: st.error("❌ Invalid authentication.")

        st.markdown("<div style='text-align:center; margin-top:24px; font-size:0.75rem; color:#94a3b8; font-weight:600; text-transform:uppercase; letter-spacing:0.1em;'>Encrypted Session</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

def show_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding: 16px 16px 32px; display: flex; align-items: center; gap: 12px;">
            <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #4f46e5, #9333ea); 
                        border-radius: 10px; display: flex; align-items: center; justify-content: center; 
                        font-size: 20px; box-shadow: 0 4px 12px rgba(79, 70, 229, 0.25); color:white;">✨</div>
            <div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #0f172a; letter-spacing: -0.02em; line-height: 1;">ClientPulse</div>
                <div style="font-size: 0.6rem; color: #6366f1; text-transform: uppercase; letter-spacing: 0.15em; font-weight: 800; margin-top: 4px;">Workspace</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        role = st.session_state.get("role", "user")
        full_name = st.session_state.get("full_name", "User")
        initials = "".join(p[0].upper() for p in full_name.split()[:2])

        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.9); border: 1px solid rgba(255,255,255,1); border-radius: 14px; padding: 12px 14px; margin: 0 16px 24px; display: flex; align-items: center; gap: 12px; box-shadow: 0 4px 12px rgba(15, 23, 42, 0.02);">
            <div style="width: 38px; height: 38px; border-radius: 8px; background: #e0e7ff; border: 1px solid #c7d2fe; display: flex; align-items: center; justify-content: center; font-size: 0.95rem; font-weight: 800; color: #4f46e5; flex-shrink: 0;">{initials}</div>
            <div style="overflow: hidden;">
                <div style="font-size: 0.85rem; font-weight: 800; color: #0f172a; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{full_name}</div>
                <div style="font-size: 0.65rem; color: #64748b; font-weight: 600; margin-top: 2px; text-transform:uppercase; letter-spacing:0.05em;">{'🛡️ Admin' if role == 'admin' else '👤 User'}</div>
            </div>
        </div>
        <div style="padding: 0 16px; font-size: 0.7rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px;">Navigation</div>
        """, unsafe_allow_html=True)

        nav_options = ["🏠  Dashboard Hub", "➕  Initialize Client", "👥  Directory Grid"]
        if role == "admin": nav_options.append("⚙️  Access Control")

        page = st.radio("Navigation", nav_options, label_visibility="collapsed")
        st.markdown("<div style='height:1px;background:rgba(15, 23, 42, 0.06);margin:24px 16px 20px;'></div>", unsafe_allow_html=True)
        
        if st.button("🚪  Secure Logout", use_container_width=True):
            for k in ["logged_in","username","role","full_name","user_id","dash_view"]: st.session_state.pop(k, None)
            st.rerun()

    return page


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD HUB
# ══════════════════════════════════════════════════════════════════════════════

def page_dashboard():
    st.markdown('<p class="page-title">Dashboard Hub</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-sub">Welcome back, <b>{st.session_state.get("full_name","User")}</b>. Here is your overview for today.</p>', unsafe_allow_html=True)

    total = db.get_total_clients()
    today_df  = db.get_todays_followups()
    over_df   = db.get_overdue_followups()
    upc_df    = db.get_upcoming_followups(7)

    if "dash_view" not in st.session_state: st.session_state.dash_view = "today"

    c1, c2, c3, c4 = st.columns(4)

    # Empty string inside the button ensures no text is rendered, and CSS forces it to stretch over the card
    with c1:
        st.markdown(f'<div class="dash-card indigo"><div class="metric-icon">👥</div><p class="metric-val">{total}</p><p class="metric-lbl">Total Network</p></div>', unsafe_allow_html=True)
        if st.button(" ", key="t_tot"): st.session_state.dash_view = "total"

    with c2:
        st.markdown(f'<div class="dash-card blue"><div class="metric-icon">⚡</div><p class="metric-val">{len(today_df)}</p><p class="metric-lbl">Active Today</p></div>', unsafe_allow_html=True)
        if st.button(" ", key="t_tod"): st.session_state.dash_view = "today"

    with c3:
        st.markdown(f'<div class="dash-card red"><div class="metric-icon">⚠️</div><p class="metric-val">{len(over_df)}</p><p class="metric-lbl">Critical Overdue</p></div>', unsafe_allow_html=True)
        if st.button(" ", key="t_ovr"): st.session_state.dash_view = "overdue"

    with c4:
        st.markdown(f'<div class="dash-card purple"><div class="metric-icon">📅</div><p class="metric-val">{len(upc_df)}</p><p class="metric-lbl">7-Day Forecast</p></div>', unsafe_allow_html=True)
        if st.button(" ", key="t_upc"): st.session_state.dash_view = "upcoming"

    # Minimal spacing below the tiles, no massive gaps
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    view = st.session_state.dash_view

    if view == "today":
        st.markdown("<h4 style='color:#0f172a; font-weight:800; margin-bottom:16px;'>⚡ Action Required Today</h4>", unsafe_allow_html=True)
        if today_df.empty: st.markdown('<div class="strip strip-ok"><div style="font-size:2rem;margin-bottom:8px;opacity:0.9;">☕</div><p class="strip-title">Inbox Zero</p><p class="strip-meta">Take a break, no calls scheduled for today.</p></div>', unsafe_allow_html=True)
        else:
            for _, r in today_df.iterrows():
                st.markdown(f"""
                <div class="strip strip-today">
                    <div class="strip-header"><p class="strip-title">{r['name']} <span style="color:#64748b; font-weight:500;">· {r['company']}</span></p><span class="strip-badge badge-blue">{r['category']}</span></div>
                    <div class="strip-meta"><span>📞 {r['phone'] or 'N/A'}</span><span>✉️ {r['email'] or 'N/A'}</span></div>
                    <p class="strip-notes">📝 {r['notes'] or 'No supplemental notes.'}</p>
                </div>""", unsafe_allow_html=True)

    elif view == "overdue":
        st.markdown("<h4 style='color:#0f172a; font-weight:800; margin-bottom:16px;'>⚠️ Overdue Tasks</h4>", unsafe_allow_html=True)
        if over_df.empty: st.markdown('<div class="strip strip-ok"><div style="font-size:2rem;margin-bottom:8px;opacity:0.9;">✅</div><p class="strip-title">Perfect Health</p><p class="strip-meta">No overdue actions detected.</p></div>', unsafe_allow_html=True)
        else:
            for _, r in over_df.iterrows():
                d = (date.today() - pd.to_datetime(r['next_followup']).date()).days
                st.markdown(f"""
                <div class="strip strip-overdue">
                    <div class="strip-header"><p class="strip-title">{r['name']} <span style="color:#64748b; font-weight:500;">· {r['company']}</span></p><span class="strip-badge badge-red">{d} Days Overdue</span></div>
                    <div class="strip-meta"><span>📞 {r['phone'] or 'N/A'}</span><span>✉️ {r['email'] or 'N/A'}</span></div>
                </div>""", unsafe_allow_html=True)

    elif view == "total":
        st.markdown("<h4 style='color:#0f172a; font-weight:800; margin-bottom:16px;'>👥 Complete Client Grid</h4>", unsafe_allow_html=True)
        df = db.get_all_clients()
        if df.empty: st.info("Database is currently empty.")
        else:
            df["Status"] = df.apply(status_label, axis=1)
            st.dataframe(df[["name", "company", "category", "Status", "next_followup", "deal_value"]], use_container_width=True, hide_index=True)

    elif view == "upcoming":
        st.markdown("<h4 style='color:#0f172a; font-weight:800; margin-bottom:16px;'>📅 7-Day Forecasting</h4>", unsafe_allow_html=True)
        if upc_df.empty: st.info("No events scheduled for the upcoming 7-day window.")
        else:
            upc_df["Days Until"] = upc_df["next_followup"].apply(lambda x: (pd.to_datetime(x).date() - date.today()).days)
            st.dataframe(upc_df[["name", "company", "category", "next_followup", "Days Until"]], use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  INITIALIZE CLIENT
# ══════════════════════════════════════════════════════════════════════════════

def page_add_client():
    st.markdown('<p class="page-title">Initialize Client</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Enter credentials to establish a new entity in the database.</p>', unsafe_allow_html=True)

    with st.form("add_client_form", clear_on_submit=True):
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 👤 Personal Details")
        c1, c2 = st.columns(2)
        with c1:
            name    = st.text_input("Full Name *", placeholder="e.g. Jane Doe")
            email   = st.text_input("Email Address", placeholder="e.g. jane@company.com")
            company = st.text_input("Company", placeholder="e.g. Acme Corp")
        with c2:
            phone    = st.text_input("Phone Number", placeholder="+1 555-0199")
            category = st.selectbox("Classification", ["Lead", "Prospect", "Active Client", "Partner", "VIP", "Churned"])
            source   = st.selectbox("Origin Source", ["Referral", "Website", "LinkedIn", "Cold Outreach", "Event", "Other"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 📅 Pipeline Scheduling")
        c3, c4 = st.columns(2)
        with c3:
            last_contacted = st.date_input("Last Contact Date", value=date.today())
            followup_days  = st.number_input("Follow-up Interval (Days) *", min_value=1, max_value=365, value=5)
            deal_value     = st.number_input("Estimated Value ($)", min_value=0, value=0, step=5000)
        with c4:
            nf = last_contacted + timedelta(days=int(followup_days))
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.5); border:1px solid rgba(255,255,255,0.8); border-radius:16px; padding:20px; text-align:center;">
                <p style="font-size:0.7rem; font-weight:800; color:#6366f1; text-transform:uppercase; letter-spacing:0.1em; margin:0;">Computed Contact Date</p>
                <p style="font-size:1.4rem; font-weight:800; color:#0f172a; margin:4px 0;">{nf.strftime("%A, %B %d, %Y")}</p>
                <p style="font-size:0.8rem; color:#64748b; font-weight:600; margin:0;">
                    Task will trigger in <span style="color:#0f172a; font-weight:800;">{int(followup_days)} days</span>
                </p>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 📝 Context Notes")
        notes = st.text_area("Entity Background", placeholder="Enter specific requirements, meeting notes...", height=100)
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("💾 Write to Database", type="primary", use_container_width=True)

    if submitted:
        if not name.strip(): st.error("❌ Full Name is required.")
        else:
            ok = db.add_client({"name": name, "email": email, "phone": phone, "company": company, "category": category, "source": source, "last_contacted": str(last_contacted), "followup_days": int(followup_days), "next_followup": str(nf), "deal_value": deal_value, "notes": notes, "created_by": st.session_state.get("user_id", 1)})
            if ok: st.success(f"✅ Success! **{name}** added. Follow-up scheduled for **{nf.strftime('%b %d')}**.")
            else: st.error("❌ Database insertion failed.")


# ══════════════════════════════════════════════════════════════════════════════
#  DIRECTORY GRID
# ══════════════════════════════════════════════════════════════════════════════

def page_all_clients():
    st.markdown('<p class="page-title">Directory Grid</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Global view of all registered entities and operational statuses.</p>', unsafe_allow_html=True)

    st.markdown('<div class="form-section" style="padding: 24px;">', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns([3, 1, 1])
    with fc1: search = st.text_input("🔍 Search Database", placeholder="Search by name, company, or email...", label_visibility="collapsed")
    with fc2: cat    = st.selectbox("Category Filter", ["All","Lead","Prospect","Active Client","Partner","VIP","Churned"], label_visibility="collapsed")
    with fc3: srt    = st.selectbox("Sort By", ["Next Follow-up","Name","Company","Deal Value"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    df = db.get_all_clients(search=search or None, category=cat if cat != "All" else None, sort_by=srt)

    if df.empty: return st.info("📭 No records found matching criteria.")

    hc1, hc2 = st.columns([5, 1])
    with hc1: st.markdown(f"<p style='color:#64748b; font-size:0.95rem; font-weight:600; padding-top:10px;'>{len(df)} Records found</p>", unsafe_allow_html=True)
    with hc2: st.download_button("📥 Extract Data", data=to_excel(df), file_name=f"Data_Export_{date.today()}.xlsx", use_container_width=True)

    df["Status"]     = df.apply(status_label, axis=1)
    df["Deal Value"] = df["deal_value"].apply(lambda x: f"${x:,.0f}" if x else "—")

    show_cols = ["name","company","phone","email","category","next_followup","Status","Deal Value"]
    rename    = {"name":"Designation","company":"Affiliation","phone":"Comms","email":"Routing", "category":"Class","next_followup":"Action Date"}

    st.dataframe(df[show_cols].rename(columns=rename), use_container_width=True, height=500, hide_index=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0f172a; font-weight:800; margin-bottom:16px;'>⚡ Execute Override</h4>", unsafe_allow_html=True)
    
    st.markdown('<div class="form-section" style="padding: 24px;">', unsafe_allow_html=True)
    rc1, rc2, rc3, rc4 = st.columns([3, 1, 1, 1])
    with rc1: 
        st.markdown("<div style='font-size:0.8rem; font-weight:700; color:#64748b; margin-bottom:4px;'>Select Target</div>", unsafe_allow_html=True)
        sel = st.selectbox("Target", df["name"].tolist(), label_visibility="collapsed")
    with rc2: 
        st.markdown("<div style='font-size:0.8rem; font-weight:700; color:#64748b; margin-bottom:4px;'>New Temporal Coordinate</div>", unsafe_allow_html=True)
        new_d = st.date_input("Date", value=date.today() + timedelta(days=7), label_visibility="collapsed")
    with rc3:
        st.markdown("<br style='line-height:1.2'>", unsafe_allow_html=True)
        if st.button("Update Date", type="primary", use_container_width=True):
            cid = int(df[df["name"] == sel]["id"].values[0]); db.update_followup(cid, str(new_d)); st.rerun()
    with rc4:
        st.markdown("<br style='line-height:1.2'>", unsafe_allow_html=True)
        if st.button("🗑 Terminate Record", use_container_width=True):
            cid = int(df[df["name"] == sel]["id"].values[0]); db.delete_client(cid); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ACCESS CONTROL (Clean, Simple, Minimalist UI)
# ══════════════════════════════════════════════════════════════════════════════

def page_user_management():
    st.markdown('<p class="page-title">Access Control</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Easily manage workspace members and their authorization levels.</p>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👥 Active Users", "➕ Add User"])

    with tab1:
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
                    <div style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(10px); padding: 16px 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,1); box-shadow: 0 4px 10px rgba(0,0,0,0.02);">
                        <div style="font-size: 1.05rem; font-weight: 800; color: #0f172a; margin-bottom: 2px;">{u['full_name']} <span style="color: #64748b; font-weight: 500; font-size: 0.85rem;">(@{u['username']})</span></div>
                        <div style="font-size: 0.8rem; font-weight: 600; color: #475569;">{role_badge} &nbsp;|&nbsp; {status_badge}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with c2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if u["username"] != st.session_state.get("username"):
                        if st.button("Suspend" if u["is_active"] else "Restore", key=f"tog_{u['id']}", use_container_width=True): 
                            db.toggle_user_status(int(u["id"])); st.rerun()
                    else:
                        st.markdown("<div style='text-align: center; margin-top: 10px; font-weight: 700; color: #10b981; font-size: 0.85rem;'>Current User</div>", unsafe_allow_html=True)
                        
                with c3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if u["username"] != st.session_state.get("username"):
                        if st.button("Delete", key=f"del_{u['id']}", use_container_width=True): 
                            db.delete_user(int(u["id"])); st.rerun()

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### Add New Member")
        with st.form("add_user_form", clear_on_submit=True):
            new_fullname = st.text_input("Full Name *", placeholder="e.g. Alex Smith")
            new_username = st.text_input("Username *", placeholder="e.g. alex.smith")
            new_password  = st.text_input("Password *", type="password", placeholder="Min 6 characters")
            new_role      = st.selectbox("Role", ["user", "admin"])

            st.markdown("<br>", unsafe_allow_html=True)
            add_submitted = st.form_submit_button("➕ Create Account", type="primary", use_container_width=True)
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
                st.success(f"✅ Success! {new_fullname} added to the workspace."); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════

if not st.session_state.get("logged_in"): show_login()
else:
    page = show_sidebar()
    
    if   "Dashboard"        in page: page_dashboard()
    elif "Initialize"       in page: page_add_client()
    elif "Directory"        in page: page_all_clients()
    elif "Access Control"   in page:
        if st.session_state.get("role") == "admin": page_user_management()
        else: st.error("🔒 ACCESS DENIED: You must be an Admin to access settings.")
