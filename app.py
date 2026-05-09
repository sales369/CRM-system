import streamlit as st
import pandas as pd
from datetime import date, timedelta
import io
import hashlib
from database import DatabaseManager

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ClientPulse CRM | Professional",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Ultra-Premium Global CSS ───────────────────────────────────────────────────
st.markdown("""
<style>
/* Import Premium Font */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* Apply Font Globally */
*, html, body, [class*="css"], [class*="st-"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ── Base App & Scrollbar ── */
.stApp {
    background-color: #f8fafc;
}
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* ── Animations ── */
@keyframes slideUpFade {
    0% { opacity: 0; transform: translateY(15px); }
    100% { opacity: 1; transform: translateY(0); }
}
@keyframes subtlePulse {
    0% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0.4); }
    70% { box-shadow: 0 0 0 10px rgba(79, 70, 229, 0); }
    100% { box-shadow: 0 0 0 0 rgba(79, 70, 229, 0); }
}

/* ── Hide default Streamlit chrome on login page ── */
.login-mode header,
.login-mode [data-testid="stSidebar"],
.login-mode footer { display: none !important; }

/* ── Sidebar (Enterprise Light Theme) ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #eaecf0 !important;
}
[data-testid="stSidebarNav"] { padding-top: 0 !important; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 6px; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: transparent;
    border-radius: 8px;
    padding: 12px 16px !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: #475467 !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    border: 1px solid transparent;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: #f9fafb !important;
    color: #101828 !important;
    border: 1px solid #eaecf0;
    transform: translateX(4px);
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-baseweb="radio"] { display: flex; }

/* ── Main Area ── */
.main .block-container { 
    padding: 2.5rem 3.5rem 3rem 3.5rem; 
    max-width: 1440px; 
    animation: slideUpFade 0.5s ease-out forwards;
}

/* ── Metric Cards ── */
.metric-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #eaecf0;
    box-shadow: 0 1px 3px rgba(16, 24, 40, 0.05), 0 1px 2px rgba(16, 24, 40, 0.03);
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 4px;
    background: linear-gradient(90deg, #e2e8f0, #f1f5f9);
    transition: background 0.3s ease;
}
.metric-card:hover { 
    transform: translateY(-4px); 
    box-shadow: 0 12px 24px -8px rgba(16, 24, 40, 0.1);
    border-color: #d0d5dd;
}
.metric-card.indigo:hover::before { background: linear-gradient(90deg, #4f46e5, #818cf8); }
.metric-card.blue:hover::before { background: linear-gradient(90deg, #0284c7, #38bdf8); }
.metric-card.red:hover::before { background: linear-gradient(90deg, #dc2626, #f87171); }
.metric-card.purple:hover::before { background: linear-gradient(90deg, #7c3aed, #a78bfa); }
.metric-card.green:hover::before { background: linear-gradient(90deg, #16a34a, #4ade80); }

.metric-icon { font-size: 1.8rem; margin-bottom: 12px; }
.metric-val  { font-size: 2.4rem; font-weight: 800; color: #101828; margin: 0 0 4px; line-height: 1.1; letter-spacing: -0.03em; }
.metric-lbl  { font-size: 0.8rem; font-weight: 600; color: #475467; text-transform: uppercase; letter-spacing: 0.08em; margin: 0; }

/* ── Typography headers ── */
.page-title { font-size: 2rem; font-weight: 800; color: #101828; margin: 0 0 6px; letter-spacing: -0.03em; }
.page-sub   { font-size: 1rem; color: #475467; font-weight: 400; margin: 0 0 2rem; }

/* ── Modern Form Cards ── */
.form-section {
    background: #ffffff;
    border-radius: 16px;
    padding: 32px 36px;
    border: 1px solid #eaecf0;
    margin-bottom: 24px;
    box-shadow: 0 1px 3px rgba(16, 24, 40, 0.03);
}
.form-section h5 { color: #101828; font-weight: 700; margin-bottom: 20px; font-size: 1.1rem; }

/* ── Native Streamlit Input Overrides ── */
[data-baseweb="input"] > div, 
[data-baseweb="select"] > div,
[data-baseweb="textarea"] > div {
    border-radius: 10px !important;
    background-color: #fcfcfd !important;
    border: 1px solid #d0d5dd !important;
    transition: all 0.2s ease !important;
}
[data-baseweb="input"] > div:hover, 
[data-baseweb="select"] > div:hover {
    border-color: #98a2b3 !important;
}
[data-baseweb="input"] > div:focus-within, 
[data-baseweb="select"] > div:focus-within {
    border-color: #4f46e5 !important;
    box-shadow: 0 0 0 4px #e0e7ff !important;
}
input, textarea { font-size: 0.95rem !important; color: #101828 !important; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.2s ease !important;
    border: 1px solid #d0d5dd !important;
    background: #ffffff !important;
    color: #344054 !important;
    box-shadow: 0 1px 2px rgba(16, 24, 40, 0.05) !important;
}
.stButton > button:hover { 
    background: #f9fafb !important;
    transform: translateY(-1px) !important; 
    box-shadow: 0 4px 6px -1px rgba(16, 24, 40, 0.05) !important; 
}
.stButton > button[kind="primary"] {
    background: linear-gradient(180deg, #6366f1 0%, #4f46e5 100%) !important;
    border: 1px solid #4338ca !important;
    color: white !important;
    box-shadow: 0 1px 2px rgba(16, 24, 40, 0.05), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(180deg, #4f46e5 0%, #4338ca 100%) !important;
    box-shadow: 0 4px 10px rgba(79, 70, 229, 0.25), inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
}

/* ── Big CTA Button ── */
.big-cta button {
    background: linear-gradient(135deg, #101828, #344054) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-size: 1.1rem !important;
    font-weight: 600 !important;
    padding: 1rem 0 !important;
    box-shadow: 0 8px 16px rgba(16, 24, 40, 0.2) !important;
    animation: subtlePulse 3s infinite;
}
.big-cta button:hover { transform: translateY(-2px) scale(1.02) !important; background: #101828 !important; }

/* ── Tabs ── */
[data-baseweb="tab-list"] {
    gap: 24px;
    border-bottom: 2px solid #eaecf0 !important;
    padding-bottom: 4px;
}
[data-baseweb="tab"] {
    font-weight: 600 !important;
    font-size: 1rem !important;
    color: #667085 !important;
    background: transparent !important;
    border: none !important;
    padding: 8px 4px !important;
}
[aria-selected="true"] {
    color: #4f46e5 !important;
    border-bottom: 2px solid #4f46e5 !important;
}

/* ── Alert strips (Today / Overdue) ── */
.strip { 
    background: #ffffff; border-radius: 12px; padding: 18px 24px; margin-bottom: 14px; 
    border: 1px solid #eaecf0; border-left-width: 6px; box-shadow: 0 1px 2px rgba(16,24,40,0.03); 
    display: flex; flex-direction: column; gap: 8px; transition: transform 0.2s, box-shadow 0.2s;
}
.strip:hover { transform: translateX(4px); box-shadow: 0 4px 12px rgba(16,24,40,0.05); }
.strip-today { border-left-color: #0ea5e9; }
.strip-overdue { border-left-color: #ef4444; }
.strip-ok { border-left-color: #10b981; align-items: center; text-align: center; }

.strip-header { display: flex; justify-content: space-between; align-items: center; }
.strip-title { font-size: 1.05rem; font-weight: 700; color: #101828; margin: 0; }
.strip-badge { font-size: 0.75rem; font-weight: 700; padding: 4px 10px; border-radius: 20px; }
.badge-blue { background: #e0f2fe; color: #0369a1; }
.badge-red { background: #fee2e2; color: #b91c1c; }

.strip-meta { display: flex; gap: 16px; font-size: 0.85rem; color: #475467; font-weight: 500; margin: 0; }
.strip-notes { margin: 4px 0 0; padding-top: 10px; border-top: 1px dashed #eaecf0; font-size: 0.85rem; color: #667085; }

/* ── Scheduled Badge ── */
.sched-badge {
    background: #f8fafc; border: 1px dashed #cbd5e1; border-radius: 12px;
    padding: 24px; text-align: center;
}
.sched-date { font-size: 1.4rem; font-weight: 800; color: #101828; margin: 8px 0; }
.sched-lbl  { font-size: 0.75rem; font-weight: 700; color: #4f46e5; text-transform: uppercase; letter-spacing: 0.1em; margin: 0; }

/* ── Expander ── */
.streamlit-expanderHeader {
    font-weight: 600 !important; color: #101828 !important;
    background: #fcfcfd !important; border-radius: 10px !important;
}
details { border: 1px solid #eaecf0 !important; border-radius: 10px !important; background: #ffffff; overflow: hidden; }

hr { border: none; border-top: 1px solid #eaecf0; margin: 2rem 0; }
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
#  LOGIN PAGE (Ultra-Premium Portal)
# ══════════════════════════════════════════════════════════════════════════════

def show_login():
    st.markdown("""
    <div style="
        position: fixed; top: 0; left: 0; right: 0; bottom: 0;
        display:flex; align-items:center; justify-content:center;
        background: radial-gradient(circle at 50% -20%, #eef2ff 0%, #f8fafc 100%);
        z-index: 99999;
    ">
        <div style="
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255,255,255,1);
            border-radius: 24px;
            padding: 64px 48px;
            width: 100%; max-width: 460px;
            box-shadow: 0 25px 50px -12px rgba(16, 24, 40, 0.08), 0 0 0 1px rgba(16, 24, 40, 0.02);
            animation: slideUpFade 0.6s cubic-bezier(0.16, 1, 0.3, 1);
        ">
            <div style="text-align:center; margin-bottom:40px;">
                <div style="width: 72px; height: 72px; background: linear-gradient(135deg, #4f46e5, #7c3aed); 
                            border-radius: 20px; display: flex; align-items: center; justify-content: center; 
                            font-size: 36px; margin: 0 auto 24px; box-shadow: 0 10px 25px rgba(79, 70, 229, 0.3);">
                    💼
                </div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #101828; letter-spacing: -0.04em; margin-bottom: 8px;">
                    ClientPulse CRM
                </div>
                <div style="font-size: 0.95rem; color: #475467; font-weight: 500;">
                    Sign in to your enterprise workspace
                </div>
            </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Work Email / Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

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
                st.error("❌ Invalid credentials.")

    st.markdown("""
            <div style="text-align:center; margin-top:32px; font-size:0.85rem; color:#98a2b3; font-weight:500;">
                Secure Access • Protected by AES-256
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
        <div style="padding: 24px 16px 32px; display: flex; align-items: center; gap: 12px;">
            <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #4f46e5, #7c3aed); 
                        border-radius: 10px; display: flex; align-items: center; justify-content: center; 
                        font-size: 20px; box-shadow: 0 4px 10px rgba(79, 70, 229, 0.2);">💼</div>
            <div>
                <div style="font-size: 1.25rem; font-weight: 800; color: #101828; letter-spacing: -0.02em; line-height: 1;">ClientPulse</div>
                <div style="font-size: 0.65rem; color: #667085; text-transform: uppercase; letter-spacing: 0.15em; font-weight: 700; margin-top: 4px;">CRM System</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        role = st.session_state.get("role", "user")
        full_name = st.session_state.get("full_name", "User")
        username  = st.session_state.get("username", "")

        initials = "".join(p[0].upper() for p in full_name.split()[:2])
        st.markdown(f"""
        <div style="background: #f8fafc; border: 1px solid #eaecf0; border-radius: 12px; padding: 16px; margin: 0 16px 24px; display: flex; align-items: center; gap: 12px;">
            <div style="width: 42px; height: 42px; border-radius: 50%; background: #e0e7ff; border: 2px solid #ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                        display: flex; align-items: center; justify-content: center; font-size: 0.9rem; font-weight: 800; color: #4f46e5; flex-shrink: 0;">
                {initials}
            </div>
            <div style="overflow: hidden;">
                <div style="font-size: 0.9rem; font-weight: 700; color: #101828; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">{full_name}</div>
                <div style="font-size: 0.75rem; color: #667085; font-weight: 500; margin-top: 2px;">
                    {'🛡️ Admin' if role == 'admin' else '👤 User'}
                </div>
            </div>
        </div>
        <div style="padding: 0 16px; font-size: 0.75rem; font-weight: 700; color: #98a2b3; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px;">Main Menu</div>
        """, unsafe_allow_html=True)

        nav_options = ["🏠  Dashboard", "➕  Add Client", "👥  All Clients", "📅  Follow-ups", "📊  Reports"]
        if role == "admin":
            nav_options.append("⚙️  User Management")

        page = st.radio("Navigation", nav_options, label_visibility="collapsed")

        st.markdown("<div style='height:1px;background:#eaecf0;margin:24px 16px 16px;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="padding: 0 16px 24px;">
            <div style="font-size: 0.75rem; color: #667085; font-weight: 600; margin-bottom: 4px;">Today's Date</div>
            <div style="font-size: 0.9rem; font-weight: 700; color: #101828;">{date.today().strftime("%A, %B %d")}</div>
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
    st.markdown('<p class="page-title">Dashboard Overview</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-sub">Welcome back, <b>{st.session_state.get("full_name","User")}</b>. Here is your pulse on the business today.</p>', unsafe_allow_html=True)

    total = db.get_total_clients()
    today_df  = db.get_todays_followups()
    over_df   = db.get_overdue_followups()
    upc_df    = db.get_upcoming_followups(7)

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, val, lbl, theme_class in [
        (c1, "👥", total,           "Total Clients",   "indigo"),
        (c2, "📞", len(today_df),   "Due Today",       "blue"),
        (c3, "🔴", len(over_df),    "Overdue Actions", "red"),
        (c4, "📆", len(upc_df),     "Next 7 Days",     "purple"),
    ]:
        col.markdown(f"""
        <div class="metric-card {theme_class}">
            <div class="metric-icon">{icon}</div>
            <p class="metric-val">{val}</p>
            <p class="metric-lbl">{lbl}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown('<div class="big-cta">', unsafe_allow_html=True)
        if st.button("🔔  Generate My Daily Action Plan", use_container_width=True):
            st.session_state.show_today = not st.session_state.get("show_today", False)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("show_today"):
        st.markdown("<br><hr>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("<h4 style='color:#101828; font-weight:800; margin-bottom:16px;'>📞 Call Today</h4>", unsafe_allow_html=True)
            if today_df.empty:
                st.markdown('<div class="strip strip-ok"><div style="font-size:2rem;margin-bottom:8px;">☕</div><p class="strip-title">All clear!</p><p class="strip-meta">No calls scheduled for today.</p></div>', unsafe_allow_html=True)
            else:
                for _, r in today_df.iterrows():
                    st.markdown(f"""
                    <div class="strip strip-today">
                        <div class="strip-header">
                            <p class="strip-title">{r['name']} <span style="color:#667085; font-weight:500;">· {r['company']}</span></p>
                            <span class="strip-badge badge-blue">{r['category']}</span>
                        </div>
                        <div class="strip-meta">
                            <span>📞 {r['phone'] or 'N/A'}</span>
                            <span>✉️ {r['email'] or 'N/A'}</span>
                        </div>
                        <p class="strip-notes">📝 {r['notes'] or 'No additional notes provided for this client.'}</p>
                    </div>""", unsafe_allow_html=True)

        with col_b:
            st.markdown("<h4 style='color:#101828; font-weight:800; margin-bottom:16px;'>⚠️ Action Required (Overdue)</h4>", unsafe_allow_html=True)
            if over_df.empty:
                st.markdown('<div class="strip strip-ok"><div style="font-size:2rem;margin-bottom:8px;">🎉</div><p class="strip-title">Inbox Zero!</p><p class="strip-meta">You are completely caught up.</p></div>', unsafe_allow_html=True)
            else:
                for _, r in over_df.iterrows():
                    d = (date.today() - pd.to_datetime(r['next_followup']).date()).days
                    st.markdown(f"""
                    <div class="strip strip-overdue">
                        <div class="strip-header">
                            <p class="strip-title">{r['name']} <span style="color:#667085; font-weight:500;">· {r['company']}</span></p>
                            <span class="strip-badge badge-red">{d}d Overdue</span>
                        </div>
                        <div class="strip-meta">
                            <span>📞 {r['phone'] or 'N/A'}</span>
                            <span>✉️ {r['email'] or 'N/A'}</span>
                        </div>
                    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ADD CLIENT
# ══════════════════════════════════════════════════════════════════════════════

def page_add_client():
    st.markdown('<p class="page-title">Add New Client</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Enter client credentials to build your pipeline.</p>', unsafe_allow_html=True)

    with st.form("add_client_form", clear_on_submit=True):
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 👤 Primary Information")
        c1, c2 = st.columns(2)
        with c1:
            name    = st.text_input("Full Name *", placeholder="e.g. Rajiv Sharma")
            email   = st.text_input("Email Address", placeholder="e.g. rajiv@company.com")
            company = st.text_input("Company", placeholder="e.g. TechVentures Pvt Ltd")
        with c2:
            phone    = st.text_input("Phone Number", placeholder="+91 98765 43210")
            category = st.selectbox("Category", ["Lead", "Prospect", "Active Client", "Partner", "VIP", "Churned"])
            source   = st.selectbox("Lead Source", ["Referral", "Website", "LinkedIn", "Cold Outreach", "Event", "Other"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 📅 Pipeline & Scheduling")
        c3, c4 = st.columns(2)
        with c3:
            last_contacted = st.date_input("Last Contacted Date", value=date.today())
            followup_days  = st.number_input("Follow-up Cadence (Days) *", min_value=1, max_value=365, value=5)
            deal_value     = st.number_input("Estimated Deal Value (₹)", min_value=0, value=0, step=5000)
        with c4:
            nf = last_contacted + timedelta(days=int(followup_days))
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="sched-badge">
                <p class="sched-lbl">Calculated Next Follow-up</p>
                <p class="sched-date">{nf.strftime("%A, %B %d, %Y")}</p>
                <p style="font-size:0.85rem; color:#667085; font-weight:500; margin:0;">
                    Scheduled <span style="color:#101828; font-weight:700;">{int(followup_days)} days</span> from last contact
                </p>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 📝 Context & Notes")
        notes = st.text_area("Initial Remarks", placeholder="Enter any specific requirements, pain points, or notes about this client...", height=120)
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("💾  Save Client Record", type="primary", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("❌ Full name is a required field.")
        else:
            ok = db.add_client({
                "name": name, "email": email, "phone": phone,
                "company": company, "category": category, "source": source,
                "last_contacted": str(last_contacted), "followup_days": int(followup_days),
                "next_followup": str(nf), "deal_value": deal_value, "notes": notes,
                "created_by": st.session_state.get("user_id", 1)
            })
            if ok:
                st.success(f"✅ **{name}** successfully added to the database. Follow-up scheduled for **{nf.strftime('%b %d')}**.")
            else:
                st.error("❌ Failed to save. Database connection error.")


# ══════════════════════════════════════════════════════════════════════════════
#  ALL CLIENTS
# ══════════════════════════════════════════════════════════════════════════════

def page_all_clients():
    st.markdown('<p class="page-title">Client Master Directory</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Search, filter, and manage your complete book of business.</p>', unsafe_allow_html=True)

    st.markdown('<div class="form-section" style="padding: 24px;">', unsafe_allow_html=True)
    fc1, fc2, fc3 = st.columns([3, 1, 1])
    with fc1: search = st.text_input("🔍 Search Database", placeholder="Search by name, company, or email...", label_visibility="collapsed")
    with fc2: cat    = st.selectbox("Category Filter", ["All","Lead","Prospect","Active Client","Partner","VIP","Churned"], label_visibility="collapsed")
    with fc3: srt    = st.selectbox("Sort Order", ["Next Follow-up","Name","Company","Deal Value"], label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)

    df = db.get_all_clients(
        search=search or None,
        category=cat if cat != "All" else None,
        sort_by=srt
    )

    if df.empty:
        st.info("📭 No records match your criteria.")
        return

    hc1, hc2 = st.columns([5, 1])
    with hc1:
        st.markdown(f"<p style='color:#475467; font-size:0.95rem; font-weight:600; padding-top:10px;'>Showing {len(df)} records</p>", unsafe_allow_html=True)
    with hc2:
        st.download_button(
            "📥 Export to Excel", data=to_excel(df),
            file_name=f"ClientPulse_Export_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    df["Status"]     = df.apply(status_label, axis=1)
    df["Deal Value"] = df["deal_value"].apply(lambda x: f"₹{x:,.0f}" if x else "—")

    show_cols = ["name","company","phone","email","category","next_followup","Status","Deal Value"]
    rename    = {"name":"Name","company":"Company","phone":"Phone","email":"Email",
                 "category":"Category","next_followup":"Next Follow-up"}

    st.markdown('<div style="border: 1px solid #eaecf0; border-radius: 12px; overflow: hidden; box-shadow: 0 1px 3px rgba(16,24,40,0.03);">', unsafe_allow_html=True)
    st.dataframe(
        df[show_cols].rename(columns=rename),
        use_container_width=True, height=500, hide_index=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h4 style='color:#101828; font-weight:800; margin-bottom:16px;'>⚡ Quick Actions</h4>", unsafe_allow_html=True)
    
    st.markdown('<div class="form-section" style="padding: 24px;">', unsafe_allow_html=True)
    rc1, rc2, rc3, rc4 = st.columns([3, 1, 1, 1])
    with rc1: 
        st.markdown("<div style='font-size:0.8rem; font-weight:600; color:#475467; margin-bottom:4px;'>Select Client</div>", unsafe_allow_html=True)
        sel = st.selectbox("Client", df["name"].tolist(), label_visibility="collapsed")
    with rc2: 
        st.markdown("<div style='font-size:0.8rem; font-weight:600; color:#475467; margin-bottom:4px;'>New Date</div>", unsafe_allow_html=True)
        new_d = st.date_input("New Date", value=date.today() + timedelta(days=7), label_visibility="collapsed")
    with rc3:
        st.markdown("<br style='line-height:1.2'>", unsafe_allow_html=True)
        if st.button("Update Date", type="primary", use_container_width=True):
            cid = int(df[df["name"] == sel]["id"].values[0])
            db.update_followup(cid, str(new_d))
            st.success(f"✅ Updated {sel}")
            st.rerun()
    with rc4:
        st.markdown("<br style='line-height:1.2'>", unsafe_allow_html=True)
        if st.button("🗑 Delete Record", use_container_width=True):
            cid = int(df[df["name"] == sel]["id"].values[0])
            db.delete_client(cid)
            st.warning(f"🗑 {sel} permanently deleted.")
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  FOLLOW-UPS
# ══════════════════════════════════════════════════════════════════════════════

def page_followups():
    st.markdown('<p class="page-title">Action Center</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Manage your daily tasks and pipeline progression.</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔴 Overdue Actions", "🟡 Today's Docket", "🟢 Upcoming Pipeline"])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        ov = db.get_overdue_followups()
        if ov.empty:
            st.success("🎉 Excellent! You have no overdue follow-ups.")
        else:
            st.error(f"⚠️ You have {len(ov)} contacts requiring immediate attention.")
            for _, r in ov.iterrows():
                days_over = (date.today() - pd.to_datetime(r["next_followup"]).date()).days
                with st.expander(f"🔴 {r['name']} ({r['company']}) — {days_over} days overdue"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.markdown(f"**📞 Phone:** {r['phone'] or '—'}")
                        st.markdown(f"**✉️ Email:** {r['email'] or '—'}")
                        st.markdown(f"**🏷 Category:** {r['category']}")
                    with cc2:
                        st.markdown(f"**💰 Deal Value:** {'₹{:,.0f}'.format(r['deal_value']) if r['deal_value'] else '—'}")
                        st.markdown(f"**📅 Original Due Date:** {pd.to_datetime(r['next_followup']).strftime('%b %d, %Y')}")
                    st.markdown(f"**📝 Notes:**<br> <span style='color:#667085;'>{r['notes'] or 'No notes provided.'}</span>", unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
                    nd = st.number_input("Reschedule in (days)", min_value=1, value=7, key=f"ov_{r['id']}")
                    if st.button("✅ Mark Contacted & Reschedule", type="primary", key=f"ovb_{r['id']}"):
                        db.update_followup(int(r["id"]), str(date.today() + timedelta(days=nd)), update_last_contacted=True)
                        st.rerun()

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        td = db.get_todays_followups()
        if td.empty:
            st.info("📭 Your docket is clear for today.")
        else:
            st.info(f"📋 You have {len(td)} contacts scheduled for today.")
            for _, r in td.iterrows():
                with st.expander(f"📞 {r['name']} ({r['company']})"):
                    st.markdown("<br>", unsafe_allow_html=True)
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.markdown(f"**📞 Phone:** {r['phone'] or '—'}")
                        st.markdown(f"**✉️ Email:** {r['email'] or '—'}")
                    with cc2:
                        st.markdown(f"**🏷 Category:** {r['category']}")
                        st.markdown(f"**💰 Deal Value:** {'₹{:,.0f}'.format(r['deal_value']) if r['deal_value'] else '—'}")
                    st.markdown(f"**📝 Notes:**<br> <span style='color:#667085;'>{r['notes'] or 'No notes provided.'}</span>", unsafe_allow_html=True)
                    st.markdown("<hr style='margin: 1rem 0;'>", unsafe_allow_html=True)
                    nd = st.number_input("Next follow-up in (days)", min_value=1, value=int(r["followup_days"]), key=f"td_{r['id']}")
                    if st.button("✅ Complete Task & Set Next Date", type="primary", key=f"tdb_{r['id']}"):
                        db.update_followup(int(r["id"]), str(date.today() + timedelta(days=nd)), update_last_contacted=True)
                        st.rerun()

    with tab3:
        st.markdown("<br>", unsafe_allow_html=True)
        days_ahead = st.slider("Forecast Window (Days)", 1, 90, 30)
        up = db.get_upcoming_followups(days_ahead)
        if up.empty:
            st.info(f"No scheduled tasks in the next {days_ahead} days.")
        else:
            up["Days Until"] = up["next_followup"].apply(
                lambda x: (pd.to_datetime(x).date() - date.today()).days)
            st.markdown('<div style="border: 1px solid #eaecf0; border-radius: 12px; overflow: hidden;">', unsafe_allow_html=True)
            st.dataframe(
                up[["name","company","phone","category","next_followup","Days Until"]].rename(columns={
                    "name":"Name","company":"Company","phone":"Phone",
                    "category":"Category","next_followup":"Follow-up Date","Days Until":"⏳ Days Left"}),
                use_container_width=True, hide_index=True
            )
            st.markdown('</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  REPORTS
# ══════════════════════════════════════════════════════════════════════════════

def page_reports():
    st.markdown('<p class="page-title">Analytics & Intelligence</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">High-level insights into your CRM data and pipeline metrics.</p>', unsafe_allow_html=True)

    df = db.get_all_clients()
    if df.empty:
        st.info("Insufficient data to generate reports."); return

    today_d = date.today()
    total_deal = df["deal_value"].sum()
    avg_deal   = df["deal_value"].mean()
    active     = len(df[df["category"] == "Active Client"])
    overdue_n  = len(df[df["next_followup"].apply(
        lambda x: pd.to_datetime(x).date() < today_d if pd.notna(x) else False)])

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, val, lbl, theme in [
        (c1, "💰", f"₹{total_deal:,.0f}",  "Total Pipeline",    "green"),
        (c2, "📊", f"₹{avg_deal:,.0f}",    "Avg Deal Value",    "blue"),
        (c3, "✅", active,                  "Active Clients",    "indigo"),
        (c4, "⚠️", overdue_n,              "Overdue Follow-ups","red"),
    ]:
        col.markdown(f"""
        <div class="metric-card {theme}">
            <div class="metric-icon">{icon}</div>
            <p class="metric-val">{val}</p>
            <p class="metric-lbl">{lbl}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown("<div class='form-section'>", unsafe_allow_html=True)
        st.markdown("<h5 style='margin-top:0;'>Distribution by Category</h5>", unsafe_allow_html=True)
        st.bar_chart(df["category"].value_counts(), height=280)
        st.markdown("</div>", unsafe_allow_html=True)
    with r1c2:
        st.markdown("<div class='form-section'>", unsafe_allow_html=True)
        st.markdown("<h5 style='margin-top:0;'>Acquisition Channels</h5>", unsafe_allow_html=True)
        st.bar_chart(df["source"].value_counts(), height=280)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='form-section'>", unsafe_allow_html=True)
    st.markdown("<h5 style='margin-top:0;'>Pipeline Value by Category (₹)</h5>", unsafe_allow_html=True)
    st.bar_chart(df.groupby("category")["deal_value"].sum(), height=320)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.download_button(
        "📥  Download Full Executive Report (Excel)", data=to_excel(df),
        file_name=f"ClientPulse_Executive_Report_{date.today()}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        type="primary"
    )


# ══════════════════════════════════════════════════════════════════════════════
#  USER MANAGEMENT  (admin only)
# ══════════════════════════════════════════════════════════════════════════════

def page_user_management():
    st.markdown('<p class="page-title">Access & Security</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Manage workspace users, roles, and system access.</p>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👥 Directory", "➕ Provision New User"])

    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        users = db.get_all_users()
        if users.empty:
            st.info("No active users found.")
        else:
            for _, u in users.iterrows():
                initials = "".join(p[0].upper() for p in str(u["full_name"]).split()[:2])
                
                if u["role"] == "admin":
                    role_bg, role_text = "#eef2ff", "#4f46e5" 
                else:
                    role_bg, role_text = "#f1f5f9", "#475467"

                status_bg = "#ecfdf5" if u["is_active"] else "#fef2f2"
                status_color = "#059669" if u["is_active"] else "#dc2626"
                status_text  = "Active" if u["is_active"] else "Suspended"

                uc1, uc2, uc3 = st.columns([5, 1.2, 1.2])
                with uc1:
                    st.markdown(f"""
                    <div style="background: #ffffff; border: 1px solid #eaecf0; border-radius: 16px;
                                padding: 20px 24px; display: flex; align-items: center; gap: 20px;
                                box-shadow: 0 1px 2px rgba(16,24,40,0.03); transition: all 0.2s;">
                        <div style="width: 52px; height: 52px; border-radius: 12px;
                                    background: {role_bg}; border: 1px solid rgba(0,0,0,0.05); display: flex; align-items: center;
                                    justify-content: center; font-size: 1.1rem; font-weight: 800;
                                    color: {role_text}; flex-shrink: 0;">{initials}</div>
                        <div style="flex: 1; min-width: 0;">
                            <div style="font-size: 1.05rem; font-weight: 800; color: #101828;">{u['full_name']}</div>
                            <div style="font-size: 0.85rem; color: #667085; font-weight: 500; margin-top: 4px; display:flex; gap:10px; align-items:center;">
                                <span>@{u['username']}</span> • 
                                <span>{u['email'] or 'No email'}</span> • 
                                <span style="background: {role_bg}; color: {role_text}; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">{u['role'].title()}</span> • 
                                <span style="background: {status_bg}; color: {status_color}; padding: 2px 8px; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">{status_text}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                with uc2:
                    st.markdown("<br style='line-height:0.8'>", unsafe_allow_html=True)
                    if u["username"] != st.session_state.get("username"):
                        lbl = "Suspend Access" if u["is_active"] else "Restore Access"
                        if st.button(lbl, key=f"tog_{u['id']}", use_container_width=True):
                            db.toggle_user_status(int(u["id"]))
                            st.rerun()
                with uc3:
                    st.markdown("<br style='line-height:0.8'>", unsafe_allow_html=True)
                    if u["username"] != st.session_state.get("username"):
                        if st.button("🗑 Revoke User", key=f"del_{u['id']}", use_container_width=True):
                            db.delete_user(int(u["id"]))
                            st.success(f"Revoked {u['username']}"); st.rerun()

                st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### Provision New Identity")
        with st.form("add_user_form", clear_on_submit=True):
            ac1, ac2 = st.columns(2)
            with ac1:
                new_fullname = st.text_input("Legal Full Name *", placeholder="e.g. Arjun Kapoor")
                new_username = st.text_input("System Username *", placeholder="e.g. arjun.kapoor")
                new_email    = st.text_input("Corporate Email", placeholder="e.g. arjun@company.com")
            with ac2:
                new_password  = st.text_input("Initial Password *", type="password", placeholder="Minimum 6 characters")
                new_password2 = st.text_input("Verify Password *", type="password", placeholder="Repeat password")
                new_role      = st.selectbox("Authorization Level", ["user", "admin"],
                                             format_func=lambda x: "👤 Standard User" if x == "user" else "🛡️ System Administrator")

            st.markdown("<br>", unsafe_allow_html=True)
            add_submitted = st.form_submit_button("➕ Provision Account", type="primary", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if add_submitted:
            errors = []
            if not new_fullname.strip(): errors.append("Full name is required.")
            if not new_username.strip():  errors.append("Username is required.")
            if not new_password:          errors.append("Password is required.")
            if len(new_password) < 6:     errors.append("Password must be at least 6 characters.")
            if new_password != new_password2: errors.append("Passwords do not match.")
            if db.username_exists(new_username): errors.append(f"Username '{new_username}' is currently allocated.")

            if errors:
                for e in errors: st.error(f"❌ {e}")
            else:
                ok = db.add_user({
                    "full_name": new_fullname, "username": new_username,
                    "email": new_email, "password_hash": hash_password(new_password),
                    "role": new_role
                })
                if ok:
                    st.success(f"✅ Identity provisioned for **{new_fullname}** with **{new_role}** rights.")
                else:
                    st.error("❌ System Error: Provisioning failed. Check database state.")


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN ROUTER
# ══════════════════════════════════════════════════════════════════════════════

if not st.session_state.get("logged_in"):
    show_login()
else:
    page = show_sidebar()
    clean = page.strip().lstrip("🏠➕👥📅📊⚙️ ")

    if   "Dashboard"        in page: page_dashboard()
    elif "Add Client"       in page: page_add_client()
    elif "All Clients"      in page: page_all_clients()
    elif "Follow-ups"       in page: page_followups()
    elif "Reports"          in page: page_reports()
    elif "User Management"  in page:
        if st.session_state.get("role") == "admin":
            page_user_management()
        else:
            st.error("🔒 Security Exception: Elevated privileges required.")
