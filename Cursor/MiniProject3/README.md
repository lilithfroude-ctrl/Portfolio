# Sky Harbor Airport - Ride-Hailing Dashboard

## CIS 541 Mini Project 3

### Project Overview

An interactive visualization dashboard for Phoenix Sky Harbor Airport's ride-hailing pickup zone, displaying real-time vehicle occupancy, service distribution, and parking spot status.

### Features

1. **Service Color Coding** - Visual identification for Uber, Lyft, Waymo, and Taxi with brand logos and color-coded borders

2. **Real-Time Statistics Panel** - Live occupancy rate, available spots, and service breakdown with progress bars

3. **Interactive Web Dashboard** - Streamlit-based UI with time slider to scrub through data

4. **Animated Visualization** - 60-frame GIF showing parking zone activity over time

### Tech Stack

- Python 3
- Pandas (data processing)
- Matplotlib (static visualization)
- Streamlit (interactive dashboard)
- Plotly (interactive charts)
- Pillow & ImageIO (image processing)

### Project Structure

```
MiniProject3/
├── assets/
│   ├── logos/          # Service brand logos
│   ├── plates/         # License plate images
│   ├── map.png         # Background parking lot map
│   └── ride_hailing.xlsx  # Source data
├── dashboard.py        # Streamlit interactive dashboard
├── visualize_ride_hailing.py  # Static visualization & animation generator
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

### Installation

```bash
pip install -r requirements.txt
```

### Usage

**Run Interactive Dashboard:**

```bash
streamlit run dashboard.py
```

**Generate Static Visualization & Animation:**

```bash
python visualize_ride_hailing.py
```

### Output Files

- `ride_hailing_preview.png` - Static dashboard preview
- `ride_hailing_animation.gif` - Animated visualization (60 frames)

### Authors

- Lilith Froude
- Nani Batchu
- Dennis Noll

Arizona State University

### Course

CIS 541 - Data Visualization with Tableau
