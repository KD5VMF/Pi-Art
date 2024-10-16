# Import necessary libraries
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation
import datetime
import random
import sys
import os
import gc
import time
import glob
import shutil  # For disk usage

# Variables for Pendulum Speeds (min and max)
pendulum1_min_speed = 5.0  # Updated min speed as per your setting
pendulum1_max_speed = 8.0
pendulum2_min_speed = 5.0  # Updated min speed as per your setting
pendulum2_max_speed = 8.0
pendulum3_min_speed = 5.0  # If third pendulum is enabled

# ======= Direction Variables =======
# Variables to control the rotation direction of the pendulums
direction_var1 = 1  # Set to 1 for positive rotation, -1 for negative rotation of first pendulum
direction_var2 = 1  # Set to 1 for positive rotation, -1 for negative rotation of second pendulum
direction_var3 = 0  # Set to 1 for positive rotation, -1 for negative rotation of third pendulum

# ======= New Boolean Flags =======
reverse_main_pendulum = True  # Set to True to enable reversing the main pendulum's direction at halfway
change_color_on_direction_change = True  # Set to True to enable color change on direction reversal

# Control whether to save the image or not
save_image = True  # Set to True to save images

# Control whether the saved image has a transparent background
transparent_background = False  # Set to True for transparent background, False for black background

# Set whether to show pendulums during the animation
show_pendulums = True  # Change to True to show pendulum arms

# Variable to enable or disable the third pendulum
enable_third_pendulum = False  # Set to True to include the third pendulum, False otherwise

# Boolean to control automatic change of direction of the second pendulum after each run
alternate_direction2 = True  # Set to True to alternate direction each run, False to keep constant

# Create an 'Images' directory if it doesn't exist
image_folder = os.path.join(os.getcwd(), 'Images')
os.makedirs(image_folder, exist_ok=True)

# Set a random duration in seconds within the range of 60 to 500 seconds, in 15-second increments.
min_duration = 60
max_duration = 550
step = 15

# Set the toolbar to None to remove it
plt.rcParams['toolbar'] = 'None'

# ======= New Variables for Line Thickness =======
# Thickness of pendulum arms
pendulum_arm_thickness = 2  # Thickness of pendulum arms (range: 1-10, default: 2)

# Thickness of pendulum path line
path_line_thickness = 1  # Thickness of pendulum path line (range: 1-5, default: 1)
# ===============================================

def random_color():
    """
    Generate a random neon color from a predefined list.
    """
    neon_colors = [
        "#39FF14", "#DFFF00", "#FF3F00", "#FF00FF", "#00FFFF", "#FF6600", "#6E0DD0", "#FFFFFF",
        "#00FF00", "#FF007F", "#FE347E", "#FE4EDA", "#9DFF00", "#FEFE22", "#7D3CF8", "#50BFE6",
        "#FF6EFF", "#EE34D2", "#FFD300", "#76FF7A", "#FF073A", "#FF6EC7", "#FFBF00", "#CCFF00",
        "#00FFEF", "#FF10F0", "#00FF7F", "#FF4500", "#9400D3", "#FF1493", "#32CD32", "#7FFF00",
        "#00CED1", "#FF00CC", "#FF69B4", "#ADFF2F", "#1E90FF", "#FFB6C1", "#00FA9A", "#FF6347",
        "#8A2BE2"
    ]
    return random.choice(neon_colors)

def format_countdown(elapsed_time, run_time_seconds):
    """
    Format the countdown timer for display.
    """
    remaining_time = int(run_time_seconds - elapsed_time)
    minutes, seconds = divmod(remaining_time, 60)
    return f"{minutes:02d}:{seconds:02d}"

def get_image_stats():
    """
    Get the total number of images and the average image size.
    """
    image_files = glob.glob(os.path.join(image_folder, '*.png'))
    image_count = len(image_files)
	if image_files:
        total_size = sum(os.path.getsize(f) for f in image_files)
        average_size = total_size / image_count
    else:
        average_size = 2 * 1024 * 1024  # Assume 2 MB average if no images yet
    return image_count, average_size

def get_free_space():
    """
    Get the free disk space in bytes.
    """
    total, used, free = shutil.disk_usage('/')
    return free

def get_remaining_images(average_size):
    """
    Estimate the number of images that can be saved before only 1GB of storage is left.
    """
    free_space = get_free_space()
    target_free_space = 1 * 1024 ** 3  # 1 GB in bytes
    usable_space = free_space - target_free_space
    if usable_space <= 0 or average_size == 0:
        remaining_images = 0
    else:
        remaining_images = int(usable_space / average_size)
    return remaining_images

def animate_pendulum(run_time_seconds, direction1, direction2, direction3, reverse_main_pendulum, image_count, remaining_images):
    """
    Animate a double or triple pendulum and optionally save its path as an image.

    Parameters:
    - run_time_seconds (int): The duration for which the animation runs.
    - direction1 (int): Rotation direction of the first pendulum (1 or -1).
    - direction2 (int): Rotation direction of the second pendulum (1 or -1).
    - direction3 (int): Rotation direction of the third pendulum (1 or -1).
    - reverse_main_pendulum (bool): Whether to reverse the main pendulum's direction at halfway.
    - image_count (int): Total number of images saved.
    - remaining_images (int): Estimated number of images that can be saved before reaching 1GB free space.
    """
    # Random pendulum parameters for variation in animations
    arm1_length = random.uniform(5, 15)
    arm2_length = random.uniform(5, 15)
    angle1 = random.uniform(0, 2 * np.pi)
    angle2 = random.uniform(0, 2 * np.pi)
	pendulum1_speed = random.uniform(pendulum1_min_speed, pendulum1_max_speed)
    pendulum2_speed = random.uniform(pendulum2_min_speed, pendulum2_max_speed)

    # If the third pendulum is enabled
    if enable_third_pendulum:
        arm3_length = random.uniform(5, 15)
        angle3 = random.uniform(0, 2 * np.pi)
        pendulum3_speed = random.uniform(pendulum3_min_speed, pendulum3_max_speed)

    # Random color for the initial path
    initial_line_color = random_color()

    # List to keep track of multiple path segments and their colors
    path_segments = []
    path_x_current, path_y_current = [], []
    path_segments.append({
        'x': path_x_current,
        'y': path_y_current,
        'line': None,
        'color': initial_line_color
    })

    # Set up the figure and axis with a larger size for higher resolution
    fig, ax = plt.subplots(figsize=(20, 20))  # Increased figure size
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Remove margins

    # Always set the background to black during animation
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    mng = plt.get_current_fig_manager()
    try:
        mng.full_screen_toggle()
    except AttributeError:
        pass  # Ignore if full screen toggle is not available

    # Initialize lines for the pendulum arms with adjustable thickness
    arm1_line, = ax.plot([], [], lw=pendulum_arm_thickness, color=initial_line_color)
    arm2_line, = ax.plot([], [], lw=pendulum_arm_thickness, color=initial_line_color)
    if enable_third_pendulum:
        arm3_line, = ax.plot([], [], lw=pendulum_arm_thickness, color=initial_line_color)
    # Initialize the first path line
    path_line, = ax.plot([], [], lw=path_line_thickness, color=initial_line_color)
    path_segments[0]['line'] = path_line
    timer_text = ax.text(
        0.05, 0.95, '', horizontalalignment='left',
		 verticalalignment='top', transform=ax.transAxes, color='white', fontsize=16
    )

    # Add the image counter text in the bottom left corner
    image_counter_text = ax.text(
        0.05, 0.05,
        f"Images saved: {image_count}\nRemaining images: {remaining_images}",
        horizontalalignment='left',
        verticalalignment='bottom',
        transform=ax.transAxes,
        color='white',
        fontsize=16
    )

    # Set axis limits and appearance
    max_length = arm1_length + arm2_length + (arm3_length if enable_third_pendulum else 0) + 0.5
    ax.set_xlim(-max_length, max_length)
    ax.set_ylim(-max_length, max_length)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')

    start_time = datetime.datetime.now()

    # Flag to ensure direction reversal happens only once
    reversed_main_pendulum = False

    # Initialize current color index
    current_path_segment = 0

    def on_key_press(event):
        """
        Exit the program if 'q' is pressed.
        """
        if event.key.lower() == 'q':
            plt.close(fig)
            sys.exit(0)

    fig.canvas.mpl_connect('key_press_event', on_key_press)

    def update(frame):
        nonlocal angle1, angle2, angle3
        nonlocal reversed_main_pendulum
        nonlocal direction1  # To allow modification of direction1
        nonlocal current_path_segment

        # Check run time
		current_time = datetime.datetime.now()
        elapsed_time = (current_time - start_time).total_seconds()

        # ======= Handle Direction Reversal =======
        if reverse_main_pendulum and not reversed_main_pendulum and elapsed_time >= run_time_seconds / 2:
            direction1 *= -1  # Reverse direction
            reversed_main_pendulum = True
            print("Main pendulum direction reversed at halfway mark.")

            # ======= Handle Color Change =======
            if change_color_on_direction_change:
                new_color = random_color()
                # Start a new path segment with the new color
                path_x_new, path_y_new = [], []
                path_segments.append({
                    'x': path_x_new,
                    'y': path_y_new,
                    'line': ax.plot([], [], lw=path_line_thickness, color=new_color)[0],
                    'color': new_color
                })
                current_path_segment += 1
                print(f"Path color changed to {new_color} upon direction reversal.")
        # ========================================

        if elapsed_time > run_time_seconds:
            ani.event_source.stop()
            # Save only the path without the pendulums and timer, conditional on save_image
            arm1_line.set_data([], [])
            arm2_line.set_data([], [])
            if enable_third_pendulum:
                arm3_line.set_data([], [])
            timer_text.set_visible(False)
            plt.draw()

            if save_image:
                # Before saving, set the background to black if required
                if transparent_background:
                    fig.patch.set_facecolor('none')
                    ax.set_facecolor('none')
                else:
                    fig.patch.set_facecolor('black')
                    ax.set_facecolor('black')

                # Ensure the entire background is black
                ax.axis('off')
				 plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
                fig.tight_layout(pad=0)

                # Save the image with a unique timestamped filename in the 'Images' folder
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"pendulum_path_{timestamp}.png"
                save_path = os.path.join(image_folder, filename)
                plt.savefig(
                    save_path, dpi=600,  # Increased DPI for higher resolution
                    transparent=transparent_background,
                    bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor()
                )
                print(f"Saved: {save_path}")

            plt.close(fig)
            # Return an empty list to satisfy FuncAnimation's requirement
            return []

        # ======= Update Angles =======
        angle_shift1 = direction1 * np.pi / 180 * pendulum1_speed
        angle_shift2 = direction2 * np.pi / 180 * pendulum2_speed
        angle1 += angle_shift1
        angle2 += angle_shift2
        if enable_third_pendulum:
            angle_shift3 = direction3 * np.pi / 180 * pendulum3_speed
            angle3 += angle_shift3
        # ============================

        # Compute the pendulum's arm positions
        x1 = arm1_length * np.sin(angle1)
        y1 = -arm1_length * np.cos(angle1)
        x2 = x1 + arm2_length * np.sin(angle2)
        y2 = y1 - arm2_length * np.cos(angle2)
        if enable_third_pendulum:
            x3 = x2 + arm3_length * np.sin(angle3)
            y3 = y2 - arm3_length * np.cos(angle3)
            path_segments[current_path_segment]['x'].append(x3)
            path_segments[current_path_segment]['y'].append(y3)
        else:
            path_segments[current_path_segment]['x'].append(x2)
            path_segments[current_path_segment]['y'].append(y2)

        # Update all path segments
        for segment in path_segments:
            segment['line'].set_data(segment['x'], segment['y'])
			if show_pendulums:
            arm1_line.set_data([0, x1], [0, y1])
            arm2_line.set_data([x1, x2], [y1, y2])
            if enable_third_pendulum:
                arm3_line.set_data([x2, x3], [y2, y3])
        else:
            arm1_line.set_data([], [])
            arm2_line.set_data([], [])
            if enable_third_pendulum:
                arm3_line.set_data([], [])

        timer_text.set_text(format_countdown(elapsed_time, run_time_seconds))

        if enable_third_pendulum:
            return [arm1_line, arm2_line, arm3_line, timer_text, image_counter_text] + [segment['line'] for segment in path_segments]
        else:
            return [arm1_line, arm2_line, timer_text, image_counter_text] + [segment['line'] for segment in path_segments]

    # Create the animation
    ani = animation.FuncAnimation(
        fig, update, blit=True, interval=5, cache_frame_data=False
    )

    plt.show()

def main():
    # Variables to store the current direction of each pendulum between runs
    # Initialize with default directions
    current_direction1 = random.choice([1, -1])  # Random initial direction
    current_direction2 = random.choice([1, -1])  # Random initial direction
    current_direction3 = random.choice([1, -1]) if enable_third_pendulum else 0  # If third pendulum is enabled

    # Get initial image stats
    image_count, average_size = get_image_stats()
    remaining_images = get_remaining_images(average_size)

    while True:
        # Generate a random duration for the animation
        possible_durations = range(min_duration, max_duration + 1, step)
        run_time_seconds = random.choice(possible_durations)

        # Set the direction for the current run (reverse from last run)
        direction1 = current_direction1 * -1  # Reverse direction from previous run
        direction2 = current_direction2 * -1  # Reverse direction from previous run
        direction3 = current_direction3 * -1 if enable_third_pendulum else 0  # Reverse if third pendulum enabled
		# Call the animation function with the random duration and directions
        animate_pendulum(run_time_seconds, direction1, direction2, direction3, reverse_main_pendulum, image_count, remaining_images)

        # Update image stats after saving the image
        image_count, average_size = get_image_stats()
        remaining_images = get_remaining_images(average_size)

        # Clean up resources
        plt.close('all')
        gc.collect()

        # Store the current directions for the next run (they've already been reversed for this run)
        current_direction1 = direction1
        current_direction2 = direction2
        if enable_third_pendulum:
            current_direction3 = direction3

        # Optional: Add a short sleep to prevent rapid looping
        time.sleep(1)

if __name__ == "__main__":
    main()