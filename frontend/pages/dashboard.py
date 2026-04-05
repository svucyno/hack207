import streamlit as st
import pandas as pd
from database.db import get_all_history
from frontend.components.cards import metric_card

def show_dashboard():
    print("[DEBUG] show_dashboard executed")
    st.markdown("### Overview Statistics")
    
    rows, columns = get_all_history()
    df_history = pd.DataFrame(rows, columns=columns)
    
    total_scans = len(df_history)
    malicious = len(df_history[df_history["result"] == "MALICIOUS"]) if total_scans > 0 else 0
    benign = len(df_history[df_history["result"] == "BENIGN"]) if total_scans > 0 else 0
    avg_score = df_history["score"].mean() * 100 if total_scans > 0 else 1
    
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        metric_card("Total Scans", total_scans, "blue", "#3b82f6")
    with m2:
        metric_card("Malicious", malicious, "red", "#ef4444")
    with m3:
        metric_card("Benign", benign, "green", "#22c55e")
    with m4:
        metric_card("Avg Risk Score", f"{avg_score:.1f}%", "purple", "#8b5cf6")
        
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### Recent Scans")
    if not df_history.empty:
        st.dataframe(df_history.head(5), use_container_width=True, hide_index=True)
    else:
        st.info("No scans performed yet. Go to 'Scan File' to analyze.")
