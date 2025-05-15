# Sorting Visualizer 🎵🔢

An interactive sorting algorithm visualizer built with Python and Pygame.  
This project features real-time **sound** feedback using the `pyo` audio library.

> ⚠️ Requires Python **3.11.9** due to `pyo` compatibility issues with newer versions.

GIF of running program, Heap Sort and then Quick Sort. (only 40fps, looks better locally)

![Demo of Heap Sort and Quick Sort](visualizer.gif)

## 🔧 Getting Started

### 🐍 Python Version

This project only works with **Python 3.11.9**.  
Download it here: [Python 3.11.9](https://www.python.org/downloads/release/python-3119/)

### Setup Instructions

1. Clone the repo:
```bash
git clone https://github.com/hugoeidem/sorting-visualizer.git
cd sorting-visualizer
```

2. Activate the virtual enviroment and run it (for windows):
```bash
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python sortingVisualizer.py
```

## 🎹 Controls & Features

- Visualize different sorting algorithms with **color and sound** feedback.
- Press keys to switch algorithms:
  - `b`: Bubble Sort
  - `p`: Improved Insertion Sort
  - `i`: Insertion Sort
  - `q`: Quick Sort
  - `m`: Merge Sort
  - `r`: Radix Sort
  - `g`: Gnome Sort
  - `h`: Heap Sort
  - `o`: Bogo Sort (you've been warned 😬)

Other controls:
- `SPACE`: Pause/resume sound
- `ENTER`: Reset to original order
- `N`: New random list
- `L / J`: Adjust speed
- `RIGHT ARROW`: Skip one frame
