"""---------------------------Packages-----------------------------------"""
import math as m
import random as rdm
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
"""---------------------------Inital Inputs-----------------------------------"""
# Max Detection Distance: 
z = 5000 #ft

# Factor of Safety
FoS = 1.5

# Fog Factor
fog = 0.5

# With Factor of Safety and fog
ztrue = z / FoS * fog

# Field of View (FOV): 
θ = 120 #degrees

# In Radians
θr = θ * m.pi / 180

# Search Height AGL: 
H = 470 #ft

# Search Velocity: 
Vs = 55 #mph

# Search Radius: 
r = 1 #mile

# Hiker Search Area: 
A = r**2 * m.pi #3.1415926535 mile^2

# Overlap Factor
over = 0.5

"""--------------------------Algorithm---------------------------------------""" 
# Effective Detection Sweep Width
d1 = 2 * H * m.tan(θr/2) #ft

# Search Flight Distance 
d2 = (A*(5280**2)) / (d1 * (1-over)) #ft

# Flight time
ts = d2 / (Vs*5280) #hr

"""--------------------------Print Calculations and Results------------------------------------------"""
# Print out the result
print(f"Max Detection Distance: {z} ft")
print(f"Factor of Safety: {FoS}")
print(f"Fog Factor: {fog}")
print(f"Expected Detection Distance Considering Conditions: {ztrue:.2f} ft")
print(f"Field of View (FOV): {θ} degrees or {θr:.2f} radians")
print(f"Search Height AGL: {H} ft")
print(f"Search Velocity: {Vs} mile/hr")
print(f"Search Radius: {r} mile")
print(f"Hiker Search Area: {A:.2f} mile^2")
print(f"Overlap Factor: {over}")
print(f"Effective Detection Sweep Width: {d1:.2f} ft")
print(f"Search Flight Distance: {d2:.2f} ft")
print(f"Flight Time: {ts:.2f} hrs")

# Check if hiker found in worst case 
if ts <= 0.5: 
    print("Hiker Found, even in Worst Case!")
else: 
    print("Hiker not Found. :(")

"""----------Randonmized Trials----------"""
# Print for Formatting
print("----------Randomized Hiker Search and Rescue Trials----------")
# Randomized Trials
times = np.zeros((1,100))
for i in range(100):
    random_d2 = rdm.randint(0, m.ceil(d2)) # Random from 0 to worst case flight distance
    random_ts =  random_d2 / (Vs*5280) #hr
    # Print the trial results
    # print(f"Trial {i+1}:")
    # print(f"Hiker Location on Search Path: {random_d2}")
    # print(f"Flight Time: {random_ts:.2f} hrs")
    times[0][i] = round(random_ts, 2) # Add trial to data numpy array

print("After 100 trials:")
# Print final results
mean_time = np.mean(times)
std_time = np.std(times)
print(f"Average Search Time: {mean_time:.2f} hrs")
print(f"Median Search Time: {np.median(times):.2f} hrs")

# Create bar graph
median_time = np.median(times)
plt.figure(figsize=(10, 6))

# Plot bar graph
plt.hist(times.flatten(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')

# Add vertical lines for mean and median
plt.axvline(mean_time, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_time:.2f} hrs')
plt.axvline(median_time, color='green', linestyle='--', linewidth=2, label=f'Median: {median_time:.2f} hrs')

plt.xlabel('Search Time (hours)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Distribution of Search Times', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3, axis='y')
plt.legend()
plt.tight_layout()
plt.show()


"""----------Drone Flight Simulation----------"""
import matplotlib.animation as animation

print("\n----------Drone Flight Simulation----------")

# Generate search pattern (parallel tracks)
sweep_width_miles = d1 / 5280  # Convert to miles
effective_spacing = sweep_width_miles * (1 - over)  # Account for overlap
num_tracks = int(np.ceil(2 * r / effective_spacing))

print(f"Sweep width: {sweep_width_miles:.4f} miles ({d1:.2f} ft)")
print(f"Effective spacing (with {over*100}% overlap): {effective_spacing:.4f} miles")
print(f"Number of tracks: {num_tracks}")

# Create search path
path_x = []
path_y = []
for track in range(num_tracks):
    y_pos = -r + track * effective_spacing
    if track % 2 == 0:  # Left to right
        path_x.extend([-r, r])
        path_y.extend([y_pos, y_pos])
    else:  # Right to left
        path_x.extend([r, -r])
        path_y.extend([y_pos, y_pos])

# Place hiker randomly in search area
hiker_angle = rdm.uniform(0, 2 * m.pi)
hiker_dist = rdm.uniform(0, r)
hiker_x = hiker_dist * m.cos(hiker_angle)
hiker_y = hiker_dist * m.sin(hiker_angle)

# Calculate when drone finds hiker
total_path_distance = 0
found_distance = None
for i in range(0, len(path_x)-1):
    segment_dist = m.sqrt((path_x[i+1] - path_x[i])**2 + (path_y[i+1] - path_y[i])**2)
    # Check if hiker is within sweep width of this segment
    if found_distance is None:
        # Simple check: is hiker close to this y-coordinate?
        if abs(path_y[i] - hiker_y) <= sweep_width_miles / 2:
            # Found the hiker on this track
            found_distance = total_path_distance + abs(path_x[i] - hiker_x)
    total_path_distance += segment_dist

if found_distance is None:
    found_distance = total_path_distance

time_to_find = (found_distance * 5280) / (Vs * 5280)  # Convert to hours

print(f"Hiker located at: ({hiker_x:.2f}, {hiker_y:.2f}) miles")
print(f"Time to find hiker: {time_to_find:.2f} hours")

# Create animation
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-r * 1.1, r * 1.1)
ax.set_ylim(-r * 1.1, r * 1.1)
ax.set_aspect('equal')

# Draw search area circle
circle = plt.Circle((0, 0), r, fill=False, color='gray', linestyle='--', linewidth=2)
ax.add_patch(circle)

# Plot hiker
ax.plot(hiker_x, hiker_y, 'ro', markersize=15, label='Hiker', zorder=5)

# Plot search path with sweep width visualization
ax.plot(path_x, path_y, 'b-', alpha=0.5, linewidth=2, label='Search Path')

# Draw sweep width rectangles for each track to show coverage and overlap
for track in range(num_tracks):
    y_pos = -r + track * effective_spacing
    rect = plt.Rectangle((-r, y_pos - sweep_width_miles/2), 2*r, sweep_width_miles, 
                         fill=True, color='blue', alpha=0.1, edgecolor='blue', linewidth=0.5)
    ax.add_patch(rect)

# Drone marker
drone, = ax.plot([], [], 'g^', markersize=20, label='Drone', zorder=10)
trail, = ax.plot([], [], 'g-', alpha=0.5, linewidth=2)

# FOV visualization (moving circle)
fov_circle = plt.Circle((0, 0), sweep_width_miles / 2, fill=True, color='green', alpha=0.2, 
                        edgecolor='green', linewidth=2, linestyle='--')
ax.add_patch(fov_circle)

ax.set_xlabel('Distance (miles)', fontsize=12)
ax.set_ylabel('Distance (miles)', fontsize=12)
ax.set_title('Drone Search Pattern Simulation', fontsize=14, fontweight='bold')
ax.legend(loc='upper right')
ax.grid(True, alpha=0.3)

# Animation data
trail_x, trail_y = [], []
time_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, fontsize=12,
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

def init():
    drone.set_data([], [])
    trail.set_data([], [])
    fov_circle.center = (path_x[0], path_y[0])
    time_text.set_text('')
    return drone, trail, fov_circle, time_text

def animate(frame):
    # Interpolate position along path
    total_points = len(path_x)
    progress = frame / 200  # 200 frames total
    
    # Calculate current distance
    current_distance = progress * total_path_distance
    
    # Stop animation if hiker found
    if current_distance >= found_distance:
        progress = found_distance / total_path_distance
    
    # Find position along path
    idx = int(progress * (total_points - 1))
    if idx >= total_points - 1:
        idx = total_points - 2
    
    t = (progress * (total_points - 1)) - idx
    x = path_x[idx] + t * (path_x[idx + 1] - path_x[idx])
    y = path_y[idx] + t * (path_y[idx + 1] - path_y[idx])
    
    drone.set_data([x], [y])
    fov_circle.center = (x, y)
    
    trail_x.append(x)
    trail_y.append(y)
    trail.set_data(trail_x, trail_y)
    
    # Calculate current time
    current_time = (current_distance * 5280) / (Vs * 5280)
    
    # Check if hiker found
    if current_distance >= found_distance:
        time_text.set_text(f'Time: {time_to_find:.2f} hrs\nHIKER FOUND!')
        time_text.set_bbox(dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
        anim.event_source.stop()
    else:
        time_text.set_text(f'Time: {current_time:.2f} hrs\nSearching...')
    
    return drone, trail, fov_circle, time_text

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=200, 
                              interval=20, blit=True, repeat=False)

plt.tight_layout()
plt.show()
