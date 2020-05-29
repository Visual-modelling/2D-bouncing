#!/bin/env python

'''
Generate simulations
===================

Randomly sample from the parameter space
'''

import yaml
import time
import os
import math
from sklearn.model_selection._search import ParameterSampler, ParameterGrid
#from utils import ParameterSamplerNoReset
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

# Parameters which can change per ball
per_ball_parameter_space = {
    "x":[0.1*i for i in range(1,10)],
    "y":[0.1*i for i in range(1,10)],
    "dx":[0.1*i for i in range(-5,5)],
    "dy":[0.1*i for i in range(-5,5)],
    "radius":[0.1*i for i in range(1,4)],
    "foreground_color":['#{0:x}{0:x}{0:x}'.format(x) for x in range(15,-1,-1)],
}

# Global parameters
parameter_space = {
    "num_balls":range(1,3),
#    "gx":[0.1*i for i in range(0,5)],
#    "gy":[0.1*i for i in range(0,5)],
    "background_color":['#{0:x}{0:x}{0:x}'.format(x) for x in range(0,16)],
}

# Make dataset dir
try:
    os.mkdir(args.output_path)
    pass
except:
    raise Exception("Folder " + args.output_path + " already exists.")

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

rng = np.random.RandomState(0)


# Loop through param space
# Run simulate gen
# Render
i = 0
balls = []

# TODO: Find a more elegant way of doing this
#   - Currently this just makes a large list of possible balls
#   - This is because ParameterSampler needs to be run in a loop and the rnd number doesnt update to there is no variety
#   - This could be fixed using a custom ParameterSampler which maintains an undated random state
for ball in ParameterSampler(per_ball_parameter_space,max(list(parameter_space["num_balls"]))*args.number_of_simulations*10,random_state=rng):
    balls.append(ball)

for params in ParameterSampler(parameter_space,9999999,random_state=rng):
#for params in ParameterGrid(parameter_space):

    if i >= args.number_of_simulations:
        break

    ball_params = []
    good_simulation = True
    while len(ball_params) < params["num_balls"]:

        # Check if too close to boundary
        ball_data = balls.pop()
        if ball_data["radius"] > ball_data["x"] or \
           ball_data["radius"] > ball_data["y"] or \
           ball_data["radius"] > (1-ball_data["x"]) or \
           ball_data["radius"] > (1-ball_data["y"]):
            print("Rejecting: Too close to boundary!")
            continue

        # Check if too close to other balls
        good_ball = True
        for existing_ball in ball_params:
            distance_between_balls = math.sqrt((ball_data["x"]-existing_ball["x"])**2 + (ball_data["y"] - existing_ball["y"]) **2)
            if distance_between_balls < existing_ball["radius"]+ball_data["radius"]:
                print("Rejecting: Too close to other balls!")
                good_ball = False
                break
        if not good_ball:
            continue

        # Check if ball colour same as background colour
        if params["background_color"] == ball_data["foreground_color"]:
            print("Rejecting: Colors match!")
            continue
        ball_params.append(ball_data.copy())

    # Simulate
    per_ball_data = {}
    for data in ball_params:
        for k in data.keys():
            per_ball_data[k] = per_ball_data.get(k,[]) + [data[k]]
    params = {**params,**per_ball_data}
    print("Simulation",i,params)
    timesteps = simulate(num_timesteps_per_simulation,**params)

    # Make directory
    formatted_name = "0"*(len(str(args.number_of_simulations))-len(str(i)))+str(i)
    formatted_name = os.path.join(args.output_path,formatted_name)
    os.mkdir(formatted_name)

    # Write positions.csv file
    with open(os.path.join(formatted_name,"positions.csv"),'w') as f:
        header = "timestep,"\
            +",".join(["x"+str(i) for i in range(params["num_balls"])])+","\
            +",".join(["y"+str(i) for i in range(params["num_balls"])])

        f.write(header+"\n")
        for t in timesteps:
            line = ""
            for item in t:
                if isinstance(item,list):
                    line += ","+",".join([str(it) for it in item])
                else:
                    line += ","+str(item)
            f.write(",".join(line+"\n"))

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
        yaml.dump(params,f)

    # Just for preview - make a gif
    os.system("convert -delay 20 "+formatted_name+"/*.png "+formatted_name+"/simulation.gif")
    i+=1
