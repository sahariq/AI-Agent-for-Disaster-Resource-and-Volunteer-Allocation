import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
import numpy as np
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Emergency Response Hub",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'active_screen' not in st.session_state:
    st.session_state.active_screen = "Overview"

# Color schemes
light_colors = {
    'bg': '#f8fafc', 'card_bg': '#ffffff', 'text': '#0f172a', 'text_light': '#64748b',
    'accent': '#6366f1', 'success': '#10b981', 'warning': '#f59e0b', 'danger': '#ef4444',
    'border': '#e2e8f0', 'glass_bg': 'rgba(255, 255, 255, 0.8)', 'glass_border': 'rgba(255, 255, 255, 0.3)'
}

dark_colors = {
    'bg': '#0a0e1a', 'card_bg': '#1e2235', 'text': '#f1f5f9', 'text_light': '#94a3b8',
    'accent': '#818cf8', 'success': '#34d399', 'warning': '#fbbf24', 'danger': '#f87171',
    'border': '#2d3548', 'glass_bg': 'rgba(30, 34, 53, 0.7)', 'glass_border': 'rgba(255, 255, 255, 0.1)'
}

colors = dark_colors if st.session_state.dark_mode else light_colors

# Ultra Modern CSS with Animations
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@600;700;800&display=swap');
    
    * {{ 
        font-family: 'Inter', -apple-system, sans-serif;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    /* Animated Background with Particles */
    .stApp {{
        background: {colors['bg']} !important;
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.2) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(67, 233, 123, 0.15) 0px, transparent 50%),
            radial-gradient(at 50% 50%, rgba(118, 75, 162, 0.1) 0px, transparent 50%) !important;
        color: {colors['text']} !important;
        position: relative;
        overflow-x: hidden;
        min-height: 100vh;
    }}
    
    /* Simplified animated background */
    .stApp::before {{
        content: '';
        position: fixed;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: 
            radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(118, 75, 162, 0.1) 0%, transparent 50%);
        animation: gradientShift 20s ease infinite;
        z-index: 0;
        pointer-events: none;
    }}
    
    @keyframes gradientShift {{
        0%, 100% {{ transform: translate(0, 0) scale(1); }}
        50% {{ transform: translate(30px, 30px) scale(1.1); }}
    }}
    
    #MainMenu, footer, header, .stDeployButton {{ visibility: hidden; }}
    [data-testid="stSidebar"] {{ display: none; }}
    
    /* Ensure main content is visible */
    .main .block-container {{
        position: relative;
        z-index: 1;
        padding-top: 2rem;
    }}
    
    /* Ensure all Streamlit elements are visible */
    .stApp > div {{
        position: relative;
        z-index: 1;
    }}
    
    /* Navigation Buttons - Ultra Cool */
    .stButton > button {{
        background: {colors['card_bg']} !important;
        color: {colors['text']} !important;
        border: 2px solid {colors['border']} !important;
        border-radius: 16px !important;
        padding: 0.7rem 1.2rem !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        white-space: nowrap !important;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15), 0 0 0 0 rgba(102, 126, 234, 0) !important;
        position: relative;
        overflow: hidden;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(102, 126, 234, 0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }}
    
    .stButton > button:hover::before {{
        width: 300px;
        height: 300px;
    }}
    
    .stButton > button:hover {{
        border-color: {colors['accent']} !important;
        color: {colors['accent']} !important;
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4), 0 0 0 4px rgba(102, 126, 234, 0.1) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(-2px) scale(0.98) !important;
    }}
    
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5), 0 0 0 0 rgba(102, 126, 234, 0.3) !important;
        transform: translateY(-2px) !important;
        animation: pulseGlow 2s ease-in-out infinite;
    }}
    
    .stButton > button[kind="primary"]:hover {{
        box-shadow: 0 10px 32px rgba(102, 126, 234, 0.6), 0 0 0 4px rgba(102, 126, 234, 0.2) !important;
        transform: translateY(-4px) scale(1.05) !important;
    }}
    
    @keyframes pulseGlow {{
        0%, 100% {{ box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5), 0 0 0 0 rgba(102, 126, 234, 0.3); }}
        50% {{ box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5), 0 0 0 8px rgba(102, 126, 234, 0); }}
    }}
    
    /* Metric Cards - Ultra Cool with Glow */
    div[data-testid="metric-container"] {{
        background: {colors['card_bg']};
        padding: 2rem 1.75rem;
        border-radius: 24px;
        box-shadow: 0 0 0 1px {colors['border']}, 0 10px 30px -10px rgba(0, 0, 0, 0.2);
        border: 1px solid {colors['border']};
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }}
    
    div[data-testid="metric-container"]::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        opacity: 0;
        transition: all 0.5s ease;
        animation: shimmer 3s infinite;
    }}
    
    @keyframes shimmer {{
        0% {{ background-position: -200% 0; }}
        100% {{ background-position: 200% 0; }}
    }}
    
    div[data-testid="metric-container"]::after {{
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102, 126, 234, 0.1) 0%, transparent 70%);
        opacity: 0;
        transition: opacity 0.5s ease;
    }}
    
    div[data-testid="metric-container"]:hover::before {{
        opacity: 1;
        height: 6px;
    }}
    
    div[data-testid="metric-container"]:hover::after {{
        opacity: 1;
    }}
    
    div[data-testid="metric-container"]:hover {{
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 0 0 1px {colors['accent']}, 0 25px 50px -10px rgba(99, 102, 241, 0.4), 0 0 30px rgba(102, 126, 234, 0.3);
        border-color: {colors['accent']};
    }}
    
    [data-testid="stMetricValue"] {{
        font-size: 2.75rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, {colors['text']} 0%, {colors['accent']} 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-size: 200% 200%;
        animation: gradientMove 3s ease infinite;
        position: relative;
        z-index: 1;
    }}
    
    @keyframes gradientMove {{
        0%, 100% {{ background-position: 0% 50%; }}
        50% {{ background-position: 100% 50%; }}
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {colors['text_light']} !important;
        font-weight: 700 !important;
        font-size: 0.875rem !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }}
    
    /* Headers */
    h1, h2, h3 {{ color: {colors['text']} !important; font-weight: 800; }}
    
    h2 {{
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        margin-bottom: 2rem;
        position: relative;
        padding-left: 1rem;
    }}
    
    h2::before {{
        content: '';
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateY(-50%);
        width: 5px;
        height: 70%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }}
    
    /* DataFrames */
    [data-testid="stDataFrame"] {{
        background: {colors['card_bg']};
        border-radius: 20px;
        border: 1px solid {colors['border']};
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
    }}
    
    /* Download Buttons */
    .stDownloadButton button {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 14px;
        padding: 1rem 1.75rem;
        font-weight: 700;
        width: 100%;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.35);
        margin-bottom: 1rem;
    }}
    
    .stDownloadButton button:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.5);
    }}
    
    /* File Uploader */
    [data-testid="stFileUploader"] {{
        background: {colors['card_bg']};
        border-radius: 18px;
        border: 2px dashed {colors['border']};
        padding: 2rem;
    }}
    
    [data-testid="stFileUploader"]:hover {{
        border-color: {colors['accent']};
        border-style: solid;
    }}
    
    /* Expanders - Cool Animation */
    .streamlit-expanderHeader {{
        background: {colors['card_bg']};
        border-radius: 16px;
        border: 2px solid {colors['border']};
        color: {colors['text']} !important;
        font-weight: 700;
        padding: 1.125rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }}
    
    .streamlit-expanderHeader::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.2), transparent);
        transition: left 0.5s;
    }}
    
    .streamlit-expanderHeader:hover::before {{
        left: 100%;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        border-color: {colors['accent']};
        transform: translateX(8px) scale(1.02);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
    }}
    
    /* Alert Boxes */
    .stSuccess {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
        border-left: 5px solid #10b981;
        border-radius: 16px;
        padding: 1.5rem;
    }}
    
    .stInfo {{
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(79, 70, 229, 0.05) 100%);
        border-left: 5px solid #6366f1;
        border-radius: 16px;
        padding: 1.5rem;
    }}
    
    /* Scrollbar - Animated */
    ::-webkit-scrollbar {{ width: 12px; }}
    ::-webkit-scrollbar-track {{ 
        background: {colors['bg']};
        border-radius: 10px;
    }}
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
        box-shadow: 0 0 10px rgba(102, 126, 234, 0.5);
    }}
    
    /* Sliders - Completely Transparent, Default Styling */
    .stSlider {{
        background: transparent !important;
    }}
    
    .stSlider > div {{
        background: transparent !important;
    }}
    
    .stSlider > div > div {{
        background: transparent !important;
    }}
    
    /* Expander Content Background - Better Contrast */
    .streamlit-expanderContent {{
        background: {colors['card_bg']} !important;
        border: 2px solid {colors['border']} !important;
        border-radius: 0 0 16px 16px !important;
        padding: 1.5rem !important;
        box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.2) !important;
    }}
    
    /* Zone Control Expander Headers - Enhanced Visibility */
    .streamlit-expanderHeader {{
        background: linear-gradient(135deg, {colors['card_bg']} 0%, rgba(102, 126, 234, 0.1) 100%) !important;
        border: 2px solid {colors['border']} !important;
        border-bottom: 3px solid {colors['accent']} !important;
        color: {colors['text']} !important;
        font-weight: 700 !important;
        padding: 1.25rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15), 0 0 0 1px rgba(102, 126, 234, 0.2) !important;
    }}
    
    .streamlit-expanderHeader:hover {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%) !important;
        border-color: {colors['accent']} !important;
        border-bottom-color: #60a5fa !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.4), 0 0 0 2px rgba(96, 165, 250, 0.3) !important;
    }}
    
    /* Success/Info Boxes with Animation */
    .stSuccess {{
        animation: slideInRight 0.5s ease;
    }}
    
    @keyframes slideInRight {{
        from {{
            opacity: 0;
            transform: translateX(-20px);
        }}
        to {{
            opacity: 1;
            transform: translateX(0);
        }}
    }}
    
    /* Pulse Animation for Critical Zones */
    @keyframes pulse {{
        0%, 100% {{
            opacity: 1;
            transform: scale(1);
        }}
        50% {{
            opacity: 0.8;
            transform: scale(1.05);
        }}
    }}
    
    .critical-zone {{
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.5);
    }}
    
    /* Glow Effect */
    @keyframes glow {{
        0%, 100% {{
            box-shadow: 0 0 5px rgba(102, 126, 234, 0.5);
        }}
        50% {{
            box-shadow: 0 0 20px rgba(102, 126, 234, 0.8), 0 0 30px rgba(118, 75, 162, 0.6);
        }}
    }}
    
    /* Smooth Page Transitions */
    .main {{
        animation: fadeIn 0.5s ease-in;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    /* Chart Container Enhancements */
    .js-plotly-plot {{
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        transition: all 0.3s ease;
    }}
    
    .js-plotly-plot:hover {{
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.3);
        transform: translateY(-5px);
    }}
    
    /* Ripple effect styles */
    .ripple {{
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.6);
        transform: scale(0);
        animation: ripple-animation 0.6s ease-out;
        pointer-events: none;
    }}
    @keyframes ripple-animation {{
        to {{
            transform: scale(4);
            opacity: 0;
        }}
    }}
    </style>
""", unsafe_allow_html=True)

# Helper function to convert numeric columns
def convert_numeric_columns(df):
    """Convert numeric columns to proper numeric types, handling string numbers."""
    numeric_columns = ['severity', 'required_volunteers', 'capacity', 'estimated_victims', 
                      'resources_available', 'min_resources_per_volunteer', 'latitude', 
                      'longitude', 'duration_hours', 'affected_population', 'casualty_estimate', 
                      'available_volunteers', 'volunteers_available', 'allocated_volunteers', 
                      'allocated_resources', 'response_time', 'efficiency']
    
    for col in numeric_columns:
        if col in df.columns:
            # Convert to numeric, coercing errors to NaN, then fill NaN with 0
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    return df

# Initialize data
if 'data' not in st.session_state:
    st.session_state.data = pd.DataFrame({
        'zone': ['Zone A', 'Zone B', 'Zone C', 'Zone D', 'Zone E'],
        'severity': [8.5, 6.2, 9.1, 5.5, 7.8],
        'volunteers_available': [50, 30, 60, 25, 45],
        'resources_available': [100, 60, 120, 50, 90],
        'allocated_volunteers': [45, 25, 55, 20, 40],
        'allocated_resources': [90, 50, 110, 40, 80],
        'latitude': [33.6844, 33.7490, 33.5731, 33.8369, 33.6995],
        'longitude': [73.0479, 73.1353, 73.0570, 73.0764, 73.1234],
        'response_time': [12, 8, 15, 6, 10],
        'efficiency': [90, 83, 92, 80, 89]
    })

# Always get fresh data from session state (updates automatically after file upload)
try:
    data = st.session_state.data.copy()  # Use copy() to avoid potential reference issues
except Exception as e:
    st.error(f"Error loading data: {e}")
    data = pd.DataFrame({
        'zone': ['Zone A', 'Zone B', 'Zone C', 'Zone D', 'Zone E'],
        'severity': [8.5, 6.2, 9.1, 5.5, 7.8],
        'volunteers_available': [50, 30, 60, 25, 45],
        'resources_available': [100, 60, 120, 50, 90],
        'allocated_volunteers': [45, 25, 55, 20, 40],
        'allocated_resources': [90, 50, 110, 40, 80],
        'latitude': [33.6844, 33.7490, 33.5731, 33.8369, 33.6995],
        'longitude': [73.0479, 73.1353, 73.0570, 73.0764, 73.1234],
        'response_time': [12, 8, 15, 6, 10],
        'efficiency': [90, 83, 92, 80, 89]
    })
    st.session_state.data = data

# Top Navigation
try:
    nav_col1, nav_col2, nav_col3 = st.columns([1.5, 7, 1.5])
except Exception as e:
    st.error(f"Navigation error: {e}")
    st.stop()

with nav_col1:
    st.markdown(f"""
        <div style="font-family: Poppins; font-size: 1.75rem; font-weight: 900; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
                    background-size: 200% 200%;
                    -webkit-background-clip: text; 
                    -webkit-text-fill-color: transparent;
                    animation: gradientMove 3s ease infinite;
                    text-shadow: 0 0 30px rgba(102, 126, 234, 0.5);
                    position: relative;
                    display: inline-block;">
            <span style="font-size: 1.2em; animation: pulse 2s ease-in-out infinite;">🚨</span> Response Hub
        </div>
        <style>
            @keyframes gradientMove {{
                0%, 100% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
            }}
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.1); }}
            }}
        </style>
    """, unsafe_allow_html=True)

with nav_col2:
    # Shorter button labels to prevent wrapping
    screens = ["Control", "Overview", "Analytics", "Map", "Reports", "Live"]
    screen_map = {
        "Control": "Command Center",
        "Overview": "Overview",
        "Analytics": "Analytics",
        "Map": "Map View",
        "Reports": "Reports",
        "Live": "Real-time"
    }
    
    nav_cols = st.columns(len(screens))
    for idx, short_label in enumerate(screens):
        with nav_cols[idx]:
            full_screen = screen_map[short_label]
            if st.button(
                short_label,
                key=f"nav_{full_screen}",
                use_container_width=True,
                type="primary" if st.session_state.active_screen == full_screen else "secondary"
            ):
                st.session_state.active_screen = full_screen
                st.rerun()

with nav_col3:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
            <div style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.5rem 1rem;
                        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                        color: white; border-radius: 100px; font-weight: 700; font-size: 0.75rem;
                        box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4);
                        animation: pulseGlow 2s ease-in-out infinite;">
                <div style="width: 10px; height: 10px; background: white; border-radius: 50%;
                            box-shadow: 0 0 10px rgba(255, 255, 255, 0.8);
                            animation: pulse 1.5s ease-in-out infinite;"></div>
                ONLINE
            </div>
            <style>
                @keyframes pulseGlow {{
                    0%, 100% {{ box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4); }}
                    50% {{ box-shadow: 0 4px 25px rgba(16, 185, 129, 0.7); }}
                }}
            </style>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🌙" if st.session_state.dark_mode else "☀️", key="theme"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# COMMAND CENTER SCREEN
if st.session_state.active_screen == "Command Center":
    # Refresh data for this screen
    data = st.session_state.data.copy()
    st.markdown(f"""
        <h1 style="font-family: Poppins; font-size: 2.5rem; margin-bottom: 0.5rem;">⚙️ Command Center</h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            System configuration, data management, and zone controls
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 Quick Stats")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Personnel", int(data['allocated_volunteers'].sum()))
            st.metric("Avg Severity", f"{data['severity'].mean():.1f}")
        with col_b:
            st.metric("Resources", int(data['allocated_resources'].sum()))
            st.metric("Efficiency", f"{data['efficiency'].mean():.0f}%")
    
    with col2:
        pass  # Empty column - Data Management removed
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("⚙️ Zone Controls")
    
    if not data.empty:
        # Determine which column to use for zones
        zone_col = None
        if 'zone' in data.columns:
            # Check if zone column has valid string values (not numeric)
            zone_sample = data['zone'].head(5).astype(str)
            if zone_sample.str.match(r'^[A-Za-z].*', na=False).any():
                zone_col = 'zone'
        
        # Fallback to zone_name or zone_id
        if zone_col is None:
            if 'zone_name' in data.columns:
                zone_col = 'zone_name'
            elif 'zone_id' in data.columns:
                zone_col = 'zone_id'
        
        if zone_col:
            # Get unique zones, limit to 9 for display
            unique_zones = data[zone_col].dropna().unique()[:9]
            
            # Track if any values changed
            data_changed = False
            
            cols = st.columns(3)
            for idx, zone in enumerate(unique_zones):
                with cols[idx % 3]:
                    # Get rows for this zone
                    zone_rows = data[data[zone_col] == zone]
                    
                    if len(zone_rows) > 0:
                        row = zone_rows.iloc[0]
                        zone_display = str(row[zone_col])
                        
                        st.markdown(f"""
                            <div class="zone-card">
                                <h3 style="color: {colors['accent']}; margin-bottom: 0.5rem;">
                                    <span style="font-size: 1.2em;">🎯</span> {zone_display}
                                </h3>
                                <p style="font-size: 0.9em; color: {colors['text_light']}; margin-bottom: 1rem;">
                                    ID: {row.get('zone_id', 'N/A')} | Lat: {row['latitude']:.4f}, Lon: {row['longitude']:.4f}
                                </p>
                                <label class="slider-label">🔥 Severity: <span id="severity-value-{zone}">{row['severity']:.1f}</span></label>
                        """, unsafe_allow_html=True)
                        
                        # Severity Slider
                        new_severity = st.slider(
                            "Severity",
                            min_value=0.0,
                            max_value=10.0,
                            value=float(row['severity']),
                            step=0.1,
                            key=f"severity_{zone}",
                            label_visibility="collapsed"
                        )
                        
                        st.markdown(f"""
                                <label class="slider-label">👥 Personnel: <span id="personnel-value-{zone}">{int(row['volunteers_available'])}</span></label>
                        """, unsafe_allow_html=True)
                        
                        # Personnel Slider
                        new_personnel = st.slider(
                            "Personnel",
                            min_value=0,
                            max_value=750,
                            value=int(row['volunteers_available']),
                            step=10,
                            key=f"personnel_{zone}",
                            label_visibility="collapsed"
                        )
                        
                        # Update data if sliders changed
                        if new_severity != row['severity']:
                            data.loc[data[zone_col] == zone, 'severity'] = new_severity
                            data_changed = True
                        if new_personnel != row['volunteers_available']:
                            data.loc[data[zone_col] == zone, 'volunteers_available'] = new_personnel
                            # Also update allocated_volunteers and required_volunteers based on new personnel
                            data.loc[data[zone_col] == zone, 'allocated_volunteers'] = int(new_personnel * 0.9) # Example: 90% allocated
                            data.loc[data[zone_col] == zone, 'required_volunteers'] = new_personnel # Assuming available = required for simplicity
                            data_changed = True
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                        # JavaScript to update slider values dynamically
                        st.markdown(f"""
                            <script>
                                var severitySlider = document.querySelector('input[type="range"][key="severity_{zone}"]');
                                var severityValueSpan = document.getElementById('severity-value-{zone}');
                                if (severitySlider && severityValueSpan) {{
                                    severityValueSpan.textContent = parseFloat(severitySlider.value).toFixed(1);
                                    severitySlider.oninput = function() {{
                                        severityValueSpan.textContent = parseFloat(this.value).toFixed(1);
                                    }}
                                }}
                                
                                var personnelSlider = document.querySelector('input[type="range"][key="personnel_{zone}"]');
                                var personnelValueSpan = document.getElementById('personnel-value-{zone}');
                                if (personnelSlider && personnelValueSpan) {{
                                    personnelValueSpan.textContent = parseInt(personnelSlider.value);
                                    personnelSlider.oninput = function() {{
                                        personnelValueSpan.textContent = parseInt(this.value);
                                    }}
                                }}
                            </script>
                        """, unsafe_allow_html=True)
                        
                    else:
                        st.error(f"Could not load data for zone: {zone}")
            
            # If any data changed, update timestamp and trigger rerun to refresh all screens
            if data_changed:
                st.session_state.data = data
                st.session_state.last_update = datetime.now()
                # Note: Streamlit sliders already trigger reruns, but we need to ensure
                # all screens refresh with the updated data, so we explicitly rerun here
                st.rerun()
        else:
            st.info("No zone column found in data")
        
# OVERVIEW SCREEN
elif st.session_state.active_screen == "Overview":
    # Refresh data for this screen
    data = st.session_state.data.copy()
    st.markdown(f"""
        <h1 style="font-family: Poppins; font-size: 2.5rem; margin-bottom: 0.5rem;">📊 System Overview</h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            Real-time monitoring of all disaster zones
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Active Zones", len(data), delta="+2")
    with col2:
        st.metric("Avg Severity", f"{data['severity'].mean():.1f}")
    with col3:
        st.metric("Personnel", int(data['allocated_volunteers'].sum()))
    with col4:
        st.metric("Resources", int(data['allocated_resources'].sum()))
    with col5:
        st.metric("Efficiency", f"{data['efficiency'].mean():.0f}%", delta="+3.2%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📍 Zone Status")
        summary_df = data[['zone', 'severity', 'volunteers_available', 'allocated_volunteers', 
                           'resources_available', 'allocated_resources']].copy()
        summary_df['deploy_%'] = (summary_df['allocated_volunteers'] / summary_df['volunteers_available'] * 100).round(1)
        summary_df.columns = ['Zone', 'Severity', 'Available', 'Deployed', 'Resources', 'Active', 'Deploy %']
        st.dataframe(summary_df, use_container_width=True, hide_index=True, height=400)
    
    with col2:
        st.subheader("🎯 Priority Zones")
        for idx, row in data.nlargest(3, 'severity')[['zone', 'severity']].iterrows():
            color = '#ef4444' if row['severity'] > 8 else '#f59e0b' if row['severity'] > 6 else '#10b981'
            st.markdown(f"""
                <div style="background: linear-gradient(135deg, {color}22 0%, {color}11 100%);
                            padding: 1rem; border-radius: 12px; border-left: 4px solid {color}; margin-bottom: 0.75rem;">
                    <div style="font-weight: 700; font-size: 1.1rem; color: {colors['text']};">{row['zone']}</div>
                    <div style="color: {color}; font-weight: 800; font-size: 1.5rem; margin-top: 0.25rem;">
                        Severity: {row['severity']:.1f}
                    </div>
                </div>
            """, unsafe_allow_html=True)

# ANALYTICS SCREEN
elif st.session_state.active_screen == "Analytics":
    # Refresh data for this screen
    data = st.session_state.data.copy()
    st.markdown(f"""
        <h1 style="font-family: Poppins; font-size: 2.5rem; margin-bottom: 0.5rem;">📈 Advanced Analytics</h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            Detailed analysis of resource allocation
        </p>
    """, unsafe_allow_html=True)
    
    st.subheader("👥 Personnel Deployment")
    fig_bar = px.bar(data, x='zone', y='allocated_volunteers', color='severity',
                     color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'],
                     labels={'allocated_volunteers': 'Deployed', 'zone': 'Zone'},
                     template='plotly_dark' if st.session_state.dark_mode else 'plotly')
    fig_bar.update_traces(
        marker=dict(
            line=dict(width=2, color='rgba(255,255,255,0.1)'),
            opacity=0.9
        ),
        hovertemplate='<b>%{x}</b><br>Deployed: %{y}<br>Severity: %{marker.color}<extra></extra>'
    )
    fig_bar.update_layout(
        height=450, 
        plot_bgcolor='rgba(0,0,0,0)', 
        paper_bgcolor=colors['card_bg'],
        font=dict(color=colors['text'], size=12, family='Inter'),
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            tickfont=dict(color=colors['text']), 
            gridcolor=colors['border'],
            showgrid=True,
            gridwidth=1
        ),
        yaxis=dict(
            tickfont=dict(color=colors['text']), 
            gridcolor=colors['border'],
            showgrid=True,
            gridwidth=1
        ),
        hovermode='closest',
        transition={'duration': 500}
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': True, 'displaylogo': False})
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔥 Severity vs Response")
        
        # Ensure required columns exist and have valid data
        if 'severity' in data.columns and 'allocated_volunteers' in data.columns:
            # Filter out invalid data
            plot_data = data[['severity', 'allocated_volunteers']].copy()
            if 'zone' in data.columns:
                plot_data['zone'] = data['zone']
            if 'allocated_resources' in data.columns:
                plot_data['allocated_resources'] = data['allocated_resources']
            
            # Remove rows with invalid values (NaN, negative, or zero severity)
            plot_data = plot_data.dropna(subset=['severity', 'allocated_volunteers'])
            plot_data = plot_data[(plot_data['severity'] > 0) & (plot_data['allocated_volunteers'] >= 0)]
            
            if len(plot_data) > 0:
                # Ensure zone column exists for color coding
                if 'zone' not in plot_data.columns:
                    plot_data['zone'] = [f"Zone {i+1}" for i in range(len(plot_data))]
                
                # Use allocated_resources for size if available, otherwise use allocated_volunteers
                size_col = 'allocated_resources' if 'allocated_resources' in plot_data.columns and plot_data['allocated_resources'].notna().any() else 'allocated_volunteers'
                
                try:
                    fig_scatter = px.scatter(
                        plot_data, 
                        x='severity', 
                        y='allocated_volunteers', 
                        size=size_col,
                        color='zone',
                        hover_data=['zone', 'severity', 'allocated_volunteers'],
                        labels={'severity': 'Severity', 'allocated_volunteers': 'Allocated Volunteers', 'zone': 'Zone'},
                        template='plotly_dark' if st.session_state.dark_mode else 'plotly'
                    )
                    fig_scatter.update_traces(
                        marker=dict(
                            line=dict(width=2, color='rgba(255,255,255,0.3)'),
                            opacity=0.8,
                            sizemin=8
                        ),
                        hovertemplate='<b>%{hovertext}</b><br>Severity: %{x}<br>Volunteers: %{y}<extra></extra>',
                        hovertext=plot_data['zone'] if 'zone' in plot_data.columns else None
                    )
                    fig_scatter.update_layout(
                        height=400, 
                        plot_bgcolor='rgba(0,0,0,0)', 
                        paper_bgcolor=colors['card_bg'],
                        font=dict(color=colors['text'], size=12, family='Inter'),
                        margin=dict(l=20, r=20, t=40, b=20),
                        xaxis=dict(
                            tickfont=dict(color=colors['text']), 
                            gridcolor=colors['border'],
                            showgrid=True,
                            gridwidth=1
                        ), 
                        yaxis=dict(
                            tickfont=dict(color=colors['text']), 
                            gridcolor=colors['border'],
                            showgrid=True,
                            gridwidth=1
                        ),
                        legend=dict(
                            font=dict(color=colors['text'], size=10),
                            bgcolor='rgba(0,0,0,0)',
                            bordercolor=colors['border'],
                            borderwidth=1
                        ),
                        hovermode='closest',
                        transition={'duration': 500}
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True, config={'displayModeBar': True, 'displaylogo': False})
                except Exception as e:
                    st.error(f"Error creating chart: {e}")
                    st.write(f"Data shape: {plot_data.shape}")
                    st.write(f"Columns: {list(plot_data.columns)}")
                    st.dataframe(plot_data.head())
            else:
                st.warning("No valid data available for Severity vs Response chart")
                st.write(f"Data shape: {data.shape}")
                st.write(f"Columns: {list(data.columns)}")
                if 'severity' in data.columns:
                    st.write(f"Severity range: {data['severity'].min()} - {data['severity'].max()}")
                if 'allocated_volunteers' in data.columns:
                    st.write(f"Allocated volunteers range: {data['allocated_volunteers'].min()} - {data['allocated_volunteers'].max()}")
        else:
            st.warning("Required columns (severity, allocated_volunteers) not found in data")
            st.write(f"Available columns: {list(data.columns)}")
    
    with col2:
        st.subheader("⚡ System Efficiency")
        avg_eff = data['efficiency'].mean()
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta", 
            value=avg_eff,
            title={'text': "Average Efficiency", 'font': {'color': colors['text'], 'size': 18, 'family': 'Poppins'}},
            delta={'reference': 80, 'font': {'color': colors['text']}}, 
            number={'font': {'color': colors['text'], 'size': 36, 'family': 'Inter'}},
            gauge={
                'axis': {'range': [None, 100], 'tickfont': {'color': colors['text'], 'size': 12}},
                'bar': {'color': "#667eea"},  # Solid color - Plotly doesn't support gradients
                'bordercolor': colors['border'],
                'borderwidth': 2,
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.4)'},
                    {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.4)'},
                    {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.4)'}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor=colors['card_bg'], 
            font={'color': colors['text'], 'family': 'Inter'},
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': True, 'displaylogo': False})

# MAP VIEW SCREEN
elif st.session_state.active_screen == "Map View":
    # Refresh data for this screen
    data = st.session_state.data.copy()
    st.markdown(f"""
        <h1 style="font-family: Poppins; font-size: 2.5rem; margin-bottom: 0.5rem;">🗺️ Geographic View</h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            Interactive map of disaster zones
        </p>
    """, unsafe_allow_html=True)
    
    if 'latitude' in data.columns and 'longitude' in data.columns:
        m = folium.Map(
            location=[data['latitude'].mean(), data['longitude'].mean()],
            zoom_start=12,
            tiles='CartoDB dark_matter' if st.session_state.dark_mode else 'CartoDB positron'
        )
        
        for _, row in data.iterrows():
            sev = row['severity']
            color = '#ef4444' if sev >= 8 else '#f59e0b' if sev >= 6 else '#10b981'
            radius = min(30, max(10, sev * 3))
            
            # Enhanced popup with more info
            popup_html = f"""
            <div style="font-family: Inter, sans-serif; padding: 10px; min-width: 200px;">
                <h3 style="margin: 0 0 10px 0; color: {color}; font-weight: 700;">{row['zone']}</h3>
                <p style="margin: 5px 0;"><strong>Severity:</strong> {sev:.1f}/10</p>
                <p style="margin: 5px 0;"><strong>Personnel:</strong> {int(row.get('allocated_volunteers', 0))}</p>
                <p style="margin: 5px 0;"><strong>Resources:</strong> {int(row.get('allocated_resources', 0))}</p>
            </div>
            """
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=radius,
                popup=folium.Popup(popup_html, max_width=300),
                color=color, 
                fill=True, 
                fillColor=color, 
                fillOpacity=0.7, 
                weight=4,
                tooltip=f"{row['zone']} - Severity: {sev:.1f}"
            ).add_to(m)
            
            # Add pulsing effect for critical zones
            if sev >= 8:
                folium.Circle(
                    location=[row['latitude'], row['longitude']],
                    radius=radius * 3,
                    color=color,
                    fill=False,
                    weight=2,
                    opacity=0.3
                ).add_to(m)
        
        folium_static(m, width=1200, height=600)

# REPORTS SCREEN
elif st.session_state.active_screen == "Reports":
    # Refresh data for this screen
    data = st.session_state.data.copy()
    st.markdown(f"""
        <h1 style="font-family: Poppins; font-size: 2.5rem; margin-bottom: 0.5rem;">📋 Data Export</h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            Export data and view statistics
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📊 Current Dataset")
        st.dataframe(data, use_container_width=True, hide_index=True, height=500)
    
    with col2:
        st.subheader("📥 Export")
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button("📄 Download CSV", csv,
                          f"data_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv", use_container_width=True)
        
        json_str = data.to_json(orient='records', indent=2)
        st.download_button("📋 Download JSON", json_str,
                          f"data_{datetime.now().strftime('%Y%m%d')}.json", "application/json", use_container_width=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📊 Statistics")
        st.dataframe(data.describe().round(2), use_container_width=True)

# REAL-TIME SCREEN
elif st.session_state.active_screen == "Real-time":
    # Refresh data for this screen
    data = st.session_state.data.copy()
    st.markdown(f"""
        <h1 style="font-family: Poppins; font-size: 2.5rem; margin-bottom: 0.5rem;">⚡ Live Monitoring</h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            Real-time status and alerts
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Status Feed")
        
        # Generate dynamic alerts based on actual data
        alerts = []
        if not data.empty and 'zone' in data.columns:
            # Get top zones by severity
            top_zones = data.nlargest(5, 'severity') if 'severity' in data.columns else data.head(5)
            
            for row_idx, (idx, row) in enumerate(top_zones.iterrows()):
                zone_name = str(row.get('zone', 'Unknown'))
                severity = float(row.get('severity', 0)) if 'severity' in row else 0
                allocated = int(row.get('allocated_volunteers', 0)) if 'allocated_volunteers' in row else 0
                required = int(row.get('required_volunteers', 0)) if 'required_volunteers' in row else int(row.get('volunteers_available', 0)) if 'volunteers_available' in row else 0
                
                # Determine status based on severity and allocation
                if severity >= 8:
                    status = "🔴 Critical"
                    if required > 0 and allocated < required * 0.5:
                        msg = f"{zone_name}: Understaffed ({allocated}/{required} volunteers)"
                    else:
                        msg = f"{zone_name}: High severity zone needs monitoring"
                elif severity >= 6:
                    status = "🟡 Alert"
                    if required > 0 and allocated < required * 0.7:
                        msg = f"{zone_name}: Needs more personnel ({allocated}/{required})"
                    else:
                        msg = f"{zone_name}: Moderate severity - monitoring"
                else:
                    status = "🟢 Normal"
                    msg = f"{zone_name}: Operational (Severity: {severity:.1f})"
                
                # Calculate time ago (simulated based on row index)
                time_ago = f"{row_idx + 1} min ago"
                alerts.append((status, msg, time_ago))
        
        # If no data, show default alerts
        if not alerts:
            alerts = [
                ("🟢 Normal", "System operational", "Just now"),
                ("🟡 Alert", "Waiting for data", "1 min ago"),
            ]
        
        # Display alerts with animations
        for idx, (status, msg, time) in enumerate(alerts[:10]):  # Limit to 10 most recent
            color = '#10b981' if '🟢' in status else '#f59e0b' if '🟡' in status else '#ef4444'
            pulse_class = 'critical-zone' if '🔴' in status else ''
            st.markdown(f"""
                <div class="alert-item" style="background: {colors['card_bg']}; padding: 1.25rem; border-radius: 16px;
                            margin-bottom: 1rem; border-left: 5px solid {color};
                            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                            transition: all 0.3s ease;
                            animation: slideInLeft 0.5s ease {idx * 0.1}s both;
                            position: relative;
                            overflow: hidden;">
                    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;
                                background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
                                transform: translateX(-100%);
                                transition: transform 0.6s;">
                    </div>
                    <div style="display: flex; justify-content: space-between; position: relative; z-index: 1;">
                        <div style="flex: 1;">
                            <div style="font-weight: 800; color: {color}; font-size: 1rem; margin-bottom: 0.5rem;
                                        display: flex; align-items: center; gap: 0.5rem;">
                                <span style="font-size: 1.2em;">{status.split()[0]}</span>
                                <span>{status.split()[1] if len(status.split()) > 1 else ''}</span>
                            </div>
                            <div style="color: {colors['text']}; font-size: 0.9rem; line-height: 1.5;">{msg}</div>
                        </div>
                        <div style="color: {colors['text_light']}; font-size: 0.75rem; font-weight: 600;
                                    padding-left: 1rem; white-space: nowrap;">{time}</div>
                    </div>
                </div>
                <style>
                    .alert-item:hover {{
                        transform: translateX(8px) translateY(-2px);
                        box-shadow: 0 8px 24px rgba(0,0,0,0.2), 0 0 0 2px {color}33;
                    }}
                    @keyframes slideInLeft {{
                        from {{
                            opacity: 0;
                            transform: translateX(-30px);
                        }}
                        to {{
                            opacity: 1;
                            transform: translateX(0);
                        }}
                    }}
                </style>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📈 Response Times")
        if 'response_time' in data.columns:
            fig = go.Figure(go.Scatter(
                x=data['zone'], y=data['response_time'], mode='lines+markers',
                line=dict(color='#667eea', width=3), marker=dict(size=10, color='#667eea'),
                fill='tozeroy', fillcolor='rgba(102, 126, 234, 0.2)'
            ))
            fig.update_layout(
                height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor=colors['card_bg'],
                font=dict(color=colors['text']), margin=dict(l=20, r=20, t=40, b=20),
                xaxis=dict(tickfont=dict(color=colors['text'])), yaxis=dict(tickfont=dict(color=colors['text']))
            )
            st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown(f"""
    <div style="text-align: center; padding: 2rem; margin-top: 3rem; border-top: 1px solid {colors['border']};">
        <div style="color: {colors['text_light']}; font-size: 0.875rem;">
            v2.1 Premium Edition | Last Update: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
""", unsafe_allow_html=True)
