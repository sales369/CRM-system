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

THEMES = {
    "dark": {
        "bg":"#080e1a","sb":"#080e1a","card":"#0f172a","border":"#1e293b",
        "text":"#f1f5f9","sub":"#94a3b8","input":"#0f172a","inputborder":"#1e293b",
        "main":"#0d1117","orb1":"rgba(99,102,241,0.25)","orb2":"rgba(124,58,237,0.2)",
        "orb3":"rgba(16,185,129,0.12)","strip":"#0f172a","stripborder":"#1e293b",
        "striptext":"#f1f5f9","stripmeta":"#64748b","metric":"#0f172a","metricborder":"#1e293b",
    },
    "light": {
        "bg":"#f8faff","sb":"#ffffff","card":"#ffffff","border":"#e2e8f0",
        "text":"#0f172a","sub":"#64748b","input":"#ffffff","inputborder":"#e2e8f0",
        "main":"#f0f4ff","orb1":"rgba(99,102,241,0.12)","orb2":"rgba(124,58,237,0.1)",
        "orb3":"rgba(16,185,129,0.08)","strip":"#ffffff","stripborder":"#e2e8f0",
        "striptext":"#0f172a","stripmeta":"#64748b","metric":"#ffffff","metricborder":"#e2e8f0",
    },
    "ocean": {
        "bg":"#020917","sb":"#020917","card":"#041428","border":"#0c2d4a",
        "text":"#e0f2fe","sub":"#7dd3fc","input":"#041428","inputborder":"#0c2d4a",
        "main":"#030f1e","orb1":"rgba(14,165,233,0.25)","orb2":"rgba(6,182,212,0.2)",
        "orb3":"rgba(56,189,248,0.15)","strip":"#041428","stripborder":"#0c2d4a",
        "striptext":"#e0f2fe","stripmeta":"#7dd3fc","metric":"#041428","metricborder":"#0c2d4a",
    },
    "forest": {
        "bg":"#030d07","sb":"#030d07","card":"#071a0f","border":"#14391f",
        "text":"#dcfce7","sub":"#86efac","input":"#071a0f","inputborder":"#14391f",
        "main":"#040f08","orb1":"rgba(34,197,94,0.22)","orb2":"rgba(16,185,129,0.18)",
        "orb3":"rgba(74,222,128,0.12)","strip":"#071a0f","stripborder":"#14391f",
        "striptext":"#dcfce7","stripmeta":"#86efac","metric":"#071a0f","metricborder":"#14391f",
    },
    "rose": {
        "bg":"#130508","sb":"#130508","card":"#1f0810","border":"#4c0519",
        "text":"#ffe4e6","sub":"#fda4af","input":"#1f0810","inputborder":"#4c0519",
        "main":"#0f040a","orb1":"rgba(244,63,94,0.25)","orb2":"rgba(251,113,133,0.2)",
        "orb3":"rgba(253,164,175,0.12)","strip":"#1f0810","stripborder":"#4c0519",
        "striptext":"#ffe4e6","stripmeta":"#fda4af","metric":"#1f0810","metricborder":"#4c0519",
    },
}

if "theme" not in st.session_state:
    st.session_state.theme = "dark"

T = THEMES[st.session_state.theme]
is_light = st.session_state.theme == "light"
sb_text  = "#0f172a" if is_light else "#e2e8f0"
sb_sub   = "#64748b" if is_light else "#475569"
sb_pill  = "#f1f5f9" if is_light else "#0d1526"
sb_pill_b= "#e2e8f0" if is_light else "#1a2540"
sb_mini  = "#e2e8f0" if is_light else "#111827"
sb_live  = "#0f172a" if is_light else "#0d1526"
sb_live_b= "#e2e8f0" if is_light else "#1a2540"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
*,html,body,[class*="css"]{{font-family:'Inter',sans-serif !important;}}

@keyframes gradientShift{{0%{{background-position:0% 50%}}50%{{background-position:100% 50%}}100%{{background-position:0% 50%}}}}
@keyframes floatOrb{{0%,100%{{transform:translateY(0) translateX(0) scale(1)}}33%{{transform:translateY(-35px) translateX(18px) scale(1.04)}}66%{{transform:translateY(18px) translateX(-14px) scale(0.96)}}}}
@keyframes floatOrb2{{0%,100%{{transform:translateY(0) translateX(0) scale(1)}}33%{{transform:translateY(28px) translateX(-22px) scale(1.06)}}66%{{transform:translateY(-16px) translateX(26px) scale(0.94)}}}}
@keyframes floatOrb3{{0%,100%{{transform:translateY(0) translateX(0)}}50%{{transform:translateY(-20px) translateX(30px)}}}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(18px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes slideLeft{{from{{opacity:0;transform:translateX(-16px)}}to{{opacity:1;transform:translateX(0)}}}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0.2}}}}
@keyframes pulseGlow{{0%,100%{{box-shadow:0 0 0 0 rgba(99,102,241,0.5)}}50%{{box-shadow:0 0 0 10px rgba(99,102,241,0)}}}}
@keyframes ripple{{to{{transform:scale(2.5);opacity:0}}}}
@keyframes spinIn{{from{{opacity:0;transform:rotate(-10deg) scale(0.8)}}to{{opacity:1;transform:rotate(0) scale(1)}}}}
@keyframes countUp{{from{{opacity:0;transform:scale(0.6)}}to{{opacity:1;transform:scale(1)}}}}
@keyframes borderFlow{{0%{{background-position:0% 50%}}50%{{background-position:100% 50%}}100%{{background-position:0% 50%}}}}
@keyframes stripSlide{{from{{opacity:0;transform:translateX(-10px)}}to{{opacity:1;transform:translateX(0)}}}}
@keyframes wiggle{{0%,100%{{transform:rotate(0)}}25%{{transform:rotate(-3deg)}}75%{{transform:rotate(3deg)}}}}

header,footer{{display:none !important;}}
.main{{background:{T['main']} !important;}}
.main .block-container{{padding:1.4rem 2rem !important;max-width:1500px !important;}}

[data-testid="stSidebar"]{{background:{T['sb']} !important;border-right:1px solid {T['border']} !important;box-shadow:4px 0 30px rgba(0,0,0,0.3);}}
[data-testid="stSidebar"] *{{color:{sb_text} !important;}}
[data-testid="stSidebar"] .stRadio>label{{display:none;}}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"]{{gap:2px;}}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label{{
    background:transparent !important;border-radius:10px !important;
    padding:10px 15px !important;font-size:0.85rem !important;
    font-weight:600 !important;transition:all 0.25s cubic-bezier(.4,0,.2,1) !important;
    border:1px solid transparent !important;position:relative;overflow:hidden;
}}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover{{
    background:{'#f1f5f9' if is_light else '#111827'} !important;
    border-color:{T['border']} !important;
    transform:translateX(4px) !important;
}}

.card{{background:{T['card']};border-radius:16px;border:1px solid {T['border']};
    padding:18px 22px;margin-bottom:14px;animation:fadeUp 0.4s ease both;
    transition:box-shadow 0.25s,transform 0.25s;}}
.card:hover{{box-shadow:0 6px 28px rgba(99,102,241,0.12);}}

.metric-card{{background:{T['metric']};border-radius:16px;border:1px solid {T['metricborder']};
    padding:18px 20px;position:relative;overflow:hidden;
    transition:all 0.3s cubic-bezier(.4,0,.2,1);cursor:default;animation:fadeUp 0.5s ease both;}}
.metric-card::before{{content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:16px 16px 0 0;}}
.metric-card.blue::before{{background:linear-gradient(90deg,#6366f1,#818cf8,#6366f1);background-size:200%;animation:borderFlow 3s ease infinite;}}
.metric-card.green::before{{background:linear-gradient(90deg,#10b981,#34d399,#10b981);background-size:200%;animation:borderFlow 3s ease infinite;}}
.metric-card.red::before{{background:linear-gradient(90deg,#ef4444,#f87171,#ef4444);background-size:200%;animation:borderFlow 3s ease infinite;}}
.metric-card.amber::before{{background:linear-gradient(90deg,#f59e0b,#fbbf24,#f59e0b);background-size:200%;animation:borderFlow 3s ease infinite;}}
.metric-card:hover{{transform:translateY(-5px) scale(1.02);box-shadow:0 14px 40px rgba(99,102,241,0.18);}}
.mval{{font-size:1.9rem;font-weight:800;color:{T['text']};margin:6px 0 2px;line-height:1;animation:countUp 0.6s cubic-bezier(.4,0,.2,1) both;}}
.mlbl{{font-size:0.68rem;font-weight:700;color:{T['sub']};text-transform:uppercase;letter-spacing:0.07em;}}

.ph{{font-size:1.3rem;font-weight:800;color:{T['text']};margin:0 0 2px;letter-spacing:-0.02em;animation:slideLeft 0.4s ease both;}}
.ps{{font-size:0.78rem;color:{T['sub']};margin:0 0 16px;animation:slideLeft 0.45s ease both;}}

.strip{{background:{T['strip']};border-radius:12px;border:1px solid {T['stripborder']};
    padding:13px 16px;margin-bottom:8px;display:flex;align-items:center;gap:12px;
    transition:all 0.25s cubic-bezier(.4,0,.2,1);animation:stripSlide 0.35s ease both;position:relative;overflow:hidden;}}
.strip::after{{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;
    background:linear-gradient(180deg,#6366f1,#8b5cf6);border-radius:3px 0 0 3px;
    transform:scaleY(0);transition:transform 0.25s ease;transform-origin:bottom;}}
.strip:hover::after{{transform:scaleY(1);}}
.strip:hover{{border-color:#6366f1;transform:translateX(5px);box-shadow:0 4px 18px rgba(99,102,241,0.14);}}
.ava{{width:38px;height:38px;border-radius:50%;flex-shrink:0;
    display:flex;align-items:center;justify-content:center;
    font-size:0.78rem;font-weight:800;background:#eef2ff;color:#4338ca;
    border:2px solid #c7d2fe;transition:transform 0.2s;}}
.strip:hover .ava{{transform:scale(1.1) rotate(5deg);}}
.sname{{font-size:0.875rem;font-weight:700;color:{T['striptext']};margin:0 0 2px;}}
.smeta{{font-size:0.72rem;color:{T['stripmeta']};margin:0;}}
.pill{{padding:3px 10px;border-radius:20px;font-size:0.68rem;font-weight:700;white-space:nowrap;flex-shrink:0;transition:transform 0.2s;}}
.strip:hover .pill{{transform:scale(1.05);}}
.pill.today{{background:#eff6ff;color:#1d4ed8;border:1px solid #bfdbfe;}}
.pill.overdue{{background:#fef2f2;color:#b91c1c;border:1px solid #fecaca;}}
.pill.soon{{background:#f0fdf4;color:#15803d;border:1px solid #bbf7d0;}}

.notif{{border-radius:12px;padding:13px 16px;margin-bottom:10px;
    display:flex;align-items:flex-start;gap:10px;animation:fadeUp 0.35s ease both;
    transition:transform 0.2s;}}
.notif:hover{{transform:translateX(3px);}}
.notif.info{{background:{'#eff6ff' if is_light else 'rgba(59,130,246,0.1)'};border:1px solid {'#bfdbfe' if is_light else 'rgba(59,130,246,0.3)'};}}
.notif.danger{{background:{'#fef2f2' if is_light else 'rgba(239,68,68,0.1)'};border:1px solid {'#fecaca' if is_light else 'rgba(239,68,68,0.3)'};}}
.notif.success{{background:{'#f0fdf4' if is_light else 'rgba(34,197,94,0.1)'};border:1px solid {'#bbf7d0' if is_light else 'rgba(34,197,94,0.3)'};}}
.nt{{font-size:0.83rem;font-weight:700;color:{T['text']};margin:0 0 2px;}}
.ns{{font-size:0.72rem;color:{T['sub']};margin:0;}}

.cta-btn button{{
    background:linear-gradient(135deg,#4f46e5,#7c3aed,#6366f1) !important;
    background-size:200% !important;animation:borderFlow 3s ease infinite !important;
    color:white !important;border:none !important;border-radius:12px !important;
    font-size:0.95rem !important;font-weight:700 !important;
    transition:all 0.3s cubic-bezier(.4,0,.2,1) !important;
    box-shadow:0 4px 18px rgba(79,70,229,0.35) !important;
}}
.cta-btn button:hover{{
    transform:translateY(-3px) scale(1.02) !important;
    box-shadow:0 10px 30px rgba(79,70,229,0.5) !important;
}}
.cta-btn button:active{{transform:scale(0.97) !important;}}

.stButton>button{{
    border-radius:10px !important;font-weight:600 !important;font-size:0.83rem !important;
    transition:all 0.25s cubic-bezier(.4,0,.2,1) !important;
    position:relative;overflow:hidden;
}}
.stButton>button:hover{{transform:translateY(-2px) !important;box-shadow:0 5px 16px rgba(0,0,0,0.15) !important;}}
.stButton>button:active{{transform:scale(0.96) !important;}}
.stButton>button[kind="primary"]{{
    background:linear-gradient(135deg,#4f46e5,#7c3aed) !important;
    color:white !important;border:none !important;
}}
.stButton>button[kind="primary"]:hover{{box-shadow:0 6px 20px rgba(79,70,229,0.4) !important;}}
[data-testid="stDownloadButton"]>button{{
    border-radius:10px !important;font-weight:600 !important;
    transition:all 0.25s !important;
}}
[data-testid="stDownloadButton"]>button:hover{{transform:translateY(-2px) !important;}}

.stTextInput>div>div>input,.stNumberInput>div>div>input,.stTextArea>div>textarea,.stSelectbox>div>div{{
    border-radius:10px !important;border-color:{T['inputborder']} !important;
    background:{T['input']} !important;color:{T['text']} !important;
    font-size:0.85rem !important;transition:all 0.2s !important;
}}
.stTextInput>div>div>input:focus,.stNumberInput>div>div>input:focus,.stTextArea>div>textarea:focus{{
    border-color:#6366f1 !important;box-shadow:0 0 0 3px rgba(99,102,241,0.15) !important;
}}
label{{color:{T['text']} !important;font-size:0.82rem !important;font-weight:600 !important;}}
details{{border-radius:12px !important;border:1px solid {T['border']} !important;background:{T['card']} !important;transition:all 0.2s !important;}}
details:hover{{box-shadow:0 4px 18px rgba(99,102,241,0.1) !important;}}
details summary{{font-weight:600 !important;font-size:0.85rem !important;color:{T['text']} !important;}}
div[data-testid="stTabs"] button{{font-weight:600 !important;font-size:0.85rem !important;color:{T['sub']} !important;transition:all 0.2s !important;}}
div[data-testid="stTabs"] button[aria-selected="true"]{{color:#6366f1 !important;border-bottom-color:#6366f1 !important;}}
[data-testid="stDataFrame"]{{border-radius:12px !important;border:1px solid {T['border']} !important;}}
.live-dot{{display:inline-block;width:7px;height:7px;border-radius:50%;background:#22c55e;margin-right:5px;animation:blink 1.5s infinite;}}
hr{{border:none;border-top:1px solid {T['border']};margin:12px 0;}}

.sb-pill{{background:{sb_pill};border:1px solid {sb_pill_b};border-radius:12px;padding:12px 14px;margin-bottom:12px;transition:all 0.2s;}}
.sb-pill:hover{{border-color:{'#c7d2fe' if is_light else '#312e81'};}}
.theme-dot{{width:20px;height:20px;border-radius:50%;cursor:pointer;transition:all 0.25s;flex-shrink:0;border:2px solid transparent;}}
.theme-dot:hover{{transform:scale(1.3);}}

.sched-box{{background:{'#f0fdf4' if is_light else 'rgba(34,197,94,0.08)'};
    border:1px solid {'#86efac' if is_light else 'rgba(34,197,94,0.3)'};
    border-radius:12px;padding:14px 16px;animation:fadeUp 0.4s ease both;}}
.sched-date{{font-size:1.05rem;font-weight:800;color:{'#15803d' if is_light else '#4ade80'};margin:4px 0 2px;}}
.sched-lbl{{font-size:0.62rem;font-weight:700;color:{'#16a34a' if is_light else '#22c55e'};text-transform:uppercase;letter-spacing:0.07em;margin:0;}}
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_db():
    db = DatabaseManager()
    db.init_user_tables()
    db.init_tables()
    db.ensure_default_admin()
    return db

db = get_db()

def hash_pw(p): return hashlib.sha256(p.encode()).hexdigest()
def ini(n):
    parts = str(n).strip().split()
    return "".join(p[0].upper() for p in parts[:2]) if parts else "?"
def to_excel(df):
    out = io.BytesIO()
    with pd.ExcelWriter(out, engine="openpyxl") as w:
        df.to_excel(w, index=False, sheet_name="Clients")
    return out.getvalue()
def get_status(row):
    nf = pd.to_datetime(row["next_followup"]).date() if pd.notna(row.get("next_followup")) else None
    if not nf: return "—","—"
    d = date.today()
    if nf < d:  return f"🔴 {(d-nf).days}d overdue","overdue"
    if nf == d: return "🟡 Due Today","today"
    return f"🟢 In {(nf-d).days}d","soon"


# ══════════════════════════════════════════════════════════════════════════════
#  LOGIN
# ══════════════════════════════════════════════════════════════════════════════
def show_login():
    t = st.session_state.theme
    orb1 = T["orb1"]; orb2 = T["orb2"]; orb3 = T["orb3"]
    if is_light:
        bg_grad = "linear-gradient(-45deg,#e0e7ff,#ede9fe,#dbeafe,#f0fdf4,#eff6ff)"
        card_bg = "rgba(255,255,255,0.95)"
        shadow  = "0 30px 80px rgba(99,102,241,0.2)"
    else:
        bg_grad = f"linear-gradient(-45deg,{T['bg']},{T['card']},#0f172a,{T['bg']})"
        card_bg = "rgba(15,23,42,0.97)"
        shadow  = "0 30px 80px rgba(0,0,0,0.6)"

    st.markdown(f"""
    <style>
    header,footer,[data-testid="stSidebar"]{{display:none !important;}}
    .main .block-container{{padding:0 !important;max-width:100% !important;}}
    .login-bg{{
        min-height:100vh;display:flex;align-items:center;justify-content:center;
        background:{bg_grad};background-size:400% 400%;
        animation:gradientShift 8s ease infinite;
        position:relative;overflow:hidden;padding:1rem;
    }}
    .orb1{{position:absolute;width:420px;height:420px;border-radius:50%;
        background:radial-gradient(circle,{orb1} 0%,transparent 70%);
        top:-80px;left:-80px;animation:floatOrb 7s ease-in-out infinite;pointer-events:none;}}
    .orb2{{position:absolute;width:350px;height:350px;border-radius:50%;
        background:radial-gradient(circle,{orb2} 0%,transparent 70%);
        bottom:-60px;right:-60px;animation:floatOrb2 9s ease-in-out infinite;pointer-events:none;}}
    .orb3{{position:absolute;width:200px;height:200px;border-radius:50%;
        background:radial-gradient(circle,{orb3} 0%,transparent 70%);
        top:40%;left:55%;animation:floatOrb3 12s ease-in-out infinite;pointer-events:none;}}
    .lcard{{
        background:{card_bg};backdrop-filter:blur(20px);border-radius:22px;
        padding:38px 38px 30px;width:100%;max-width:390px;
        box-shadow:{shadow};border:1px solid {T['border']};
        position:relative;z-index:10;animation:fadeUp 0.65s cubic-bezier(.4,0,.2,1) both;
    }}
    .llogo{{
        width:58px;height:58px;border-radius:16px;
        background:linear-gradient(135deg,#4f46e5,#7c3aed);
        display:flex;align-items:center;justify-content:center;
        font-size:1.6rem;margin:0 auto 10px;
        box-shadow:0 6px 22px rgba(79,70,229,0.45);
        animation:spinIn 0.7s cubic-bezier(.4,0,.2,1) both;
        transition:transform 0.3s;
    }}
    .llogo:hover{{transform:rotate(10deg) scale(1.1);}}
    .lapp{{font-size:1.25rem;font-weight:800;color:{T['text']};margin:0 0 2px;text-align:center;letter-spacing:-0.02em;}}
    .ltag{{font-size:0.68rem;color:{T['sub']};text-align:center;text-transform:uppercase;letter-spacing:0.09em;margin:0 0 24px;}}
    .lfooter{{text-align:center;margin-top:18px;font-size:0.7rem;color:{T['sub']};}}
    </style>
    <div class="login-bg">
      <div class="orb1"></div><div class="orb2"></div><div class="orb3"></div>
      <div class="lcard">
        <div class="llogo">💼</div>
        <p class="lapp">ClientPulse CRM</p>
        <p class="ltag">Sign in to your workspace</p>
    """, unsafe_allow_html=True)

    with st.form("lf"):
        st.text_input("Username", placeholder="Enter username", key="lu")
        st.text_input("Password", type="password", placeholder="Enter password", key="lp")
        sub = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

    if sub:
        if not st.session_state.get("lu") or not st.session_state.get("lp"):
            st.error("Enter both fields.")
        else:
            u = db.authenticate_user(st.session_state.lu, hash_pw(st.session_state.lp))
            if u:
                st.session_state.update(logged_in=True, username=u["username"],
                    role=u["role"], full_name=u["full_name"], user_id=u["id"])
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

    st.markdown(f'<div class="lfooter">Contact your admin to get access</div></div></div>',
                unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def show_sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div style="padding:20px 14px 4px;text-align:center;">
          <div style="width:44px;height:44px;border-radius:13px;
               background:linear-gradient(135deg,#4f46e5,#7c3aed);
               display:flex;align-items:center;justify-content:center;
               font-size:1.35rem;margin:0 auto 7px;
               box-shadow:0 5px 18px rgba(79,70,229,0.45);
               transition:transform 0.3s;cursor:default;"
               onmouseover="this.style.transform='rotate(8deg) scale(1.1)'"
               onmouseout="this.style.transform='none'">💼</div>
          <div style="font-size:0.95rem;font-weight:800;color:{sb_text};">ClientPulse</div>
          <div style="font-size:0.58rem;color:{sb_sub};text-transform:uppercase;letter-spacing:0.1em;margin-bottom:14px;">CRM</div>
        </div>
        """, unsafe_allow_html=True)

        fn   = st.session_state.get("full_name","User")
        un   = st.session_state.get("username","")
        role = st.session_state.get("role","user")
        tc   = len(db.get_todays_followups())
        oc   = len(db.get_overdue_followups())

        st.markdown(f"""
        <div class="sb-pill">
          <div style="display:flex;align-items:center;gap:8px;">
            <div style="width:30px;height:30px;border-radius:50%;
                 background:linear-gradient(135deg,#4f46e5,#7c3aed);
                 display:flex;align-items:center;justify-content:center;
                 font-size:0.7rem;font-weight:800;color:white;flex-shrink:0;">{ini(fn)}</div>
            <div>
              <div style="font-size:0.78rem;font-weight:700;color:{sb_text};">{fn}</div>
              <div style="font-size:0.62rem;color:{sb_sub};">{'⚙️ Admin' if role=='admin' else '👤 User'} · @{un}</div>
            </div>
          </div>
          <div style="display:flex;gap:4px;margin-top:8px;">
            <div style="flex:1;background:{sb_mini};border-radius:7px;padding:5px 7px;text-align:center;transition:transform 0.2s;"
                 onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='none'">
              <div style="font-size:0.9rem;font-weight:800;color:#a5b4fc;">{tc}</div>
              <div style="font-size:0.55rem;color:{sb_sub};text-transform:uppercase;">Today</div>
            </div>
            <div style="flex:1;background:{sb_mini};border-radius:7px;padding:5px 7px;text-align:center;transition:transform 0.2s;"
                 onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='none'">
              <div style="font-size:0.9rem;font-weight:800;color:#fca5a5;">{oc}</div>
              <div style="font-size:0.55rem;color:{sb_sub};text-transform:uppercase;">Overdue</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        opts = ["🏠  Dashboard","➕  Add Client","👥  Clients","📅  Follow-ups"]
        if role == "admin": opts.append("⚙️  Users")
        page = st.radio("Nav", opts, label_visibility="collapsed")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:0.62rem;font-weight:700;color:{sb_sub};text-transform:uppercase;letter-spacing:0.08em;padding:0 2px;margin-bottom:5px;'>Theme</p>", unsafe_allow_html=True)

        theme_cols = st.columns(5)
        theme_map  = {
            "dark":   ("#4f46e5","🌙"),
            "light":  ("#f8faff","☀️"),
            "ocean":  ("#0ea5e9","🌊"),
            "forest": ("#22c55e","🌿"),
            "rose":   ("#f43f5e","🌸"),
        }
        for i,(tk,(tc_color,tlabel)) in enumerate(theme_map.items()):
            with theme_cols[i]:
                active = st.session_state.theme == tk
                if st.button(tlabel, key=f"th_{tk}",
                             help=tk.title(),
                             use_container_width=True):
                    st.session_state.theme = tk
                    st.rerun()

        st.markdown(f"""
        <div style="margin-top:8px;padding:9px 11px;background:{sb_live};
             border:1px solid {sb_live_b};border-radius:9px;">
          <span class="live-dot"></span>
          <span style="font-size:0.7rem;color:{sb_sub};">{date.today().strftime("%b %d, %Y")}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
        if st.button("🚪  Sign Out", use_container_width=True):
            for k in ["logged_in","username","role","full_name","user_id","show_today"]:
                st.session_state.pop(k, None)
            st.rerun()

    return page


# ══════════════════════════════════════════════════════════════════════════════
#  DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
def page_dashboard():
    fn = st.session_state.get("full_name","User")
    st.markdown(f'<p class="ph">👋 Hi, {fn.split()[0]}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="ps">{date.today().strftime("%A, %B %d %Y")} — here\'s your day</p>', unsafe_allow_html=True)

    total    = db.get_total_clients()
    today_df = db.get_todays_followups()
    over_df  = db.get_overdue_followups()
    upc_df   = db.get_upcoming_followups(7)

    c1,c2,c3,c4 = st.columns(4)
    for col,color,icon,val,lbl in [
        (c1,"blue",  "👥",total,         "Total Clients"),
        (c2,"green", "📞",len(today_df), "Due Today"),
        (c3,"red",   "⚠️",len(over_df),  "Overdue"),
        (c4,"amber", "📆",len(upc_df),   "This Week"),
    ]:
        col.markdown(f"""
        <div class="metric-card {color}">
          <div style="font-size:1.3rem;margin-bottom:6px;">{icon}</div>
          <p class="mval">{val}</p>
          <p class="mlbl">{lbl}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    _,mid,_ = st.columns([1,2,1])
    with mid:
        st.markdown('<div class="cta-btn">', unsafe_allow_html=True)
        if st.button("🔔  Who Do I Call Today?", use_container_width=True):
            st.session_state.show_today = not st.session_state.get("show_today", False)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("show_today"):
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        L,R = st.columns(2)
        with L:
            st.markdown(f"<p style='font-size:0.82rem;font-weight:700;color:{T['text']};margin-bottom:8px;'>📞 Call Today ({len(today_df)})</p>", unsafe_allow_html=True)
            if today_df.empty:
                st.markdown('<div class="notif success"><div><p class="nt">All clear!</p><p class="ns">No calls today.</p></div></div>', unsafe_allow_html=True)
            else:
                for _,r in today_df.iterrows():
                    st.markdown(f"""
                    <div class="strip">
                      <div class="ava">{ini(str(r['name']))}</div>
                      <div style="flex:1;min-width:0;">
                        <p class="sname">{r['name']}</p>
                        <p class="smeta">{r.get('company','—') or '—'} · {r.get('phone','—') or '—'}</p>
                      </div>
                      <span class="pill today">Today</span>
                    </div>""", unsafe_allow_html=True)
        with R:
            st.markdown(f"<p style='font-size:0.82rem;font-weight:700;color:{T['text']};margin-bottom:8px;'>⚠️ Overdue ({len(over_df)})</p>", unsafe_allow_html=True)
            if over_df.empty:
                st.markdown('<div class="notif success"><div><p class="nt">Zero overdue!</p><p class="ns">All caught up.</p></div></div>', unsafe_allow_html=True)
            else:
                for _,r in over_df.iterrows():
                    d = (date.today()-pd.to_datetime(r["next_followup"]).date()).days
                    st.markdown(f"""
                    <div class="strip">
                      <div class="ava" style="background:#fef2f2;color:#b91c1c;border-color:#fecaca;">{ini(str(r['name']))}</div>
                      <div style="flex:1;min-width:0;">
                        <p class="sname">{r['name']}</p>
                        <p class="smeta">{r.get('company','—') or '—'} · {r.get('phone','—') or '—'}</p>
                      </div>
                      <span class="pill overdue">{d}d late</span>
                    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ADD CLIENT
# ══════════════════════════════════════════════════════════════════════════════
def page_add_client():
    st.markdown('<p class="ph">➕ Add Client</p>', unsafe_allow_html=True)
    st.markdown('<p class="ps">Store a new client and schedule a follow-up</p>', unsafe_allow_html=True)

    with st.form("acf", clear_on_submit=True):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1,c2 = st.columns(2)
        with c1:
            name    = st.text_input("Full Name *", placeholder="Rajiv Sharma")
            phone   = st.text_input("Phone", placeholder="+91 98765 43210")
            company = st.text_input("Company", placeholder="Acme Corp")
        with c2:
            email    = st.text_input("Email", placeholder="rajiv@acme.com")
            category = st.selectbox("Category", ["Lead","Prospect","Active Client","Partner","VIP","Churned"])
            source   = st.selectbox("Source", ["Referral","Website","LinkedIn","Cold Outreach","Event","Other"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="card">', unsafe_allow_html=True)
        c3,c4 = st.columns(2)
        with c3:
            last_contacted = st.date_input("Last Contacted", value=date.today())
            followup_days  = st.number_input("Follow-up after (days)", min_value=1, max_value=365, value=5)
            deal_value     = st.number_input("Deal Value (₹)", min_value=0, value=0, step=1000)
        with c4:
            nf = last_contacted + timedelta(days=int(followup_days))
            days_away = (nf - date.today()).days
            st.markdown(f"""
            <div class="sched-box">
              <p class="sched-lbl">📌 Scheduled follow-up</p>
              <p class="sched-date">{nf.strftime("%B %d, %Y")}</p>
              <p style="font-size:0.72rem;color:{T['sub']};margin:3px 0 8px;">
                In {days_away} day{'s' if days_away!=1 else ''}
              </p>
            </div>""", unsafe_allow_html=True)
            notes = st.text_area("Notes", placeholder="Relevant notes…", height=78)
        st.markdown('</div>', unsafe_allow_html=True)

        sub = st.form_submit_button("💾  Save Client", type="primary", use_container_width=True)

    if sub:
        if not name.strip():
            st.error("Name is required.")
        else:
            ok = db.add_client({
                "name":name.strip(),"email":email,"phone":phone,"company":company,
                "category":category,"source":source,"last_contacted":str(last_contacted),
                "followup_days":int(followup_days),"next_followup":str(nf),
                "deal_value":deal_value,"notes":notes,
                "created_by":st.session_state.get("user_id",1)
            })
            if ok:
                st.success(f"✅ {name} saved! Follow-up on {nf.strftime('%b %d, %Y')}.")
                st.balloons()
            else:
                st.error("Failed to save. Check DB.")


# ══════════════════════════════════════════════════════════════════════════════
#  CLIENTS
# ══════════════════════════════════════════════════════════════════════════════
def page_clients():
    st.markdown('<p class="ph">👥 Clients</p>', unsafe_allow_html=True)

    st.markdown('<div class="card" style="padding:12px 16px;margin-bottom:10px;">', unsafe_allow_html=True)
    fc1,fc2,fc3 = st.columns([3,1,1])
    with fc1: search = st.text_input("S","",placeholder="🔍 Name, company, phone…",label_visibility="collapsed")
    with fc2: cat    = st.selectbox("C",["All","Lead","Prospect","Active Client","Partner","VIP","Churned"],label_visibility="collapsed")
    with fc3: srt    = st.selectbox("O",["Next Follow-up","Name","Company","Deal Value"],label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    df = db.get_all_clients(search=search.strip() or None,
                            category=cat if cat!="All" else None, sort_by=srt)

    if df.empty:
        st.markdown('<div class="notif info"><div><p class="nt">No clients found</p><p class="ns">Adjust filters or add a client.</p></div></div>', unsafe_allow_html=True)
        return

    hc1,hc2,hc3 = st.columns([4,1,1])
    with hc1: st.markdown(f"<p style='font-size:0.78rem;color:{T['sub']};margin:5px 0;'><b>{len(df)}</b> client(s)</p>", unsafe_allow_html=True)
    with hc2:
        st.download_button("📥 Excel", data=to_excel(df),
            file_name=f"clients_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True)
    with hc3:
        if st.button("🔄", use_container_width=True): st.rerun()

    df["Status"] = df.apply(lambda r: get_status(r)[0], axis=1)
    df["Deal"]   = df["deal_value"].apply(lambda x: f"₹{x:,.0f}" if x else "—")
    show = df[["name","company","phone","email","category","next_followup","Status","Deal"]].rename(
        columns={"name":"Name","company":"Company","phone":"Phone","email":"Email",
                 "category":"Category","next_followup":"Next Follow-up","Deal":"💰 Deal"})
    st.dataframe(show, use_container_width=True, height=380, hide_index=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.8rem;font-weight:700;color:{T['text']};margin-bottom:8px;'>Quick Actions</p>", unsafe_allow_html=True)
    qa1,qa2,qa3,qa4 = st.columns([3,1,1,1])
    with qa1: sel = st.selectbox("Cl", df["name"].tolist(), label_visibility="collapsed")
    with qa2: nd  = st.date_input("D", value=date.today()+timedelta(days=7), label_visibility="collapsed")
    with qa3:
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("📅 Reschedule", type="primary", use_container_width=True):
            db.update_followup(int(df[df["name"]==sel]["id"].values[0]), str(nd))
            st.success(f"✅ {sel} → {nd.strftime('%b %d')}"); st.rerun()
    with qa4:
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        if st.button("🗑 Delete", use_container_width=True):
            db.delete_client(int(df[df["name"]==sel]["id"].values[0]))
            st.warning(f"Deleted {sel}"); st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  FOLLOW-UPS
# ══════════════════════════════════════════════════════════════════════════════
def page_followups():
    st.markdown('<p class="ph">📅 Follow-ups</p>', unsafe_allow_html=True)
    st.markdown('<p class="ps">Track and action all client follow-ups</p>', unsafe_allow_html=True)

    tab1,tab2,tab3 = st.tabs(["🔴  Overdue","🟡  Today","🟢  Upcoming"])

    with tab1:
        ov = db.get_overdue_followups()
        if ov.empty:
            st.markdown('<div class="notif success"><div><p class="nt">🎉 Zero overdue!</p><p class="ns">You\'re on top of every client.</p></div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="notif danger"><div><p class="nt">⚠️ {len(ov)} overdue</p><p class="ns">Reach out to these clients now.</p></div></div>', unsafe_allow_html=True)
            for _,r in ov.iterrows():
                d = (date.today()-pd.to_datetime(r["next_followup"]).date()).days
                with st.expander(f"🔴  {r['name']}  ·  {r.get('company','—') or '—'}  ·  {d}d overdue"):
                    cc1,cc2 = st.columns([3,2])
                    with cc1:
                        st.write(f"📞 **{r['phone'] or '—'}**")
                        st.write(f"✉️ {r['email'] or '—'}")
                        st.write(f"🏷 {r['category']}")
                        if r.get("notes"): st.info(f"📝 {r['notes']}")
                    with cc2:
                        nd2 = st.number_input("Reschedule in (days)", 1, 365, 7, key=f"ov{r['id']}")
                        if st.button("✅ Mark contacted", key=f"ovb{r['id']}", type="primary", use_container_width=True):
                            db.update_followup(int(r["id"]), str(date.today()+timedelta(days=int(nd2))), True)
                            st.success("Updated!"); st.rerun()

    with tab2:
        td = db.get_todays_followups()
        if td.empty:
            st.markdown('<div class="notif info"><div><p class="nt">No calls today</p><p class="ns">Nothing scheduled for today.</p></div></div>', unsafe_allow_html=True)
        else:
            for _,r in td.iterrows():
                with st.expander(f"📞  {r['name']}  ·  {r.get('company','—') or '—'}"):
                    cc1,cc2 = st.columns([3,2])
                    with cc1:
                        st.write(f"📞 **{r['phone'] or '—'}**")
                        st.write(f"✉️ {r['email'] or '—'}")
                        st.write(f"🏷 {r['category']}")
                        if r.get("notes"): st.info(f"📝 {r['notes']}")
                    with cc2:
                        nd2 = st.number_input("Next in (days)", 1, 365, int(r["followup_days"]), key=f"td{r['id']}")
                        if st.button("✅ Mark contacted", key=f"tdb{r['id']}", type="primary", use_container_width=True):
                            db.update_followup(int(r["id"]), str(date.today()+timedelta(days=int(nd2))), True)
                            st.success("Done!"); st.rerun()

    with tab3:
        days = st.slider("Next N days", 3, 60, 14)
        up   = db.get_upcoming_followups(days)
        if up.empty:
            st.info(f"Nothing in the next {days} days.")
        else:
            up["In"]   = up["next_followup"].apply(lambda x:(pd.to_datetime(x).date()-date.today()).days)
            up["Deal"] = up["deal_value"].apply(lambda x: f"₹{x:,.0f}" if x else "—")
            st.dataframe(
                up[["name","company","phone","category","next_followup","In","Deal"]].rename(
                    columns={"name":"Name","company":"Company","phone":"Phone",
                             "category":"Category","next_followup":"Date","In":"⏳","Deal":"💰"}),
                use_container_width=True, hide_index=True, height=360)


# ══════════════════════════════════════════════════════════════════════════════
#  USERS
# ══════════════════════════════════════════════════════════════════════════════
def page_users():
    st.markdown('<p class="ph">⚙️ User Management</p>', unsafe_allow_html=True)
    st.markdown('<p class="ps">Manage CRM access and roles</p>', unsafe_allow_html=True)

    tab1,tab2 = st.tabs(["👥  Users","➕  Add User"])

    with tab1:
        users = db.get_all_users()
        if users.empty:
            st.info("No users found."); return
        for _,u in users.iterrows():
            is_self  = u["username"] == st.session_state.get("username")
            is_admin = u["role"] == "admin"
            is_act   = u["is_active"]
            rb = "#eef2ff" if is_admin else "#f0fdf4"
            rc = "#3730a3" if is_admin else "#15803d"
            rc1,rc2,rc3 = st.columns([5,1,1])
            with rc1:
                st.markdown(f"""
                <div style="background:{T['card']};border:1px solid {T['border']};border-radius:12px;
                     padding:12px 15px;display:flex;align-items:center;gap:11px;margin-bottom:4px;
                     transition:all 0.2s;"
                     onmouseover="this.style.borderColor='#6366f1';this.style.transform='translateX(3px)'"
                     onmouseout="this.style.borderColor='{T['border']}';this.style.transform='none'">
                  <div style="width:34px;height:34px;border-radius:50%;background:{rb};
                       border:2px solid {'#c7d2fe' if is_admin else '#bbf7d0'};
                       display:flex;align-items:center;justify-content:center;
                       font-size:0.72rem;font-weight:800;color:{rc};flex-shrink:0;">{ini(str(u['full_name']))}</div>
                  <div style="flex:1;min-width:0;">
                    <div style="font-size:0.85rem;font-weight:700;color:{T['text']};">{u['full_name']}
                      <span style="background:{rb};color:{rc};padding:1px 7px;border-radius:20px;font-size:0.62rem;font-weight:700;margin-left:5px;">{u['role'].title()}</span>
                      {'<span style="background:#f0fdf4;color:#15803d;padding:1px 7px;border-radius:20px;font-size:0.62rem;font-weight:700;margin-left:3px;">● Active</span>' if is_act else '<span style="background:#fef2f2;color:#b91c1c;padding:1px 7px;border-radius:20px;font-size:0.62rem;font-weight:700;margin-left:3px;">● Off</span>'}
                      {'<span style="background:#fefce8;color:#854d0e;padding:1px 7px;border-radius:20px;font-size:0.62rem;font-weight:700;margin-left:3px;">You</span>' if is_self else ''}
                    </div>
                    <div style="font-size:0.7rem;color:{T['sub']};">@{u['username']} · {u['email'] or '—'}</div>
                  </div>
                </div>""", unsafe_allow_html=True)
            with rc2:
                if not is_self:
                    if st.button("Deactivate" if is_act else "Activate", key=f"tog{u['id']}", use_container_width=True):
                        db.toggle_user_status(int(u["id"])); st.rerun()
            with rc3:
                if not is_self:
                    if st.button("🗑", key=f"del{u['id']}", use_container_width=True):
                        db.delete_user(int(u["id"])); st.rerun()

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        with st.form("auf", clear_on_submit=True):
            nc1,nc2 = st.columns(2)
            with nc1:
                nfn = st.text_input("Full Name *", placeholder="Arjun Kapoor")
                nun = st.text_input("Username *", placeholder="arjun.kapoor")
                nem = st.text_input("Email", placeholder="arjun@company.com")
            with nc2:
                npw  = st.text_input("Password *", type="password", placeholder="Min 6 chars")
                npw2 = st.text_input("Confirm *", type="password", placeholder="Repeat")
                nrl  = st.selectbox("Role", ["user","admin"],
                                    format_func=lambda x:"👤 User" if x=="user" else "⚙️ Admin")
            asub = st.form_submit_button("➕  Create User", type="primary", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if asub:
            errs = []
            if not nfn.strip():              errs.append("Full name required.")
            if not nun.strip():              errs.append("Username required.")
            if not npw:                      errs.append("Password required.")
            if len(npw) < 6:                 errs.append("Min 6 chars.")
            if npw != npw2:                  errs.append("Passwords don't match.")
            if db.username_exists(nun.strip()): errs.append(f"@{nun} taken.")
            if errs:
                for e in errs: st.error(e)
            else:
                ok = db.add_user({"full_name":nfn.strip(),"username":nun.strip(),
                                  "email":nem.strip(),"password_hash":hash_pw(npw),"role":nrl})
                if ok: st.success(f"✅ {nfn} created."); st.balloons()
                else:  st.error("Failed. Check DB.")


# ══════════════════════════════════════════════════════════════════════════════
#  ROUTER
# ══════════════════════════════════════════════════════════════════════════════
if not st.session_state.get("logged_in"):
    show_login()
else:
    page = show_sidebar()
    if   "Dashboard" in page: page_dashboard()
    elif "Add"       in page: page_add_client()
    elif "Clients"   in page: page_clients()
    elif "Follow"    in page: page_followups()
    elif "Users"     in page:
        if st.session_state.get("role") == "admin": page_users()
        else: st.error("🔒 Admins only.")
