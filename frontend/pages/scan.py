import streamlit as st
import os
import time
import random
from backend.utils import extract_metadata, detect_urls, calculate_md5
from backend.model import get_dummy_features_for_inference
from backend.behavior import simulate_file_behavior, calculate_behavior_risk
from backend.predictor import get_prediction
from backend.quarantine import quarantine_file
from database.db import log_scan, is_file_blocked, add_blocked_file

from backend.explain import generate_shap_explanation

def show_scan(model, feature_names=None):
    st.markdown("### 🔍 Advanced Malware Scan")
    uploaded_file = st.file_uploader("Drop any file to analyze behavior and code", type=None)
    
    if uploaded_file is not None:
        # Step 1: Save temporary file
        file_path = os.path.join("uploads", uploaded_file.name)
        os.makedirs("uploads", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        # Step 2: Hashing
        file_hash = calculate_md5(file_path)
        st.info(f"🧬 File Fingerprint (MD5): `{file_hash}`")
            
        # Step 3: Duplicate Check
        if is_file_blocked(file_hash):
            st.markdown(f"""
            <div class="card glow-red">
                <h3 style="color:#ef4444;text-align:center;">🚫 ACCESS DENIED</h3>
                <p style="text-align:center;">This file was already blocked earlier and is stored in quarantine.</p>
                <p style="text-align:center;font-family:monospace;font-size:12px;">ID: {file_hash}</p>
            </div>
            """, unsafe_allow_html=True)
            if os.path.exists(file_path):
                os.remove(file_path)
            return

        # Step 4: Full Analysis
        with st.spinner("🚀 Analyzing File & User DNA..."):
            time.sleep(1.5) 
            
            # File Analysis
            metadata = extract_metadata(file_path)
            urls = detect_urls(file_path)
            features = get_dummy_features_for_inference(model, metadata)
            
            # DNA Behavior Analysis (Simulated Current for Demo)
            current_typing = st.session_state.get('sim_typing', random.randint(30, 100))
            current_mouse = st.session_state.get('sim_mouse', random.randint(100, 400))
            current_clicks = st.session_state.get('sim_clicks', random.randint(10, 80))
            
            total_dna_dev, behavior_score_normalized, risk_level_dna = calculate_behavior_risk(
                1, current_typing, current_mouse, current_clicks
            )
            
            # Prediction
            is_malicious_file, file_score, _ = get_prediction(model, features, 0, urls_detected=bool(urls))
            
            # Combine Logic: Block if File Malicious OR DNA High Risk
            final_decision_blocked = is_malicious_file or risk_level_dna == "High Risk"
            risk_percent = max(file_score, behavior_score_normalized) * 100
            
            # Get SHAP explanation if malicious file
            shap_reasons = []
            if is_malicious_file and feature_names:
                _, shap_reasons = generate_shap_explanation(model, features, feature_names)
            
            # Log results
            res_label = "BLOCKED" if final_decision_blocked else "SAFE"
            log_scan(uploaded_file.name, res_label, risk_percent/100.0)
            
            st.markdown("---")
            
            if final_decision_blocked:
                # Step 5: Quarantine
                new_path = quarantine_file(file_path, file_hash)
                if new_path:
                    add_blocked_file(file_hash, uploaded_file.name, new_path)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
                reason_text = "Anomalous DNA Behavior detected."
                if is_malicious_file:
                    reason_text = "Static code analysis identified malicious patterns."
                
                shap_html = ""
                if shap_reasons:
                    shap_html = "<div style='margin-top:10px; font-size:0.9em; border-top:1px solid rgba(255,255,255,0.1); padding-top:10px;'><b>Analysis Insights (SHAP):</b><ul style='text-align:left; margin-top:5px;'>"
                    for r in shap_reasons:
                        shap_html += f"<li>{r}</li>"
                    shap_html += "</ul></div>"

                st.markdown(f"""
                <div class="card glow-red">
                    <h2 style="color:#ef4444;text-align:center;">🚫 THREAT BLOCKED</h2>
                    <h4 style="text-align:center;">{uploaded_file.name}</h4>
                    <p style="text-align:center;">Risk Score: <b>{risk_percent:.1f}%</b></p>
                    <p style="text-align:center; color:#fca5a5;"><b>Primary Threat:</b> {reason_text}</p>
                    {shap_html}
                    <div style="background:rgba(239, 68, 68, 0.1); padding:10px; border-radius:8px; text-align:center; border:1px solid #ef4444; margin-top:15px;">
                        🛡️ <b>Isolated to prevent system damage.</b><br>
                        <span style="font-size:12px; font-family:monospace;">/quarantine/{file_hash}.blocked</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="card glow-green">
                    <h2 style="color:#22c55e;text-align:center;">✅ SYSTEM SAFE</h2>
                    <h4 style="text-align:center;">{uploaded_file.name}</h4>
                    <p style="text-align:center;">Risk Score: <b>{risk_percent:.1f}%</b></p>
                    <p style="text-align:center;">Status: Benign (Normal Baseline)</p>
                </div>
                """, unsafe_allow_html=True)

            # Detail Panels
            c1, c2 = st.columns(2)
            with c1:
                st.info("🧬 Behavioral DNA Analysis")
                dna_status_color = "#ef4444" if risk_level_dna == "High Risk" else ("#f59e0b" if risk_level_dna == "Medium Risk" else "#22c55e")
                st.markdown(f"**Session Risk**: <span style='color:{dna_status_color}; font-weight:bold;'>{risk_level_dna}</span>", unsafe_allow_html=True)
                st.write(f"**Total Deviation**: `{total_dna_dev:.1f}` units from baseline")
                st.progress(min(total_dna_dev / 200.0, 1.0))
                if risk_level_dna != "Normal":
                    st.warning(f"⚠️ User activity shows {risk_level_dna} deviation.")
                
            with c2:
                st.info("📄 File Forensic Metadata")
                st.write(f"**Type**: `{metadata['extension']}`")
                st.write(f"**Entropy**: `{metadata['entropy']:.2f}` ({metadata['randomness']})")
                if urls:
                    st.warning(f"Found {len(urls)} embedded URLs")

            st.session_state["latest_features"] = features
            st.session_state["latest_filename"] = uploaded_file.name
    else:
        st.info("Awaiting file upload for security triage.")
