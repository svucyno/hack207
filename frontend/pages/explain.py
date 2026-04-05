import streamlit as st
from backend.explain import generate_shap_explanation

def show_explain(model, feature_names):
    print("[DEBUG] show_explain executed")
    st.markdown("### 🔍 Model Explainability (SHAP)")
    
    if "latest_features" not in st.session_state:
        st.info("Upload and scan a file first to see its explanation.")
        st.write("The SHAP panel will dynamically render bar charts to illustrate how decisions were made once a file is scanned.")
        return
        
    st.write(f"Explanation for the most recently scanned file: **{st.session_state.get('latest_filename')}**")
    
    fig, readable_reasons = generate_shap_explanation(model, st.session_state["latest_features"], feature_names)
    
    if fig:
        st.pyplot(fig)
        
        st.markdown("### This file is classified as malicious because:")
        for idx, reason in enumerate(readable_reasons):
            st.markdown(f"**{idx+1}.** {reason}")
    else:
        st.warning("⚠️ Could not map live SHAP features. Using heuristic approach...")
        st.markdown("### This file is classified as malicious because:")
        st.markdown("* High entropy indicates packed or obfuscated code")
        st.markdown("* Suspicious API calls were detected")
        st.markdown("* File structure is abnormal compared to benign files")
