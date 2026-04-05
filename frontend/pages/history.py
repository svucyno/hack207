import streamlit as st
import pandas as pd
from database.db import get_history

def show_history():
    print("[DEBUG] show_history executed")
    st.markdown("### 📜 Scan History")
    
    rows, columns = get_history()
    df_history = pd.DataFrame(rows, columns=columns)
    
    if not df_history.empty:
        def highlight_result(val):
            if val == "MALICIOUS":
                return 'background-color: rgba(239, 68, 68, 0.2); color: #ef4444'
            elif val == "BENIGN":
                return 'background-color: rgba(34, 197, 94, 0.2); color: #22c55e'
            return ''
        
        st.dataframe(df_history.style.map(highlight_result, subset=['result']), use_container_width=True, hide_index=True)
    else:
        st.info("No scan history found. Data will appear here after a scan.")
