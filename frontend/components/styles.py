import streamlit as st

def load_css():
    st.markdown("""
<style>
/* Full cyber styling */
body {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #020617;
}

.card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 0 20px rgba(0,0,0,0.5);
    margin-bottom: 20px;
}

.glow-blue { box-shadow: 0 0 10px #3b82f6, inset 0 0 5px #3b82f6; border: 1px solid #3b82f6;}
.glow-red { box-shadow: 0 0 15px #ef4444, inset 0 0 10px #ef4444; border: 1px solid #ef4444;}
.glow-green { box-shadow: 0 0 15px #22c55e, inset 0 0 10px #22c55e; border: 1px solid #22c55e;}
.glow-purple { box-shadow: 0 0 10px #8b5cf6, inset 0 0 5px #8b5cf6; border: 1px solid #8b5cf6;}

h1, h2, h3, h4, h5, h6, p, div {
    color: #e2e8f0;
}

.metric-card {
    background: rgba(15, 23, 42, 0.6);
    border-radius: 12px;
    padding: 15px;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.1);
}

.metric-value {
    font-size: 2rem;
    font-weight: bold;
}
.metric-label {
    font-size: 1rem;
    color: #94a3b8;
}

div[data-testid="stMetricValue"] {
    font-size: 2rem;
}

hr {
    border-color: rgba(255,255,255,0.1);
}
</style>
""", unsafe_allow_html=True)
