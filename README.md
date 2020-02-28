# 2D-bouncing
Simple 2D dataset of bouncing balls

![](example.gif)

## Usage
`WIP`

To generate a dataset of N videos, run:
`generate_dataset.py N my_dataset_name`

This will create a directory `my_dataset_name` with a directory per simulation:
```
.
└── my_dataset_name
    ├── sequence_000
    │   ├── config.yaml
    │   ├── frame_000.png
    │   ...
    │   └── frame_100.png
    ....
    └── sequence_N
        └── ...
```

Each sequence contains a `config.yaml` file recording the simulation parameters.

## Components
Made of 3 components:

1. Script which generates a dataset of unique simulation parameters

2. Script which takes in the simulation parameters (radius,speed,initial position), and calculates the position of the ball at each timestep

4. Script which takes the position and draws the ball as an image

    E.g. `./drawCircle.sh 10 50 frame_0.png` will draw a circle at (10,50)


## Initial proof-of-concept

- [x] White circle on black background
- [ ] Ball bounces off image edges
- [ ] Vary physical properties:
    - [ ] Starting position
    - [ ] Ball radius
    - [ ] Initial direction
    - [ ] Initial speed
    - [ ] Gravity
    - [ ] Ball mass
    - etc
