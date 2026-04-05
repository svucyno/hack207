import streamlit as st
import sqlite3
import random

# ---------------- DATABASE SETUP ----------------
conn = sqlite3.connect("behavior.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS baseline (
    user_id INTEGER PRIMARY KEY,
    typing INTEGER,
    mouse INTEGER,
    click INTEGER
)
""")
conn.commit()


def save_user_baseline(user_id, typing, mouse, click):
    cursor.execute("""
    INSERT OR REPLACE INTO baseline (user_id, typing, mouse, click)
    VALUES (?, ?, ?, ?)
    """, (user_id, typing, mouse, click))
    conn.commit()


def get_user_baseline(user_id):
    cursor.execute("SELECT typing, mouse, click FROM baseline WHERE user_id=?", (user_id,))
    return cursor.fetchone()


# ---------------- ANOMALY DETECTION ----------------
def detect_anomaly(current, baseline, threshold=60):
    c_typing, c_mouse, c_click = current
    b_typing, b_mouse, b_click = baseline

    typing_dev = abs(c_typing - b_typing) / (b_typing + 1) * 100
    mouse_dev = abs(c_mouse - b_mouse) / (b_mouse + 1) * 100
    click_dev = abs(c_click - b_click) / (b_click + 1) * 100

    total_dev = (typing_dev + mouse_dev + click_dev) / 3

    return total_dev > threshold, total_dev


# ---------------- UI ----------------
def show_BehavioralDNA(is_malicious_context=False):

    if is_malicious_context:
        st.markdown("""
        <div style="padding:20px; border-radius:10px; background:#2b0033; color:white;">
            <h3>🛡️ Mitigation & Isolation</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        - ⚠️ **Execution Blocked**
        - 🛑 **Network Access Disabled**
        - 🛡️ **File moved to Quarantine**
        """)
        return

    st.title("⚙️ DNA Security BehavioralDNA")

    st.markdown("Configure your behavioral baseline to detect anomalies.")

    baseline = get_user_baseline(1)
    if baseline:
        b_typing, b_mouse, b_click = baseline
    else:
        b_typing, b_mouse, b_click = 65, 220, 40

    # -------- BASELINE FORM --------
    with st.form("dna_baseline_form"):
        typing_speed = st.number_input("Typing Speed (WPM)", 0, 500, int(b_typing))
        mouse_speed = st.number_input("Mouse Speed (px/s)", 0, 2000, int(b_mouse))
        click_rate = st.number_input("Click Rate (per min)", 0, 1000, int(b_click))

        save_btn = st.form_submit_button("💾 SAVE BASELINE")

        if save_btn:
            save_user_baseline(1, typing_speed, mouse_speed, click_rate)
            st.success("✅ Baseline saved!")

    st.markdown("---")

    # -------- SETTINGS --------
    st.subheader("⚙️ Engine Settings")
    threshold = st.slider("DNA Deviation Limit", 0, 200, 60)
    auto_quarantine = st.toggle("Auto-Quarantine on High Risk", value=True)

    st.markdown("---")

    # -------- SCAN BUTTON --------
    st.subheader("🔍 Real-Time Behavioral Scan")

    if st.button("🚀 Run Scan"):

        baseline = get_user_baseline(1)

        if not baseline:
            st.warning("⚠️ Please save baseline first!")
            return

        # Simulated behavior
        current_behavior = (
            random.randint(30, 120),
            random.randint(100, 500),
            random.randint(10, 100)
        )

        is_anomaly, deviation = detect_anomaly(current_behavior, baseline, threshold)

        st.write("### 📊 Current Behavior")
        st.write(f"Typing: {current_behavior[0]} WPM")
        st.write(f"Mouse: {current_behavior[1]} px/s")
        st.write(f"Clicks: {current_behavior[2]} per min")

        st.write(f"### 📉 Deviation Score: {deviation:.2f}%")

        # -------- RESULT --------
        if is_anomaly:
            st.error("🚨 HIGH RISK: Anomaly Detected!")

            if auto_quarantine:
                st.session_state["malicious_detected"] = True

        else:
            st.success("✅ Behavior Normal")

    # -------- AUTO MITIGATION --------
    if st.session_state.get("malicious_detected"):
        show_BehavioralDNA(is_malicious_context=True)


# ---------------- MAIN ----------------
if "malicious_detected" not in st.session_state:
    st.session_state["malicious_detected"] = False

show_BehavioralDNA()