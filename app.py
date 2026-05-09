import streamlit as st
import pandas as pd
from datetime import date, timedelta
import io
import hashlib
import secrets
from database import DatabaseManager

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ClientPulse CRM",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

*, html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── Hide default Streamlit chrome on login page ── */
.login-mode header,
.login-mode [data-testid="stSidebar"],
.login-mode footer { display: none !important; }

/* ── Smooth Fade-In Animation ── */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

/* ── Sidebar (Light Modern Theme) ── */
[data-testid="stSidebar"] {
    background: #ffffff !important;
    border-right: 1px solid #e2e8f0;
}
[data-testid="stSidebar"] section { padding-top: 0 !important; }
[data-testid="stSidebar"] * { color: #334155 !important; }
[data-testid="stSidebar"] .stRadio > label { display: none; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] { gap: 4px; }
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    background: transparent;
    border-radius: 8px;
    padding: 10px 14px !important;
    font-size: 0.875rem !important;
    font-weight: 600 !important;
    color: #475569 !important;
    transition: all 0.2s ease;
    cursor: pointer;
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
    background: #f1f5f9 !important;
    color: #0f172a !important;
    transform: translateX(4px);
}
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[data-baseweb="radio"] { display: flex; }

/* ── Main area ── */
.main .block-container { 
    padding: 2rem 2.5rem 2rem 2.5rem; 
    max-width: 1400px; 
    animation: fadeIn 0.4s ease-out;
}
.main { background: #fafaf9; } /* Extremely light warm gray */

/* ── Metric cards with Interactive Hover ── */
.metric-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.metric-card:hover { 
    box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.08); 
    transform: translateY(-4px); 
    border-color: #cbd5e1;
}
.metric-icon { font-size: 1.8rem; margin-bottom: 12px; }
.metric-val  { font-size: 2.2rem; font-weight: 800; color: #0f172a; margin: 0 0 4px; line-height:1; }
.metric-lbl  { font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; margin: 0; }

/* ── Section headers ── */
.page-title { font-size: 1.75rem; font-weight: 800; color: #0f172a; margin: 0 0 4px; letter-spacing: -0.02em; }
.page-sub   { font-size: 0.9rem; color: #64748b; margin: 0 0 1.8rem; }

/* ── Alert strips ── */
.strip-today   { background: white; border-left: 4px solid #3b82f6; border-radius: 12px; padding: 16px 20px; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); border: 1px solid #e2e8f0; border-left-width: 4px; transition: transform 0.2s;}
.strip-today:hover { transform: translateX(2px); }
.strip-overdue { background: white; border-left: 4px solid #ef4444; border-radius: 12px; padding: 16px 20px; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); border: 1px solid #e2e8f0; border-left-width: 4px; transition: transform 0.2s;}
.strip-overdue:hover { transform: translateX(2px); }
.strip-ok      { background: white; border-left: 4px solid #22c55e; border-radius: 12px; padding: 16px 20px; margin-bottom: 12px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); border: 1px solid #e2e8f0; border-left-width: 4px; }
.strip-title   { font-size: 0.95rem; font-weight: 700; color: #0f172a; margin: 0 0 4px; }
.strip-meta    { font-size: 0.8rem; color: #64748b; margin: 0; font-weight: 500; }

/* ── Big CTA ── */
.big-cta button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 14px !important;
    font-size: 1.05rem !important;
    font-weight: 600 !important;
    padding: 0.85rem 0 !important;
    letter-spacing: 0.01em;
    box-shadow: 0 8px 20px rgba(79, 70, 229, 0.25) !important;
    transition: all 0.2s ease !important;
}
.big-cta button:hover { opacity: 0.95 !important; transform: translateY(-2px) scale(1.01) !important; box-shadow: 0 12px 25px rgba(79, 70, 229, 0.35) !important; }

/* ── Form card ── */
.form-section {
    background: white;
    border-radius: 16px;
    padding: 28px 32px;
    border: 1px solid #e2e8f0;
    margin-bottom: 20px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.02);
}

/* ── Scheduled badge ── */
.sched-badge {
    background: #f8fafc;
    border: 1px dashed #cbd5e1;
    border-radius: 12px;
    padding: 16px 18px;
    text-align: center;
}
.sched-date { font-size: 1.25rem; font-weight: 800; color: #0f172a; margin: 4px 0 0; }
.sched-lbl  { font-size: 0.72rem; font-weight: 700; color: #475569; text-transform: uppercase; letter-spacing: 0.08em; margin: 0; }

/* ── Buttons ── */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    transition: all 0.2s ease !important;
    border: 1px solid #e2e8f0 !important;
}
.stButton > button:hover { 
    transform: translateY(-2px) !important; 
    box-shadow: 0 6px 15px rgba(0,0,0,0.08) !important; 
    border-color: #cbd5e1 !important;
}
[data-testid="stDownloadButton"] > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    background: white !important;
    border: 1px solid #e2e8f0 !important;
    transition: all 0.2s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 15px rgba(0,0,0,0.05) !important;
}

div[data-testid="stTabs"] button { font-weight: 600 !important; }

/* ── Expander ── */
details { 
    border-radius: 12px !important; 
    border: 1px solid #e2e8f0 !important; 
    background: white !important;
    transition: box-shadow 0.2s ease !important;
}
details:hover { box-shadow: 0 4px 10px rgba(0,0,0,0.03) !important; }
details summary { font-weight: 600 !important; color: #0f172a !important; }

hr { border: none; border-top: 1px solid #e2e8f0; margin: 1.5rem 0; }
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
#  LOGIN PAGE (Modern Light SaaS Look)
# ══════════════════════════════════════════════════════════════════════════════

def show_login():
    st.markdown("""
    <div style="
        min-height:100vh;
        display:flex;
        align-items:center;
        justify-content:center;
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
        padding:2rem;
        margin:-6rem -2.5rem -2rem -2.5rem;
    ">
    <div style="
        background:rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.5);
        border-radius:24px;
        padding:56px 48px;
        width:100%;
        max-width:440px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
    ">
        <div style="text-align:center;margin-bottom:36px;">
            <div style="font-size:3.2rem;margin-bottom:8px; animation: fadeIn 0.6s ease-out;">💼</div>
            <div style="font-size:1.6rem;font-weight:800;color:#0f172a;letter-spacing:-0.03em;">ClientPulse CRM</div>
            <div style="font-size:0.85rem;color:#64748b;font-weight:600;text-transform:uppercase;letter-spacing:0.1em;margin-top:6px;">Sign in to your workspace</div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button("Sign In →", use_container_width=True, type="primary")

    if submitted:
        if not username or not password:
            st.error("Please enter both username and password.")
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
                st.error("❌ Invalid username or password.")

    st.markdown("""
        <div style="text-align:center;margin-top:28px;font-size:0.8rem;color:#94a3b8;font-weight:500;">
            Secure access • Contact admin for setup
        </div>
    </div></div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

def show_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align:center;padding:24px 0 24px;">
            <div style="font-size:2.2rem; margin-bottom: 4px;">💼</div>
            <div style="font-size:1.2rem;font-weight:800;color:#0f172a;letter-spacing:-0.02em;">ClientPulse</div>
            <div style="font-size:0.7rem;color:#64748b;text-transform:uppercase;letter-spacing:0.1em;font-weight:600;">CRM System</div>
        </div>
        """, unsafe_allow_html=True)

        role = st.session_state.get("role", "user")
        full_name = st.session_state.get("full_name", "User")
        username  = st.session_state.get("username", "")

        initials = "".join(p[0].upper() for p in full_name.split()[:2])
        st.markdown(f"""
        <div class="sb-user" style="background:#f8fafc; border: 1px solid #e2e8f0; border-radius: 12px; padding: 12px 14px; margin: 8px 0 20px; transition: all 0.2s ease;">
            <div style="display:flex;align-items:center;gap:12px;">
                <div style="width:38px;height:38px;border-radius:10px;background:#e0e7ff;
                            display:flex;align-items:center;justify-content:center;
                            font-size:0.85rem;font-weight:800;color:#4f46e5;flex-shrink:0;">
                    {initials}
                </div>
                <div>
                    <div style="font-size:0.85rem;font-weight:700;color:#0f172a;">{full_name}</div>
                    <div style="font-size:0.72rem;color:#64748b;font-weight:500;">
                        {'⚙️ Admin' if role == 'admin' else '👤 User'} · @{username}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        nav_options = ["🏠  Dashboard", "➕  Add Client", "👥  All Clients", "📅  Follow-ups", "📊  Reports"]
        if role == "admin":
            nav_options.append("⚙️  User Management")

        page = st.radio("Navigation", nav_options, label_visibility="collapsed")

        st.markdown("<div style='height:1px;background:#e2e8f0;margin:16px 0;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="padding:12px 16px;background:#f8fafc; border: 1px solid #e2e8f0; border-radius:12px;margin-bottom:16px;">
            <div style="font-size:0.68rem;font-weight:700;color:#64748b;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:2px;">Today's Date</div>
            <div style="font-size:0.85rem;font-weight:700;color:#0f172a;">{date.today().strftime("%B %d, %Y")}</div>
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
    st.markdown('<p class="page-title">Dashboard</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="page-sub">Welcome back, <b>{st.session_state.get("full_name","User")}</b> 👋 Here is what’s happening today.</p>', unsafe_allow_html=True)

    total = db.get_total_clients()
    today_df  = db.get_todays_followups()
    over_df   = db.get_overdue_followups()
    upc_df    = db.get_upcoming_followups(7)

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, val, lbl, color in [
        (c1, "👥", total,           "Total Clients",   "#0f172a"),
        (c2, "📞", len(today_df),   "Due Today",       "#3b82f6"),
        (c3, "🔴", len(over_df),    "Overdue",         "#ef4444"),
        (c4, "📆", len(upc_df),     "Next 7 Days",     "#8b5cf6"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <p class="metric-val" style="color:{color};">{val}</p>
            <p class="metric-lbl">{lbl}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown('<div class="big-cta">', unsafe_allow_html=True)
        if st.button("🔔  Who Do I Call Today?", use_container_width=True):
            st.session_state.show_today = not st.session_state.get("show_today", False)
        st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.get("show_today"):
        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("#### 📞 Call Today")
            if today_df.empty:
                st.markdown('<div class="strip-ok"><p class="strip-title">All clear!</p><p class="strip-meta">No follow-ups scheduled for today.</p></div>', unsafe_allow_html=True)
            else:
                for _, r in today_df.iterrows():
                    st.markdown(f"""
                    <div class="strip-today">
                        <p class="strip-title">👤 {r['name']} <span style="color:#64748b;font-weight:500;">— {r['company']}</span></p>
                        <p class="strip-meta">📞 {r['phone'] or '—'} &nbsp;·&nbsp; ✉️ {r['email'] or '—'} &nbsp;·&nbsp; <span style="background:#f1f5f9;padding:2px 6px;border-radius:4px;">🏷 {r['category']}</span></p>
                        <p class="strip-meta" style="margin-top:8px; padding-top:8px; border-top:1px dashed #e2e8f0;">📝 {r['notes'] or 'No notes provided'}</p>
                    </div>""", unsafe_allow_html=True)

        with col_b:
            st.markdown("#### ⚠️ Overdue")
            if over_df.empty:
                st.markdown('<div class="strip-ok"><p class="strip-title">No overdue!</p><p class="strip-meta">You\'re on top of everything.</p></div>', unsafe_allow_html=True)
            else:
                for _, r in over_df.iterrows():
                    d = (date.today() - pd.to_datetime(r['next_followup']).date()).days
                    st.markdown(f"""
                    <div class="strip-overdue">
                        <p class="strip-title">⏰ {r['name']} <span style="color:#64748b;font-weight:500;">— {r['company']}</span> <span style="font-size:0.75rem;color:#ef4444;background:#fef2f2;padding:2px 6px;border-radius:4px;">{d}d overdue</span></p>
                        <p class="strip-meta">📞 {r['phone'] or '—'} &nbsp;·&nbsp; ✉️ {r['email'] or '—'}</p>
                    </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
#  ADD CLIENT
# ══════════════════════════════════════════════════════════════════════════════

def page_add_client():
    st.markdown('<p class="page-title">Add New Client</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Fill in the details below to add a client and schedule a follow-up</p>', unsafe_allow_html=True)

    with st.form("add_client_form", clear_on_submit=True):
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 👤 Personal Information")
        c1, c2 = st.columns(2)
        with c1:
            name    = st.text_input("Full Name *", placeholder="Rajiv Sharma")
            email   = st.text_input("Email Address", placeholder="rajiv@company.com")
            company = st.text_input("Company", placeholder="TechVentures Pvt Ltd")
        with c2:
            phone    = st.text_input("Phone Number", placeholder="+91 98765 43210")
            category = st.selectbox("Category", ["Lead", "Prospect", "Active Client", "Partner", "VIP", "Churned"])
            source   = st.selectbox("Lead Source", ["Referral", "Website", "LinkedIn", "Cold Outreach", "Event", "Other"])
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 📅 Follow-up Schedule")
        c3, c4 = st.columns(2)
        with c3:
            last_contacted = st.date_input("Last Contacted Date", value=date.today())
            followup_days  = st.number_input("Follow-up After (days) *", min_value=1, max_value=365, value=5,
                                             help="System will remind you after this many days")
            deal_value     = st.number_input("Deal Value (₹)", min_value=0, value=0, step=1000)
        with c4:
            nf = last_contacted + timedelta(days=int(followup_days))
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="sched-badge">
                <p class="sched-lbl">📌 Scheduled Follow-up</p>
                <p class="sched-date">{nf.strftime("%B %d, %Y")}</p>
                <p style="font-size:0.8rem;color:#475569;margin:6px 0 0;font-weight:500;">
                    In <span style="color:#0f172a;font-weight:700;">{int(followup_days)} days</span> from last contact
                </p>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### 📝 Notes")
        notes = st.text_area("Notes / Remarks", placeholder="Any important details about this client…", height=100)
        st.markdown('</div>', unsafe_allow_html=True)

        submitted = st.form_submit_button("💾  Save Client", type="primary", use_container_width=True)

    if submitted:
        if not name.strip():
            st.error("❌ Full name is required.")
        else:
            ok = db.add_client({
                "name": name, "email": email, "phone": phone,
                "company": company, "category": category, "source": source,
                "last_contacted": str(last_contacted), "followup_days": int(followup_days),
                "next_followup": str(nf), "deal_value": deal_value, "notes": notes,
                "created_by": st.session_state.get("user_id", 1)
            })
            if ok:
                st.success(f"✅ **{name}** added! Follow-up scheduled for **{nf.strftime('%B %d, %Y')}**.")
            else:
                st.error("❌ Failed to save. Check your database connection.")


# ══════════════════════════════════════════════════════════════════════════════
#  ALL CLIENTS
# ══════════════════════════════════════════════════════════════════════════════

def page_all_clients():
    st.markdown('<p class="page-title">All Clients</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Search, filter and manage your entire client database</p>', unsafe_allow_html=True)

    fc1, fc2, fc3 = st.columns([3, 1, 1])
    with fc1: search = st.text_input("🔍 Search", placeholder="Name, company or email…", label_visibility="collapsed")
    with fc2: cat    = st.selectbox("Category", ["All","Lead","Prospect","Active Client","Partner","VIP","Churned"], label_visibility="collapsed")
    with fc3: srt    = st.selectbox("Sort", ["Next Follow-up","Name","Company","Deal Value"], label_visibility="collapsed")

    df = db.get_all_clients(
        search=search or None,
        category=cat if cat != "All" else None,
        sort_by=srt
    )

    if df.empty:
        st.info("📭 No clients found. Try adjusting your filters or add a new client.")
        return

    hc1, hc2 = st.columns([5, 1])
    with hc1:
        st.markdown(f"<p style='color:#64748b;font-size:0.85rem;margin:0;padding-top:10px;'>Showing <b>{len(df)}</b> client(s)</p>", unsafe_allow_html=True)
    with hc2:
        st.download_button(
            "📥 Export Excel", data=to_excel(df),
            file_name=f"clients_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

    df["Status"]     = df.apply(status_label, axis=1)
    df["Deal Value"] = df["deal_value"].apply(lambda x: f"₹{x:,.0f}" if x else "—")

    show_cols = ["name","company","phone","email","category","next_followup","Status","Deal Value"]
    rename    = {"name":"Name","company":"Company","phone":"Phone","email":"Email",
                 "category":"Category","next_followup":"Next Follow-up"}

    st.dataframe(
        df[show_cols].rename(columns=rename),
        use_container_width=True, height=460, hide_index=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("##### ✏️ Reschedule a Follow-up")
    rc1, rc2, rc3, rc4 = st.columns([3, 1, 1, 1])
    with rc1: sel    = st.selectbox("Client", df["name"].tolist(), label_visibility="collapsed")
    with rc2: new_d  = st.date_input("New Date", value=date.today() + timedelta(days=7), label_visibility="collapsed")
    with rc3:
        if st.button("Update", type="primary", use_container_width=True):
            cid = int(df[df["name"] == sel]["id"].values[0])
            db.update_followup(cid, str(new_d))
            st.success(f"✅ {sel} → {new_d.strftime('%b %d, %Y')}")
            st.rerun()
    with rc4:
        if st.button("🗑 Delete", use_container_width=True):
            cid = int(df[df["name"] == sel]["id"].values[0])
            db.delete_client(cid)
            st.warning(f"🗑 {sel} deleted.")
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
#  FOLLOW-UPS
# ══════════════════════════════════════════════════════════════════════════════

def page_followups():
    st.markdown('<p class="page-title">Follow-up Calendar</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Track every scheduled, overdue and upcoming follow-up</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["🔴  Overdue", "🟡  Due Today", "🟢  Upcoming"])

    with tab1:
        ov = db.get_overdue_followups()
        if ov.empty:
            st.success("🎉 Zero overdue follow-ups — great job!")
        else:
            st.warning(f"⚠️ {len(ov)} overdue contact(s) need attention")
            for _, r in ov.iterrows():
                days_over = (date.today() - pd.to_datetime(r["next_followup"]).date()).days
                with st.expander(f"🔴  {r['name']}  —  {r['company']}  ·  {days_over}d overdue"):
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.write(f"📞 **Phone:** {r['phone'] or '—'}")
                        st.write(f"✉️ **Email:** {r['email'] or '—'}")
                        st.write(f"🏷 **Category:** {r['category']}")
                    with cc2:
                        st.write(f"💰 **Deal Value:** {'₹{:,.0f}'.format(r['deal_value']) if r['deal_value'] else '—'}")
                        st.write(f"📅 **Was due:** {pd.to_datetime(r['next_followup']).strftime('%b %d, %Y')}")
                        st.write(f"📝 {r['notes'] or 'No notes'}")
                    nd = st.number_input("Reschedule in (days)", min_value=1, value=7, key=f"ov_{r['id']}")
                    if st.button("✅ Mark contacted & reschedule", key=f"ovb_{r['id']}"):
                        db.update_followup(int(r["id"]), str(date.today() + timedelta(days=nd)), update_last_contacted=True)
                        st.success("Updated!"); st.rerun()

    with tab2:
        td = db.get_todays_followups()
        if td.empty:
            st.info("📭 No follow-ups scheduled for today.")
        else:
            st.info(f"📞 {len(td)} client(s) to contact today")
            for _, r in td.iterrows():
                with st.expander(f"📞  {r['name']}  —  {r['company']}"):
                    cc1, cc2 = st.columns(2)
                    with cc1:
                        st.write(f"📞 **Phone:** {r['phone'] or '—'}")
                        st.write(f"✉️ **Email:** {r['email'] or '—'}")
                    with cc2:
                        st.write(f"🏷 **Category:** {r['category']}")
                        st.write(f"💰 {'₹{:,.0f}'.format(r['deal_value']) if r['deal_value'] else '—'}")
                    st.write(f"📝 {r['notes'] or 'No notes'}")
                    nd = st.number_input("Next follow-up in (days)", min_value=1, value=int(r["followup_days"]), key=f"td_{r['id']}")
                    if st.button("✅ Done — set next follow-up", key=f"tdb_{r['id']}"):
                        db.update_followup(int(r["id"]), str(date.today() + timedelta(days=nd)), update_last_contacted=True)
                        st.success("Saved!"); st.rerun()

    with tab3:
        days_ahead = st.slider("Show next N days", 1, 90, 30)
        up = db.get_upcoming_followups(days_ahead)
        if up.empty:
            st.info(f"Nothing in the next {days_ahead} days.")
        else:
            up["Days Until"] = up["next_followup"].apply(
                lambda x: (pd.to_datetime(x).date() - date.today()).days)
            st.dataframe(
                up[["name","company","phone","category","next_followup","Days Until"]].rename(columns={
                    "name":"Name","company":"Company","phone":"Phone",
                    "category":"Category","next_followup":"Follow-up Date","Days Until":"⏳ Days"}),
                use_container_width=True, hide_index=True
            )


# ══════════════════════════════════════════════════════════════════════════════
#  REPORTS
# ══════════════════════════════════════════════════════════════════════════════

def page_reports():
    st.markdown('<p class="page-title">Reports & Analytics</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Pipeline insights and downloadable exports</p>', unsafe_allow_html=True)

    df = db.get_all_clients()
    if df.empty:
        st.info("No client data yet."); return

    today_d = date.today()
    total_deal = df["deal_value"].sum()
    avg_deal   = df["deal_value"].mean()
    active     = len(df[df["category"] == "Active Client"])
    overdue_n  = len(df[df["next_followup"].apply(
        lambda x: pd.to_datetime(x).date() < today_d if pd.notna(x) else False)])

    c1, c2, c3, c4 = st.columns(4)
    for col, icon, val, lbl, color in [
        (c1, "💰", f"₹{total_deal:,.0f}",  "Total Pipeline",    "#0f172a"),
        (c2, "📊", f"₹{avg_deal:,.0f}",    "Avg Deal Value",    "#3b82f6"),
        (c3, "✅", active,                  "Active Clients",    "#22c55e"),
        (c4, "⚠️", overdue_n,              "Overdue Follow-ups","#ef4444"),
    ]:
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <p class="metric-val" style="color:{color};">{val}</p>
            <p class="metric-lbl">{lbl}</p>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown("##### Clients by category")
        st.bar_chart(df["category"].value_counts(), height=260)
    with r1c2:
        st.markdown("##### Clients by source")
        st.bar_chart(df["source"].value_counts(), height=260)

    st.markdown("<br>##### Deal value by category (₹)", unsafe_allow_html=True)
    st.bar_chart(df.groupby("category")["deal_value"].sum(), height=280)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.download_button(
        "📥  Download Full Report (Excel)", data=to_excel(df),
        file_name=f"crm_report_{date.today()}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ══════════════════════════════════════════════════════════════════════════════
#  USER MANAGEMENT  (admin only)
# ══════════════════════════════════════════════════════════════════════════════

def page_user_management():
    st.markdown('<p class="page-title">User Management</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Add, view and manage CRM users (admin only)</p>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👥  All Users", "➕  Add User"])

    with tab1:
        users = db.get_all_users()
        if users.empty:
            st.info("No users found.")
        else:
            for _, u in users.iterrows():
                initials = "".join(p[0].upper() for p in str(u["full_name"]).split()[:2])
                role_color = "#4f46e5" if u["role"] == "admin" else "#3b82f6"
                role_bg    = "#e0e7ff" if u["role"] == "admin" else "#eff6ff"
                status_color = "#22c55e" if u["is_active"] else "#ef4444"
                status_text  = "Active" if u["is_active"] else "Inactive"

                uc1, uc2, uc3 = st.columns([5, 1, 1])
                with uc1:
                    st.markdown(f"""
                    <div style="background:white; border:1px solid #e2e8f0; border-radius:12px;
                                padding:16px 20px; display:flex; align-items:center; gap:16px;
                                box-shadow: 0 2px 4px rgba(0,0,0,0.02); transition: transform 0.2s; cursor:default;"
                         onmouseover="this.style.transform='translateY(-2px)'" onmouseout="this.style.transform='translateY(0)'">
                        <div style="width:44px; height:44px; border-radius:12px;
                                    background:{role_bg}; display:flex; align-items:center;
                                    justify-content:center; font-size:0.9rem; font-weight:800;
                                    color:{role_color}; flex-shrink:0;">{initials}</div>
                        <div style="flex:1;min-width:0;">
                            <div style="font-size:0.95rem; font-weight:700; color:#0f172a;">{u['full_name']}</div>
                            <div style="font-size:0.8rem; color:#64748b; font-weight:500; margin-top:2px;">
                                @{u['username']} &nbsp;·&nbsp; {u['email'] or '—'} &nbsp;·&nbsp;
                                <span style="background:{role_bg}; color:{role_color};
                                             padding:2px 8px; border-radius:6px; font-size:0.72rem;
                                             font-weight:700;">{u['role'].title()}</span>
                                &nbsp;·&nbsp;
                                <span style="color:{status_color}; font-size:0.75rem; font-weight:700;">● {status_text}</span>
                            </div>
                        </div>
                    </div>""", unsafe_allow_html=True)
                with uc2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if u["username"] != st.session_state.get("username"):
                        lbl = "Deactivate" if u["is_active"] else "Activate"
                        if st.button(lbl, key=f"tog_{u['id']}", use_container_width=True):
                            db.toggle_user_status(int(u["id"]))
                            st.rerun()
                with uc3:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if u["username"] != st.session_state.get("username"):
                        if st.button("🗑 Delete", key=f"del_{u['id']}", use_container_width=True):
                            db.delete_user(int(u["id"]))
                            st.success(f"Deleted {u['username']}"); st.rerun()

                st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="form-section">', unsafe_allow_html=True)
        st.markdown("##### New user details")
        with st.form("add_user_form", clear_on_submit=True):
            ac1, ac2 = st.columns(2)
            with ac1:
                new_fullname = st.text_input("Full Name *", placeholder="Arjun Kapoor")
                new_username = st.text_input("Username *", placeholder="arjun.kapoor")
                new_email    = st.text_input("Email", placeholder="arjun@company.com")
            with ac2:
                new_password  = st.text_input("Password *", type="password", placeholder="Min 6 characters")
                new_password2 = st.text_input("Confirm Password *", type="password", placeholder="Repeat password")
                new_role      = st.selectbox("Role", ["user", "admin"],
                                             format_func=lambda x: "👤 User" if x == "user" else "⚙️ Admin")

            st.markdown("<br>", unsafe_allow_html=True)
            add_submitted = st.form_submit_button("➕  Create User", type="primary", use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if add_submitted:
            errors = []
            if not new_fullname.strip(): errors.append("Full name is required.")
            if not new_username.strip():  errors.append("Username is required.")
            if not new_password:          errors.append("Password is required.")
            if len(new_password) < 6:     errors.append("Password must be at least 6 characters.")
            if new_password != new_password2: errors.append("Passwords do not match.")
            if db.username_exists(new_username): errors.append(f"Username '{new_username}' already taken.")

            if errors:
                for e in errors: st.error(f"❌ {e}")
            else:
                ok = db.add_user({
                    "full_name": new_fullname, "username": new_username,
                    "email": new_email, "password_hash": hash_password(new_password),
                    "role": new_role
                })
                if ok:
                    st.success(f"✅ User **{new_fullname}** (@{new_username}) created as **{new_role}**.")
                else:
                    st.error("❌ Failed to create user. Check DB connection.")


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
            st.error("🔒 Access denied. Admins only.")
