
# Pi5K - Double and Triple Pendulum Path Animation

## Overview

Pi5K is a Python-based animation that simulates the motion of double and triple pendulums with colorful and dynamic path drawings. The program generates artistic pendulum paths and allows for saving high-resolution images of the pendulum trajectories. The project runs on a Raspberry Pi and is designed for continuous operation, creating stunning visualizations with pendulums of varying speeds and colors.

The program includes several customization options, such as the ability to reverse pendulum direction, change colors, control path thickness, and save images to disk.

## Features

- **Double and Triple Pendulum Animation**: Animate double or triple pendulums with customizable pendulum arm lengths and speeds.
- **Dynamic Path Colors**: Automatically change the color of the pendulum path during animation, including color changes when the main pendulum reverses direction.
- **Image Saving**: Save high-resolution PNG images of pendulum paths in the `Images/` directory.
- **Transparent or Black Backgrounds**: Save images with either a transparent or black background.
- **On-screen Counters**: Display the total number of saved images and the number of images that can still be saved before storage runs low.
- **Automatic File Size Calculation**: Recalculate the average image file size after each save to ensure accuracy in estimating remaining disk space.
- **System Resilience**: Includes strategies to protect the system from power loss by minimizing unnecessary disk writes.

## Requirements

- Python 3.x
- Matplotlib
- NumPy
- Animation support in Matplotlib
- Raspberry Pi (tested on Raspberry Pi Zero W2)

## Installation

1. Install Python dependencies:
   ```bash
   sudo apt-get install python3 python3-pip
   pip3 install matplotlib numpy
   ```

2. Clone or copy the `pi5K` program to your Raspberry Pi.

3. Make sure the following directories exist:
   ```bash
   mkdir -p /home/sysop/Images
   ```

4. Optional: Set up the program to run at startup. You can configure `systemd` or add the program to your `rc.local`.

## Usage

Run the program manually:
```bash
python3 pi5K.py
```

The program will continuously run, generating pendulum path animations and saving images to the `Images/` directory.

### Key Features and Controls:

- **Pendulum Speeds**: Customize the speed of pendulums using the following variables in the code:
  ```python
  pendulum1_min_speed = 0.5
  pendulum1_max_speed = 3.0
  pendulum2_min_speed = 0.5
  pendulum2_max_speed = 3.0
  ```

- **Reverse Direction**: Set whether the main pendulum reverses direction at the halfway point:
  ```python
  reverse_main_pendulum = True  # Enable or disable direction reversal
  ```

- **Dynamic Color Changes**: Enable automatic color change when pendulum direction changes:
  ```python
  change_color_on_direction_change = True  # Enable or disable color change
  ```

- **Background Options**: Choose between transparent or black backgrounds for saved images:
  ```python
  transparent_background = False  # Set to True for transparent background
  ```

### Counters and Storage Management:

Pi5K automatically tracks how many images have been saved and calculates the remaining available storage space. The following counters are displayed on-screen during the animation:

- **Total images saved**.
- **Remaining images that can be saved** before the disk space drops to 1 GB.

The image file sizes are dynamically calculated after each save to ensure accurate storage estimates.

## System Protection from Power Loss

To help protect the Raspberry Pi from filesystem corruption due to sudden power loss, the following strategies are recommended:

1. **Read-only filesystem**: Configure your Pi's root filesystem to be read-only and mount temporary directories (`/tmp`, `/var/log`, etc.) in RAM.
2. **Regular backups**: Set up regular backups of important files to external storage.
3. **Disable unnecessary writes**: Minimize log and temporary file writes by using `tmpfs` mounts.

## License

This project is open-source. Feel free to modify and share.

## Author

Developed by [Your Name]. Special thanks to all the contributors.
