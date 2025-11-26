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

# Modern CSS
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@600;700;800&display=swap');
    
    * {{ font-family: 'Inter', -apple-system, sans-serif; }}
    
    .stApp {{
        background: {colors['bg']};
        background-image: 
            radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
            radial-gradient(at 100% 100%, rgba(67, 233, 123, 0.10) 0px, transparent 50%);
        color: {colors['text']};
    }}
    
    #MainMenu, footer, header, .stDeployButton {{ visibility: hidden; }}
    [data-testid="stSidebar"] {{ display: none; }}
    
    /* Navigation Buttons - Fixed */
    .stButton > button {{
        background: {colors['card_bg']} !important;
        color: {colors['text']} !important;
        border: 2px solid {colors['border']} !important;
        border-radius: 12px !important;
        padding: 0.7rem 1.2rem !important;
        font-weight: 700 !important;
        font-size: 0.85rem !important;
        white-space: nowrap !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }}
    
    .stButton > button:hover {{
        border-color: {colors['accent']} !important;
        color: {colors['accent']} !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }}
    
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-color: transparent !important;
        box-shadow: 0 4px 16px rgba(102, 126, 234, 0.4) !important;
        transform: translateY(-2px) !important;
    }}
    
    /* Metric Cards */
    div[data-testid="metric-container"] {{
        background: {colors['card_bg']};
        padding: 2rem 1.75rem;
        border-radius: 24px;
        box-shadow: 0 0 0 1px {colors['border']}, 0 10px 30px -10px rgba(0, 0, 0, 0.2);
        border: 1px solid {colors['border']};
        position: relative;
        overflow: hidden;
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
    }}
    
    div[data-testid="metric-container"]:hover::before {{
        opacity: 1;
    }}
    
    div[data-testid="metric-container"]:hover {{
        transform: translateY(-8px);
        box-shadow: 0 0 0 1px {colors['accent']}, 0 20px 40px -10px rgba(99, 102, 241, 0.3);
        border-color: {colors['accent']};
    }}
    
    [data-testid="stMetricValue"] {{
        font-size: 2.75rem !important;
        font-weight: 900 !important;
        background: linear-gradient(135deg, {colors['text']} 0%, {colors['accent']} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
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
    
    /* Expanders */
    .streamlit-expanderHeader {{
        background: {colors['card_bg']};
        border-radius: 16px;
        border: 2px solid {colors['border']};
        color: {colors['text']} !important;
        font-weight: 700;
        padding: 1.125rem 1.5rem !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    
    .streamlit-expanderHeader:hover {{
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(118, 75, 162, 0.15) 100%);
        border-color: {colors['accent']};
        transform: translateX(6px);
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
    
    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 12px; }}
    ::-webkit-scrollbar-track {{ background: {colors['bg']}; }}
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

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

data = st.session_state.data

# Top Navigation
nav_col1, nav_col2, nav_col3 = st.columns([1.5, 7, 1.5])

with nav_col1:
    st.markdown(f"""
        <div style="font-family: Poppins; font-size: 1.5rem; font-weight: 800; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            🚨 Response Hub
        </div>
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
                        color: white; border-radius: 100px; font-weight: 700; font-size: 0.75rem;">
                <div style="width: 8px; height: 8px; background: white; border-radius: 50%;"></div>
                ONLINE
            </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🌙" if st.session_state.dark_mode else "☀️", key="theme"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# COMMAND CENTER SCREEN
if st.session_state.active_screen == "Command Center":
    st.markdown(f"""
        <h1 style="font-family: Poppins; font-size: 2.5rem; margin-bottom: 0.5rem;">⚙️ Command Center</h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            System configuration, data management, and zone controls
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📁 Data Management")
        
        def load_data():
            uploaded_file = st.session_state.uploaded_file
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    if 'zone' in df.columns:
                        if 'severity' not in df.columns:
                            df['severity'] = np.random.uniform(1, 10, len(df)).round(1)
                        if 'volunteers_available' not in df.columns:
                            df['volunteers_available'] = np.random.randint(20, 100, len(df))
                        if 'resources_available' not in df.columns:
                            df['resources_available'] = np.random.randint(50, 200, len(df))
                        if 'allocated_volunteers' not in df.columns:
                            df['allocated_volunteers'] = (df['volunteers_available'] * 0.8).astype(int)
                        if 'allocated_resources' not in df.columns:
                            df['allocated_resources'] = (df['resources_available'] * 0.8).astype(int)
                        if 'latitude' not in df.columns or 'longitude' not in df.columns:
                            base_lat, base_lon = 33.6844, 73.0479
                            df['latitude'] = base_lat + np.random.uniform(-0.1, 0.1, len(df))
                            df['longitude'] = base_lon + np.random.uniform(-0.1, 0.1, len(df))
                        if 'response_time' not in df.columns:
                            df['response_time'] = np.random.randint(5, 20, len(df))
                        if 'efficiency' not in df.columns:
                            df['efficiency'] = np.random.randint(75, 95, len(df))
                        
                        st.session_state.data = df
                        st.session_state.last_update = datetime.now()
                        st.toast("✅ Data uploaded successfully!", icon="✅")
                    else:
                        st.error("CSV must contain a 'zone' column.")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        st.file_uploader("Upload CSV File", type=['csv'], key="uploaded_file", on_change=load_data)
        st.info(f"📊 Dataset: **{len(data)} zones**")
        st.success(f"🕐 Updated: {st.session_state.last_update.strftime('%H:%M:%S')}")
    
    with col2:
        st.subheader("🎯 Quick Stats")
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Personnel", int(data['allocated_volunteers'].sum()))
            st.metric("Avg Severity", f"{data['severity'].mean():.1f}")
        with col_b:
            st.metric("Resources", int(data['allocated_resources'].sum()))
            st.metric("Efficiency", f"{data['efficiency'].mean():.0f}%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("⚙️ Zone Controls")
    
    if not data.empty and 'zone' in data.columns:
        cols = st.columns(3)
        for idx, zone in enumerate(data['zone'].unique()[:9]):
            with cols[idx % 3]:
                with st.expander(f"🎯 {zone}"):
                    row_idx = data.index[data['zone'] == zone][0]
                    current_sev = float(data.at[row_idx, 'severity'])
                    current_vol = int(data.at[row_idx, 'volunteers_available'])
                    
                    max_sev = max(10.0, float(data['severity'].max()))
                    max_vol = max(100, int(data['volunteers_available'].max() * 1.5))
                    
                    new_sev = st.slider("🔥 Severity", 0.0, max_sev, current_sev, 0.1, key=f"sev_{zone}")
                    new_vol = st.slider("👥 Personnel", 0, max_vol, current_vol, 5, key=f"vol_{zone}")
                    
                    st.session_state.data.at[row_idx, 'severity'] = new_sev
                    st.session_state.data.at[row_idx, 'volunteers_available'] = new_vol
                    st.session_state.data.at[row_idx, 'allocated_volunteers'] = int(new_vol * 0.9)
        
        data = st.session_state.data

# OVERVIEW SCREEN
elif st.session_state.active_screen == "Overview":
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
    st.markdown(f"""
        <h1 style="font-family: Poppins; font-size: 2.5rem; margin-bottom: 0.5rem;">📈 Advanced Analytics</h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            Detailed analysis of resource allocation
        </p>
    """, unsafe_allow_html=True)
    
    st.subheader("👥 Personnel Deployment")
    fig_bar = px.bar(data, x='zone', y='allocated_volunteers', color='severity',
                     color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'],
                     labels={'allocated_volunteers': 'Deployed', 'zone': 'Zone'})
    fig_bar.update_layout(
        height=450, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor=colors['card_bg'],
        font=dict(color=colors['text']), margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(tickfont=dict(color=colors['text']), gridcolor=colors['border']),
        yaxis=dict(tickfont=dict(color=colors['text']), gridcolor=colors['border'])
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔥 Severity vs Response")
        fig_scatter = px.scatter(data, x='severity', y='allocated_volunteers', size='allocated_resources', color='zone')
        fig_scatter.update_layout(
            height=400, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor=colors['card_bg'],
            font=dict(color=colors['text']), margin=dict(l=20, r=20, t=40, b=20),
            xaxis=dict(tickfont=dict(color=colors['text'])), yaxis=dict(tickfont=dict(color=colors['text'])),
            legend=dict(font=dict(color=colors['text']))
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.subheader("⚡ System Efficiency")
        avg_eff = data['efficiency'].mean()
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta", value=avg_eff,
            title={'text': "Average Efficiency", 'font': {'color': colors['text']}},
            delta={'reference': 80}, number={'font': {'color': colors['text']}},
            gauge={'axis': {'range': [None, 100], 'tickfont': {'color': colors['text']}},
                   'bar': {'color': "#667eea"}, 'bordercolor': colors['border'],
                   'steps': [{'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.3)'},
                            {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.3)'},
                            {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.3)'}]}
        ))
        fig_gauge.update_layout(paper_bgcolor=colors['card_bg'], font={'color': colors['text']}, height=400)
        st.plotly_chart(fig_gauge, use_container_width=True)

# MAP VIEW SCREEN
elif st.session_state.active_screen == "Map View":
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
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=min(25, sev * 2.5),
                popup=f"<b>{row['zone']}</b><br>Severity: {sev:.1f}",
                color=color, fill=True, fillColor=color, fillOpacity=0.7, weight=3,
                tooltip=f"{row['zone']}"
            ).add_to(m)
        
        folium_static(m, width=1200, height=600)

# REPORTS SCREEN
elif st.session_state.active_screen == "Reports":
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
    st.markdown(f"""
        <h1 style="font-family: Poppins; font-size: 2.5rem; margin-bottom: 0.5rem;">⚡ Live Monitoring</h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            Real-time status and alerts
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🔴 Status Feed")
        alerts = [
            ("🟢 Normal", "Zone A operational", "2 min ago"),
            ("🟡 Alert", "Zone C severity increased", "5 min ago"),
            ("🔴 Critical", "Zone D attention needed", "8 min ago"),
        ]
        for status, msg, time in alerts:
            color = '#10b981' if '🟢' in status else '#f59e0b' if '🟡' in status else '#ef4444'
            st.markdown(f"""
                <div style="background: {colors['card_bg']}; padding: 1rem; border-radius: 12px;
                            margin-bottom: 0.75rem; border-left: 4px solid {color};">
                    <div style="display: flex; justify-content: space-between;">
                        <div>
                            <div style="font-weight: 700; color: {colors['text']};">{status}</div>
                            <div style="color: {colors['text_light']}; font-size: 0.875rem;">{msg}</div>
                        </div>
                        <div style="color: {colors['text_light']}; font-size: 0.75rem;">{time}</div>
                    </div>
                </div>
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
