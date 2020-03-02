# 2D-bouncing ![](https://github.com/Visual-modelling/2D-bouncing/workflows/2D-bouncing/badge.svg)
Simple 2D dataset of bouncing balls

![](example.gif)

## Requirements

Install the python dependancies (`pip install -r requirements.txt`) and [imagemagick](https://www.archlinux.org/packages/?name=imagemagick)

## Usage

To generate a dataset of N videos, run:

`python src/generate_dataset.py N my_dataset_name`

This will create a directory `my_dataset_name` with a directory per simulation:
```
.
└── my_dataset_name
    ├── 000
    │   ├── config.yaml
    │   ├── frame_000.png
    │   ...
    │   └── frame_100.png
    ....
    └── N
        └── ...
```

Each sequence contains a `config.yaml` file recording the simulation parameters.

## Components
Made of 3 components:

1. Script which generates a dataset of unique simulation parameters

2. Script which takes in the simulation parameters (radius,speed,initial position), and calculates the position of the ball at each timestep

4. Script which takes the position and draws the ball as an image

    E.g. `./drawCircle.sh 10 50 frame_0.png` will draw a circle at (10,50)
    
    (images are 100x100)


## Initial proof-of-concept

- [x] White circle on black background
- [x] Ball bounces off image edges
- [ ] Vary physical properties:
    - [x] Starting position
    - [x] Ball radius
    - [x] Initial direction
    - [x] Initial speed
    - [x] Gravity
    - [ ] Ball mass
    - etc
