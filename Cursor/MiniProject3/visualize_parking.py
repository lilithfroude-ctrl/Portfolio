import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import imageio
import os
import numpy as np
import io

# Vertical offset constant to shift elements upward on the map
# Since Y=0 is at top and increases downward, subtract to move UP
VERTICAL_OFFSET = 250

# Load data from Excel file
df = pd.read_excel('demo/ride_hailing.xlsx')

# Create status column based on reservation_id
# If reservation_id has any text or number, status is "occupied", otherwise "vacant"
df['status'] = df['reservation_id'].apply(
    lambda x: 'occupied' if pd.notna(x) and str(x).strip() != '' else 'vacant'
)

# Convert current_time column to datetime
df['current_time'] = pd.to_datetime(df['current_time'])

# Print some basic info about the data
print(f"Total rows in dataset: {len(df)}")
print(f"Date range: {df['current_time'].min()} to {df['current_time'].max()}")
print(f"Status distribution:\n{df['status'].value_counts()}")

# Get unique timestamps (minutes) for animation
unique_timestamps = sorted(df['current_time'].unique())
print(f"\nTotal unique timestamps (frames): {len(unique_timestamps)}")

# Load background image
map_file_used = None
try:
    # Try map_v3.png first, fall back to map.png if not found
    try:
        background_img = Image.open('demo/map_v3.png')
        map_file_used = 'demo/map_v3.png'
        print(f"Loaded map_v3.png")
    except FileNotFoundError:
        background_img = Image.open('demo/map.png')
        map_file_used = 'demo/map.png'
        print(f"Loaded map.png (map_v3.png not found)")
    
    # Get image dimensions to set plot extent
    img_width, img_height = background_img.size
    print(f"Background image loaded: {img_width}x{img_height} pixels from {map_file_used}")
except Exception as e:
    print(f"Warning: Could not load background image: {e}")
    background_img = None
    img_width, img_height = None, None

# Data Verification (Debug): Print coordinates and image dimensions
print("\n=== COORDINATE DEBUG ===")
print(f"Total rows in dataset: {len(df)}")
print(f"Unique slot_ids: {sorted(df['slot_id'].unique())}")

# Print coordinate ranges
print(f"\nCoordinate ranges:")
print(f"  X range: {df['x'].min():.1f} to {df['x'].max():.1f}")
print(f"  Y range: {df['y'].min():.1f} to {df['y'].max():.1f}")

# Print all unique coordinates by slot_id
print(f"\nAll coordinates by slot_id (from Excel file):")
print("  Expected: Slots 1-12 on LEFT, Slots 13-24 on RIGHT")
print("  " + "-" * 60)
for slot in sorted(df['slot_id'].unique()):
    slot_data = df[df['slot_id'] == slot].iloc[0]
    side = "LEFT" if slot <= 12 else "RIGHT"
    print(f"  Slot {slot:2d} ({side:5s}): x={slot_data['x']:7.1f}, y={slot_data['y']:7.1f}")

# Group by left/right to check X coordinate separation
left_slots = df[df['slot_id'] <= 12]
right_slots = df[df['slot_id'] > 12]
if len(left_slots) > 0 and len(right_slots) > 0:
    left_x_min, left_x_max = left_slots['x'].min(), left_slots['x'].max()
    right_x_min, right_x_max = right_slots['x'].min(), right_slots['x'].max()
    print(f"\nX coordinate separation (should show left vs right):")
    print(f"  LEFT side (slots 1-12):  x range = {left_x_min:.1f} to {left_x_max:.1f}")
    print(f"  RIGHT side (slots 13-24): x range = {right_x_min:.1f} to {right_x_max:.1f}")
    x_separation = right_x_min - left_x_max
    print(f"  Separation between sides: {x_separation:.1f} pixels")
    if abs(x_separation) < 50:
        print(f"  WARNING: Left and right sides are too close! They should be separated.")
    if left_x_max > right_x_min:
        print(f"  WARNING: Left and right X ranges overlap!")

# Print coordinates after applying VERTICAL_OFFSET
print(f"\nCoordinates after applying VERTICAL_OFFSET={VERTICAL_OFFSET}:")
for slot in sorted(df['slot_id'].unique()):
    slot_data = df[df['slot_id'] == slot].iloc[0]
    adjusted_y = slot_data['y'] - VERTICAL_OFFSET
    print(f"  Slot {slot:2d}: x={slot_data['x']:7.1f}, y={adjusted_y:7.1f} (original y={slot_data['y']:7.1f})")

if background_img is not None:
    print(f"\nMap image dimensions:")
    print(f"  img_width: {img_width}")
    print(f"  img_height: {img_height}")
    print(f"  Image aspect ratio: {img_width/img_height:.2f}")
    
    # Check if coordinates are within image bounds
    print(f"\nCoordinate bounds check:")
    x_min, x_max = df['x'].min(), df['x'].max()
    y_min, y_max = df['y'].min(), df['y'].max()
    y_min_adj, y_max_adj = y_min - VERTICAL_OFFSET, y_max - VERTICAL_OFFSET
    print(f"  X coordinates: {x_min:.1f} to {x_max:.1f} (image width: 0 to {img_width})")
    print(f"  Y coordinates (original): {y_min:.1f} to {y_max:.1f} (image height: 0 to {img_height})")
    print(f"  Y coordinates (adjusted): {y_min_adj:.1f} to {y_max_adj:.1f} (image height: 0 to {img_height})")
    if x_min < 0 or x_max > img_width:
        print(f"  WARNING: X coordinates out of bounds!")
    if y_min_adj < 0 or y_max_adj > img_height:
        print(f"  WARNING: Adjusted Y coordinates out of bounds!")
    
    # Analyze Y coordinate distribution to suggest VERTICAL_OFFSET
    print(f"\nVERTICAL_OFFSET analysis:")
    print(f"  Current VERTICAL_OFFSET: {VERTICAL_OFFSET}")
    print(f"  Y coordinate center (original): {(y_min + y_max) / 2:.1f}")
    print(f"  Y coordinate center (adjusted): {(y_min_adj + y_max_adj) / 2:.1f}")
    print(f"  Image center Y: {img_height / 2:.1f}")
    
    # Calculate what offset would center the Y coordinates in the image
    y_center_original = (y_min + y_max) / 2
    suggested_offset = y_center_original - (img_height / 2)
    print(f"  Suggested VERTICAL_OFFSET to center Y: {suggested_offset:.1f}")
    
    # Check Y coordinate spread
    y_spread = y_max - y_min
    print(f"  Y coordinate spread: {y_spread:.1f} pixels")
    if y_spread < 100:
        print(f"  WARNING: Y coordinates are very close together (spread < 100px)")
        print(f"           This might cause spots to appear bunched vertically.")
    
    # Check X coordinate spread
    x_spread = x_max - x_min
    print(f"  X coordinate spread: {x_spread:.1f} pixels")
    if x_spread < 100:
        print(f"  WARNING: X coordinates are very close together (spread < 100px)")
        print(f"           This might cause spots to appear bunched horizontally.")
else:
    print("\nWARNING: Background image not loaded!")

print("=" * 60)
print("\nDEBUGGING SUMMARY:")
print("  If spots are bunched together, check:")
print("  1. X coordinate spread - should show clear left/right separation")
print("  2. Y coordinate spread - should be distributed vertically")
print("  3. VERTICAL_OFFSET value - may need adjustment for this map")
print("  4. Compare coordinates with visualize_ride_hailing.py output")
print("  5. Verify map file dimensions match expected layout")
print("=" * 60 + "\n")

# Function to create a frame for a given timestamp
def create_frame(timestamp):
    """Create a single frame for the animation at the given timestamp."""
    # Filter data for this timestamp
    df_frame = df[df['current_time'] == timestamp].copy()
    
    # Create figure
    fig, ax = plt.subplots(figsize=(16, 12))
    
    # Set background image if available
    if background_img is not None:
        # Use extent=[0, width, height, 0] to match image coordinate system (0,0 at top-left)
        # origin='upper' ensures (0,0) is at top-left, matching standard image coordinates
        ax.imshow(background_img, extent=[0, img_width, img_height, 0], 
                  aspect='auto', alpha=0.8, zorder=0, origin='upper')
    
    # Plot vacant spots in gray
    vacant_data = df_frame[df_frame['status'] == 'vacant']
    if len(vacant_data) > 0:
        ax.scatter(vacant_data['x'], vacant_data['y'] - VERTICAL_OFFSET, 
                   c='gray', label='Vacant', alpha=0.8, s=100, zorder=2, 
                   edgecolors='darkgray', linewidths=1)
    
    # Plot occupied spots with license plate images
    occupied_data = df_frame[df_frame['status'] == 'occupied']
    if len(occupied_data) > 0:
        for idx, row in occupied_data.iterrows():
            plate_number = row['plate_number']
            if pd.notna(plate_number):
                plate_path = f'demo/plates/{plate_number}.png'
                if os.path.exists(plate_path):
                    try:
                        # Load license plate image
                        plate_img = Image.open(plate_path)
                        # Resize to appropriate size (adjust zoom factor as needed)
                        zoom_factor = 0.15  # Adjust this to change plate size
                        plate_img_resized = plate_img.resize(
                            (int(plate_img.width * zoom_factor), 
                             int(plate_img.height * zoom_factor)),
                            Image.Resampling.LANCZOS
                        )
                        
                        # Create OffsetImage for annotation
                        imagebox = OffsetImage(plate_img_resized, zoom=1.0)
                        
                        # Create AnnotationBbox to place image at coordinates
                        # Apply vertical offset to shift upward (subtract since Y increases downward)
                        ab = AnnotationBbox(imagebox, (row['x'], row['y'] - VERTICAL_OFFSET), 
                                          frameon=False, box_alignment=(0.5, 0.5))
                        ax.add_artist(ab)
                    except Exception as e:
                        print(f"Warning: Could not load plate image {plate_path}: {e}")
                        # Fallback to red dot if image fails
                        ax.scatter(row['x'], row['y'] - VERTICAL_OFFSET, c='red', s=100, 
                                 zorder=2, edgecolors='darkred', linewidths=1)
                else:
                    # Fallback to red dot if image file doesn't exist
                    ax.scatter(row['x'], row['y'] - VERTICAL_OFFSET, c='red', s=100, 
                             zorder=2, edgecolors='darkred', linewidths=1)
            else:
                # Fallback to red dot if no plate number
                ax.scatter(row['x'], row['y'] - VERTICAL_OFFSET, c='red', s=100, 
                         zorder=2, edgecolors='darkred', linewidths=1)
    
    # Remove white background and grid
    ax.set_facecolor('none')
    fig.patch.set_facecolor('white')
    
    # Hide x and y axis numbers and ticks
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    
    # Remove axis spines
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Set fixed axis limits to match full image dimensions for 1:1 coordinate mapping
    # Note: Y-axis is inverted (img_height to 0) to match image coordinate system (0,0 at top-left)
    if background_img is not None:
        ax.set_xlim(0, img_width)
        ax.set_ylim(img_height, 0)  # Inverted Y-axis: height to 0 (top to bottom)
    else:
        # Fallback: should not happen if image loaded correctly
        print("Warning: No background image available, using data ranges")
        x_min, x_max = df['x'].min(), df['x'].max()
        y_min, y_max = df['y'].min(), df['y'].max()
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_max, y_min)  # Invert Y for consistency
    
    # Add informative title with date and time
    formatted_time = pd.to_datetime(timestamp).strftime('%B %d, %Y at %I:%M %p')
    ax.set_title(f'Parking Status - {formatted_time}', 
                 fontsize=18, fontweight='bold', pad=20)
    
    # Add legend
    ax.legend(loc='upper right', fontsize=12, framealpha=0.9, 
              facecolor='white', edgecolor='black', fancybox=True)
    
    plt.tight_layout()
    
    # Convert figure to numpy array for imageio with fixed dimensions
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', 
                facecolor='white', pad_inches=0.1)
    buf.seek(0)
    frame = imageio.v2.imread(buf)
    buf.close()
    
    plt.close(fig)
    return frame

# Generate all frames
print("\nGenerating animation frames...")
frames = []
for i, timestamp in enumerate(unique_timestamps):
    if (i + 1) % 10 == 0 or i == 0:
        print(f"Processing frame {i + 1}/{len(unique_timestamps)}: {timestamp}")
    frame = create_frame(timestamp)
    frames.append(frame)

# Ensure all frames have the same dimensions
print("\nStandardizing frame dimensions...")
if len(frames) > 0:
    # Get target dimensions from first frame
    target_shape = frames[0].shape
    standardized_frames = []
    for i, frame in enumerate(frames):
        if frame.shape != target_shape:
            # Resize frame to match target dimensions
            from PIL import Image as PILImage
            pil_frame = PILImage.fromarray(frame)
            pil_frame = pil_frame.resize((target_shape[1], target_shape[0]), PILImage.Resampling.LANCZOS)
            frame = np.array(pil_frame)
        standardized_frames.append(frame)
    frames = standardized_frames

# Create GIF with 2 seconds per frame
print(f"\nCreating GIF with {len(frames)} frames (2 seconds per frame)...")
# Duration is in seconds per frame
imageio.v2.mimsave('parking_animation.gif', frames, duration=2.0, loop=0)
print("Animation saved as 'parking_animation.gif'")
