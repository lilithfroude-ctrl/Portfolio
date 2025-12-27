"""
Sky Harbor Airport Ride-Hailing Dashboard
Streamlit Web Application

Features:
- Dark theme with professional header
- Real-time metrics display
- Service breakdown with logos
- Interactive time slider
- Parking map with occupied spot markers
- Auto-refresh animation option
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import time
from datetime import datetime
import base64
from io import BytesIO
import os

def get_base64_image(path):
    """Convert image file to base64 string."""
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Initialize session state for slider
if 'selected_time' not in st.session_state:
    st.session_state.selected_time = 0

# Page configuration
st.set_page_config(
    page_title="Sky Harbor Airport - Ride-Hailing Dashboard",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Additional polished styling
st.markdown("""
<style>
    /* Smooth animations */
    .stMetric, .stProgress > div > div {
        transition: all 0.3s ease;
    }
    
    /* Better metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    /* Rounded progress bars */
    .stProgress > div > div {
        border-radius: 10px;
        height: 12px;
    }
    
    /* Card hover effect */
    .stMetric:hover {
        transform: scale(1.02);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# CSS to center all images and text in columns
st.markdown("""
<style>
    [data-testid="column"] {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
    }
    [data-testid="column"] img {
        margin: 0 auto;
    }
    [data-testid="stImage"] {
        display: flex;
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

# Custom CSS for modern dark theme with glassmorphism
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d2d44 100%);
    }
    
    /* Header styling with gradient */
    .main-header {
        background: linear-gradient(135deg, #0f3460 0%, #16213e 100%);
        padding: 2.5rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .main-header:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
    }
    
    .main-header h1 {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Glassmorphism metric cards - style the metric container directly */
    [data-testid="stMetricContainer"] {
        background: rgba(255, 255, 255, 0.08) !important;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stMetricContainer"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4) !important;
        background: rgba(255, 255, 255, 0.12) !important;
    }
    
    /* Metric values */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        color: #b0b0b0;
    }
    
    /* Service breakdown - ensure equal column widths and alignment */
    div[data-testid="column"] {
        padding: 0.5rem;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    /* Center images in columns */
    div[data-testid="column"] img {
        margin: 0 auto;
        display: block;
    }
    
    /* Center progress bars */
    div[data-testid="column"] .stProgress {
        width: 100%;
        margin: 0 auto;
    }
    
    /* Thicker, more vibrant progress bars */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, rgba(255,255,255,0.3), rgba(255,255,255,0.5));
        height: 12px !important;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    /* Slider styling */
    .stSlider {
        padding: 1rem 0;
    }
    
    /* Map container - style plotly chart container */
    [data-testid="stPlotlyChart"] {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Section spacing */
    .section-spacing {
        margin: 2rem 0;
    }
    
    /* Smooth transitions */
    * {
        transition: all 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Service configuration
SERVICE_COLORS = {
    'Uber': '#000000',
    'Lyft': '#FF00BF',
    'Waymo': '#00B4A2',
    'Taxi': '#F5A623'
}

LOGO_PATHS = {
    'Uber': 'assets/logos/uber.png',
    'Lyft': 'assets/logos/lyft.png',
    'Waymo': 'assets/logos/waymo.png',
    'Taxi': 'assets/logos/taxi.png'
}

VERTICAL_OFFSET = 30
TOTAL_SPOTS = 24

# Load data
@st.cache_data
def load_data():
    """Load and process the ride-hailing data."""
    df = pd.read_excel('assets/ride_hailing.xlsx')
    
    # Split "Other" service entries if any
    other_mask = df['service'] == 'Other'
    other_indices = df[other_mask].index.tolist()
    if len(other_indices) > 0:
        half_point = len(other_indices) // 2
        for idx in other_indices[:half_point]:
            df.at[idx, 'service'] = 'Waymo'
        for idx in other_indices[half_point:]:
            df.at[idx, 'service'] = 'Taxi'
    
    # Create status column
    df['status'] = df['reservation_id'].apply(
        lambda x: 'occupied' if pd.notna(x) and str(x).strip() != '' else 'vacant'
    )
    
    # Convert current_time to datetime
    df['current_time'] = pd.to_datetime(df['current_time'])
    
    return df

@st.cache_data
def get_timestamps(df):
    """Get sorted unique timestamps."""
    return sorted(df['current_time'].unique())

def calculate_stats(df_frame):
    """Calculate statistics for the current frame."""
    occupied = df_frame[df_frame['status'] == 'occupied']
    vacant = df_frame[df_frame['status'] == 'vacant']
    
    stats = {
        'total_spots': TOTAL_SPOTS,
        'occupied_count': int(len(occupied)),
        'vacant_count': int(len(vacant)),
        'occupancy_rate': (len(occupied) / TOTAL_SPOTS) * 100 if TOTAL_SPOTS > 0 else 0,
        'total_vehicles': int(len(occupied)),
        'uber_count': int(len(occupied[occupied['service'] == 'Uber'])),
        'lyft_count': int(len(occupied[occupied['service'] == 'Lyft'])),
        'waymo_count': int(len(occupied[occupied['service'] == 'Waymo'])),
        'taxi_count': int(len(occupied[occupied['service'] == 'Taxi']))
    }
    return stats

def create_live_status_panel(stats):
    """Create HTML for the Live Status panel matching visualize_ride_hailing.py style."""
    
    # Calculate occupancy rate color
    rate = stats['occupancy_rate']
    rate_color = '#27ae60' if rate < 50 else '#f39c12' if rate < 80 else '#e74c3c'
    
    # Get service counts
    services_data = [
        {'name': 'Uber', 'count': stats['uber_count'], 'color': '#000000'},
        {'name': 'Lyft', 'count': stats['lyft_count'], 'color': '#FF00BF'},
        {'name': 'Waymo', 'count': stats['waymo_count'], 'color': '#00B4A2'},
        {'name': 'Taxi', 'count': stats['taxi_count'], 'color': '#F5A623'}
    ]
    
    max_count = max(s['count'] for s in services_data) if max(s['count'] for s in services_data) > 0 else 1
    
    # Convert service logos to base64
    service_logos_base64 = {}
    for service in services_data:
        try:
            logo_path = f"assets/logos/{service['name'].lower()}.png"
            if os.path.exists(logo_path):
                service_logos_base64[service['name']] = get_base64_image(logo_path)
            else:
                service_logos_base64[service['name']] = ""
        except:
            service_logos_base64[service['name']] = ""
    
    # Build service rows HTML
    service_rows_html = ""
    for service in services_data:
        logo_base64 = service_logos_base64.get(service['name'], "")
        bar_width = (service['count'] / max_count) * 100 if max_count > 0 else 0
        
        logo_html = ""
        if logo_base64:
            logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="width: 28px; height: 28px; object-fit: contain; vertical-align: middle;">'
        else:
            logo_html = f'<span style="font-size: 12px; font-weight: bold; color: {service["color"]};">{service["name"][0]}</span>'
        
        service_rows_html += f'<div style="display: flex; align-items: center; margin-bottom: 20px;"><div style="width: 35px; display: flex; justify-content: center;">{logo_html}</div><div style="flex: 1; margin-left: 10px;"><div style="background: #ecf0f1; border-radius: 5px; height: 10px; width: 100%; overflow: hidden;"><div style="background: {service["color"]}; height: 100%; width: {bar_width}%; border-radius: 5px;"></div></div></div><div style="width: 30px; text-align: right; font-size: 14px; font-weight: bold; color: {service["color"]}; margin-left: 10px;">{service["count"]}</div></div>'
    
    panel_html = f"""<div style="position: relative; background: #f5f6fa; border-radius: 15px; border: 2px solid #2c3e50; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3), 4px 4px 8px rgba(0, 0, 0, 0.2); padding: 0; margin: 20px 0; overflow: hidden; width: 100%;"><div style="position: absolute; top: 4px; left: 4px; right: -4px; bottom: -4px; background: #333333; opacity: 0.3; border-radius: 15px; z-index: 0;"></div><div style="position: relative; z-index: 1;"><div style="background: #2c3e50; padding: 12px 0; text-align: center; border-radius: 15px 15px 0 0;"><div style="color: white; font-size: 14px; font-weight: bold; letter-spacing: 1px;">LIVE STATUS</div></div><div style="padding: 20px; background: #f5f6fa;"><div style="text-align: center; margin-bottom: 20px;"><div style="font-size: 32px; font-weight: bold; color: {rate_color}; margin-bottom: 5px;">{rate:.0f}%</div><div style="font-size: 9px; color: #7f8c8d; font-weight: bold; letter-spacing: 0.5px;">OCCUPANCY</div></div><div style="text-align: center; margin-bottom: 20px;"><div style="font-size: 40px; font-weight: bold; color: #27ae60; margin-bottom: 5px;">{stats['vacant_count']}</div><div style="font-size: 9px; color: #7f8c8d; font-weight: bold; letter-spacing: 0.5px;">SPOTS AVAILABLE</div></div><div style="height: 2px; background: #ecf0f1; margin: 20px 0;"></div><div style="text-align: center; font-size: 10px; font-weight: bold; color: #2c3e50; margin-bottom: 15px; letter-spacing: 0.5px;">BY SERVICE</div><div style="padding: 0 10px;">{service_rows_html}</div></div></div></div>"""
    
    return panel_html

def create_map_plot(df_frame, img_path, img_width, img_height):
    """Create a plotly figure with the map, license plate images, service logos, and colored borders."""
    from PIL import ImageDraw
    
    # Load map image and convert to base64
    map_img = Image.open(img_path)
    buffered = BytesIO()
    map_img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    img_data = f"data:image/png;base64,{img_str}"
    
    # Create figure
    fig = go.Figure()
    
    # Add map image as background
    fig.add_layout_image(
        dict(
            source=img_data,
            xref="x",
            yref="y",
            x=0,
            y=img_height,
            sizex=img_width,
            sizey=img_height,
            sizing="stretch",
            opacity=0.85,
            layer="below"
        )
    )
    
    # Service colors for borders
    SERVICE_BORDER_COLORS = {
        'Uber': '#000000',
        'Lyft': '#FF00BF',
        'Waymo': '#00B4A2',
        'Taxi': '#F5A623'
    }
    
    # Load service logos
    service_logos = {}
    logo_paths = {
        'Uber': 'assets/logos/uber.png',
        'Lyft': 'assets/logos/lyft.png',
        'Waymo': 'assets/logos/waymo.png',
        'Taxi': 'assets/logos/taxi.png'
    }
    for service, logo_path in logo_paths.items():
        try:
            if os.path.exists(logo_path):
                service_logos[service] = Image.open(logo_path)
        except:
            pass
    
    # Add license plate images for occupied spots
    occupied_data = df_frame[df_frame['status'] == 'occupied']
    plate_size = 80  # Size of license plate images
    logo_size = 24  # Size of service logo badges
    border_width = 3  # Width of colored border
    
    for idx, row in occupied_data.iterrows():
        plate_number = row['plate_number']
        service = row['service'] if pd.notna(row['service']) else 'Taxi'
        border_color = SERVICE_BORDER_COLORS.get(service, '#808080')
        
        # Convert y coordinates: image uses top-left origin, plotly uses bottom-left
        x_coord = row['x']
        y_coord = img_height - (row['y'] - VERTICAL_OFFSET)
        
        # Try to load license plate image
        if pd.notna(plate_number):
            plate_path = f'assets/plates/{plate_number}.png'
            if os.path.exists(plate_path):
                try:
                    plate_img = Image.open(plate_path)
                    # Resize plate image
                    plate_img_resized = plate_img.resize((plate_size, int(plate_img.height * plate_size / plate_img.width)), Image.Resampling.LANCZOS)
                    
                    # Create bordered plate image
                    border_size = border_width * 2
                    bordered_plate = Image.new('RGBA', 
                                               (plate_img_resized.width + border_size, 
                                                plate_img_resized.height + border_size),
                                               (0, 0, 0, 0))
                    
                    # Draw colored border
                    draw = ImageDraw.Draw(bordered_plate)
                    # Convert hex color to RGB
                    border_rgb = tuple(int(border_color[i:i+2], 16) for i in (1, 3, 5))
                    draw.rectangle([(0, 0), 
                                   (bordered_plate.width - 1, bordered_plate.height - 1)],
                                  outline=border_rgb, width=border_width)
                    
                    # Paste plate image in center
                    bordered_plate.paste(plate_img_resized, (border_width, border_width), 
                                       plate_img_resized if plate_img_resized.mode == 'RGBA' else None)
                    
                    # Convert to base64
                    plate_buffered = BytesIO()
                    bordered_plate.save(plate_buffered, format="PNG")
                    plate_str = base64.b64encode(plate_buffered.getvalue()).decode()
                    plate_data = f"data:image/png;base64,{plate_str}"
                    
                    # Calculate plate height for positioning
                    plate_height = bordered_plate.height
                    
                    # Add license plate image overlay with border
                    fig.add_layout_image(
                        dict(
                            source=plate_data,
                            xref="x",
                            yref="y",
                            x=x_coord,
                            y=y_coord,
                            sizex=bordered_plate.width,
                            sizey=plate_height,
                            sizing="stretch",
                            opacity=1.0,
                            layer="above",
                            xanchor="center",
                            yanchor="middle"
                        )
                    )
                    
                    # Add service logo badge below the plate (similar to visualize_ride_hailing.py)
                    if service in service_logos:
                        try:
                            logo = service_logos[service]
                            logo_resized = logo.copy()
                            logo_resized.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
                            
                            # Convert logo to base64
                            logo_buffered = BytesIO()
                            logo_resized.save(logo_buffered, format="PNG")
                            logo_str = base64.b64encode(logo_buffered.getvalue()).decode()
                            logo_data = f"data:image/png;base64,{logo_str}"
                            
                            # Position logo below plate (y_coord - plate_height/2 - logo_size/2 - 5)
                            logo_y = y_coord - (plate_height / 2) - (logo_size / 2) - 5
                            
                            fig.add_layout_image(
                                dict(
                                    source=logo_data,
                                    xref="x",
                                    yref="y",
                                    x=x_coord,
                                    y=logo_y,
                                    sizex=logo_size,
                                    sizey=logo_size,
                                    sizing="stretch",
                                    opacity=1.0,
                                    layer="above",
                                    xanchor="center",
                                    yanchor="middle"
                                )
                            )
                        except:
                            pass
                    
                except Exception as e:
                    # Fallback to colored dot if image fails
                    fig.add_trace(go.Scatter(
                        x=[x_coord],
                        y=[y_coord],
                        mode='markers',
                        marker=dict(
                            size=15,
                            color=SERVICE_COLORS.get(service, '#808080'),
                            line=dict(width=2, color='white')
                        ),
                        name=service,
                        showlegend=False,
                        hovertemplate=f'<b>{service}</b><br>Plate: {plate_number}<extra></extra>'
                    ))
            else:
                # Fallback to colored dot if file doesn't exist
                fig.add_trace(go.Scatter(
                    x=[x_coord],
                    y=[y_coord],
                    mode='markers',
                    marker=dict(
                        size=15,
                        color=SERVICE_COLORS.get(service, '#808080'),
                        line=dict(width=2, color='white')
                    ),
                    name=service,
                    showlegend=False,
                    hovertemplate=f'<b>{service}</b><br>Plate: {plate_number}<extra></extra>'
                ))
        else:
            # Fallback to colored dot if no plate number
            fig.add_trace(go.Scatter(
                x=[x_coord],
                y=[y_coord],
                mode='markers',
                marker=dict(
                    size=15,
                    color=SERVICE_COLORS.get(service, '#808080'),
                    line=dict(width=2, color='white')
                ),
                name=service,
                showlegend=False,
                hovertemplate=f'<b>{service}</b><extra></extra>'
            ))
    
    # Add invisible traces for legend (positioned off-screen)
    legend_services = [
        ('Uber', '#000000'),
        ('Lyft', '#FF00BF'),
        ('Waymo', '#00B4A2'),
        ('Taxi', '#F5A623')
    ]
    
    for service_name, color in legend_services:
        fig.add_trace(go.Scatter(
            x=[-1000],  # Off-screen position
            y=[-1000],
            mode='markers',
            marker=dict(
                size=10,
                color=color,
                line=dict(width=1.5, color='white')
            ),
            name=service_name,
            showlegend=True,
            hoverinfo='skip'
        ))
    
    # Configure layout with styled legend
    fig.update_layout(
        xaxis=dict(range=[0, img_width], showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(range=[0, img_height], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="x", scaleratio=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
        showlegend=True,
        legend=dict(
            title=dict(text="Service Legend", font=dict(size=12, color="black", family="Arial Black")),
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="rgba(0,0,0,0.3)",
            borderwidth=1,
            font=dict(color="black", size=11),
            x=0.02,
            y=0.98,
            xanchor='left',
            yanchor='top',
            traceorder='normal',
            itemclick='toggleothers',
            itemdoubleclick='toggle'
        )
    )
    
    return fig

# Main app
def main():
    # Load data
    df = load_data()
    timestamps = get_timestamps(df)
    
    # Debug: Print unique timestamps
    st.sidebar.write("### 🔍 Debug Info")
    st.sidebar.write(f"Unique timestamps found: {len(timestamps)}")
    if len(timestamps) > 0:
        st.sidebar.write(f"First: {timestamps[0]}")
        st.sidebar.write(f"Last: {timestamps[-1]}")
    
    # Header
    st.markdown('<div class="main-header"><h1>✈️ SKY HARBOR AIRPORT - Ride-Hailing Pickup Zone</h1></div>', unsafe_allow_html=True)
    
    # Sidebar for controls
    with st.sidebar:
        st.header("⚙️ Controls")
        
        # Auto-refresh option
        auto_refresh = st.checkbox("🔄 Auto-refresh Animation", value=False)
        refresh_interval = st.slider("Refresh Interval (seconds)", 0.5, 5.0, 2.0, 0.5) if auto_refresh else None
        
        st.markdown("---")
        st.markdown("### 📊 Data Info")
        st.write(f"Total timestamps: {len(timestamps)}")
        if len(timestamps) > 0:
            st.write(f"Date range:")
            st.write(f"{timestamps[0].strftime('%Y-%m-%d %H:%M')} to {timestamps[-1].strftime('%Y-%m-%d %H:%M')}")
    
    # Auto-refresh logic
    if auto_refresh and len(timestamps) > 0:
        time.sleep(refresh_interval)
        st.session_state.selected_time = (st.session_state.selected_time + 1) % len(timestamps)
        st.rerun()
    
    # Time slider - filter to only available timestamps
    if len(timestamps) > 0:
        st.slider(
            "⏰ Select Time",
            min_value=0,
            max_value=len(timestamps) - 1,
            key="selected_time"
        )
    else:
        st.error("No timestamps found in data!")
        return
    
    # Display selected timestamp
    current_timestamp = timestamps[st.session_state.selected_time]
    formatted_time = current_timestamp.strftime('%B %d, %Y at %I:%M %p')
    st.markdown(f"<div style='text-align: center; color: #b0b0b0; margin-bottom: 1rem;'><strong>{formatted_time}</strong></div>", unsafe_allow_html=True)
    
    # Filter data for current timestamp
    df_frame = df[df['current_time'] == current_timestamp].copy()
    stats = calculate_stats(df_frame)
    
    # Top row: Metric cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Occupancy Rate",
            value=f"{stats['occupancy_rate']:.1f}%",
            delta=None
        )
    
    with col2:
        st.metric(
            label="Available Spots",
            value=stats['vacant_count'],
            delta=None
        )
    
    with col3:
        st.metric(
            label="Total Vehicles",
            value=stats['total_vehicles'],
            delta=None
        )
    
    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
    
    # Service breakdown section
    st.markdown("### 🚗 Service Breakdown")
    
    # Calculate percentages
    total_vehicles = max(stats['total_vehicles'], 1)
    uber_count = int(stats['uber_count'])
    lyft_count = int(stats['lyft_count'])
    waymo_count = int(stats['waymo_count'])
    taxi_count = int(stats['taxi_count'])
    
    uber_pct = (uber_count / total_vehicles) * 100
    lyft_pct = (lyft_count / total_vehicles) * 100
    waymo_pct = (waymo_count / total_vehicles) * 100
    taxi_pct = (taxi_count / total_vehicles) * 100
    
    # Convert logos to base64
    try:
        uber_logo_base64 = get_base64_image("assets/logos/uber.png")
    except:
        uber_logo_base64 = ""
    try:
        lyft_logo_base64 = get_base64_image("assets/logos/lyft.png")
    except:
        lyft_logo_base64 = ""
    try:
        waymo_logo_base64 = get_base64_image("assets/logos/waymo.png")
    except:
        waymo_logo_base64 = ""
    try:
        taxi_logo_base64 = get_base64_image("assets/logos/taxi.png")
    except:
        taxi_logo_base64 = ""
    
    # Create HTML for service breakdown
    service_html = f"""
    <div style="display: flex; justify-content: space-around; align-items: flex-start; margin: 20px 0;">
        <div style="text-align: center; width: 22%;">
            <img src="data:image/png;base64,{uber_logo_base64}" style="width: 80px; height: 80px; object-fit: contain;">
            <h2 style="color: #000000; margin: 10px 0;">{uber_count}</h2>
            <div style="background: #333; border-radius: 10px; height: 20px; width: 100%;">
                <div style="background: #000000; height: 100%; width: {uber_pct}%; border-radius: 10px;"></div>
            </div>
            <p style="color: #888; margin-top: 5px;">{uber_pct:.1f}% of vehicles</p>
        </div>
        <div style="text-align: center; width: 22%;">
            <img src="data:image/png;base64,{lyft_logo_base64}" style="width: 80px; height: 80px; object-fit: contain;">
            <h2 style="color: #FF00BF; margin: 10px 0;">{lyft_count}</h2>
            <div style="background: #333; border-radius: 10px; height: 20px; width: 100%;">
                <div style="background: #FF00BF; height: 100%; width: {lyft_pct}%; border-radius: 10px;"></div>
            </div>
            <p style="color: #888; margin-top: 5px;">{lyft_pct:.1f}% of vehicles</p>
        </div>
        <div style="text-align: center; width: 22%;">
            <img src="data:image/png;base64,{waymo_logo_base64}" style="width: 80px; height: 80px; object-fit: contain;">
            <h2 style="color: #00B4A2; margin: 10px 0;">{waymo_count}</h2>
            <div style="background: #333; border-radius: 10px; height: 20px; width: 100%;">
                <div style="background: #00B4A2; height: 100%; width: {waymo_pct}%; border-radius: 10px;"></div>
            </div>
            <p style="color: #888; margin-top: 5px;">{waymo_pct:.1f}% of vehicles</p>
        </div>
        <div style="text-align: center; width: 22%;">
            <img src="data:image/png;base64,{taxi_logo_base64}" style="width: 80px; height: 80px; object-fit: contain;">
            <h2 style="color: #F5A623; margin: 10px 0;">{taxi_count}</h2>
            <div style="background: #333; border-radius: 10px; height: 20px; width: 100%;">
                <div style="background: #F5A623; height: 100%; width: {taxi_pct}%; border-radius: 10px;"></div>
            </div>
            <p style="color: #888; margin-top: 5px;">{taxi_pct:.1f}% of vehicles</p>
        </div>
    </div>
    """
    
    st.markdown(service_html, unsafe_allow_html=True)
    
    st.markdown('<div class="section-spacing"></div>', unsafe_allow_html=True)
    
    # Map section with Live Status panel
    st.markdown("### 🗺️ Parking Map")
    
    # Load map dimensions
    try:
        map_img = Image.open('assets/map.png')
        img_width, img_height = map_img.size
    except:
        img_width, img_height = 1280, 960
        st.error("Could not load map image")
        return
    
    # Create two-column layout
    map_col, panel_col = st.columns([0.7, 0.3])
    
    with map_col:
        # Create and display map
        fig = create_map_plot(df_frame, 'assets/map.png', img_width, img_height)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    
    with panel_col:
        # Generate Live Status panel HTML
        panel_html = create_live_status_panel(stats)
        st.markdown(panel_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

