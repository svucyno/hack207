import streamlit as st

def render_sidebar():
    st.sidebar.markdown("### 🛡️ MalwareGuard AI")
    st.sidebar.markdown("---")
    
    pages = {
        "Dashboard": "🏠 Dashboard",
        "Scan": "🔍 Scan File",
        "Explainability": "🔍 Explainability",
        "History": "📜 History",
        "Quarantine": "🚫 Quarantine",
        "BehavioralDNA": "🛡️ BehavioralDNA"
    }
    
    current_page = st.sidebar.radio("Navigation", list(pages.values()))
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 👁️ Live Behavior Monitor")
    
    from pages.BehavioralDNA import get_user_baseline, detect_anomaly
    
    baseline = get_user_baseline(1)
    if baseline:
        b_typing, b_mouse, b_click = baseline
    else:
        b_typing, b_mouse, b_click = 65, 220, 40

    c_typing = st.sidebar.slider("Current Typing Speed (WPM)", 0, 500, int(b_typing))
    c_mouse = st.sidebar.slider("Current Mouse Speed (px/s)", 0, 2000, int(b_mouse))
    c_click = st.sidebar.slider("Current Click Rate (/min)", 0, 1000, int(b_click))
    
    current_behavior = (c_typing, c_mouse, c_click)
    
    st.sidebar.markdown("---")
    if baseline:
        is_anomaly, deviation = detect_anomaly(current_behavior, baseline, threshold=60)
        
        status_text = "🚨 Anomaly / High Risk" if is_anomaly else "✅ Normal"
        status_col = "#ef4444" if is_anomaly else "#22c55e"
        
        st.sidebar.markdown(f"**Deviation Status**: <span style='color:{status_col}; font-weight:bold;'>{status_text}</span>", unsafe_allow_html=True)
        st.sidebar.markdown(f"**Score**: {deviation:.1f}%")
        
        # Update global lockout state
        if is_anomaly:
            st.session_state["dna_quarantine"] = True
        else:
            st.session_state["dna_quarantine"] = False
    else:
        st.sidebar.info("Set baseline in BehavioralDNA page first.")
        
    return current_page
