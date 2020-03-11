#!/bin/env python

'''
Generate simulations
===================

Randomly sample from the parameter space
'''

import yaml
import time
import os
from sklearn.model_selection._search import ParameterSampler, ParameterGrid
import numpy as np
import subprocess

from simulate import simulate

import argparse
parser = argparse.ArgumentParser(description='Generate ball simulations')
parser.add_argument('number_of_simulations', metavar='NUM_SIMS', type=int,
                    help='Number of simulations to run')
parser.add_argument('output_path', metavar='OUTPUT_NAME', type=str,
                    help='Path to save simulations')
args = parser.parse_args()

num_timesteps_per_simulation = 100
image_size = 64

parameter_space = {
    "x":[0.1*i for i in range(1,10)],
    "y":[0.1*i for i in range(1,10)],
    "dx":[0.1*i for i in range(-5,5)],
    "dy":[0.1*i for i in range(-5,5)],
#    "gx":[0.1*i for i in range(0,5)],
#    "gy":[0.1*i for i in range(0,5)],
    "radius":[0.1*i for i in range(1,4)]
}

# Make dataset dir
try:
    os.mkdir(args.output_path)
except:
    raise Exception("Folder " + args.output_path + " already exist.")
#   write config
config = {}
config["date"] = time.time()
config["githash"] = subprocess.Popen("cd {} && git log | head -n 1".format(
    os.path.dirname(__file__)),
    shell=True,
    stdout=subprocess.PIPE
    ).stdout.read().split()[1].decode()
config["parameter_space"] = parameter_space
config["number_of_simulations"] = args.number_of_simulations
with open(os.path.join(args.output_path,"config.yml"),'w') as f:
    yaml.dump(config,f)


rng = np.random.RandomState(0)
# Loop through param space
# Run simulate gen
# Render
i = 0
for params in ParameterSampler(parameter_space,9999999,random_state=rng):
#for params in ParameterGrid(parameter_space):

    if i >= args.number_of_simulations:
        break

    print("Simulation",i,params)


    # Scale X,Y in range radius - 1-radius
    if params["radius"] > params["x"] or \
       params["radius"] > params["y"] or \
       params["radius"] > (1-params["x"]) or \
       params["radius"] > (1-params["y"]):
        print("Too close!")
    else:

        # Simulate
        timesteps = simulate(num_timesteps_per_simulation,**params)

        # Make directory
        formatted_name = "0"*(len(str(args.number_of_simulations))-len(str(i)))+str(i)
        formatted_name = os.path.join(args.output_path,formatted_name)
        os.mkdir(formatted_name)

        with open(os.path.join(formatted_name,"positions.csv"),'w') as f:
            f.write("timestep,x,y\n")
            for t in timesteps:
                f.write(",".join([str(i) for i in t])+"\n")

        for t in timesteps:
            # Render the images
            os.system(os.path.join(os.path.dirname(__file__),"drawCircle.sh")+" -r"+str(int(params["radius"]*image_size))+" "+str(round(t[1]*image_size))+" "+str(round(t[2]*image_size))+" "+os.path.join(formatted_name,"frame_"+"{:03d}".format(t[0])+".png"))

        # Add metadata
        with open(os.path.join(formatted_name,"config.yml"),'w') as f:
            params["date"] = time.time()
            yaml.dump(params,f)


        # Just for preview - make a gif
        os.system("convert -delay 20 "+formatted_name+"/*.png "+formatted_name+"/simulation.gif")
        i+=1
