import streamlit as st
import pandas as pd
from datetime import date, timedelta
import io
import hashlib
from database import DatabaseManager

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ClientPulse | Premium SaaS",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── 🌌 LIVE ANIMATED LIGHT MESH BACKGROUND ─────────────────────────────────────
# This creates the stunning moving gradient and floating pastel orbs
st.markdown("""
<div class="mesh-bg">
    <div class="orb orb-1"></div>
    <div class="orb orb-2"></div>
    <div class="orb orb-3"></div>
    <div class="orb orb-4"></div>
</div>
""", unsafe_allow_html=True)

# ── 💎 ULTRA-PREMIUM LIGHT GLASSMORPHISM CSS ───────────────────────────────────
st.markdown("""
<style>
/* ── Premium Font ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

*, html, body, [class*="css"], [class*="st-"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Base App Transparency to show background ── */
.stApp {
    background-color: transparent !important;
}
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.3); }

/* ── Animated Mesh Gradient Background ── */
.mesh-bg {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: -999; overflow: hidden; pointer-events: none;
    background: linear-gradient(-45deg, #f8fafc, #e0e7ff, #fae8ff, #f0f9ff);
    background-size: 400% 400%;
    animation: gradientShift 15s ease infinite;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Floating Soft Orbs */
.orb {
    position: absolute; border-radius: 50%; filter: blur(80px);
    opacity: 0.6; animation: floatOrb 20s infinite alternate cubic-bezier(0.4, 0, 0.2, 1);
}
.orb-1 { width: 50vw; height: 50vw; top: -10vw; left: -10vw; background: #c7d2fe; animation-delay: 0s; }
.orb-2 { width: 45vw; height: 45vw; bottom: -5vw; right: -10vw; background: #fbcfe8; animation-delay: -5s; }
.orb-3 { width: 35vw; height: 35vw; top: 30vh; left: 40vw; background: #bae6fd; animation-delay: -10s; }
.orb-4 { width: 30vw; height: 30vw; bottom: 20vh; left: -5vw; background: #ddd6fe; animation-delay: -15s; }

@keyframes floatOrb {
    0% { transform: translate(0, 0) scale(1); }
    50% { transform: translate(30px, -50px) scale(1.05); }
    100% { transform: translate(-40px, 30px) scale(0.95); }
}

/* ── Animations ── */
@keyframes slideUpFade {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

/* ── Hide Chrome on Login ── */
.login-mode header, .login-mode [data-testid="stSidebar"], .login-mode footer { display: none !important; }

/* ── Glassmorphic Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.6) !important;
    backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    border-right: 1px solid rgba(255,255,255,0.8) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.02);
}
[data-testid="stSidebarNav"] { padding-top: 0 !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 6px; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: transparent; border-radius: 12px; padding: 12px 16px !important;
    font-size: 0.95rem !important; font-weight: 600 !important; color: #475569 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); border: 1px solid transparent; cursor: pointer;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: rgba(255,255,255,0.8) !important; color: #0f172a !important;
    transform: translateX(4px); box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    border: 1px solid rgba(255,255,255,0.9);
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-baseweb="radio"] { display: flex; }

/* ── Main Area ── */
.main .block-container { 
    padding: 3rem 4rem !important; max-width: 1440px; 
    animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* ── Premium Typography ── */
.page-title { font-size: 2.4rem; font-weight: 800; color: #0f172a; margin: 0 0 4px; letter-spacing: -0.03em; }
.page-sub   { font-size: 1.05rem; color: #64748b; font-weight: 500; margin: 0 0 2.5rem; letter-spacing: 0.01em; }

/* ── Interactive Dashboard Tiles (Clickable via invisible overlay hack) ── */
div[data-testid="stHorizontalBlock"]:has(.dash-card) div[data-testid="column"] { position: relative; }
div[data-testid="stHorizontalBlock"]:has(.dash-card) [data-testid="stButton"] {
    position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 999;
}
div[data-testid="stHorizontalBlock"]:has(.dash-card) [data-testid="stButton"] button {
    width: 100%; height: 100%; opacity: 0; cursor: pointer; background: transparent; border: none;
}

.dash-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.9);
    border-radius: 20px; padding: 28px 24px; position: relative; overflow: hidden;
    transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1); margin-bottom: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
}
.dash-card::after { 
    content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 4px;
    background: transparent; transition: background 0.4s ease;
}
div[data-testid="column"]:has(button:hover) .dash-card {
    transform: translateY(-6px);
    background: rgba(255, 255, 255, 0.95);
    box-shadow: 0 20px 40px -10px rgba(0,0,0,0.1), 0 0 20px rgba(255,255,255,0.5);
}
div[data-testid="column"]:has(button:hover) .dash-card.indigo::after { background: linear-gradient(90deg, #6366f1, #818cf8); }
div[data-testid="column"]:has(button:hover) .dash-card.blue::after   { background: linear-gradient(90deg, #0ea5e9, #38bdf8); }
div[data-testid="column"]:has(button:hover) .dash-card.red::after    { background: linear-gradient(90deg, #ef4444, #f87171); }
div[data-testid="column"]:has(button:hover) .dash-card.purple::after { background: linear-gradient(90deg, #8b5cf6, #c084fc); }

.metric-icon { font-size: 2rem; margin-bottom: 16px; }
.metric-val  { font-size: 2.6rem; font-weight: 800; color: #0f172a; margin: 0 0 4px; line-height: 1; letter-spacing: -0.02em; }
.metric-lbl  { font-size: 0.85rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; margin: 0; }

/* ── Light Glassmorphic Forms & Containers ── */
.form-section {
    background: rgba(255, 255, 255, 0.65);
    backdrop-filter: blur(24px); -webkit-backdrop-filter: blur(24px);
    border-radius: 20px; padding: 32px 36px;
    border: 1px solid rgba(255,255,255,0.9);
    box-shadow: 0 8px 32px rgba(0,0,0,0.04);
    margin-bottom: 24px;
}
.form-section h5 { color: #0f172a; font-weight: 800; margin-bottom: 20px; font-size: 1.15rem; letter-spacing: -0.01em;}

/* ── Custom Inputs ── */
[data-baseweb="input"] > div, [data-baseweb="select"] > div, [data-baseweb="textarea"] > div {
    border-radius: 12px !important; background-color: rgba(255,255,255,0.7) !important;
    border: 1px solid rgba(0,0,0,0.08) !important; transition: all 0.2s ease !important;
}
[data-baseweb="input"] > div:hover, [data-baseweb="select"] > div:hover { border-color: rgba(0,0,0,0.15) !important; background-color: rgba(255,255,255,0.9) !important;}
[data-baseweb="input"] > div:focus-within, [data-baseweb="select"] > div:focus-within {
    border-color: #6366f1 !important; box-shadow: 0 0 0 4px rgba(99,102,241,0.15) !important; background-color: #ffffff !important;
}
input, textarea { font-size: 0.95rem !important; color: #0f172a !important; font-weight: 500 !important; }
.stSelectbox label, .stTextInput label, .stNumberInput label, .stDateInput label { color: #475569 !important; font-weight: 600 !important; font-size: 0.85rem !important; }

/* ── Smooth Premium Buttons ── */
.stButton > button {
    border-radius: 12px !important; font-weight: 700 !important; font-size: 0.95rem !important;
    padding: 0.6rem 1.4rem !important; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    border: 1px solid rgba(0,0,0,0.05) !important; background: rgba(255,255,255,0.8) !important; color: #334155 !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03) !important;
}
.stButton > button:hover { 
    background: #ffffff !important; transform: translateY(-2px) !important; 
    box-shadow: 0 8px 20px rgba(0,0,0,0.08) !important; border-color: rgba(0,0,0,0.1) !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important; border: none !important;
    color: white !important; box-shadow: 0 8px 20px rgba(79, 70, 229, 0.25) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #4338ca 0%, #6d28d9 100%) !important;
    box-shadow: 0 12px 25px rgba(79, 70, 229, 0.4) !important; transform: translateY(-2px) scale(1.02) !important;
}

/* ── Beautiful Alert Strips ── */
.strip { 
    background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); border-radius: 16px; padding: 20px 24px; margin-bottom: 16px; 
    border: 1px solid rgba(255,255,255,0.9); border-left-width: 4px; display: flex; flex-direction: column; gap: 8px; transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0,0,0,0.02);
}
.strip:hover { transform: translateX(6px); background: #ffffff; box-shadow: 0 8px 25px rgba(0,0,0,0.05); }
.strip-today { border-left-color: #3b82f6; }
.strip-overdue { border-left-color: #ef4444; }
.strip-ok { border-left-color: #10b981; align-items: center; text-align: center; }

.strip-header { display: flex; justify-content: space-between; align-items: center; }
.strip-title { font-size: 1.1rem; font-weight: 800; color: #0f172a; margin: 0; }
.strip-badge { font-size: 0.75rem; font-weight: 800; padding: 4px 12px; border-radius: 20px; text-transform: uppercase; letter-spacing: 0.05em;}
.badge-blue { background: #e0f2fe; color: #0284c7; }
.badge-red { background: #fee2e2; color: #b91c1c; }

.strip-meta { display: flex; gap: 16px; font-size: 0.85rem; color: #475569; font-weight: 600; margin: 0; }
.strip-notes { margin: 6px 0 0; padding-top: 12px; border-top: 1px dashed rgba(0,0,0,0.08); font-size: 0.85rem; color: #64748b; }

/* ── Expanders, Dividers, Tabs ── */
.streamlit-expanderHeader {
    font-weight: 700 !important; color: #0f172a !important;
    background: rgba(255,255,255,0.6) !important; border-radius: 12px !important; border: 1px solid rgba(255,255,255,0.8) !important;
}
details { border: none !important; border-radius: 12px !important; background: transparent; overflow: hidden; }
hr { border: none; border-top: 1px solid rgba(0,0,0,0.06); margin: 2rem 0; }

[data-baseweb="tab-list"] { gap: 30px; border-bottom: 2px solid rgba(0,0,0,0.05) !important; padding-bottom: 4px; }
[data-baseweb="tab"] { font-weight: 700 !important; font-size: 1.05rem !important; color: #64748b !important; background: transparent !important; border: none !important; padding: 8px 4px !important; transition: color 0.3s ease; }
[aria-selected="true"] { color: #4f46e5 !important; border-bottom: 2px solid #4f46e5 !important; }
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
#  LOGIN PAGE (Bright Glassmorphism Portal)
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
        background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(30px); -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(255, 255, 255, 0.9) !important;
        border-radius: 32px; padding: 56px 48px !important; width: 100%; max-width: 440px; margin: 0 auto;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.1), 0 0 0 1px rgba(0,0,0,0.02);
        animation: slideUpFade 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }
    </style>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown("""
        <div style="text-align:center; margin-bottom:40px;">
            <div style="width: 72px; height: 72px; background: linear-gradient(135deg, #4f46e5, #9333ea); 
                        border-radius: 22px; display: flex; align-items: center; justify-content: center; 
                        font-size: 32px; margin: 0 auto 24px; box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3); color:white;">✨</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: #0f172a; letter-spacing: -0.02em; margin-bottom: 8px;">ClientPulse CRM</div>
            <div style="font-size: 0.95rem; color: #64748b; font-weight: 500; letter-spacing: 0.02em;">Sign in to your premium workspace</div>
        </div>
        """, unsafe_allow_html=True)

        username = st.text_input("Work Email / Handle", placeholder="Enter your username")
        password = st.text_input("Security Key", type="password", placeholder="Enter your password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Enter Workspace ➜", use_container_width=True, type="primary")

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
                    st.error("❌ Invalid authentication.")

        st.markdown("""
        <div style="text-align:center; margin-top:32px; font-size:0.8rem; color:#94a3b8; font-weight:600; text-transform:uppercase; letter-spacing:0.1em;">
            Secure Encrypted Session
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

def show_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding: 32px 16px 40px; display: flex; align-items: center; gap: 14px;">
            <div style="width: 44px; height: 44px; background: linear-gradient(135deg, #4f46e5, #9333ea); 
                        border-radius: 14px; display: flex; align-items: center; justify-content: center; 
                        font-size: 22px; box-shadow: 0 6px 15px rgba(79, 70, 229, 0.25); color:white;">✨</div>
            <div>
                <div style="font-size: 1.4rem; font-weight: 800; color: #0f172a; letter-spacing: -0.02em; line-height: 1;">ClientPulse</div>
                <div style="font-size: 0.65rem; color: #6366f1; text-transform: uppercase; letter-spacing: 0.15em; font-weight: 800; margin-top: 6px;">Workspace</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        role = st.session_state.get("role", "user")
        full_name = st.session_state.get("full_name", "User")
        username  = st.session_state.get("username", "")

        initials = "".join(p[0].upper() for p in full_name.split()[:2])
        st.markdown(f"""
        <div style="background: rgba(255,255,255,0.8); border: 1px solid rgba(255,255,255,1); border-radius: 16px; padding: 16px; margin: 0 16px 32px; display: flex; align-items: center; gap: 14px; box-shadow: 0 4px 15px rgba(0,0,0,0.02);">
            <div style="width: 46px; height: 46px; border-radius: 12px; background: #e0e7ff; border: 1px solid #c7d2fe;
                        display: flex; align-items: center; justify-content: center; font-size: 1rem; font-weight: 800; color: #4f46e5; flex-shrink: 0;">
                {initials}
            </div>
            <div style="overflow: hidden;">
                <div style="font-size: 0.95rem; font-weight: 800; color: #0f172a; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{full_name}</div>
                <div style="font-size: 0.75rem; color: #64748b; font-weight: 600; margin-top: 4px; text-transform:uppercase; letter-spacing:0.05em;">
                    {'🛡️ Admin' if role == 'admin' else '👤 User Profile'}
                </div>
            </div>
        </div>
        <div style="padding: 0 16px; font-size: 0.7rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px;">Main Navigation</div>
        """, unsafe_allow_html=True)

        nav_options = ["🏠  Dashboard Hub", "➕  Add New Client", "👥  Directory Grid", "📅  Task Pipeline", "📊  Analytics"]
        if role == "admin":
            nav_options.append("⚙️  Workspace Settings")

        page = st.radio("Navigation", nav_options, label_visibility="collapsed")

        st.markdown("<div style='height:1px;background:rgba(0,0,0,0.06);margin:32px 16px 24px;'></div>", unsafe_allow_html=True)
        
        if st.button("🚪  Log Out securely", use_container_width=True):
            for k in ["logged_in","username","role","full_name","user_id","show_today","dash_view"]:
                st.session_state.pop(k, None)
            st.rerun()

    return page


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD (Interactive Light Glass Tiles)
# ══════════════════════════════════════════════════════════════════════════════

def page_dashboard():
    st.markdown('<p class="page-title">Dashboard Hub</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-sub">Welcome back, <b>{st.session_state.get("full_name","User")}</b>. Here is your overview for today.</p>', unsafe_allow_html=True)

    total = db.get_total_clients()
    today_df  = db.get_todays_followups()
    over_df   = db.get_overdue_followups()
    upc_df    = db.get_upcoming_followups(7)

    if "dash_view" not in st.session_state:
        st.session_state.dash_view = "today"

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f'<div class="metric-card dash-card indigo"><div class="metric-icon">👥</div><p class="metric-val">{total}</p><p class="metric-lbl">Total Clients</p></div>', unsafe_allow_html=True)
        if st.button(" ", key="btn_tot", use_container_width=True): st.session_state.dash_view = "total"

    with c2:
        st.markdown(f'<div class="metric-card dash-card blue"><div class="metric-icon">⚡</div><p class="metric-val">{len(today_df)}</p><p class="metric-lbl">Due Today</p></div>', unsafe_allow_html=True)
        if st.button("  ", key="btn_tod", use_container_width=True): st.session_state.dash_view = "today"

    with c3:
        st.markdown(f'<div class="metric-card dash-card red"><div class="metric-icon">⚠️</div><p class="metric-val">{len(over_df)}</p><p class="metric-lbl">Overdue Actions</p></div>', unsafe_allow_html=True)
        if st.button("   ", key="btn_ovr", use_container_width=True): st.session_state.dash_view = "overdue"

    with c4:
        st.markdown(f'<div class="metric-card dash-card purple"><div class="metric-icon">📅</div><p class="metric-val">{len(upc_df)}</p><p class="metric-lbl">Next 7 Days</p></div>', unsafe_allow_html=True)
        if st.button("    ", key="btn_upc", use_container_width=True): st.session_state.dash_view = "upcoming"

    st.markdown("<hr>", unsafe_allow_html=True)

    view = st.session_state.dash_view

    if view == "today":
        st.markdown("<h4 style='color:#0f172a; font-weight:800; margin-bottom:20px;'>⚡ Action Required Today</h4>", unsafe_allow_html=True)
        if today_df.empty:
            st.markdown('<div class="strip strip-ok"><div style="font-size:2rem;margin-bottom:8px;opacity:0.9;">☕</div><p class="strip-title">Inbox Zero</p><p class="strip-meta">Take a break, no calls scheduled for today.</p></div>', unsafe_allow_html=True)
        else:
            for _, r in today_df.iterrows():
                st.markdown(f"""
                <div class="strip strip-today">
                    <div class="strip-header">
                        <p class="strip-title">{r['name']} <span style="color:#64748b; font-weight:500;">· {r['company']}</span></p>
                        <span class="strip-badge badge-blue">{r['category']}</span>
                    </div>
                    <div class="strip-meta">
                        <span>📞 {r['phone'] or 'N/A'}</span>
                        <span>✉️ {r['email'] or 'N/A'}</span>
                    </div>
                    <p class="strip-notes">📝 {r['notes'] or 'No supplemental notes.'}</p>
                </div>""", unsafe_allow_html=True)

    elif view == "overdue":
        st.markdown("<h4 style='color:#0f172a; font-weight:800; margin-bottom:20px;'>⚠️ Overdue Tasks</h4>", unsafe_allow_html=True)
        if over_df.empty:
            st.markdown('<div class="strip strip-ok"><div style="font-size:2rem;margin-bottom:8px;opacity:0.9;">✅</div><p class="strip-title">Perfect Health</p><p class="strip-meta">No overdue actions detected.</p></div>', unsafe_allow_html=True)
        else:
            for _, r in over_df.iterrows():
                d = (date.today() - pd.to_datetime(r['next_followup']).date()).days
                st.markdown(f"""
                <div class="strip strip-overdue">
                    <div class="strip-header">
                        <p class="strip-title">{r['name']} <span style="color:#64748b; font-weight:500;">· {r['company']}</span></p>
                        <span class="strip-badge badge-red">{d} Days Overdue</span>
                    </div>
                    <div class="strip-meta">
                        <span>📞 {r['phone'] or 'N/A'}</span>
                        <span>✉️ {r['email'] or 'N/A'}</span>
                    </div>
                </div>""", unsafe_allow_html=True)

    elif view == "total":
        st.markdown("<h4 style='color:#0f172a; font-weight:800; margin-bottom:20px;'>👥 Complete Client Grid</h4>", unsafe_allow_html=True)
        df = db.get_all_clients()
        if df.empty:
            st.info("Database is currently empty.")
        else:
            df["Status"] = df.apply(status_label, axis=1)
            show_cols = ["name", "company", "category", "Status", "next_followup", "deal_value"]
            st.dataframe(df[show_cols], use_container_width=True, hide_index=True)

    elif view == "upcoming":
        st.markdown("<h4 style='color:#0f172a; font-weight:800; margin-bottom:20px;'>📅 7-Day Forecasting</h4>", unsafe_allow_html=True)
        if upc_df.empty:
            st.info("No events scheduled for the upcoming 7-day window.")
        else:
            upc_df["Days Until"] = upc_df["next_followup"].apply(lambda x: (pd.to_datetime(x).date() - date.today()).days)
            st.dataframe(upc_df[["name", "company", "category", "next_followup", "Days Until"]], use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ADD CLIENT
# ══════════════════════════════════════════════════════════════════════════════

def page_add_client():
    st.markdown('<p class="page-title">Add New Client</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Enter credentials to establish a new client in the database.</p>', unsafe_allow_html=True)

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
            <div style="background:#f8fafc; border:1px dashed #cbd5e1; border-radius:16px; padding:24px; text-align:center;">
                <p style="font-size:0.75rem; font-weight:800; color:#6366f1; text-transform:uppercase; letter-spacing:0.1em; margin:0;">Next Scheduled Contact</p>
                <p style="font-size:1.6rem; font-weight:800; color:#0f172a; margin:8px 0;">{nf.strftime("%A, %B %d, %Y")}</p>
                <p style="font-size:0.85rem; color:#64748b; font-weight:600; margin:0;">
                    Task will generate in <span style="color:#0f172a; font-weight:800;">{int(followup_days)} days</span>
                </p>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 📝 Context Notes")
        notes = st.text_area("Client Background", placeholder="Enter specific requirements, meeting notes...", height=120)
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("💾 Save to Database", type="primary", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("❌ Full Name is required.")
        else:
            ok = db.add_client({
                "name": name, "email": email, "phone": phone,
                "company": company, "category": category, "source": source,
                "last_contacted": str(last_contacted), "followup_days": int(followup_days),
                "next_followup": str(nf), "deal_value": deal_value, "notes": notes,
                "created_by": st.session_state.get("user_id", 1)
            })
            if ok:
                st.success(f"✅ Success! **{name}** added. Follow-up scheduled for **{nf.strftime('%b %d')}**.")
            else:
                st.error("❌ Database insertion failed.")


# ══════════════════════════════════════════════════════════════════════════════
#  ALL CLIENTS 
# ══════════════════════════════════════════════════════════════════════════════

def page_all_clients():
    st.markdown('<p class="page-title">Directory Grid</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Global view of all registered clients and operational statuses.</p>', unsafe_allow_html=True)

    st.markdown('<div class="form-section" style="padding: 24px;">', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns([3, 1, 1])
    with fc1: search = st.text_input("🔍 Search Database", placeholder="Search by name, company, or email...", label_visibility="collapsed")
    with fc2: cat    = st.selectbox("Category Filter", ["All","Lead","Prospect","Active Client","Partner","VIP","Churned"], label_visibility="collapsed")
    with fc3: srt    = st.selectbox("Sort By", ["Next Follow-up","Name","Company","Deal Value"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    df = db.get_all_clients(search=search or None, category=cat if cat != "All" else None, sort_by=srt)

    if df.empty:
        st.info("📭 No clients found matching criteria.")
        return

    hc1, hc2 = st.columns([5, 1])
    with hc1: st.markdown(f"<p style='color:#64748b; font-size:0.95rem; font-weight:600; padding-top:10px;'>{len(df)} Records found</p>", unsafe_allow_html=True)
    with hc2:
        st.download_button("📥 Export to Excel", data=to_excel(df), file_name=f"CRM_Export_{date.today()}.xlsx", use_container_width=True)

    df["Status"]     = df.apply(status_label, axis=1)
    df["Deal Value"] = df["deal_value"].apply(lambda x: f"${x:,.0f}" if x else "—")

    show_cols = ["name","company","phone","email","category","next_followup","Status","Deal Value"]
    rename    = {"name":"Full Name","company":"Company","phone":"Phone","email":"Email",
                 "category":"Class","next_followup":"Action Date"}

    st.dataframe(df[show_cols].rename(columns=rename), use_container_width=True, height=500, hide_index=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#0f172a; font-weight:800; margin-bottom:16px;'>⚡ Quick Actions</h4>", unsafe_allow_html=True)
    
    st.markdown('<div class="form-section" style="padding: 24px;">', unsafe_allow_html=True)
    rc1, rc2, rc3, rc4 = st.columns([3, 1, 1, 1])
    with rc1: 
        st.markdown("<div style='font-size:0.8rem; font-weight:700; color:#64748b; margin-bottom:4px;'>Select Target</div>", unsafe_allow_html=True)
        sel = st.selectbox("Target", df["name"].tolist(), label_visibility="collapsed")
    with rc2: 
        st.markdown("<div style='font-size:0.8rem; font-weight:700; color:#64748b; margin-bottom:4px;'>New Follow-up Date</div>", unsafe_allow_html=True)
        new_d = st.date_input("Date", value=date.today() + timedelta(days=7), label_visibility="collapsed")
    with rc3:
        st.markdown("<br style='line-height:1.2'>", unsafe_allow_html=True)
        if st.button("Update Date", type="primary", use_container_width=True):
            cid = int(df[df["name"] == sel]["id"].values[0])
            db.update_followup(cid, str(new_d))
            st.rerun()
    with rc4:
        st.markdown("<br style='line-height:1.2'>", unsafe_allow_html=True)
        if st.button("🗑 Delete Record", use_container_width=True):
            cid = int(df[df["name"] == sel]["id"].values[0])
            db.delete_client(cid)
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  FOLLOW-UPS
# ══════════════════════════════════════════════════════════════════════════════

def page_followups():
    st.markdown('<p class="page-title">Task Pipeline</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Actionable view of pending and upcoming communications.</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔴 OVERDUE TASKS", "⚡ TODAY'S QUEUE", "📅 UPCOMING SCHEDULE"])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        ov = db.get_overdue_followups()
        if ov.empty: st.success("🎉 You're fully caught up! No overdue tasks.")
        else:
            for _, r in ov.iterrows():
                days_over = (date.today() - pd.to_datetime(r["next_followup"]).date()).days
                with st.expander(f"🔴 {r['name']} // {r['company']} [-{days_over} Days]"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.markdown(f"**📞 Phone:** {r['phone'] or '—'}")
                        st.markdown(f"**✉️ Email:** {r['email'] or '—'}")
                    with cc2:
                        st.markdown(f"**💰 Projected Value:** {'${:,.0f}'.format(r['deal_value']) if r['deal_value'] else '—'}")
                        st.markdown(f"**📅 Was Due:** {pd.to_datetime(r['next_followup']).strftime('%b %d, %Y')}")
                    st.markdown(f"**📝 Notes:**<br> <span style='color:#64748b;'>{r['notes'] or 'None'}</span>", unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
                    nd = st.number_input("Reschedule In (Days)", min_value=1, value=7, key=f"ov_{r['id']}")
                    if st.button("✅ Mark Done & Reschedule", type="primary", key=f"ovb_{r['id']}"):
                        db.update_followup(int(r["id"]), str(date.today() + timedelta(days=nd)), update_last_contacted=True)
                        st.rerun()

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        td = db.get_todays_followups()
        if td.empty: st.info("📭 Today's queue is empty. Relax!")
        else:
            for _, r in td.iterrows():
                with st.expander(f"⚡ {r['name']} // {r['company']}"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.markdown(f"**📞 Phone:** {r['phone'] or '—'}")
                        st.markdown(f"**✉️ Email:** {r['email'] or '—'}")
                    with cc2:
                        st.markdown(f"**🏷 Class:** {r['category']}")
                        st.markdown(f"**💰 Value:** {'${:,.0f}'.format(r['deal_value']) if r['deal_value'] else '—'}")
                    st.markdown(f"**📝 Notes:**<br> <span style='color:#64748b;'>{r['notes'] or 'None'}</span>", unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
                    nd = st.number_input("Next Follow-up In (Days)", min_value=1, value=int(r["followup_days"]), key=f"td_{r['id']}")
                    if st.button("✅ Complete Task", type="primary", key=f"tdb_{r['id']}"):
                        db.update_followup(int(r["id"]), str(date.today() + timedelta(days=nd)), update_last_contacted=True)
                        st.rerun()

    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        days_ahead = st.slider("Forecast Range (Days)", 1, 90, 30)
        up = db.get_upcoming_followups(days_ahead)
        if up.empty: st.info(f"No tasks scheduled in the next {days_ahead} days.")
        else:
            up["Days Left"] = up["next_followup"].apply(lambda x: (pd.to_datetime(x).date() - date.today()).days)
            st.dataframe(up[["name","company","phone","category","next_followup","Days Left"]], use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════════════════════
#  REPORTS
# ══════════════════════════════════════════════════════════════════════════════

def page_reports():
    st.markdown('<p class="page-title">Analytics Dashboard</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Visual breakdown of your pipeline and network health.</p>', unsafe_allow_html=True)

    df = db.get_all_clients()
    if df.empty: return st.info("Not enough data to generate charts.")

    today_d = date.today()
    total_deal = df["deal_value"].sum()
    avg_deal   = df["deal_value"].mean()
    active     = len(df[df["category"] == "Active Client"])
    overdue_n  = len(df[df["next_followup"].apply(lambda x: pd.to_datetime(x).date() < today_d if pd.notna(x) else False)])

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, val, lbl, theme in [
        (c1, "💰", f"${total_deal:,.0f}",  "Total Pipeline",    "green"),
        (c2, "📊", f"${avg_deal:,.0f}",    "Average Deal",      "blue"),
        (c3, "✅", active,                  "Active Accounts",   "indigo"),
        (c4, "⚠️", overdue_n,              "Overdue Tasks",     "red"),
    ]:
        col.markdown(f'<div class="metric-card {theme}"><div class="metric-icon">{icon}</div><p class="metric-val">{val}</p><p class="metric-lbl">{lbl}</p></div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown("<div class='form-section'><h5 style='margin-top:0;'>Client Categories</h5>", unsafe_allow_html=True)
        st.bar_chart(df["category"].value_counts(), height=280)
        st.markdown("</div>", unsafe_allow_html=True)
    with r1c2:
        st.markdown("<div class='form-section'><h5 style='margin-top:0;'>Acquisition Channels</h5>", unsafe_allow_html=True)
        st.bar_chart(df["source"].value_counts(), height=280)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='form-section'><h5 style='margin-top:0;'>Pipeline Value by Category ($)</h5>", unsafe_allow_html=True)
    st.bar_chart(df.groupby("category")["deal_value"].sum(), height=320)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  USER MANAGEMENT  (admin only)
# ══════════════════════════════════════════════════════════════════════════════

def page_user_management():
    st.markdown('<p class="page-title">Workspace Settings</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Manage team access and permissions.</p>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👥 Team Directory", "➕ Add New User"])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        users = db.get_all_users()
        if users.empty: st.info("No users found.")
        else:
            for _, u in users.iterrows():
                initials = "".join(p[0].upper() for p in str(u["full_name"]).split()[:2])
                role_bg, role_text = ("#e0e7ff", "#4f46e5") if u["role"] == "admin" else ("#f1f5f9", "#475569")
                status_bg, status_color, status_text = ("#dcfce7", "#16a34a", "ACTIVE") if u["is_active"] else ("#fee2e2", "#dc2626", "INACTIVE")

                uc1, uc2, uc3 = st.columns([5, 1.2, 1.2])
                with uc1:
                    st.markdown(f"""
                    <div style="background:rgba(255,255,255,0.8); backdrop-filter:blur(10px); border:1px solid rgba(255,255,255,1); border-radius:16px; padding:20px 24px; display:flex; align-items:center; gap:20px; box-shadow:0 4px 10px rgba(0,0,0,0.02);">
                        <div style="width:52px; height:52px; border-radius:12px; background:{role_bg}; display:flex; align-items:center; justify-content:center; font-size:1.1rem; font-weight:800; color:{role_text};">{initials}</div>
                        <div style="flex:1;">
                            <div style="font-size:1.05rem; font-weight:800; color:#0f172a;">{u['full_name']}</div>
                            <div style="font-size:0.85rem; color:#64748b; margin-top:6px; display:flex; gap:10px; align-items:center;">
                                <span>@{u['username']}</span> • 
                                <span style="background:{role_bg}; color:{role_text}; padding:2px 8px; border-radius:6px; font-weight:800; font-size:0.7rem;">{u['role'].upper()}</span> • 
                                <span style="background:{status_bg}; color:{status_color}; padding:2px 8px; border-radius:6px; font-weight:800; font-size:0.7rem;">{status_text}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                with uc2:
                    st.markdown("<br style='line-height:0.8'>", unsafe_allow_html=True)
                    if u["username"] != st.session_state.get("username"):
                        if st.button("Suspend" if u["is_active"] else "Restore", key=f"tog_{u['id']}", use_container_width=True):
                            db.toggle_user_status(int(u["id"])); st.rerun()
                with uc3:
                    st.markdown("<br style='line-height:0.8'>", unsafe_allow_html=True)
                    if u["username"] != st.session_state.get("username"):
                        if st.button("🗑 Delete", key=f"del_{u['id']}", use_container_width=True):
                            db.delete_user(int(u["id"])); st.rerun()
                st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### New User Configuration")
        with st.form("add_user_form", clear_on_submit=True):
            ac1, ac2 = st.columns(2)
            with ac1:
                new_fullname = st.text_input("Full Name *", placeholder="e.g. Alex Smith")
                new_username = st.text_input("Username *", placeholder="e.g. alex.smith")
                new_email    = st.text_input("Email", placeholder="alex@company.com")
            with ac2:
                new_password  = st.text_input("Password *", type="password", placeholder="Min 6 characters")
                new_password2 = st.text_input("Confirm Password *", type="password")
                new_role      = st.selectbox("Role", ["user", "admin"])

            st.markdown("<br>", unsafe_allow_html=True)
            add_submitted = st.form_submit_button("➕ Create Account", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if add_submitted:
            errors = []
            if not new_fullname.strip() or not new_username.strip() or not new_password: errors.append("Missing required fields.")
            if len(new_password) < 6: errors.append("Password too short.")
            if new_password != new_password2: errors.append("Passwords do not match.")
            if db.username_exists(new_username): errors.append("Username already taken.")

            if errors:
                for e in errors: st.error(f"❌ {e}")
            else:
                db.add_user({"full_name": new_fullname, "username": new_username, "email": new_email, "password_hash": hash_password(new_password), "role": new_role})
                st.success(f"✅ Success! {new_fullname} added to the workspace."); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════

if not st.session_state.get("logged_in"):
    show_login()
else:
    page = show_sidebar()
    if   "Dashboard"        in page: page_dashboard()
    elif "Add"              in page: page_add_client()
    elif "Directory"        in page: page_all_clients()
    elif "Pipeline"         in page: page_followups()
    elif "Analytics"        in page: page_reports()
    elif "Settings"         in page:
        if st.session_state.get("role") == "admin": page_user_management()
        else: st.error("🔒 Security: You must be an Admin to access settings.")
