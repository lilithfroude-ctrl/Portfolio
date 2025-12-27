"""
Sky Harbor Airport Ride-Hailing Dashboard
Mini Project 3 - CIS 541

New Features Implemented:
1. SERVICE COLOR CODING & LOGOS: Color-coded borders with brand logos for Uber, Lyft, 
   Waymo, and Taxi services so passengers can quickly identify their ride.
2. REAL-TIME STATISTICS PANEL: Dashboard panel with logos showing occupancy rate, 
   available spots, and breakdown by service type.

Author: Lilith Froude
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
from PIL import Image
import imageio
import os
import numpy as np
import io

# ============================================================================
# CONFIGURATION
# ============================================================================

# Vertical offset to align elements with parking map
VERTICAL_OFFSET = 30

# Service brand colors
SERVICE_COLORS = {
    'Uber': {'primary': '#000000', 'secondary': '#276EF1'},
    'Lyft': {'primary': '#FF00BF', 'secondary': '#352384'},
    'Waymo': {'primary': '#00B4A2', 'secondary': '#008B7A'},
    'Taxi': {'primary': '#F5A623', 'secondary': '#FFD700'}
}

# Logo file paths
LOGO_PATHS = {
    'Uber': 'assets/logos/uber.png',
    'Lyft': 'assets/logos/lyft.png',
    'Waymo': 'assets/logos/waymo.png',
    'Taxi': 'assets/logos/taxi.png'
}

# Default color for vacant spots
VACANT_COLOR = '#808080'

# ============================================================================
# DATA LOADING
# ============================================================================

# Load data from Excel file
df = pd.read_excel('assets/ride_hailing.xlsx')

# Split "Other" service entries: half to "Waymo", half to "Taxi"
other_mask = df['service'] == 'Other'
other_indices = df[other_mask].index.tolist()
if len(other_indices) > 0:
    half_point = len(other_indices) // 2
    # Change first half to "Waymo"
    for idx in other_indices[:half_point]:
        df.at[idx, 'service'] = 'Waymo'
    # Change second half to "Taxi"
    for idx in other_indices[half_point:]:
        df.at[idx, 'service'] = 'Taxi'
    # Save updated data back to Excel
    df.to_excel('assets/ride_hailing.xlsx', index=False)
    print(f"Updated {len(other_indices)} 'Other' entries: {half_point} to Waymo, {len(other_indices) - half_point} to Taxi")

# Create status column based on reservation_id
df['status'] = df['reservation_id'].apply(
    lambda x: 'occupied' if pd.notna(x) and str(x).strip() != '' else 'vacant'
)

# Convert current_time column to datetime
df['current_time'] = pd.to_datetime(df['current_time'])

# Print data summary
print(f"{'='*60}")
print(f"SKY HARBOR RIDE-HAILING DASHBOARD - Data Summary")
print(f"{'='*60}")
print(f"Total data points: {len(df)}")
print(f"Date range: {df['current_time'].min()} to {df['current_time'].max()}")
print(f"\nService distribution (occupied spots):")
service_counts = df[df['status'] == 'occupied']['service'].value_counts()
for service, count in service_counts.items():
    print(f"  {service}: {count}")
print(f"{'='*60}\n")

# Get unique timestamps for animation frames
unique_timestamps = sorted(df['current_time'].unique())
print(f"Total animation frames: {len(unique_timestamps)}")

# Load background image
try:
    background_img = Image.open('assets/map.png')
    img_width, img_height = background_img.size
    print(f"Background loaded: {img_width}x{img_height} pixels")
except Exception as e:
    print(f"Error loading background: {e}")
    background_img = None
    img_width, img_height = 1280, 960

# Load service logos
service_logos = {}
for service, path in LOGO_PATHS.items():
    try:
        logo = Image.open(path)
        # Convert to RGBA if needed
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        service_logos[service] = logo
        print(f"Loaded logo: {service}")
    except Exception as e:
        print(f"Warning: Could not load {service} logo: {e}")
        service_logos[service] = None

# ============================================================================
# STATISTICS CALCULATOR
# ============================================================================

def calculate_statistics(df_frame):
    """Calculate real-time statistics for the dashboard panel."""
    total_spots = 24
    
    occupied = df_frame[df_frame['status'] == 'occupied']
    vacant = df_frame[df_frame['status'] == 'vacant']
    
    stats = {
        'total_spots': total_spots,
        'occupied_count': len(occupied),
        'vacant_count': len(vacant),
        'occupancy_rate': (len(occupied) / total_spots) * 100 if total_spots > 0 else 0,
        'uber_count': len(occupied[occupied['service'] == 'Uber']),
        'lyft_count': len(occupied[occupied['service'] == 'Lyft']),
        'waymo_count': len(occupied[occupied['service'] == 'Waymo']),
        'taxi_count': len(occupied[occupied['service'] == 'Taxi'])
    }
    return stats

# ============================================================================
# STATISTICS PANEL WITH LOGOS
# ============================================================================

def draw_statistics_panel(ax, stats, img_width, img_height):
    """Draw the real-time statistics panel with service logos."""
    
    # Panel position and size
    panel_x = img_width - 290
    panel_y = 120
    panel_width = 270
    panel_height = 480
    
    # Draw panel background with shadow effect
    shadow = FancyBboxPatch(
        (panel_x + 4, panel_y + 4), panel_width, panel_height,
        boxstyle="round,pad=0.02,rounding_size=15",
        facecolor='#333333', edgecolor='none', alpha=0.3, zorder=9
    )
    ax.add_patch(shadow)
    
    panel_bg = FancyBboxPatch(
        (panel_x, panel_y), panel_width, panel_height,
        boxstyle="round,pad=0.02,rounding_size=15",
        facecolor='#f0f0f0', edgecolor='#2c3e50', linewidth=2,
        alpha=0.97, zorder=10
    )
    ax.add_patch(panel_bg)
    
    # Panel header bar
    header_bg = FancyBboxPatch(
        (panel_x, panel_y), panel_width, 45,
        boxstyle="round,pad=0.02,rounding_size=15",
        facecolor='#2c3e50', edgecolor='none', zorder=11
    )
    ax.add_patch(header_bg)
    
    # Panel title
    ax.text(panel_x + panel_width/2, panel_y + 25, 
            'LIVE STATUS', 
            fontsize=14, fontweight='bold', ha='center', va='center',
            color='white', zorder=12)
    
    # Occupancy rate section
    rate = stats['occupancy_rate']
    rate_color = '#27ae60' if rate < 50 else '#f39c12' if rate < 80 else '#e74c3c'
    
    ax.text(panel_x + panel_width/2, panel_y + 85,
            f"{rate:.0f}%", 
            fontsize=32, fontweight='bold', ha='center', va='center',
            color=rate_color, zorder=12)
    ax.text(panel_x + panel_width/2, panel_y + 115,
            'OCCUPANCY', 
            fontsize=9, ha='center', va='center',
            color='#7f8c8d', fontweight='bold', zorder=12)
    
    # Available spots
    ax.text(panel_x + panel_width/2, panel_y + 160,
            f"{stats['vacant_count']}", 
            fontsize=40, fontweight='bold', ha='center', va='center',
            color='#27ae60', zorder=12)
    ax.text(panel_x + panel_width/2, panel_y + 198,
            'SPOTS AVAILABLE', 
            fontsize=9, ha='center', va='center',
            color='#7f8c8d', fontweight='bold', zorder=12)
    
    # Divider line
    ax.plot([panel_x + 20, panel_x + panel_width - 20], 
            [panel_y + 220, panel_y + 220], 
            color='#ecf0f1', linewidth=2, zorder=12)
    
    # Service breakdown title
    ax.text(panel_x + panel_width/2, panel_y + 245,
            'BY SERVICE', 
            fontsize=10, fontweight='bold', ha='center', va='center',
            color='#2c3e50', zorder=12)
    
    # Service breakdown with logos
    services = [
        ('Uber', stats['uber_count'], SERVICE_COLORS['Uber']['primary']),
        ('Lyft', stats['lyft_count'], SERVICE_COLORS['Lyft']['primary']),
        ('Waymo', stats['waymo_count'], SERVICE_COLORS['Waymo']['primary']),
        ('Taxi', stats['taxi_count'], SERVICE_COLORS['Taxi']['primary'])
    ]
    
    y_offset = 270
    bar_max_width = 130
    max_count = max(s[1] for s in services) if max(s[1] for s in services) > 0 else 1
    
    for service_name, count, color in services:
        # Draw logo if available
        logo = service_logos.get(service_name)
        if logo is not None:
            try:
                # Resize logo to fit
                logo_size = 28
                logo_resized = logo.copy()
                logo_resized.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
                
                imagebox = OffsetImage(np.array(logo_resized), zoom=1.0)
                ab = AnnotationBbox(imagebox, 
                                   (panel_x + 35, panel_y + y_offset + 8),
                                   frameon=False, box_alignment=(0.5, 0.5),
                                   zorder=13)
                ax.add_artist(ab)
            except Exception as e:
                # Fallback: just show text
                ax.text(panel_x + 35, panel_y + y_offset + 8,
                       service_name[0], fontsize=12, fontweight='bold',
                       ha='center', va='center', color=color, zorder=13)
        
        # Count on the right
        ax.text(panel_x + panel_width - 25, panel_y + y_offset + 8,
                str(count), 
                fontsize=14, fontweight='bold', ha='right', va='center',
                color=color, zorder=12)
        
        # Progress bar background
        bar_x = panel_x + 60
        bar_bg = FancyBboxPatch(
            (bar_x, panel_y + y_offset + 20), bar_max_width, 10,
            boxstyle="round,pad=0.01,rounding_size=5",
            facecolor='#ecf0f1', edgecolor='none', zorder=11
        )
        ax.add_patch(bar_bg)
        
        # Progress bar fill
        bar_width = (count / max_count) * bar_max_width if count > 0 else 0
        if bar_width > 0:
            bar_fill = FancyBboxPatch(
                (bar_x, panel_y + y_offset + 20), max(bar_width, 5), 10,
                boxstyle="round,pad=0.01,rounding_size=5",
                facecolor=color, edgecolor='none', alpha=0.85, zorder=12
            )
            ax.add_patch(bar_fill)
        
        y_offset += 48

# ============================================================================
# SERVICE BADGE RENDERER
# ============================================================================

def draw_service_badge(ax, x, y, service):
    """Draw a small service logo badge below the license plate."""
    logo = service_logos.get(service)
    color_info = SERVICE_COLORS.get(service, SERVICE_COLORS['Taxi'])
    
    if logo is not None:
        try:
            logo_size = 24
            logo_resized = logo.copy()
            logo_resized.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)
            
            imagebox = OffsetImage(np.array(logo_resized), zoom=1.0)
            ab = AnnotationBbox(imagebox, (x, y + 38),
                               frameon=False, box_alignment=(0.5, 0.5),
                               zorder=5)
            ax.add_artist(ab)
        except:
            # Fallback to colored dot
            ax.scatter(x, y + 35, c=color_info['primary'], s=80, 
                      zorder=5, edgecolors='white', linewidths=1.5)
    else:
        ax.scatter(x, y + 35, c=color_info['primary'], s=80, 
                  zorder=5, edgecolors='white', linewidths=1.5)

# ============================================================================
# MAIN FRAME CREATION
# ============================================================================

def create_frame(timestamp):
    """Create a single frame for the animation at the given timestamp."""
    
    # Filter data for this timestamp
    df_frame = df[df['current_time'] == timestamp].copy()
    
    # Calculate statistics
    stats = calculate_statistics(df_frame)
    
    # Create figure
    fig, ax = plt.subplots(figsize=(18, 12))
    
    # Draw background image
    if background_img is not None:
        ax.imshow(background_img, extent=[0, img_width, img_height, 0], 
                  aspect='auto', alpha=0.85, zorder=0, origin='upper')
    
    # Process vacant spots
    vacant_data = df_frame[df_frame['status'] == 'vacant']
    if len(vacant_data) > 0:
        ax.scatter(vacant_data['x'], vacant_data['y'] - VERTICAL_OFFSET, 
                   c=VACANT_COLOR, s=120, zorder=2, 
                   edgecolors='#4a4a4a', linewidths=1.5, alpha=0.7)
    
    # Process occupied spots
    occupied_data = df_frame[df_frame['status'] == 'occupied']
    services_shown = set()
    
    for idx, row in occupied_data.iterrows():
        x, y = row['x'], row['y'] - VERTICAL_OFFSET
        plate_number = row['plate_number']
        service = row['service'] if pd.notna(row['service']) else 'Taxi'
        color_info = SERVICE_COLORS.get(service, SERVICE_COLORS['Taxi'])
        
        services_shown.add(service)
        
        # Try to load license plate image
        plate_loaded = False
        if pd.notna(plate_number):
            plate_path = f'assets/plates/{plate_number}.png'
            if os.path.exists(plate_path):
                try:
                    plate_img = Image.open(plate_path)
                    zoom_factor = 0.15
                    plate_img_resized = plate_img.resize(
                        (int(plate_img.width * zoom_factor), 
                         int(plate_img.height * zoom_factor)),
                        Image.Resampling.LANCZOS
                    )
                    
                    imagebox = OffsetImage(plate_img_resized, zoom=1.0)
                    ab = AnnotationBbox(imagebox, (x, y), 
                                       frameon=True, 
                                       bboxprops=dict(
                                           facecolor='white',
                                           edgecolor=color_info['primary'],
                                           linewidth=3,
                                           boxstyle='round,pad=0.1'
                                       ),
                                       box_alignment=(0.5, 0.5))
                    ax.add_artist(ab)
                    plate_loaded = True
                    
                    # Draw service logo badge
                    draw_service_badge(ax, x, y, service)
                    
                except Exception as e:
                    pass
        
        # Fallback: colored dot
        if not plate_loaded:
            ax.scatter(x, y, c=color_info['primary'], s=200, 
                      zorder=3, edgecolors='white', linewidths=2)
    
    # Draw statistics panel
    draw_statistics_panel(ax, stats, img_width, img_height)
    
    # Configure axes
    ax.set_facecolor('none')
    fig.patch.set_facecolor('#f5f6fa')
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Set axis limits
    if background_img is not None:
        ax.set_xlim(0, img_width)
        ax.set_ylim(img_height, 0)
    
    # Title
    formatted_time = pd.to_datetime(timestamp).strftime('%B %d, %Y  |  %I:%M %p')
    ax.set_title(
        f'SKY HARBOR AIRPORT  -  Ride-Hailing Pickup Zone\n{formatted_time}', 
        fontsize=16, fontweight='bold', pad=20, 
        color='#2c3e50', loc='center'
    )
    
    # Create legend with logos
    legend_elements = []
    
    for service in ['Uber', 'Lyft', 'Waymo', 'Taxi']:
        if service in services_shown:
            legend_elements.append(
                Line2D([0], [0], marker='o', color='w',
                      markerfacecolor=SERVICE_COLORS[service]['primary'],
                      markersize=10, label=service,
                      markeredgecolor='white', markeredgewidth=1.5)
            )
    
    ax.legend(handles=legend_elements, loc='upper left', fontsize=10, 
              framealpha=0.95, facecolor='white', edgecolor='#2c3e50',
              title='Service Legend', title_fontsize=11)
    
    plt.tight_layout()
    
    # Convert to image array
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', 
                facecolor='#f5f6fa', pad_inches=0.1)
    buf.seek(0)
    frame = imageio.v2.imread(buf)
    buf.close()
    plt.close(fig)
    
    return frame

# ============================================================================
# GENERATE OUTPUTS
# ============================================================================

def generate_static_preview():
    """Generate a single static preview image."""
    print("\nGenerating static preview...")
    timestamp = unique_timestamps[0]
    frame = create_frame(timestamp)
    imageio.v2.imwrite('ride_hailing_preview.png', frame)
    print("Static preview saved: ride_hailing_preview.png")
    return frame

def generate_animation():
    """Generate the full animation GIF."""
    print(f"\nGenerating animation ({len(unique_timestamps)} frames)...")
    
    frames = []
    for i, timestamp in enumerate(unique_timestamps):
        if (i + 1) % 10 == 0 or i == 0:
            print(f"  Frame {i + 1}/{len(unique_timestamps)}")
        frame = create_frame(timestamp)
        frames.append(frame)
    
    # Standardize frame dimensions
    if len(frames) > 0:
        target_shape = frames[0].shape
        standardized_frames = []
        for frame in frames:
            if frame.shape != target_shape:
                pil_frame = Image.fromarray(frame)
                pil_frame = pil_frame.resize(
                    (target_shape[1], target_shape[0]), 
                    Image.Resampling.LANCZOS
                )
                frame = np.array(pil_frame)
            standardized_frames.append(frame)
        frames = standardized_frames
    
    print(f"\nSaving animation...")
    imageio.v2.mimsave('ride_hailing_animation.gif', frames, duration=2.0, loop=0)
    print("Animation saved: ride_hailing_animation.gif")

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*60)
    print("SKY HARBOR RIDE-HAILING DASHBOARD")
    print("="*60)
    print("\nFeatures:")
    print("  1. Service Color Coding with Brand Logos")
    print("  2. Real-Time Statistics Panel")
    print("="*60)
    
    generate_static_preview()
    generate_animation()
    
    print("\n" + "="*60)
    print("COMPLETE!")
    print("="*60)
    print("\nOutput files:")
    print("  - ride_hailing_preview.png")
    print("  - ride_hailing_animation.gif")
    print("="*60 + "\n")
