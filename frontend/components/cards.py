import streamlit as st

def metric_card(title, value, glow_color="blue", text_color="#3b82f6"):
    st.markdown(f"""
    <div class="metric-card glow-{glow_color}">
        <div class="metric-label">{title}</div>
        <div class="metric-value" style="color:{text_color}">{value}</div>
    </div>
    """, unsafe_allow_html=True)

def alert_card(title, text, glow_type="red", text_color="#ef4444"):
    st.markdown(f"""
    <div class="card glow-{glow_type}">
        <h3 style="color:{text_color};margin-bottom:5px;">{title}</h3>
        <p style="margin:0;">{text}</p>
    </div>
    """, unsafe_allow_html=True)
