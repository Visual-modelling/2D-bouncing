# 2D-bouncing [![](https://github.com/Visual-modelling/2D-bouncing/workflows/2D-bouncing/badge.svg)](https://github.com/Visual-modelling/2D-bouncing/actions)
Simple 2D dataset of bouncing balls

![](https://user-images.githubusercontent.com/13795113/94870745-47907680-0440-11eb-93f9-7d162a24cca0.gif)

## Requirements

Install the python dependancies (`pip install -r requirements.txt`) and [imagemagick](https://www.archlinux.org/packages/?name=imagemagick)

## Usage

To generate a dataset of N videos, run:

`python src/generate_dataset.py N my_dataset_name`

This will create a directory `my_dataset_name` with a directory per simulation:
```
.
└── my_dataset_name
    ├── config.yaml
    ├── 0000
    │   ├── config.yaml
    │   ├── positions.csv
    │   ├── frame_000.png
    │   ...
    │   ├── frame_099.png
    │   └── simulation.gif
    ....
    └── N
        └── ...
```

Each sequence contains a `config.yaml` file recording the simulation parameters.

## Components
Made of 3 components:

1. Script which generates a dataset of unique simulation parameters (`generate_dataset.py`). Edit `parameter_space` to define which parameters the dataset is created over.

2. Script which takes in the simulation parameters (radius,speed,initial position, etc..), and calculates the position of the ball(s) at each timestep. (`simulate.py`)

4. Script which takes the position and draws the ball(s) as an image

    E.g. `./drawCircle.sh 10 50 frame_0.png` will draw a circle at (10,50)

    (images are 64x64)

There are also optional utility scripts to apply random obscuring objects (`random_masking.sh`), and random blurs (`random_blurring.sh`) to a generated dataset.

## Initial proof-of-concept

- [x] White circle on black background
- [x] Ball bounces off image edges
- [ ] Vary physical properties:
    - [x] Starting position
    - [x] Ball radius
    - [x] Initial direction
    - [x] Initial speed
    - [x] Gravity
    - [ ] Ball mass (only relevent for ball-ball collisions)
    - [ ] Random ball intensity jitter
    - [x] Random ball colour/background color
    - [ ] Add random ball jitter
    - [x] Add gausian blur
    - [x] Add multiple balls
