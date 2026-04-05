import streamlit as st
import sys
import os

# ✅ MUST be first
st.set_page_config(page_title="MalwareGuard AI", page_icon="🛡️", layout="wide")

# ✅ Fix import path (important)
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# ✅ Import components (UPDATED)
from components.styles import load_css
from components.navbar import render_sidebar

# ✅ Import pages (UPDATED FIX)
from pages import dashboard, scan, explain, history, BehavioralDNA, quarantine

# ✅ Backend + DB
from database.db import init_db
from backend.model import load_or_train_model

# -------------------------------
# ✅ INIT SYSTEM
# -------------------------------
init_db()
load_css()

# Load model once
model, dummy_X = load_or_train_model()
feature_names = dummy_X.columns.tolist()

# -------------------------------
# ✅ HEADER
# -------------------------------
col1, col2 = st.columns([4, 1])

with col1:
    st.title("🛡️ MalwareGuard AI")
    st.caption("Explainable Malware Detection")

with col2:
    st.markdown("""
    <div style='text-align:right; margin-top:15px;'>
        <span style='background:#065f46; color:#a7f3d0; padding:6px 12px;
        border-radius:20px; font-weight:bold;'>
        ✅ Secure
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -------------------------------
# ✅ SIDEBAR NAVIGATION
# -------------------------------
page = render_sidebar()

# -------------------------------
# ✅ DNA QUARANTINE OVERRIDE
# -------------------------------
if st.session_state.get("dna_quarantine", False):
    st.markdown("""
    <div style='background:#ef4444; color:white; padding:50px; text-align:center; border-radius:10px; margin-top:50px;'>
        <h1 style='font-size:50px;'>🚫 ACCESS DENIED</h1>
        <h2>System Quarantined due to Behavioral DNA Anomaly</h2>
        <p>Your simulated input behavior deviated significantly from the baseline security profile.</p>
        <p><i>The system is completely locked out. Adjust the live monitor back to normal ranges to restore access.</i></p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# Debug (optional)
st.write(f"DEBUG → Current Page: {page}")

# -------------------------------
# ✅ ROUTING (NO BLANK PAGE GUARANTEE)
# -------------------------------
try:
    if page == "🏠 Dashboard":
        dashboard.show_dashboard()

    elif page == "🔍 Scan File":
        scan.show_scan(model, feature_names)

    elif page == "🔍 Explainability":
        explain.show_explain(model, feature_names)

    elif page == "📜 History":
        history.show_history()

    elif page == "🚫 Quarantine":
        quarantine.show_quarantine()

    elif page == "🛡️ BehavioralDNA":
        BehavioralDNA.show_BehavioralDNA(is_malicious_context=False)

    else:
        st.warning("⚠️ Page not found. Defaulting to Dashboard.")
        dashboard.show_dashboard()

except Exception as e:
    st.error("🚨 Something went wrong while loading the page.")
    st.exception(e)

# -------------------------------
# ✅ REMOVE DEFAULT STREAMLIT NAV
# -------------------------------
st.markdown("""
<style>
[data-testid="stSidebarNav"] {display: none;}
</style>
""", unsafe_allow_html=True)