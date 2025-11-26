import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import folium_static
import numpy as np
from datetime import datetime, timedelta

# Page config
st.set_page_config(
    page_title="Emergency Response Command Center",
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

# Premium color schemes
light_colors = {
    'bg': '#f8fafc',
    'sidebar_bg': '#ffffff',
    'card_bg': '#ffffff',
    'text': '#0f172a',
    'text_light': '#64748b',
    'accent': '#6366f1',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    'border': '#e2e8f0',
    'glass_bg': 'rgba(255, 255, 255, 0.8)',
    'glass_border': 'rgba(255, 255, 255, 0.3)'
}

dark_colors = {
    'bg': '#0a0e1a',
    'sidebar_bg': '#1a1d2e',
    'card_bg': '#1e2235',
    'text': '#f1f5f9',
    'text_light': '#94a3b8',
    'accent': '#818cf8',
    'success': '#34d399',
    'warning': '#fbbf24',
    'danger': '#f87171',
    'info': '#60a5fa',
    'border': '#2d3548',
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
    
    /* Premium DataFrames */
    [data-testid="stDataFrame"] {{
        background: {colors['card_bg']};
        border-radius: 20px;
        border: 1px solid {colors['border']};
        box-shadow: 0 10px 30px rgba(0,0,0,0.12);
        overflow: hidden;
    }}
    
    /* Enhanced Headers */
    h1, h2, h3 {{
        color: {colors['text']} !important;
        font-weight: 800;
    }}
    
    h2 {{
        font-family: 'Poppins', sans-serif;
        font-size: 2rem;
        margin-bottom: 2rem;
        letter-spacing: -0.02em;
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
    
    /* Premium Alert Boxes */
    .stSuccess {{
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(5, 150, 105, 0.05) 100%);
        border-left: 5px solid #10b981;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(16, 185, 129, 0.2);
    }}
    
    .stInfo {{
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(79, 70, 229, 0.05) 100%);
        border-left: 5px solid #6366f1;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.2);
    }}
    
    /* Expander */
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
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.2);
    }}
    
    /* Advanced Animations */
    @keyframes pulse {{
        0%, 100% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.05); opacity: 0.95; }}
    }}
    
    @keyframes blink {{
        0%, 100% {{ opacity: 1; }}
        50% {{ opacity: 0.3; }}
    }}
    
    /* File Uploader */
    [data-testid="stFileUploader"] {{
        background: {colors['card_bg']};
        border-radius: 18px;
        border: 2px dashed {colors['border']};
        padding: 2rem;
        transition: all 0.3s ease;
    }}
    
    [data-testid="stFileUploader"]:hover {{
        border-color: {colors['accent']};
        background: {colors['glass_bg']};
        border-style: solid;
    }}
    
    /* Sliders */
    .stSlider {{
        padding: 2rem 0;
    }}
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {{
        width: 12px;
        height: 12px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors['bg']};
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        border: 2px solid {colors['bg']};
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: linear-gradient(135deg, #764ba2 0%, #f093fb 100%);
    }}
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for data
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

# Top Navigation Bar
nav_col1, nav_col2, nav_col3 = st.columns([2, 6, 2])

with nav_col1:
    st.markdown(f"""
        <div class="nav-brand">
            <span>🚨</span>
            <span>Response Hub</span>
        </div>
    """, unsafe_allow_html=True)

with nav_col2:
    screens = ["Command Center", "Overview", "Analytics", "Map View", "Reports", "Real-time"]
    nav_cols = st.columns(len(screens))
    
    for idx, screen in enumerate(screens):
        with nav_cols[idx]:
            if st.button(
                screen,
                key=f"nav_{screen}",
                use_container_width=True,
                type="primary" if st.session_state.active_screen == screen else "secondary"
            ):
                st.session_state.active_screen = screen
                st.rerun()

with nav_col3:
    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown(f"""
            <div class="status-badge" style="font-size: 0.75rem; padding: 0.4rem 0.9rem;">
                <div class="status-indicator"></div>
                ONLINE
            </div>
        """, unsafe_allow_html=True)
    with col2:
        if st.button("🌙" if st.session_state.dark_mode else "☀️", key="theme_toggle"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

st.markdown("<br>", unsafe_allow_html=True)

# SCREEN 1: Command Center
if st.session_state.active_screen == "Command Center":
    st.markdown(f"""
        <h1 style="font-family: 'Poppins', sans-serif; font-size: 2.5rem; margin-bottom: 1rem;">
            ⚙️ Command Center
        </h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            Configure system settings, import data, and manage zone controls
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
                        st.toast("✅ Data uploaded & enriched successfully!", icon="✅")
                    else:
                        st.error("CSV must contain at least a 'zone' column.")
                except Exception as e:
                    st.error(f"Error reading file: {e}")
        
        st.file_uploader(
            "Upload CSV File",
            type=['csv'],
            key="uploaded_file",
            on_change=load_data
        )
        
        st.info(f"📊 Current dataset: **{len(data)} zones**")
        st.success(f"🕐 Last updated: {st.session_state.last_update.strftime('%H:%M:%S')}")
    
    with col2:
        st.subheader("🎯 Quick Stats")
        
        col_a, col_b = st.columns(2)
        with col_a:
            st.metric("Total Personnel", int(data['allocated_volunteers'].sum()))
            st.metric("Avg Severity", f"{data['severity'].mean():.1f}")
        with col_b:
            st.metric("Total Resources", int(data['allocated_resources'].sum()))
            st.metric("Avg Efficiency", f"{data['efficiency'].mean():.0f}%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Zone Controls
    st.subheader("⚙️ Zone Controls")
    
    if not data.empty and 'zone' in data.columns:
        unique_zones = data['zone'].unique()
        
        cols = st.columns(3)
        for idx, zone in enumerate(unique_zones[:9]):
            with cols[idx % 3]:
                with st.expander(f"🎯 {zone}"):
                    row_idx = data.index[data['zone'] == zone][0]
                    
                    current_severity = float(data.at[row_idx, 'severity'])
                    current_volunteers = int(data.at[row_idx, 'volunteers_available'])
                    
                    max_sev_val = max(10.0, float(data['severity'].max()))
                    max_vol_val = max(100, int(data['volunteers_available'].max() * 1.5))
                    
                    new_severity = st.slider(
                        "🔥 Severity",
                        0.0, max_sev_val,
                        current_severity,
                        0.1,
                        key=f"sev_{zone}"
                    )
                    
                    new_volunteers = st.slider(
                        "👥 Personnel",
                        0, max_vol_val,
                        current_volunteers,
                        5,
                        key=f"vol_{zone}"
                    )
                    
                    st.session_state.data.at[row_idx, 'severity'] = new_severity
                    st.session_state.data.at[row_idx, 'volunteers_available'] = new_volunteers
                    st.session_state.data.at[row_idx, 'allocated_volunteers'] = int(new_volunteers * 0.9)
        
        data = st.session_state.data

# SCREEN 2: Overview
elif st.session_state.active_screen == "Overview":
    st.markdown(f"""
        <h1 style="font-family: 'Poppins', sans-serif; font-size: 2.5rem; margin-bottom: 1rem;">
            📊 System Overview
        </h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            Real-time monitoring of all disaster zones and resources
        </p>
    """, unsafe_allow_html=True)
    
    # Premium KPIs
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Active Zones", len(data), delta="+2 from yesterday")
    
    with col2:
        avg_severity = data['severity'].mean()
        st.metric("Avg Severity", f"{avg_severity:.1f}", delta=f"Range: {data['severity'].max() - data['severity'].min():.1f}")
    
    with col3:
        total_deployed = int(data['allocated_volunteers'].sum())
        st.metric("Personnel", total_deployed, delta=f"+{int(data['volunteers_available'].sum() - total_deployed)} standby")
    
    with col4:
        total_resources = int(data['allocated_resources'].sum())
        st.metric("Resources", total_resources, delta=f"+{int(data['resources_available'].sum() - total_resources)} reserve")
    
    with col5:
        avg_efficiency = data['efficiency'].mean() if 'efficiency' in data.columns else 85
        st.metric("Efficiency", f"{avg_efficiency:.1f}%", delta="+3.2%")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Zone Status
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📍 Zone Status Dashboard")
        summary_df = data[['zone', 'severity', 'volunteers_available', 'allocated_volunteers', 
                           'resources_available', 'allocated_resources']].copy()
        
        summary_df['deployment_%'] = summary_df.apply(
            lambda x: (x['allocated_volunteers'] / x['volunteers_available'] * 100) if x['volunteers_available'] > 0 else 0, 
            axis=1
        ).round(1)
        
        summary_df.columns = ['Zone', 'Severity', 'Available', 'Deployed', 'Resources', 'Active', 'Deploy %']
        st.dataframe(summary_df, use_container_width=True, hide_index=True, height=400)
    
    with col2:
        st.subheader("🎯 Priority Zones")
        
        critical_zones = data.nlargest(3, 'severity')[['zone', 'severity']]
        for idx, row in critical_zones.iterrows():
            severity_color = '#ef4444' if row['severity'] > 8 else '#f59e0b' if row['severity'] > 6 else '#10b981'
            st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, {severity_color}22 0%, {severity_color}11 100%);
                    padding: 1rem;
                    border-radius: 12px;
                    border-left: 4px solid {severity_color};
                    margin-bottom: 0.75rem;
                ">
                    <div style="font-weight: 700; font-size: 1.1rem; color: {colors['text']};">{row['zone']}</div>
                    <div style="color: {severity_color}; font-weight: 800; font-size: 1.5rem; margin-top: 0.25rem;">
                        Severity: {row['severity']:.1f}
                    </div>
                </div>
            """, unsafe_allow_html=True)

# SCREEN 3: Analytics
elif st.session_state.active_screen == "Analytics":
    st.markdown(f"""
        <h1 style="font-family: 'Poppins', sans-serif; font-size: 2.5rem; margin-bottom: 1rem;">
            📈 Advanced Analytics
        </h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            Detailed analysis and insights into resource allocation
        </p>
    """, unsafe_allow_html=True)
    
    # Deployment Overview
    st.subheader("👥 Personnel Deployment Analysis")
    fig_bar = px.bar(
        data,
        x='zone',
        y='allocated_volunteers',
        color='severity',
        color_continuous_scale=['#10b981', '#f59e0b', '#ef4444'],
        labels={'allocated_volunteers': 'Deployed Personnel', 'zone': 'Zone'},
        title='Personnel Distribution by Zone'
    )
    fig_bar.update_layout(
        height=450,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor=colors['card_bg'],
        font=dict(color=colors['text'], family='Inter'),
        title_font=dict(size=20, family='Poppins', color=colors['text']),
        margin=dict(l=20, r=20, t=60, b=20),
        showlegend=True,
        hovermode='x unified',
        xaxis=dict(title_font=dict(color=colors['text']), tickfont=dict(color=colors['text']), gridcolor=colors['border'], showgrid=True),
        yaxis=dict(title_font=dict(color=colors['text']), tickfont=dict(color=colors['text']), gridcolor=colors['border'], showgrid=True)
    )
    fig_bar.update_traces(marker_line_color='rgba(0,0,0,0.1)', marker_line_width=1)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Severity vs Response")
        fig_scatter = px.scatter(
            data,
            x='severity',
            y='allocated_volunteers',
            size='allocated_resources',
            color='zone',
            labels={'severity': 'Severity Level', 'allocated_volunteers': 'Deployed Personnel'},
            title='Response Correlation'
        )
        fig_scatter.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=colors['card_bg'],
            font=dict(color=colors['text'], family='Inter'),
            title_font=dict(size=18, family='Poppins', color=colors['text']),
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis=dict(title_font=dict(color=colors['text']), tickfont=dict(color=colors['text']), gridcolor=colors['border'], showgrid=True),
            yaxis=dict(title_font=dict(color=colors['text']), tickfont=dict(color=colors['text']), gridcolor=colors['border'], showgrid=True),
            legend=dict(font=dict(color=colors['text']))
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    with col2:
        st.subheader("⚡ System Efficiency")
        avg_eff = data['efficiency'].mean() if 'efficiency' in data.columns else 85
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=avg_eff,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Average Efficiency", 'font': {'size': 20, 'family': 'Poppins', 'color': colors['text']}},
            delta={'reference': 80, 'increasing': {'color': "#10b981"}},
            number={'font': {'color': colors['text']}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': colors['text'], 'tickfont': {'color': colors['text']}},
                'bar': {'color': "#667eea"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': colors['border'],
                'steps': [
                    {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.3)'},
                    {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.3)'},
                    {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.3)'}
                ],
                'threshold': {'line': {'color': "#ef4444", 'width': 4}, 'thickness': 0.75, 'value': 90}
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor=colors['card_bg'],
            font={'color': colors['text'], 'family': 'Inter'},
            height=400,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Resource Comparison
    st.subheader("📦 Resource Allocation Comparison")
    col1, col2 = st.columns(2)
    
    with col1:
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Bar(name='Available', x=data['zone'], y=data['volunteers_available'], marker_color='#a5b4fc'))
        fig_vol.add_trace(go.Bar(name='Deployed', x=data['zone'], y=data['allocated_volunteers'], marker_color='#667eea'))
        fig_vol.update_layout(
            barmode='group',
            title='Personnel Availability',
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=colors['card_bg'],
            font=dict(color=colors['text'], family='Inter'),
            title_font=dict(size=18, family='Poppins', color=colors['text']),
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=True,
            xaxis=dict(title_font=dict(color=colors['text']), tickfont=dict(color=colors['text']), gridcolor=colors['border']),
            yaxis=dict(title_font=dict(color=colors['text']), tickfont=dict(color=colors['text']), gridcolor=colors['border']),
            legend=dict(font=dict(color=colors['text']))
        )
        st.plotly_chart(fig_vol, use_container_width=True)
    
    with col2:
        fig_res = go.Figure()
        fig_res.add_trace(go.Bar(name='Available', x=data['zone'], y=data['resources_available'], marker_color='#f9a8d4'))
        fig_res.add_trace(go.Bar(name='Active', x=data['zone'], y=data['allocated_resources'], marker_color='#f093fb'))
        fig_res.update_layout(
            barmode='group',
            title='Resource Distribution',
            height=350,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor=colors['card_bg'],
            font=dict(color=colors['text'], family='Inter'),
            title_font=dict(size=18, family='Poppins', color=colors['text']),
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=True,
            xaxis=dict(title_font=dict(color=colors['text']), tickfont=dict(color=colors['text']), gridcolor=colors['border']),
            yaxis=dict(title_font=dict(color=colors['text']), tickfont=dict(color=colors['text']), gridcolor=colors['border']),
            legend=dict(font=dict(color=colors['text']))
        )
        st.plotly_chart(fig_res, use_container_width=True)

# SCREEN 4: Map View
elif st.session_state.active_screen == "Map View":
    st.markdown(f"""
        <h1 style="font-family: 'Poppins', sans-serif; font-size: 2.5rem; margin-bottom: 1rem;">
            🗺️ Geographic Overview
        </h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            Interactive map showing all disaster zones and their severity levels
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
            
            popup_html = f"""
            <div style="font-family: Inter, sans-serif; min-width: 250px; padding: 15px; background: white; border-radius: 12px;">
                <h3 style="color: #667eea; margin: 0 0 12px 0; font-family: Poppins, sans-serif; font-size: 1.25rem; font-weight: 700;">
                    🎯 {row['zone']}
                </h3>
                <div style="background: linear-gradient(135deg, {color}22 0%, {color}11 100%); padding: 10px; border-radius: 8px; border-left: 4px solid {color}; margin-bottom: 10px;">
                    <div style="font-weight: 700; color: {color}; font-size: 1.5rem;">Severity: {sev:.1f}</div>
                </div>
                <div style="display: grid; gap: 8px; margin-top: 12px;">
                    <div style="background: #f8fafc; padding: 8px; border-radius: 6px;">
                        <strong style="color: #64748b;">👥 Personnel:</strong> 
                        <span style="color: #0f172a; font-weight: 600;">{int(row['allocated_volunteers'])}/{int(row['volunteers_available'])}</span>
                    </div>
                    <div style="background: #f8fafc; padding: 8px; border-radius: 6px;">
                        <strong style="color: #64748b;">📦 Resources:</strong> 
                        <span style="color: #0f172a; font-weight: 600;">{int(row['allocated_resources'])}/{int(row['resources_available'])}</span>
                    </div>
                </div>
            </div>
            """
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=min(25, sev * 2.5),
                popup=folium.Popup(popup_html, max_width=350),
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                weight=3,
                tooltip=f"<b>{row['zone']}</b><br>Severity: {sev:.1f}"
            ).add_to(m)
        
        folium_static(m, width=1200, height=600)
    else:
        st.warning("Map requires latitude/longitude data")

# SCREEN 5: Reports
elif st.session_state.active_screen == "Reports":
    st.markdown(f"""
        <h1 style="font-family: 'Poppins', sans-serif; font-size: 2.5rem; margin-bottom: 1rem;">
            📋 Data Export & Reports
        </h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            Export data and view detailed statistics
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Current Dataset")
        st.dataframe(data, use_container_width=True, hide_index=True, height=500)
    
    with col2:
        st.subheader("📥 Export Options")
        
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📄 Download CSV",
            csv,
            f"response_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "text/csv",
            use_container_width=True
        )
        
        json_str = data.to_json(orient='records', indent=2)
        st.download_button(
            "📋 Download JSON",
            json_str,
            f"response_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "application/json",
            use_container_width=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("📊 Statistics")
        st.dataframe(data.describe().round(2), use_container_width=True)

# SCREEN 6: Real-time
elif st.session_state.active_screen == "Real-time":
    st.markdown(f"""
        <h1 style="font-family: 'Poppins', sans-serif; font-size: 2.5rem; margin-bottom: 1rem;">
            ⚡ Real-time Monitoring
        </h1>
        <p style="color: {colors['text_light']}; font-size: 1.1rem; margin-bottom: 2rem;">
            Live status updates and response time analytics
        </p>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔴 Live Status Feed")
        
        alerts = [
            ("🟢 Normal", "Zone A operational", "2 min ago"),
            ("🟡 Alert", "Zone C severity increased", "5 min ago"),
            ("🔴 Critical", "Zone D requires immediate attention", "8 min ago"),
            ("🟢 Normal", "Zone B resources replenished", "12 min ago"),
        ]
        
        for status, message, time in alerts:
            st.markdown(f"""
                <div style="
                    background: {colors['card_bg']};
                    padding: 1rem;
                    border-radius: 12px;
                    margin-bottom: 0.75rem;
                    border-left: 4px solid {'#10b981' if '🟢' in status else '#f59e0b' if '🟡' in status else '#ef4444'};
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                ">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div style="font-weight: 700; color: {colors['text']};">{status}</div>
                            <div style="color: {colors['text_light']}; font-size: 0.875rem; margin-top: 0.25rem;">{message}</div>
                        </div>
                        <div style="color: {colors['text_light']}; font-size: 0.75rem;">{time}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("📈 Response Time Trends")
        
        if 'response_time' in data.columns:
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=data['zone'],
                y=data['response_time'],
                mode='lines+markers',
                name='Response Time',
                line=dict(color='#667eea', width=3),
                marker=dict(size=10, color='#667eea', line=dict(color='white', width=2)),
                fill='tozeroy',
                fillcolor='rgba(102, 126, 234, 0.2)'
            ))
            fig_line.update_layout(
                title='Average Response Time (minutes)',
                height=450,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor=colors['card_bg'],
                font=dict(color=colors['text'], family='Inter'),
                title_font=dict(size=18, family='Poppins', color=colors['text']),
                margin=dict(l=20, r=20, t=50, b=20),
                hovermode='x unified',
                xaxis=dict(title_font=dict(color=colors['text']), tickfont=dict(color=colors['text']), gridcolor=colors['border'], showgrid=True),
                yaxis=dict(title_font=dict(color=colors['text']), tickfont=dict(color=colors['text']), gridcolor=colors['border'], showgrid=True)
            )
            st.plotly_chart(fig_line, use_container_width=True)

# Footer
st.markdown(f"""
    <div style="
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        border-top: 1px solid {colors['border']};
    ">
        <div style="color: {colors['text_light']}; font-size: 0.875rem; font-family: 'JetBrains Mono', monospace;">
            v2.1 Premium Edition | Last Update: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}
        </div>
    </div>
""", unsafe_allow_html=True)