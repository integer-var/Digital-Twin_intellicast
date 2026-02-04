"""
IntelliCast AI-Native Orchestration Dashboard
Real-time visualization of AI predictions, network state, and orchestration decisions
"""
import streamlit as st
import json
import time
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import os

# Page configuration
st.set_page_config(
    page_title="IntelliCast AI Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- NEW CSS FOR HARDWARE STATUS ---
st.markdown("""
    <style>
    .big-metric { font-size: 2em; font-weight: bold; text-align: center; }
    .status-normal { color: #28a745; font-weight: bold;}
    .status-warning { color: #ffc107; font-weight: bold;}
    .status-emergency { color: #dc3545; font-weight: bold;}
    
    /* Hardware Integration Styles */
    .hardware-active { 
        background-color: #d4edda; 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 5px solid #28a745; 
        color: #155724;
        margin-bottom: 10px;
    }
    .hardware-inactive { 
        background-color: #f8f9fa; 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 5px solid #6c757d; 
        color: #6c757d;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# File paths
STATE_FILE = "network_state.json"
TRIGGER_FILE = "sensor_trigger.json"
DECISION_LOG = "decision_log.json"

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = {
        'timestamps': [], 'load': [], 'latency': [], 'jitter': [], 'ai_confidence': []
    }

def read_json_file(filepath, default=None):
    try:
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return json.load(f)
    except:
        pass
    return default or {}

def update_history(state):
    now = datetime.now()
    st.session_state.history['timestamps'].append(now)
    st.session_state.history['load'].append(state.get('live_load', 0))
    st.session_state.history['latency'].append(state.get('latency', 0))
    st.session_state.history['ai_confidence'].append(state.get('ai_confidence', 0))
    # Keep last 100 points
    if len(st.session_state.history['timestamps']) > 100:
        for key in st.session_state.history:
            st.session_state.history[key] = st.session_state.history[key][-100:]

# --- CHART FUNCTIONS ---
def create_time_series_chart():
    fig = go.Figure()
    hist = st.session_state.history
    if len(hist['timestamps']) > 0:
        fig.add_trace(go.Scatter(x=hist['timestamps'], y=hist['load'], name='Network Load (%)', line=dict(color='#3498db', width=2)))
        fig.add_trace(go.Scatter(x=hist['timestamps'], y=[c * 100 for c in hist['ai_confidence']], name='AI Confidence (%)', line=dict(color='#e74c3c', width=2, dash='dash')))
        fig.add_hline(y=90, line_dash="dot", line_color="red", annotation_text="AI Trigger")
    
    fig.update_layout(height=350, margin=dict(l=0, r=0, t=30, b=0), hovermode='x unified', title="Real-Time Network Telemetry")
    return fig

def create_gauge(value, title, max_value=100, threshold=80):
    color = "green" if value < threshold else "red"
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=value,
        title={'text': title},
        gauge={'axis': {'range': [None, max_value]}, 'bar': {'color': color}, 'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': threshold}}
    ))
    fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20))
    return fig

# --- MAIN LAYOUT ---
st.title("🧠 IntelliCast: Digital-Twin Control Plane")
st.caption("AI-Native Orchestration System with ATSC 3.0 Integration")

# Sidebar
with st.sidebar:
    st.header("⚙️ System Control")
    refresh_rate = st.slider("Refresh Rate (s)", 0.5, 5.0, 1.0)
    st.markdown("---")
    st.header("📊 System Status")
    
    # Read Data
    state = read_json_file(STATE_FILE)
    trigger = read_json_file(TRIGGER_FILE)
    
    if state:
        is_emergency = state.get('offload_active', False)
        status_text = "🔴 EMERGENCY ACTIVE" if is_emergency else "🟢 NORMAL OPERATION"
        st.subheader(status_text)
        
        st.metric("Offload Active", "✅ YES" if is_emergency else "❌ NO")
        st.metric("Current Phase", state.get('phase', 'UNKNOWN'))

# Check Data Source
if not os.path.exists(STATE_FILE):
    st.warning("⚠️ Waiting for Network Simulator...")
    time.sleep(1)
    st.rerun()

# Update History
update_history(state)
is_emergency = state.get('offload_active', False)

# --- TOP METRICS ROW ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Network Load", f"{state.get('live_load',0):.1f}%", "-40% (Offloaded)" if is_emergency else None)
col2.metric("AI Confidence", f"{state.get('ai_confidence',0):.3f}", "CRITICAL" if state.get('ai_confidence',0) > 0.9 else None)
col3.metric("Latency", f"{state.get('latency',0):.1f}ms")
col4.metric("Jitter", f"{state.get('jitter',0):.1f}ms")

# --- 🔌 REAL-WORLD INTEGRATION SECTION (THE NEW PART) ---
st.markdown("---")
st.subheader("🔌 Real-World Network Integration Status")

# Three columns for the three hardware components
int_col1, int_col2, int_col3 = st.columns(3)

with int_col1:
    st.markdown("**1. Geolocation (GIS)**")
    if is_emergency:
        st.markdown("""
        <div class='hardware-active'>
        <b>📍 ZONING ACTIVE</b><br>
        • High Risk: Zone_001, Zone_002<br>
        • Action: Targeted Broadcast
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='hardware-inactive'>📍 GIS Scanner: Standby<br>No active zones detected</div>", unsafe_allow_html=True)

with int_col2:
    st.markdown("**2. Network Slicing**")
    if is_emergency:
        st.markdown("""
        <div class='hardware-active'>
        <b>🍰 SLICE CREATED</b><br>
        • ID: SST-1 (Critical)<br>
        • Bandwidth: 100Mbps Reserved<br>
        • User: First Responders
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='hardware-inactive'>🍰 Slice Status: Shared<br>Standard QoS Profile</div>", unsafe_allow_html=True)

with int_col3:
    st.markdown("**3. ATSC 3.0 Switching**")
    if is_emergency:
        st.markdown("""
        <div class='hardware-active'>
        <b>📡 BROADCAST: ON</b><br>
        • Route: UPF -> N6 -> ATSC_GW<br>
        • Protocol: ROUTE/MMTP<br>
        • 5G Unicast: Relieved
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<div class='hardware-inactive'>📡 Broadcast: Standby<br>Route: 5G Unicast</div>", unsafe_allow_html=True)

# --- CHARTS ROW ---
st.markdown("---")
st.plotly_chart(create_time_series_chart(), use_container_width=True)

# --- GAUGES ROW ---
g_col1, g_col2, g_col3 = st.columns(3)
with g_col1:
    st.plotly_chart(create_gauge(state.get('live_load', 0), "Load (%)", 100, 80), use_container_width=True)
with g_col2:
    st.plotly_chart(create_gauge(state.get('ai_confidence', 0) * 100, "AI Confidence (%)", 100, 90), use_container_width=True)
with g_col3:
    st.plotly_chart(create_gauge(state.get('latency', 0), "Latency (ms)", 100, 50), use_container_width=True)

# --- LOGS ROW ---
st.subheader("📝 Live Orchestrator Logs")
decisions = read_json_file(DECISION_LOG)
if decisions:
    df = pd.DataFrame(decisions[-5:][::-1])
    if not df.empty and 'action' in df.columns:
        st.dataframe(
            df[['timestamp_human', 'action', 'trigger_source', 'ai_confidence']], 
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No decisions logged yet.")
else:
    st.info("System monitoring... No actions taken yet.")

# Auto-refresh
time.sleep(refresh_rate)
st.rerun()
