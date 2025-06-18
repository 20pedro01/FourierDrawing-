import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

#  Fourier Tools
def get_contour_points(image_path, num_points=300):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    contour = max(contours, key=cv2.contourArea).squeeze()
    step = max(1, len(contour) // num_points)
    contour = contour[::step]
    
    # Convert to complex numbers
    complex_points = np.array([complex(p[0], p[1]) for p in contour])
    
    # Center the contour: shift to centroid (mean)
    center = np.mean(complex_points)
    centered_points = complex_points - center
    
    return centered_points

def dft(x):
    N = len(x)
    X = []
    for k in range(N):
        s = sum(x[n] * np.exp(-2j * np.pi * k * n / N) for n in range(N)) / N
        freq = k
        amp = abs(s)
        phase = np.angle(s)
        X.append((freq, amp, phase, s))
    return sorted(X, key=lambda x: x[1], reverse=True)

#  Visualization
def draw_epicycles(ax, origin, fourier, time):
    x, y = origin
    lines = []
    for freq, amp, phase, coef in fourier:
        prevx, prevy = x, y
        angle = freq * time + phase
        x += amp * np.cos(angle)
        y += amp * np.sin(angle)
        # Draw the circle
        circle = plt.Circle((prevx, prevy), amp, fill=False, color='gray', linewidth=1)
        ax.add_patch(circle)
        # Draw the arm line
        line, = ax.plot([prevx, x], [prevy, y], color='white', lw=1)
        lines.append(line)
    return (x, y), lines

# Main Animation
path = []
fig, ax = plt.subplots()
fig.set_facecolor("black")
ax.set_facecolor("black")
ax.set_aspect("equal")
ax.axis("off")

# Load and process image
points = get_contour_points("cat.jpg", num_points=300)
fourier = dft(points)
N = len(fourier)

# Animation update function
time = 0
dt = 8 * np.pi / N
trace, = ax.plot([], [], color='cyan', lw=2)

def update(frame):
    global time, path
    ax.clear()
    ax.set_facecolor("black")
    ax.set_xlim(0, 800)
    ax.set_ylim(800, 0)  # invert Y-axis
    ax.axis("off")

    pos, lines = draw_epicycles(ax, (400, 400), fourier, time)
    path.insert(0, pos)

    if len(path) > N:
        path = path[:N]

    x_vals = [p[0] for p in path]
    y_vals = [p[1] for p in path]
    ax.plot(x_vals, y_vals, color='cyan', lw=2)

    time += dt
    return lines + [trace]

# Run animation
ani = FuncAnimation(fig, update, frames=range(N), blit=False, interval=10, repeat=False)

# Save the animation as an mp4 video (requires ffmpeg installed)
import matplotlib.animation as animation
print(animation.writers.list())

ani.save("cat_animation.mp4", writer='ffmpeg', fps=30)

plt.show()