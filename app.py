import streamlit as st
import pandas as pd
from datetime import date, timedelta
import io
import hashlib
from database import DatabaseManager

st.set_page_config(
    page_title="ClientPulse CRM",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
#  MASTER CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    box-sizing: border-box;
}

/* ── Animated login background ── */
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
@keyframes floatOrb {
    0%, 100% { transform: translateY(0px) translateX(0px) scale(1); }
    33%       { transform: translateY(-40px) translateX(20px) scale(1.05); }
    66%       { transform: translateY(20px) translateX(-15px) scale(0.95); }
}
@keyframes floatOrb2 {
    0%, 100% { transform: translateY(0px) translateX(0px) scale(1); }
    33%       { transform: translateY(30px) translateX(-25px) scale(1.08); }
    66%       { transform: translateY(-20px) translateX(30px) scale(0.92); }
}
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(24px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse-ring {
    0%   { box-shadow: 0 0 0 0 rgba(99,102,241,0.4); }
    70%  { box-shadow: 0 0 0 14px rgba(99,102,241,0); }
    100% { box-shadow: 0 0 0 0 rgba(99,102,241,0); }
}
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position: 200% center; }
}
@keyframes countUp {
    from { opacity: 0; transform: scale(0.7); }
    to   { opacity: 1; transform: scale(1); }
}
@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-20px); }
    to   { opacity: 1; transform: translateX(0); }
}
@keyframes blink-dot {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.2; }
}

/* ── Hide Streamlit chrome on login ── */
[data-testid="stAppViewContainer"] > section:first-child { padding: 0 !important; }
.login-active header { display: none !important; }
.login-active [data-testid="stSidebar"] { display: none !important; }
.login-active footer { display: none !important; }
.login-active .main .block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #080e1a !important;
    border-right: 1px solid #1a2540 !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.4);
}
[data-testid="stSidebar"] section { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: #8892a4 !important; }
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 3px; display: flex; flex-direction: column; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: transparent !important;
    border-radius: 10px !important;
    padding: 11px 16px !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    color: #8892a4 !important;
    transition: all 0.2s ease !important;
    border: 1px solid transparent !important;
    cursor: pointer;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: #111827 !important;
    color: #e2e8f0 !important;
    border-color: #1e293b !important;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-checked="true"],
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
    background: linear-gradient(135deg, #1e1b4b, #1e3a5f) !important;
    color: #a5b4fc !important;
    border-color: #312e81 !important;
}

/* ── Main area ── */
.main { background: #f0f2f8 !important; }
.main .block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1500px !important;
}

/* ── Metric cards ── */
.metric-card {
    background: white;
    border-radius: 18px;
    padding: 24px;
    border: 1px solid #e8edf5;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(.4,0,.2,1);
    cursor: default;
    animation: fadeSlideUp 0.5s ease both;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 18px 18px 0 0;
}
.metric-card.blue::before  { background: linear-gradient(90deg, #6366f1, #818cf8); }
.metric-card.teal::before  { background: linear-gradient(90deg, #0f766e, #14b8a6); }
.metric-card.red::before   { background: linear-gradient(90deg, #dc2626, #f87171); }
.metric-card.violet::before{ background: linear-gradient(90deg, #7c3aed, #a78bfa); }
.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(99,102,241,0.15);
    border-color: #c7d2fe;
}
.metric-card .metric-icon {
    width: 44px; height: 44px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.3rem; margin-bottom: 14px;
}
.metric-card .metric-icon.blue   { background: #eef2ff; }
.metric-card .metric-icon.teal   { background: #f0fdfa; }
.metric-card .metric-icon.red    { background: #fef2f2; }
.metric-card .metric-icon.violet { background: #f5f3ff; }
.metric-val { font-size: 2rem; font-weight: 800; color: #0f172a; margin: 0 0 2px; line-height: 1; animation: countUp 0.6s ease both; }
.metric-lbl { font-size: 0.72rem; font-weight: 600; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.07em; margin: 0; }
.metric-trend { font-size: 0.75rem; font-weight: 600; margin-top: 8px; }
.metric-trend.up   { color: #10b981; }
.metric-trend.warn { color: #f59e0b; }

/* ── Page header ── */
.page-header {
    display: flex; align-items: center; gap: 14px;
    margin-bottom: 28px;
    animation: slideInLeft 0.4s ease both;
}
.page-header-icon {
    width: 48px; height: 48px; border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    background: linear-gradient(135deg, #eef2ff, #e0e7ff);
    border: 1px solid #c7d2fe;
}
.page-title { font-size: 1.6rem; font-weight: 800; color: #0f172a; margin: 0; letter-spacing: -0.02em; }
.page-sub   { font-size: 0.83rem; color: #64748b; margin: 2px 0 0; }

/* ── Cards ── */
.glass-card {
    background: white;
    border-radius: 16px;
    border: 1px solid #e8edf5;
    padding: 24px 28px;
    margin-bottom: 20px;
    transition: box-shadow 0.2s;
}
.glass-card:hover { box-shadow: 0 4px 20px rgba(99,102,241,0.08); }

/* ── Scheduled badge ── */
.sched-badge {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border: 1px solid #86efac;
    border-radius: 14px;
    padding: 18px 20px;
    animation: fadeSlideUp 0.4s ease both;
}
.sched-date { font-size: 1.25rem; font-weight: 800; color: #15803d; margin: 4px 0 0; }
.sched-lbl  { font-size: 0.68rem; font-weight: 700; color: #16a34a; text-transform: uppercase; letter-spacing: 0.08em; }

/* ── Client strip cards ── */
.client-strip {
    background: white;
    border-radius: 14px;
    border: 1px solid #e8edf5;
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: all 0.2s ease;
    animation: fadeSlideUp 0.4s ease both;
}
.client-strip:hover {
    border-color: #c7d2fe;
    box-shadow: 0 4px 16px rgba(99,102,241,0.1);
    transform: translateX(4px);
}
.client-strip .avatar {
    width: 42px; height: 42px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.85rem; font-weight: 700; flex-shrink: 0;
    background: #eef2ff; color: #4338ca;
    border: 2px solid #c7d2fe;
}
.client-strip .info { flex: 1; min-width: 0; }
.client-strip .cname { font-size: 0.9rem; font-weight: 700; color: #0f172a; margin: 0; }
.client-strip .cmeta { font-size: 0.78rem; color: #64748b; margin: 2px 0 0; }
.status-pill {
    padding: 4px 12px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 700;
    white-space: nowrap; flex-shrink: 0;
}
.status-pill.today   { background: #eff6ff; color: #1d4ed8; border: 1px solid #bfdbfe; }
.status-pill.overdue { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.status-pill.ok      { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }

/* ── Live dot ── */
.live-dot {
    display: inline-block;
    width: 8px; height: 8px; border-radius: 50%;
    background: #22c55e; margin-right: 6px;
    animation: blink-dot 1.5s ease infinite;
}

/* ── CTA button ── */
.cta-wrap .stButton > button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    padding: 0.85rem 0 !important;
    letter-spacing: 0.01em;
    transition: all 0.3s ease !important;
    animation: pulse-ring 2.5s cubic-bezier(0.4,0,0.6,1) infinite !important;
}
.cta-wrap .stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(79,70,229,0.45) !important;
    animation: none !important;
}

/* ── Primary button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    transition: all 0.2s !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(79,70,229,0.35) !important;
}
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; }
[data-testid="stDownloadButton"] > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ── Sidebar user pill ── */
.sb-pill {
    background: #0d1526;
    border: 1px solid #1e2d45;
    border-radius: 12px;
    padding: 14px 16px;
    margin: 0 0 16px;
}

/* ── Tabs ── */
div[data-testid="stTabs"] button {
    font-weight: 600 !important;
    border-radius: 8px 8px 0 0 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #4f46e5 !important;
    border-bottom: 2px solid #4f46e5 !important;
}

/* ── Expander ── */
details {
    border-radius: 14px !important;
    border: 1px solid #e8edf5 !important;
    background: white !important;
    transition: box-shadow 0.2s !important;
}
details:hover { box-shadow: 0 4px 16px rgba(99,102,241,0.08) !important; }
details summary { font-weight: 600 !important; padding: 14px 18px !important; }

/* ── Data table ── */
.dataframe { border-radius: 14px !important; overflow: hidden !important; }
[data-testid="stDataFrame"] { border-radius: 14px !important; overflow: hidden !important; border: 1px solid #e8edf5 !important; }

/* ── Form inputs ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div,
.stTextArea > div > textarea {
    border-radius: 10px !important;
    border-color: #e2e8f0 !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea > div > textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

/* ── User row ── */
.user-row {
    background: white;
    border: 1px solid #e8edf5;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 14px;
    transition: all 0.2s ease;
}
.user-row:hover {
    border-color: #c7d2fe;
    box-shadow: 0 4px 16px rgba(99,102,241,0.08);
}

/* ── Section divider ── */
.sec-div {
    height: 1px;
    background: linear-gradient(90deg, transparent, #e2e8f0 20%, #e2e8f0 80%, transparent);
    margin: 28px 0;
}

/* ── Notification banner ── */
.notif-banner {
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 14px;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    animation: slideInLeft 0.4s ease both;
}
.notif-banner.info    { background: #eff6ff; border: 1px solid #bfdbfe; }
.notif-banner.danger  { background: #fef2f2; border: 1px solid #fecaca; }
.notif-banner.success { background: #f0fdf4; border: 1px solid #bbf7d0; }
.notif-banner .notif-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }
.notif-banner .notif-title { font-size: 0.88rem; font-weight: 700; color: #0f172a; margin: 0 0 2px; }
.notif-banner .notif-sub   { font-size: 0.78rem; color: #64748b; margin: 0; }

hr { border: none; border-top: 1px solid #e8edf5; margin: 1.5rem 0; }

/* ── Reports bar chart ── */
.stVegaLiteChart { border-radius: 14px !important; overflow: hidden !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  INIT
# ══════════════════════════════════════════════════════════════════════════════

@st.cache_resource
def get_db():
    db = DatabaseManager()
    db.init_user_tables()
    db.init_tables()
    db.ensure_default_admin()
    return db

db = get_db()

def hash_pw(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def to_excel(df: pd.DataFrame) -> bytes:
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="Clients")
    return out.getvalue()

def initials(name: str) -> str:
    parts = str(name).split()
    return "".join(p[0].upper() for p in parts[:2]) if parts else "?"

def status_label(row) -> str:
    nf = pd.to_datetime(row["next_followup"]).date() if pd.notna(row.get("next_followup")) else None
    if not nf: return "—"
    d = date.today()
    if nf < d:  return f"🔴 Overdue ({(d - nf).days}d)"
    if nf == d: return "🟡 Due Today"
    return f"🟢 In {(nf - d).days}d"

def page_header(icon: str, title: str, sub: str):
    st.markdown(f"""
    <div class="page-header">
        <div class="page-header-icon">{icon}</div>
        <div>
            <p class="page-title">{title}</p>
            <p class="page-sub">{sub}</p>
        </div>
    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN
# ══════════════════════════════════════════════════════════════════════════════

def show_login():
    st.markdown("""
    <style>
    header, footer, [data-testid="stSidebar"] { display: none !important; }
    .main .block-container { padding: 0 !important; max-width: 100% !important; }

    .login-bg {
        min-height: 100vh;
        background: linear-gradient(-45deg, #0a0f1e, #0f1e3d, #0d1b2a, #060b18, #1a0a2e, #0a1628);
        background-size: 400% 400%;
        animation: gradientShift 12s ease infinite;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
        padding: 2rem;
    }
    .orb1 {
        position: absolute;
        width: 500px; height: 500px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(99,102,241,0.18) 0%, transparent 70%);
        top: -100px; left: -100px;
        animation: floatOrb 8s ease-in-out infinite;
        pointer-events: none;
    }
    .orb2 {
        position: absolute;
        width: 400px; height: 400px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(124,58,237,0.15) 0%, transparent 70%);
        bottom: -80px; right: -60px;
        animation: floatOrb2 10s ease-in-out infinite;
        pointer-events: none;
    }
    .orb3 {
        position: absolute;
        width: 250px; height: 250px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(16,185,129,0.1) 0%, transparent 70%);
        top: 50%; left: 60%;
        animation: floatOrb 14s ease-in-out infinite reverse;
        pointer-events: none;
    }
    .login-card {
        background: rgba(255,255,255,0.97);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 52px 48px;
        width: 100%;
        max-width: 420px;
        box-shadow: 0 30px 80px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.1);
        position: relative;
        z-index: 10;
        animation: fadeSlideUp 0.7s cubic-bezier(0.4,0,0.2,1) both;
    }
    .login-logo {
        text-align: center;
        margin-bottom: 36px;
    }
    .login-logo-ring {
        width: 72px; height: 72px;
        border-radius: 20px;
        background: linear-gradient(135deg, #4f46e5, #7c3aed);
        display: flex; align-items: center; justify-content: center;
        font-size: 2rem;
        margin: 0 auto 14px;
        box-shadow: 0 8px 30px rgba(79,70,229,0.4);
    }
    .login-appname {
        font-size: 1.5rem; font-weight: 800;
        color: #0f172a; letter-spacing: -0.02em; margin: 0 0 4px;
    }
    .login-tagline {
        font-size: 0.78rem; color: #94a3b8;
        font-weight: 500; letter-spacing: 0.06em;
        text-transform: uppercase; margin: 0;
    }
    .login-label {
        font-size: 0.8rem; font-weight: 600; color: #374151;
        margin-bottom: 6px; display: block;
    }
    .login-footer {
        text-align: center;
        margin-top: 28px;
        font-size: 0.75rem;
        color: #94a3b8;
    }
    .login-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        margin-bottom: 12px;
    }
    .login-feature {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 10px 12px;
        font-size: 0.75rem;
        color: #64748b;
        display: flex;
        align-items: center;
        gap: 7px;
    }
    .login-feature span { font-size: 0.9rem; }
    </style>

    <div class="login-bg">
        <div class="orb1"></div>
        <div class="orb2"></div>
        <div class="orb3"></div>
        <div class="login-card">
            <div class="login-logo">
                <div class="login-logo-ring">💼</div>
                <p class="login-appname">ClientPulse CRM</p>
                <p class="login-tagline">Your client command centre</p>
            </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Sign in →", use_container_width=True, type="primary")

    if submitted:
        if not username or not password:
            st.error("Please enter both username and password.")
        else:
            user = db.authenticate_user(username, hash_pw(password))
            if user:
                st.session_state.logged_in  = True
                st.session_state.username   = user["username"]
                st.session_state.role       = user["role"]
                st.session_state.full_name  = user["full_name"]
                st.session_state.user_id    = user["id"]
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

    st.markdown("""
            <div class="login-footer">
                <div class="login-grid">
                    <div class="login-feature"><span>📊</span> Live analytics</div>
                    <div class="login-feature"><span>🔔</span> Follow-up alerts</div>
                    <div class="login-feature"><span>📥</span> Excel export</div>
                    <div class="login-feature"><span>🔒</span> Role-based access</div>
                </div>
                Contact your admin to get access
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

def show_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="padding:28px 20px 0;text-align:center;">
            <div style="width:52px;height:52px;border-radius:15px;
                        background:linear-gradient(135deg,#4f46e5,#7c3aed);
                        display:flex;align-items:center;justify-content:center;
                        font-size:1.6rem;margin:0 auto 10px;
                        box-shadow:0 6px 20px rgba(79,70,229,0.4);">💼</div>
            <div style="font-size:1.05rem;font-weight:800;color:#f1f5f9;letter-spacing:-0.01em;">ClientPulse</div>
            <div style="font-size:0.62rem;color:#334155;text-transform:uppercase;letter-spacing:0.1em;margin:3px 0 22px;">CRM System</div>
        </div>
        """, unsafe_allow_html=True)

        role      = st.session_state.get("role","user")
        full_name = st.session_state.get("full_name","User")
        username  = st.session_state.get("username","")
        ini       = initials(full_name)
        today_count = len(db.get_todays_followups())
        over_count  = len(db.get_overdue_followups())

        st.markdown(f"""
        <div class="sb-pill">
            <div style="display:flex;align-items:center;gap:10px;">
                <div style="width:36px;height:36px;border-radius:50%;
                            background:linear-gradient(135deg,#4f46e5,#7c3aed);
                            display:flex;align-items:center;justify-content:center;
                            font-size:0.78rem;font-weight:800;color:white;flex-shrink:0;">{ini}</div>
                <div style="min-width:0;">
                    <div style="font-size:0.83rem;font-weight:700;color:#e2e8f0;
                                white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{full_name}</div>
                    <div style="font-size:0.68rem;color:#475569;">
                        {'⚙️ Admin' if role=='admin' else '👤 User'} &nbsp;·&nbsp; @{username}
                    </div>
                </div>
            </div>
            <div style="display:flex;gap:6px;margin-top:10px;">
                <div style="flex:1;background:#111827;border-radius:8px;padding:7px 10px;text-align:center;">
                    <div style="font-size:1rem;font-weight:800;color:#a5b4fc;">{today_count}</div>
                    <div style="font-size:0.6rem;color:#374151;text-transform:uppercase;letter-spacing:0.05em;">Today</div>
                </div>
                <div style="flex:1;background:#111827;border-radius:8px;padding:7px 10px;text-align:center;">
                    <div style="font-size:1rem;font-weight:800;color:#fca5a5;">{over_count}</div>
                    <div style="font-size:0.6rem;color:#374151;text-transform:uppercase;letter-spacing:0.05em;">Overdue</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="font-size:0.65rem;font-weight:600;color:#1e293b;text-transform:uppercase;letter-spacing:0.08em;padding:0 4px;margin-bottom:6px;">Menu</div>', unsafe_allow_html=True)

        nav_options = [
            "🏠  Dashboard",
            "➕  Add Client",
            "👥  All Clients",
            "📅  Follow-ups",
            "📊  Reports",
        ]
        if role == "admin":
            nav_options.append("⚙️  User Management")

        page = st.radio("Navigation", nav_options, label_visibility="collapsed")

        st.markdown(f"""
        <div style="height:1px;background:#0d1526;margin:16px 0;"></div>
        <div style="padding:12px 14px;background:#0d1526;border:1px solid #1a2540;
                    border-radius:10px;margin-bottom:12px;">
            <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px;">
                <div class="live-dot"></div>
                <span style="font-size:0.65rem;color:#334155;text-transform:uppercase;letter-spacing:0.06em;">System live</span>
            </div>
            <div style="font-size:0.82rem;font-weight:600;color:#64748b;">{date.today().strftime("%A, %b %d %Y")}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚪  Sign Out", use_container_width=True):
            for k in ["logged_in","username","role","full_name","user_id","show_today"]:
                st.session_state.pop(k, None)
            st.rerun()

    return page


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def page_dashboard():
    page_header("🏠", "Dashboard", f"Welcome back, {st.session_state.get('full_name','User')} — here's your day at a glance")

    total    = db.get_total_clients()
    today_df = db.get_todays_followups()
    over_df  = db.get_overdue_followups()
    upc_df   = db.get_upcoming_followups(7)

    c1, c2, c3, c4 = st.columns(4)
    cards = [
        (c1, "blue",   "👥", total,          "Total Clients",    "📈 Growing pipeline"),
        (c2, "teal",   "📞", len(today_df),  "Due Today",        "🔔 Needs attention" if today_df is not None and len(today_df) > 0 else "✅ Clear"),
        (c3, "red",    "⚠️", len(over_df),   "Overdue",          "🚨 Action required" if len(over_df) > 0 else "✅ All clear"),
        (c4, "violet", "📆", len(upc_df),    "Next 7 Days",      "🗓 Plan ahead"),
    ]
    for col, color, icon, val, lbl, trend in cards:
        col.markdown(f"""
        <div class="metric-card {color}">
            <div class="metric-icon {color}">{icon}</div>
            <p class="metric-val">{val}</p>
            <p class="metric-lbl">{lbl}</p>
            <p class="metric-trend {'warn' if '🚨' in trend or '🔔' in trend else 'up'}">{trend}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown('<div class="cta-wrap">', unsafe_allow_html=True)
        if st.button("🔔  Who Do I Call Today?", use_container_width=True):
            st.session_state.show_today = not st.session_state.get("show_today", False)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("show_today"):
        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        left, right = st.columns(2)

        with left:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
                <span style="font-size:1rem;font-weight:800;color:#0f172a;">📞 Call Today</span>
                <span style="background:#eff6ff;color:#1d4ed8;padding:2px 10px;
                             border-radius:20px;font-size:0.72rem;font-weight:700;
                             border:1px solid #bfdbfe;">{len(today_df)}</span>
            </div>""", unsafe_allow_html=True)

            if today_df.empty:
                st.markdown("""
                <div class="notif-banner success">
                    <div class="notif-icon">✅</div>
                    <div>
                        <p class="notif-title">All clear for today!</p>
                        <p class="notif-sub">No follow-ups scheduled. Great job staying on top.</p>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                for _, r in today_df.iterrows():
                    ini = initials(str(r["name"]))
                    st.markdown(f"""
                    <div class="client-strip">
                        <div class="avatar">{ini}</div>
                        <div class="info">
                            <p class="cname">{r['name']}</p>
                            <p class="cmeta">🏢 {r['company'] or '—'} &nbsp;·&nbsp; 📞 {r['phone'] or '—'}</p>
                            <p class="cmeta" style="margin-top:3px;">📝 {str(r['notes'])[:60] + '…' if r['notes'] and len(str(r['notes'])) > 60 else (r['notes'] or 'No notes')}</p>
                        </div>
                        <span class="status-pill today">Due Today</span>
                    </div>""", unsafe_allow_html=True)

        with right:
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:14px;">
                <span style="font-size:1rem;font-weight:800;color:#0f172a;">⚠️ Overdue</span>
                <span style="background:#fef2f2;color:#b91c1c;padding:2px 10px;
                             border-radius:20px;font-size:0.72rem;font-weight:700;
                             border:1px solid #fecaca;">{len(over_df)}</span>
            </div>""", unsafe_allow_html=True)

            if over_df.empty:
                st.markdown("""
                <div class="notif-banner success">
                    <div class="notif-icon">🎉</div>
                    <div>
                        <p class="notif-title">Zero overdue!</p>
                        <p class="notif-sub">You're on top of every client relationship.</p>
                    </div>
                </div>""", unsafe_allow_html=True)
            else:
                for _, r in over_df.iterrows():
                    d = (date.today() - pd.to_datetime(r["next_followup"]).date()).days
                    ini = initials(str(r["name"]))
                    st.markdown(f"""
                    <div class="client-strip">
                        <div class="avatar" style="background:#fef2f2;color:#b91c1c;border-color:#fecaca;">{ini}</div>
                        <div class="info">
                            <p class="cname">{r['name']}</p>
                            <p class="cmeta">🏢 {r['company'] or '—'} &nbsp;·&nbsp; 📞 {r['phone'] or '—'}</p>
                        </div>
                        <span class="status-pill overdue">{d}d overdue</span>
                    </div>""", unsafe_allow_html=True)

        if not upc_df.empty:
            st.markdown('<div class="sec-div"></div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="font-size:1rem;font-weight:800;color:#0f172a;margin-bottom:14px;">
                📆 Upcoming this week
                <span style="background:#f5f3ff;color:#5b21b6;padding:2px 10px;
                             border-radius:20px;font-size:0.72rem;font-weight:700;
                             border:1px solid #ddd6fe;margin-left:8px;">{len(upc_df)}</span>
            </div>""", unsafe_allow_html=True)
            cols = st.columns(min(len(upc_df), 3))
            for i, (_, r) in enumerate(upc_df.head(3).iterrows()):
                days_left = (pd.to_datetime(r["next_followup"]).date() - date.today()).days
                with cols[i]:
                    ini = initials(str(r["name"]))
                    st.markdown(f"""
                    <div style="background:white;border:1px solid #e8edf5;border-radius:14px;
                                padding:16px;text-align:center;transition:all 0.2s;"
                         onmouseover="this.style.borderColor='#c7d2fe';this.style.transform='translateY(-3px)'"
                         onmouseout="this.style.borderColor='#e8edf5';this.style.transform='none'">
                        <div style="width:40px;height:40px;border-radius:50%;
                                    background:linear-gradient(135deg,#eef2ff,#e0e7ff);
                                    display:flex;align-items:center;justify-content:center;
                                    font-size:0.8rem;font-weight:800;color:#4338ca;
                                    margin:0 auto 10px;">{ini}</div>
                        <p style="font-size:0.85rem;font-weight:700;color:#0f172a;margin:0 0 2px;">{r['name']}</p>
                        <p style="font-size:0.72rem;color:#64748b;margin:0 0 10px;">{r['company'] or '—'}</p>
                        <span style="background:#f5f3ff;color:#5b21b6;padding:4px 12px;
                                     border-radius:20px;font-size:0.72rem;font-weight:700;">In {days_left}d</span>
                    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ADD CLIENT
# ══════════════════════════════════════════════════════════════════════════════

def page_add_client():
    page_header("➕", "Add New Client", "Fill in the details below to create a new client record")

    with st.form("add_client_form", clear_on_submit=True):
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("##### 👤 Personal Information")
        c1, c2 = st.columns(2)
        with c1:
            name    = st.text_input("Full Name *", placeholder="Rajiv Sharma")
            email   = st.text_input("Email Address", placeholder="rajiv@company.com")
            company = st.text_input("Company / Organisation", placeholder="TechVentures Pvt Ltd")
        with c2:
            phone    = st.text_input("Phone Number", placeholder="+91 98765 43210")
            category = st.selectbox("Category", ["Lead","Prospect","Active Client","Partner","VIP","Churned"])
            source   = st.selectbox("Lead Source", ["Referral","Website","LinkedIn","Cold Outreach","Event","Other"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("##### 📅 Follow-up Schedule")
        c3, c4 = st.columns(2)
        with c3:
            last_contacted = st.date_input("Last Contacted Date", value=date.today())
            followup_days  = st.number_input("Follow-up After (days) *", min_value=1, max_value=365, value=5,
                                              help="CRM will alert you after this many days")
            deal_value     = st.number_input("Deal Value (₹)", min_value=0, value=0, step=1000)
        with c4:
            nf = last_contacted + timedelta(days=int(followup_days))
            days_from_today = (nf - date.today()).days
            st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="sched-badge">
                <p class="sched-lbl">📌 Scheduled follow-up date</p>
                <p class="sched-date">{nf.strftime("%A, %B %d %Y")}</p>
                <p style="font-size:0.78rem;color:#22c55e;margin:6px 0 0;font-weight:600;">
                    {'Today' if days_from_today == 0 else f'In {days_from_today} day{"s" if days_from_today != 1 else ""}'}
                    from last contact
                </p>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("##### 📝 Notes & Remarks")
        notes = st.text_area("Notes", placeholder="Any important context, requirements or prior conversation details…", height=100)
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("💾  Save Client", type="primary", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("❌ Full name is required.")
        else:
            ok = db.add_client({
                "name": name.strip(), "email": email, "phone": phone,
                "company": company, "category": category, "source": source,
                "last_contacted": str(last_contacted), "followup_days": int(followup_days),
                "next_followup": str(nf), "deal_value": deal_value,
                "notes": notes, "created_by": st.session_state.get("user_id", 1)
            })
            if ok:
                st.success(f"✅ **{name}** saved successfully! Follow-up scheduled for **{nf.strftime('%B %d, %Y')}**.")
                st.balloons()
            else:
                st.error("❌ Failed to save. Check your database connection.")


# ══════════════════════════════════════════════════════════════════════════════
#  ALL CLIENTS
# ══════════════════════════════════════════════════════════════════════════════

def page_all_clients():
    page_header("👥", "All Clients", "Search, filter and manage your complete client database")

    st.markdown('<div class="glass-card" style="padding:18px 22px;margin-bottom:16px;">', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns([3, 1, 1])
    with fc1: search = st.text_input("Search", placeholder="🔍  Search by name, company, email or phone…", label_visibility="collapsed")
    with fc2: cat    = st.selectbox("Category", ["All","Lead","Prospect","Active Client","Partner","VIP","Churned"], label_visibility="collapsed")
    with fc3: srt    = st.selectbox("Sort", ["Next Follow-up","Name","Company","Deal Value"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    df = db.get_all_clients(
        search=search.strip() or None,
        category=cat if cat != "All" else None,
        sort_by=srt
    )

    if df.empty:
        st.markdown("""
        <div class="notif-banner info">
            <div class="notif-icon">📭</div>
            <div>
                <p class="notif-title">No clients found</p>
                <p class="notif-sub">Try adjusting your filters or add a new client from the sidebar.</p>
            </div>
        </div>""", unsafe_allow_html=True)
        return

    hc1, hc2, hc3 = st.columns([4, 1, 1])
    with hc1:
        st.markdown(f"<p style='color:#64748b;font-size:0.85rem;margin:8px 0;'>Showing <b style='color:#0f172a;'>{len(df)}</b> client(s)</p>", unsafe_allow_html=True)
    with hc2:
        st.download_button(
            "📥 Excel", data=to_excel(df),
            file_name=f"clients_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    with hc3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

    df["Status"]     = df.apply(status_label, axis=1)
    df["Deal Value"] = df["deal_value"].apply(lambda x: f"₹{x:,.0f}" if x else "—")
    df["Company"]    = df["company"].fillna("—")

    show = df[["name","Company","phone","email","category","next_followup","Status","Deal Value"]].rename(
        columns={"name":"Name","phone":"Phone","email":"Email",
                 "category":"Category","next_followup":"Next Follow-up"})

    st.dataframe(show, use_container_width=True, height=460, hide_index=True)

    st.markdown('<div class="sec-div"></div>', unsafe_allow_html=True)
    st.markdown("##### ✏️ Quick Actions")
    ac1, ac2, ac3, ac4 = st.columns([3, 1, 1, 1])
    client_names = df["name"].tolist()
    with ac1: sel   = st.selectbox("Select client", client_names, label_visibility="collapsed")
    with ac2: new_d = st.date_input("New date", value=date.today() + timedelta(days=7), label_visibility="collapsed")
    with ac3:
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("📅 Reschedule", type="primary", use_container_width=True):
            cid = int(df[df["name"] == sel]["id"].values[0])
            db.update_followup(cid, str(new_d))
            st.success(f"✅ {sel} rescheduled to {new_d.strftime('%b %d, %Y')}")
            st.rerun()
    with ac4:
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("🗑 Delete", use_container_width=True):
            cid = int(df[df["name"] == sel]["id"].values[0])
            db.delete_client(cid)
            st.warning(f"🗑 {sel} has been deleted.")
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  FOLLOW-UPS
# ══════════════════════════════════════════════════════════════════════════════

def page_followups():
    page_header("📅", "Follow-up Calendar", "Track overdue, today's and upcoming client follow-ups")

    tab1, tab2, tab3 = st.tabs(["🔴  Overdue", "🟡  Due Today", "🟢  Upcoming"])

    with tab1:
        ov = db.get_overdue_followups()
        if ov.empty:
            st.markdown("""
            <div class="notif-banner success">
                <div class="notif-icon">🎉</div>
                <div><p class="notif-title">Zero overdue follow-ups!</p>
                <p class="notif-sub">You're on top of every client. Keep it up.</p></div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="notif-banner danger">
                <div class="notif-icon">⚠️</div>
                <div><p class="notif-title">{len(ov)} overdue contact(s) need your attention</p>
                <p class="notif-sub">These clients were supposed to be contacted in the past. Reach out now.</p></div>
            </div>""", unsafe_allow_html=True)

            for _, r in ov.iterrows():
                days_over = (date.today() - pd.to_datetime(r["next_followup"]).date()).days
                ini = initials(str(r["name"]))
                with st.expander(f"🔴  {r['name']}  ·  {r['company'] or '—'}  ·  {days_over}d overdue"):
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.markdown(f"""
                        <div style="background:#f8fafc;border-radius:12px;padding:14px 16px;">
                            <p style="font-size:0.78rem;color:#64748b;margin:0 0 8px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;">Contact Details</p>
                            <p style="margin:4px 0;font-size:0.88rem;color:#0f172a;">📞 {r['phone'] or '—'}</p>
                            <p style="margin:4px 0;font-size:0.88rem;color:#0f172a;">✉️ {r['email'] or '—'}</p>
                            <p style="margin:4px 0;font-size:0.88rem;color:#0f172a;">🏷 {r['category']}</p>
                            <p style="margin:4px 0;font-size:0.88rem;color:#0f172a;">💰 {'₹{:,.0f}'.format(r['deal_value']) if r['deal_value'] else '—'}</p>
                        </div>""", unsafe_allow_html=True)
                    with cc2:
                        st.markdown(f"""
                        <div style="background:#fef2f2;border:1px solid #fecaca;border-radius:12px;padding:14px 16px;">
                            <p style="font-size:0.78rem;color:#b91c1c;margin:0 0 6px;font-weight:700;text-transform:uppercase;">Was due</p>
                            <p style="font-size:1.1rem;font-weight:800;color:#7f1d1d;margin:0 0 6px;">{pd.to_datetime(r['next_followup']).strftime('%b %d, %Y')}</p>
                            <p style="font-size:0.78rem;color:#b91c1c;font-weight:600;">{days_over} days ago</p>
                        </div>""", unsafe_allow_html=True)
                    if r["notes"]:
                        st.info(f"📝 {r['notes']}")
                    nd = st.number_input("Reschedule follow-up in (days)", min_value=1, value=7, key=f"ov_{r['id']}")
                    if st.button("✅  Mark contacted & reschedule", key=f"ovb_{r['id']}", type="primary"):
                        db.update_followup(int(r["id"]), str(date.today() + timedelta(days=int(nd))), True)
                        st.success("✅ Updated!"); st.rerun()

    with tab2:
        td = db.get_todays_followups()
        if td.empty:
            st.markdown("""
            <div class="notif-banner info">
                <div class="notif-icon">📭</div>
                <div><p class="notif-title">No follow-ups scheduled for today</p>
                <p class="notif-sub">Enjoy a clear day or reach out to a high-value client proactively.</p></div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="notif-banner info">
                <div class="notif-icon">📞</div>
                <div><p class="notif-title">{len(td)} client(s) to contact today</p>
                <p class="notif-sub">Mark each one as contacted after you reach out.</p></div>
            </div>""", unsafe_allow_html=True)
            for _, r in td.iterrows():
                with st.expander(f"📞  {r['name']}  ·  {r['company'] or '—'}"):
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.markdown(f"""
                        <div style="background:#f8fafc;border-radius:12px;padding:14px 16px;">
                            <p style="margin:4px 0;font-size:0.88rem;color:#0f172a;">📞 {r['phone'] or '—'}</p>
                            <p style="margin:4px 0;font-size:0.88rem;color:#0f172a;">✉️ {r['email'] or '—'}</p>
                            <p style="margin:4px 0;font-size:0.88rem;color:#0f172a;">🏷 {r['category']}</p>
                        </div>""", unsafe_allow_html=True)
                    with cc2:
                        st.markdown(f"""
                        <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:14px 16px;">
                            <p style="font-size:0.78rem;color:#15803d;margin:0 0 4px;font-weight:700;">Deal value</p>
                            <p style="font-size:1.1rem;font-weight:800;color:#14532d;margin:0;">'₹{r["deal_value"]:,.0f}' if r['deal_value'] else '—'</p>
                        </div>""", unsafe_allow_html=True)
                    if r["notes"]:
                        st.info(f"📝 {r['notes']}")
                    nd = st.number_input("Next follow-up in (days)", min_value=1, value=int(r["followup_days"]), key=f"td_{r['id']}")
                    if st.button("✅  Done — set next follow-up", key=f"tdb_{r['id']}", type="primary"):
                        db.update_followup(int(r["id"]), str(date.today() + timedelta(days=int(nd))), True)
                        st.success("✅ Saved!"); st.rerun()

    with tab3:
        days_ahead = st.slider("Show upcoming follow-ups for next N days", 1, 90, 30)
        up = db.get_upcoming_followups(days_ahead)
        if up.empty:
            st.info(f"📭 No follow-ups in the next {days_ahead} days.")
        else:
            up["Days Until"] = up["next_followup"].apply(
                lambda x: (pd.to_datetime(x).date() - date.today()).days)
            up["Deal Value"] = up["deal_value"].apply(lambda x: f"₹{x:,.0f}" if x else "—")
            st.dataframe(
                up[["name","company","phone","category","next_followup","Days Until","Deal Value"]].rename(
                    columns={"name":"Name","company":"Company","phone":"Phone",
                             "category":"Category","next_followup":"Follow-up Date",
                             "Days Until":"⏳ Days","Deal Value":"💰 Value"}),
                use_container_width=True, hide_index=True
            )


# ══════════════════════════════════════════════════════════════════════════════
#  REPORTS
# ══════════════════════════════════════════════════════════════════════════════

def page_reports():
    page_header("📊", "Reports & Analytics", "Pipeline insights, deal values and exportable data")

    df = db.get_all_clients()
    if df.empty:
        st.info("📭 No client data yet. Start by adding clients."); return

    today_d   = date.today()
    total_deal = df["deal_value"].sum()
    avg_deal   = df["deal_value"].mean()
    active_n   = len(df[df["category"] == "Active Client"])
    overdue_n  = len(df[df["next_followup"].apply(
        lambda x: pd.to_datetime(x).date() < today_d if pd.notna(x) else False)])

    c1, c2, c3, c4 = st.columns(4)
    for col, color, icon, val, lbl in [
        (c1,"blue",  "💰", f"₹{total_deal:,.0f}", "Total Pipeline"),
        (c2,"teal",  "📊", f"₹{avg_deal:,.0f}",   "Avg Deal Value"),
        (c3,"violet","✅", active_n,               "Active Clients"),
        (c4,"red",   "⚠️", overdue_n,              "Overdue Follow-ups"),
    ]:
        col.markdown(f"""
        <div class="metric-card {color}">
            <div class="metric-icon {color}">{icon}</div>
            <p class="metric-val">{val}</p>
            <p class="metric-lbl">{lbl}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    r1, r2 = st.columns(2)
    with r1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("##### 📊 Clients by category")
        cat_data = df["category"].value_counts().reset_index()
        cat_data.columns = ["Category","Count"]
        st.bar_chart(cat_data.set_index("Category"), height=220, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with r2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("##### 📊 Clients by source")
        src_data = df["source"].value_counts().reset_index()
        src_data.columns = ["Source","Count"]
        st.bar_chart(src_data.set_index("Source"), height=220, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("##### 💰 Deal value by category (₹)")
    deal_data = df.groupby("category")["deal_value"].sum().reset_index()
    deal_data.columns = ["Category","Total"]
    st.bar_chart(deal_data.set_index("Category"), height=240, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("##### 📋 Category breakdown table")
    summary = df.groupby("category").agg(
        Count=("id","count"),
        Total_Value=("deal_value","sum"),
        Avg_Value=("deal_value","mean")
    ).reset_index()
    summary["Total_Value"] = summary["Total_Value"].apply(lambda x: f"₹{x:,.0f}")
    summary["Avg_Value"]   = summary["Avg_Value"].apply(lambda x: f"₹{x:,.0f}")
    summary.columns        = ["Category","Clients","Total Value","Avg Value"]
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="sec-div"></div>', unsafe_allow_html=True)
    dc1, dc2 = st.columns(2)
    with dc1:
        st.download_button(
            "📥  Download Full Report (Excel)", data=to_excel(df),
            file_name=f"crm_report_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    with dc2:
        overdue_df = db.get_overdue_followups()
        if not overdue_df.empty:
            st.download_button(
                "📥  Download Overdue List (Excel)", data=to_excel(overdue_df),
                file_name=f"overdue_{date.today()}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )


# ══════════════════════════════════════════════════════════════════════════════
#  USER MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════

def page_user_management():
    page_header("⚙️", "User Management", "Add, manage and control access for CRM users (admin only)")

    tab1, tab2 = st.tabs(["👥  All Users", "➕  Add User"])

    with tab1:
        users = db.get_all_users()
        if users.empty:
            st.info("No users found."); return

        for _, u in users.iterrows():
            ini        = initials(str(u["full_name"]))
            is_admin   = u["role"] == "admin"
            is_active  = u["is_active"]
            is_self    = u["username"] == st.session_state.get("username")
            role_bg    = "#eef2ff" if is_admin else "#f0fdf4"
            role_color = "#3730a3" if is_admin else "#15803d"
            role_lbl   = "Admin" if is_admin else "User"

            uc1, uc2, uc3 = st.columns([5, 1, 1])
            with uc1:
                st.markdown(f"""
                <div class="user-row">
                    <div style="width:42px;height:42px;border-radius:50%;
                                background:{role_bg};border:2px solid {'#c7d2fe' if is_admin else '#bbf7d0'};
                                display:flex;align-items:center;justify-content:center;
                                font-size:0.82rem;font-weight:800;color:{role_color};flex-shrink:0;">{ini}</div>
                    <div style="flex:1;min-width:0;">
                        <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;">
                            <span style="font-size:0.9rem;font-weight:700;color:#0f172a;">{u['full_name']}</span>
                            <span style="background:{role_bg};color:{role_color};padding:2px 9px;
                                         border-radius:20px;font-size:0.68rem;font-weight:700;">{role_lbl}</span>
                            {'<span style="background:#f0fdf4;color:#15803d;padding:2px 9px;border-radius:20px;font-size:0.68rem;font-weight:700;">● Active</span>' if is_active else '<span style="background:#fef2f2;color:#b91c1c;padding:2px 9px;border-radius:20px;font-size:0.68rem;font-weight:700;">● Inactive</span>'}
                            {'<span style="background:#fefce8;color:#854d0e;padding:2px 9px;border-radius:20px;font-size:0.68rem;font-weight:700;">You</span>' if is_self else ''}
                        </div>
                        <div style="font-size:0.77rem;color:#64748b;margin-top:3px;">
                            @{u['username']} &nbsp;·&nbsp; {u['email'] or '—'} &nbsp;·&nbsp;
                            Joined {pd.to_datetime(u['created_at']).strftime('%b %d, %Y') if pd.notna(u.get('created_at')) else '—'}
                        </div>
                    </div>
                </div>""", unsafe_allow_html=True)

            with uc2:
                if not is_self:
                    toggle_lbl = "Deactivate" if is_active else "Activate"
                    if st.button(toggle_lbl, key=f"tog_{u['id']}", use_container_width=True):
                        db.toggle_user_status(int(u["id"]))
                        st.rerun()

            with uc3:
                if not is_self:
                    if st.button("🗑 Delete", key=f"del_{u['id']}", use_container_width=True):
                        db.delete_user(int(u["id"]))
                        st.success(f"Deleted {u['username']}"); st.rerun()

            st.markdown("<div style='height:2px'></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("##### 🆕 New user details")

        with st.form("add_user_form", clear_on_submit=True):
            nc1, nc2 = st.columns(2)
            with nc1:
                new_fullname = st.text_input("Full Name *", placeholder="Arjun Kapoor")
                new_username = st.text_input("Username *", placeholder="arjun.kapoor")
                new_email    = st.text_input("Email", placeholder="arjun@company.com")
            with nc2:
                new_password  = st.text_input("Password *", type="password", placeholder="Min 6 characters")
                new_password2 = st.text_input("Confirm Password *", type="password", placeholder="Repeat password")
                new_role      = st.selectbox("Role", ["user","admin"],
                                             format_func=lambda x: "👤 User — standard access" if x == "user" else "⚙️ Admin — full access")

            st.markdown(f"""
            <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:12px 14px;margin-top:8px;">
                <p style="font-size:0.75rem;color:#64748b;margin:0;font-weight:500;">
                    <b>User</b> — can view, add clients and manage follow-ups &nbsp;·&nbsp;
                    <b>Admin</b> — full access including user management
                </p>
            </div>""", unsafe_allow_html=True)

            add_submitted = st.form_submit_button("➕  Create User", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if add_submitted:
            errors = []
            if not new_fullname.strip():   errors.append("Full name is required.")
            if not new_username.strip():   errors.append("Username is required.")
            if not new_password:           errors.append("Password is required.")
            if len(new_password) < 6:      errors.append("Password must be at least 6 characters.")
            if new_password != new_password2: errors.append("Passwords do not match.")
            if db.username_exists(new_username.strip()): errors.append(f"Username '@{new_username}' is already taken.")

            if errors:
                for e in errors: st.error(f"❌ {e}")
            else:
                ok = db.add_user({
                    "full_name":     new_fullname.strip(),
                    "username":      new_username.strip(),
                    "email":         new_email.strip(),
                    "password_hash": hash_pw(new_password),
                    "role":          new_role,
                })
                if ok:
                    st.success(f"✅ User **{new_fullname}** (@{new_username}) created as **{new_role}**.")
                    st.balloons()
                else:
                    st.error("❌ Failed to create user. Check database connection.")


# ══════════════════════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════════════════════

if not st.session_state.get("logged_in"):
    show_login()
else:
    page = show_sidebar()

    if   "Dashboard"       in page: page_dashboard()
    elif "Add Client"      in page: page_add_client()
    elif "All Clients"     in page: page_all_clients()
    elif "Follow-ups"      in page: page_followups()
    elif "Reports"         in page: page_reports()
    elif "User Management" in page:
        if st.session_state.get("role") == "admin":
            page_user_management()
        else:
            st.error("🔒 Access denied. This page is for admins only.")
