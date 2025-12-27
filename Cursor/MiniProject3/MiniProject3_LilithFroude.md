# Mini Project 3 - Sky Harbor Airport Ride-Hailing Dashboard

**Authors:** Lilith Froude, Nani Batchu, Dennis Noll

**Course:** CIS 541 - Data Visualization with Tableau

**Date:** December 2025

---

## Q1: Justify your new design features (Why did you choose this layout/logic?)

**Answer:** We implemented two main features for the Sky Harbor Airport Ride-Hailing Dashboard:

1. **Service Color Coding with Brand Logos** - We added visual identification for four ride services: Uber (black), Lyft (pink), Waymo (teal), and Taxi (orange). Each vehicle displays its license plate with a color-coded border and the service logo beneath it. This helps passengers instantly locate their booked ride from across the pickup zone without needing to read individual license plates.

2. **Real-Time Statistics Panel** - We created a live dashboard panel showing occupancy percentage (color-coded green/yellow/red based on congestion), available spots count, and a breakdown by service with progress bars. This provides at-a-glance information for both passengers (to know if the zone is busy) and airport operations staff (to monitor utilization patterns).

3. **Interactive Streamlit Dashboard** - We built a web-based dashboard using Streamlit that allows users to scrub through timestamps with a slider, view real-time statistics, and see the parking map update dynamically. This adds interactivity beyond the static animation.

---

## Q2: Describe your experience of Mini Project 3. Reflect on using Cursor and GitHub during implementation.

**Answer:** Working with Cursor significantly accelerated our development process. The AI assistant helped us debug coordinate alignment issues (adjusting VERTICAL_OFFSET to position license plates correctly on the map), generate complex matplotlib visualizations, and build an interactive Streamlit dashboard from scratch. The file explorer made managing assets (logos, plates, data files) intuitive and organized.

Using GitHub with feature branches allowed us to work independently without affecting each other's code. The git integration in Cursor made committing and pushing changes seamless. We learned to commit frequently after each working feature, which made it easy to track progress and revert if needed.

The combination of AI-assisted coding and version control created an efficient workflow where we could experiment freely knowing we could always roll back changes.

---

## Q3: Weigh the pros and cons of using Cursor & GitHub for your work projects.

### PROS:

- Cursor's AI dramatically speeds up coding, debugging, and learning new libraries
- Real-time suggestions help discover better approaches and best practices
- GitHub branching prevents merge conflicts when collaborating with teammates
- Version control provides safety net to experiment and revert mistakes
- Integrated terminal and file management keeps everything in one place
- AI can explain unfamiliar code and suggest improvements

### CONS:

- Initial learning curve for git commands and workflow
- AI suggestions require review - not always perfect or optimal
- Dependency on internet connection for AI features
- Can be overwhelming for users new to IDEs
- Over-reliance on AI may slow down learning fundamentals
- Merge conflicts still possible if branch discipline isn't followed

