#!/bin/env python

'''
Generate simulations
===================

Randomly sample from the parameter space
'''

import yaml
import time
import os
from sklearn.model_selection._search import ParameterSampler

output_dir = "output"
num_simulations = 10

parameter_space = {
    "x":[0.1*i for i in range(1,10)],
    "y":[0.1*i for i in range(1,10)],
    "dx":[0.1*i for i in range(0,5)],
    "dy":[0.1*i for i in range(0,5)],
    "gx":[0.1*i for i in range(0,5)],
    "gy":[0.1*i for i in range(0,5)],
    "radius":[0.1*i for i in range(1,6)],
    "date":[time.time()]
}

# Loop through param space
# Run simulate gen
# Render
for i,params in enumerate(ParameterSampler(parameter_space,num_simulations)):

    # Scale X,Y in range radius - 1-radius
    params["x"] = params["radius"] + params["x"]*(1-2*params["radius"])
    params["y"] = params["radius"] + params["y"]*(1-2*params["radius"])


    # Simulate
    #timesteps = simulate(**params)
    timesteps = []

    # Make directory
    formatted_name = "0"*(len(str(num_simulations))-len(str(i)))+str(i)
    formatted_name = os.path.join(output_dir,formatted_name)
    os.mkdir(formatted_name)

    for t in timesteps:
        pass
        # Render the images

    # Save
    with open(os.path.join(formatted_name,"params.yml"),'w') as f:
        yaml.dump(params,f)
