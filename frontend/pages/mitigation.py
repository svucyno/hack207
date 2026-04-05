import streamlit as st
from database.db import save_user_baseline, get_user_baseline

def show_mitigation(is_malicious_context=False):
    if is_malicious_context:
        st.markdown("""
        <div class="card glow-purple">
            <h3 style='margin-bottom:0px;'>🛡️ Mitigation & Isolation</h3>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        - ⚠️ **Avoid Execution**: The file has been quarantined.
        - 🛑 **Network Block**: Hash blacklisted.
        - 🛡️ **System Isolation**: File is securely moved to the quarantine folder.
        """)
        return
        
    st.markdown("### ⚙️ DNA Security BehavioralDNA")
    st.markdown("Configure your behavioral baseline to detect system anomalies.")
    
    # Fetch current baseline
    baseline = get_user_baseline(1)
    if baseline:
        b_typing, b_mouse, b_click = baseline
    else:
        b_typing, b_mouse, b_click = 65, 220, 40
        
    with st.form("dna_baseline_form"):
        typing_speed = st.number_input("Baseline Typing Speed (WPM)", min_value=0, max_value=500, value=int(b_typing))
        mouse_speed = st.number_input("Baseline Mouse Speed (px/s)", min_value=0, max_value=2000, value=int(b_mouse))
        click_rate = st.number_input("Baseline Click Rate (per min)", min_value=0, max_value=1000, value=int(b_click))
        
        save_btn = st.form_submit_button("SAVE BASELINE")
        if save_btn:
            save_user_baseline(1, typing_speed, mouse_speed, click_rate)
            st.toast("✅ Baseline saved to database!", icon="💾")
            st.session_state["baseline_saved"] = True
            
    if st.session_state.get("baseline_saved"):
        st.success("✅ Baseline saved successfully. Anomalies will now be detected relative to these values.")
        # Clear it next time
        st.session_state["baseline_saved"] = False

    st.markdown("---")
    st.markdown("#### Engine Thresholds")
    st.slider("DNA Deviation Limit", 0, 200, 60, help="Total deviation above this will trigger High Risk")
    st.toggle("Auto-Quarantine on High Risk", value=True)
