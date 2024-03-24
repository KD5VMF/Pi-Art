"""
Title: Pendulum Path Animation with Restart
About: This program generates a random pendulum animation. Depending on the 'save_image' variable, 
       it can save the pendulum's path as a high-resolution image in a specific folder, then restarts itself.
"""

"""
Copyright (c) 2024 MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
from mpmath import mp
import datetime
import random
import sys
import os

# Control whether to save the image or not
save_image = False  # Set to False to prevent saving images

# Set whether to show pendulums during the animation
show_pendulums = False  # Change to True to show pendulums

# Create an 'Images' directory if it doesn't exist
image_folder = os.path.join(os.getcwd(), 'Images')
if not os.path.exists(image_folder):
    os.makedirs(image_folder)

# Set a random duration in seconds within the range of 60 to 500 seconds, in 45-second increments.
min_duration = 10
max_duration = 100
step = 45

# Set the toolbar to None to remove it
plt.rcParams['toolbar'] = 'None'

# Function to generate a random color
def random_color():
    # Define a list of neon colors for the pendulum and path
    neon_colors = [
        "#39FF14",  # Neon Green
        "#DFFF00",  # Neon Yellow
        "#FF3F00",  # Neon Red
        "#FF00FF",  # Neon Pink
        "#00FFFF",  # Neon Cyan
        "#FF6600",  # Neon Orange
        "#6E0DD0",  # Neon Purple
        "#FFFFFF",  # Neon White
        "#00FF00",  # Another Neon Green
        "#FF007F",  # Neon Magenta
        "#FE347E",  # Neon Rose
        "#FE4EDA",  # Neon Fuchsia
        "#9DFF00",  # Neon Lime
        "#FEFE22",  # Neon Lemon
        "#7D3CF8",  # Neon Violet
        "#50BFE6",  # Neon Blue
        "#FF6EFF",  # Neon Lavender
        "#EE34D2",  # Neon Dark Pink
        "#FFD300",  # Neon Sunflower
        "#76FF7A"   # Neon Light Green
    ]
    return random.choice(neon_colors)

def format_countdown(elapsed_time, run_time_seconds):
    # Format the countdown timer for display
    remaining_time = int(run_time_seconds - elapsed_time)
    minutes, seconds = divmod(remaining_time, 60)
    return f"{minutes:02d}:{seconds:02d}"

def animate_pendulum_pi(run_time_seconds):
    # Main function to animate the pendulum and potentially save the path
    random.seed()
    frames_per_digit = random.randint(50, 4000)
    mp.dps = random.randint(5, 100) + 2
    pi_digits = str(mp.pi)[2:]

    # Random pendulum parameters for variation in animations
    arm1_length = random.uniform(0.1, 20)
    arm2_length = random.uniform(0.1, 20)
    angle1 = random.uniform(0, 2 * np.pi)
    angle2 = random.uniform(0, 2 * np.pi)
    pendulum1_speed = random.uniform(1, 4)
    pendulum2_speed = random.uniform(1, 5)

    direction1 = 1
    direction2 = -1

    angle_shift1 = direction1 * np.pi / 180 * pendulum1_speed
    angle_shift2 = direction2 * np.pi / 180 * pendulum2_speed

    # Random color for this run
    line_color = random_color()

    fig, ax = plt.subplots(figsize=(12, 12))
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove margins

    fig.patch.set_facecolor('black')
    mng = plt.get_current_fig_manager()
    mng.full_screen_toggle()

    arm1_line, = ax.plot([], [], lw=2, color=line_color)
    arm2_line, = ax.plot([], [], lw=2, color=line_color)
    path_line, = ax.plot([], [], lw=0.5, color=line_color)
    timer_text = ax.text(0.05, 0.95, '', horizontalalignment='left', verticalalignment='top', transform=ax.transAxes, color='white')

    ax.set_xlim(-arm1_length - arm2_length, arm1_length + arm2_length)
    ax.set_ylim(-arm1_length - arm2_length, arm1_length + arm2_length)
    ax.set_aspect('equal', adjustable='box')
    ax.set_facecolor('black')
    ax.axis('off')

    path_x, path_y = [], []

    start_time = datetime.datetime.now()

    def on_key_press(event):
        # Exit the program if 'q' is pressed
        if event.key.lower() == 'q':
            sys.exit(0)

    fig.canvas.mpl_connect('key_press_event', on_key_press)

    def update(frame):
        nonlocal angle1, angle2
        # Check run time
        current_time = datetime.datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()
        if elapsed_time > run_time_seconds:
            ani.event_source.stop()
            # Save only the path without the pendulums, conditional on save_image
            arm1_line.set_data([], [])
            arm2_line.set_data([], [])
            plt.draw()

            if save_image:
                # Save the image with a unique timestamped filename in the 'Images' folder
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"pendulum_path_{timestamp}.png"
                save_path = os.path.join(image_folder, filename)
                plt.savefig(save_path, dpi=600, transparent=True, bbox_inches='tight', pad_inches=0)
                print(f"Saved: {save_path}")

            plt.close(fig)
            return

        # Update angles
        angle1 += angle_shift1
        angle2 += angle_shift2

        # Compute the pendulum's arm positions
        x1 = arm1_length * np.sin(angle1)
        y1 = -arm1_length * np.cos(angle1)
        x2 = x1 + arm2_length * np.sin(angle2)
        y2 = y1 - arm2_length * np.cos(angle2)

        path_x.append(x2)
        path_y.append(y2)
        path_line.set_data(path_x, path_y)

        if show_pendulums:
            arm1_line.set_data([0, x1], [0, y1])
            arm2_line.set_data([x1, x2], [y1, y2])
        else:
            arm1_line.set_data([], [])
            arm2_line.set_data([], [])

        timer_text.set_text(format_countdown(elapsed_time, run_time_seconds))

        return path_line, arm1_line, arm2_line, timer_text

    ani = animation.FuncAnimation(fig, update, frames=(mp.dps - 2) * frames_per_digit, blit=True, interval=5)

    plt.show()

# Generate a random duration for the animation
run_time_seconds = random.randrange(min_duration, max_duration, step)

# Call the animation function with the random duration
animate_pendulum_pi(run_time_seconds)

# Restart the program
os.execv(sys.executable, ['python'] + sys.argv)
