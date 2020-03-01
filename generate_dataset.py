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

from simpleOneBall import simulate

output_dir = "output"
num_simulations = 10
num_timesteps_per_simulation = 100

parameter_space = {
    "x":[0.1*i for i in range(1,10)],
    "y":[0.1*i for i in range(1,10)],
    "dx":[0.1*i for i in range(0,8)],
    "dy":[0.1*i for i in range(0,8)],
    "gx":[0.1*i for i in range(0,5)],
    "gy":[0.1*i for i in range(0,5)],
    "radius":[0.1*i for i in range(1,4)]
}

# Loop through param space
# Run simulate gen
# Render
for i,params in enumerate(ParameterSampler(parameter_space,num_simulations)):


    # Scale X,Y in range radius - 1-radius
    params["x"] = params["radius"] + params["x"]*(1-2*params["radius"])
    params["y"] = params["radius"] + params["y"]*(1-2*params["radius"])

    print("Simulation",i,params)

    # Simulate
    timesteps = simulate(num_timesteps_per_simulation,**params)

    # Make directory
    formatted_name = "0"*(len(str(num_simulations))-len(str(i)))+str(i)
    formatted_name = os.path.join(output_dir,formatted_name)
    os.mkdir(formatted_name)

    for t in timesteps:
        # Render the images
        os.system("./drawCircle.sh -r"+str(int(params["radius"]*100))+" "+str(round(t[1]*100))+" "+str(round(t[2]*100))+" "+os.path.join(formatted_name,"frame_"+"{:02d}".format(t[0])+".png"))

    # Add metadata
    with open(os.path.join(formatted_name,"params.yml"),'w') as f:
        params["date"] = time.time()
        yaml.dump(params,f)


    # Just for preview - make a gif
    os.system("convert -delay 20 "+formatted_name+"/*.png "+formatted_name+"/simulation.gif")
