# ~~2D~~3D-bouncing [![](https://github.com/Visual-modelling/2D-bouncing/workflows/2D-bouncing/badge.svg)](https://github.com/Visual-modelling/2D-bouncing/actions)
Simple ~~2D~~3D dataset of bouncing balls

![](https://user-images.githubusercontent.com/13795113/94870745-47907680-0440-11eb-93f9-7d162a24cca0.gif)

## Requirements

Install the python dependancies (`pip install -r requirements.txt`) and install blender.

## Usage
The 3D dataset takes much longer than the 2D one to render so the parameter space can be divided between multiple machines. First generate lists of parameters for each node to render:
```
python src/generate_parameter_space.py DATASET_NAME NUM_MACHINES SIZE_OF_DATASET
```
This will create a directory with the files:
```
.
└── DATASET_NAME
    ├── config.yaml
    ├── parameter_space0.yaml
    ├── ...
    └── parameter_spaceN.yaml
```
Then on each machine run the following to render the dataset:
```
python src/generate_dataset.py DATASET_NAME/parameter_spaceN.yaml [--segmentation_map]
```
This will add the simulations to the `DATASET_NAME` directory. The contents of each machine's `DATASET_NAME` dir can be safely combined to form the full dataset.


## Components
Made of 3 components:

1. Script which generates a dataset of unique simulation parameters (`generate_dataset.py`). Edit `parameter_space` to define which parameters the dataset is created over.

2. Script which takes in the simulation parameters (radius,speed,initial position, etc..), and calculates the position of the ball(s) at each timestep. (`simulate.py`)

4. A blender script to render as images

There are also optional utility scripts to apply random obscuring objects (`random_masking.sh`), and random blurs (`random_blurring.sh`) to a generated dataset.
