import streamlit as st
import pandas as pd
from database.db import get_all_blocked_files

def show_quarantine():
    st.markdown("### 🚫 Universal Quarantine Repository")
    st.write("The following files have been globally blacklisted across the system.")
    
    rows, columns = get_all_blocked_files()
    if rows:
        df = pd.DataFrame(rows, columns=columns)
        
        # Rename and Reorder for UI
        df = df.rename(columns={
            "original_name": "File Name",
            "file_hash": "MD5 Hash",
            "timestamp": "Date Blocked"
        })
        df["Status"] = "🚫 Blocked"
        
        # Select specific columns to show
        show_cols = ["File Name", "MD5 Hash", "Date Blocked", "Status"]
        st.dataframe(df[show_cols], use_container_width=True, hide_index=True)
        
        st.info(f"Total Quarantined Items: {len(rows)}")
    else:
        st.info("No threats currently isolated in the quarantine vault.")
