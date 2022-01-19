#!/bin/env python

'''
Generate simulations
===================

Randomly sample from the parameter space
'''

import yaml
import time
import os, sys, shutil
import math
from sklearn.model_selection._search import ParameterSampler, ParameterGrid
import numpy as np
import subprocess
import random
from simulate import simulate
import scipy.stats.distributions as dists

import argparse
parser = argparse.ArgumentParser(description='Generate ball simulations')
parser.add_argument('number_of_simulations', metavar='NUM_SIMS', type=int,
                    help='Number of simulations to run')
parser.add_argument('output_path', metavar='OUTPUT_NAME', type=str,
                    help='Path to save simulations')
args = parser.parse_args()

num_timesteps_per_simulation = 60
image_size = 64

# Parameters which can change per ball
per_ball_parameter_space = {
    #"x":dists.uniform(0.1,0.9),
    #"y":dists.uniform(0.1,0.9),
    #"dx":dists.uniform(-0.5,0.4),
    #"dy":dists.uniform(-0.5,0.4),
    #"radius":dists.uniform(0.1,0.3),
    "x":[0.1*i for i in range(1,10)],
    "y":[0.1*i for i in range(1,10)],
    "dx":[0.1*i for i in range(-5,5)],
    "dy":[0.1*i for i in range(-5,5)],
    "radius":[0.1*i for i in range(1,4)],
    "foreground_color":['#{0:x}{0:x}{0:x}'.format(x) for x in range(15,-1,-1)],
}

#per_ball_parameter_space = {
#    "x":dists.uniform(0.1,0.9),
#    "y":dists.uniform(0.1,0.9),
#    "dx":dists.uniform(-0.5,0.4),
#    "dy":dists.uniform(-0.5,0.4),
#    "radius":dists.uniform(0.1,0.3),
#    "foreground_color":['#{0:x}{0:x}{0:x}'.format(x) for x in range(15,-1,-1)]
#}

# Global parameters
parameter_space = {
    "num_balls":range(1,5),
    #"gx":dists.uniform(0,0.04),  # As long as at least one parameter is a distribution, the sampler will sample WITHOUT REPLACEMENT (important)
    "gy":dists.uniform(0,0.02),
    "background_color":['#{0:x}{0:x}{0:x}'.format(x) for x in range(0,16)],
}

## How the rest of the parameter space make look if you wish to sample from continuous space
#parameter_space = {
#    "num_balls":range(1,4), # YOU CANNOT MAKE NUMBALLS A `dists.randint' distribution without changing your ``Building space'' code
#    "gx":dists.uniform(0,0.4),
#    "gy":dists.uniform(0,0.4),
#    "background_color":['#{0:x}{0:x}{0:x}'.format(x) for x in range(0,16)]
#}

# Make dataset dir
try:
    os.mkdir(args.output_path)
    pass
except:
    raise Exception("Folder "  + args.output_path + " already exists.")

#   write config
config = {}
config["date"] = time.time()
config["githash"] = subprocess.Popen("cd {} && git log | head -n 1".format(
    os.path.dirname(__file__)),
    shell=True,
    stdout=subprocess.PIPE
    ).stdout.read().split()[1].decode()
config["parameter_space"] = parameter_space
config["per_ball_parameter_space"] = per_ball_parameter_space
config["number_of_simulations"] = args.number_of_simulations
with open(os.path.join(args.output_path,"config.yml"),'w') as f:
    yaml.dump(config,f)

rng = np.random.RandomState(42)
random.seed(42)

# Create combined parameter space (expand by max_num_balls
print("Building space...")
for key in per_ball_parameter_space:
    for i in range(max(list(parameter_space["num_balls"]))):
        parameter_space[key+str(i)] = per_ball_parameter_space[key]
print("Done")

# Loop through param space
# Run simulate gen
# Render
simulation_num = 0
balls = []

# If one of the parameters given is a scipy.stats.distributions object, then it will sample with replacement
sampler = ParameterSampler(parameter_space, min(1000, args.number_of_simulations))
sampler = list(sampler)
sampler_idx = 0


while simulation_num < args.number_of_simulations:
    if(sampler_idx == min(1000, args.number_of_simulations)):
        sampler_idx = 0
        sampler = list(ParameterSampler(parameter_space, min(1000, args.number_of_simulations)))
    params = sampler[sampler_idx]
    sampler_idx += 1
    good_simulation = True
    for i in range(params["num_balls"]):

        # Check if too close to boundary
        if params["radius"+str(i)] > params["x"+str(i)] or \
           params["radius"+str(i)] > params["y"+str(i)] or \
           params["radius"+str(i)] > (1-params["x"+str(i)]) or \
           params["radius"+str(i)] > (1-params["y"+str(i)]):
            print("Rejecting: Too close to boundary!")
            good_simulation = False
            break

        # Check if too close to other balls
        good_ball = True
        for j in range(i):
            distance_between_balls = math.sqrt((params["x"+str(i)]-params["x"+str(j)])**2 + (params["y"+str(i)] - params["y"+str(j)]) **2)
            if distance_between_balls < params["radius"+str(j)]+params["radius"+str(i)]:
                print("Rejecting: Too close to other balls!")
                good_ball = False
                break
        if not good_ball:
            good_simulation = False
            break

        # Check if ball colour same as background colour
        if params["background_color"] == params["foreground_color"+str(i)]:
            print("Rejecting: Colors match!")
            good_simulation = False
            break

        # Add to lists
        for key in per_ball_parameter_space.keys():
            params[key] = params.get(key,[]) + [params[key+str(i)]]

    # Remove old keys
    for i in range(max(list(parameter_space["num_balls"]))):
        for key in per_ball_parameter_space.keys():
            del params[key+str(i)]

    if good_simulation:
        print("Simulation",simulation_num,params)
        print()
        print()
        timesteps, bounces = simulate(num_timesteps_per_simulation,**params)

        # Make directory
        formatted_name = "0"*(len(str(args.number_of_simulations))-len(str(simulation_num)))+str(simulation_num)
        formatted_name = os.path.join(args.output_path,formatted_name)
        os.mkdir(formatted_name)

        # Write positions.csv file
        with open(os.path.join(formatted_name,"positions.csv"),'w') as f:
            header = "timestep,"\
                +",".join(["x"+str(i) for i in range(params["num_balls"])])+","\
                +",".join(["y"+str(i) for i in range(params["num_balls"])])
            f.write(header+"\n")
            for t in timesteps:
                line = []
                for item in t:
                    if isinstance(item,list):
                        line += [",".join([str(it) for it in item])]
                    else:
                        line += [str(item)]
                f.write(",".join(line)+"\n")

        # Render the images
        for t in timesteps:
            filename = os.path.join(formatted_name,"frame_"+"{:03d}".format(t[0])+".png")
            for j in range(len(t[1])):
                base = os.path.dirname(__file__)
                if base == "":
                    base = "./"
                cmd = os.path.join(base,"draw_circle.sh")

                if j == 0:
                    # First ball - pick background colour
                    cmd += " -b '"+params["background_color"]+"'"
                else:
                    # Other balls - use image of previous ball as background image
                    cmd += " -i '"+filename+"'"

                cmd += " -r "+str(int(params["radius"][j]*image_size))
                cmd += " -f '"+params["foreground_color"][j]+"'"
                cmd += " "+str(round(t[1][j]*image_size))
                cmd += " "+str(round(t[2][j]*image_size))
                cmd += " "+filename
                os.system(cmd)

        # Add metadata
        with open(os.path.join(formatted_name,"config.yml"),'w') as f:
            params["date"] = time.time()
            params["bounces"] = bounces
            yaml.dump(params,f)

        # Just for preview - make a gif
        os.system("convert -delay 20 "+formatted_name+"/*.png "+formatted_name+"/simulation.gif")
        simulation_num+=1
