# Pi-Art
# Pendulum Path Animation with Restart

## About
This program generates a random pendulum animation. Depending on the 'save_image' variable, it can save the pendulum's path as a high-resolution image in a specific folder, then restarts itself.

### Features
- Randomly generated pendulum animations.
- Option to save high-resolution images of the pendulum's path.
- Customizable parameters for pendulum behavior.

## Installation

### Prerequisites
- Anaconda or Miniconda installed on your system. You can download Anaconda [here](https://www.anaconda.com/products/individual) or Miniconda [here](https://docs.conda.io/en/latest/miniconda.html).

### Setting Up the Environment
To run this program, you need to set up an Anaconda environment with Python 3.8. Follow these steps:

1. Open your terminal (or Anaconda Prompt if you are on Windows).
2. Create a new Anaconda environment by running:

conda create --name pendulum-env python=3.8

3. Activate the environment:

conda activate pendulum-env


### Installing Dependencies
This project requires `matplotlib`, `numpy`, and `mpmath`. Install these by running:

conda install matplotlib numpy
pip install mpmath


## Running the Program
Once you have set up your environment and installed the dependencies, you can run the program with the following command:

python pi1000.py


### Configuration
- To enable or disable saving images, edit the `save_image` variable in the `pi1000.py` file.
- To show or hide pendulums during the animation, adjust the `show_pendulums` variable.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- This project was inspired by the fascinating physics of pendulums.

### Note
Ensure your environment is activated (`conda activate pendulum-env`) each time you want to run the program.
