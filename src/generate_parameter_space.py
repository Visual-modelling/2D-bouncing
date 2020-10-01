"""Generate random list of parameters
----------------------------------
    This can be split up and provided to render_dataset.py
"""
import json
import subprocess
import time
import os
import math
import yaml
import numpy as np
import random
import operator
from functools import reduce
from tqdm import tqdm

MAX_SIZE = 100000



import argparse
parser = argparse.ArgumentParser(description='Generate ball simulations')
parser.add_argument('output_path', metavar='OUTPUT_NAME', type=str,
                    help='Path to save simulations')
parser.add_argument("num_splits", type=int,
                    help="Number of computers the space is to be split over")
parser.add_argument('number_of_simulations', metavar='NUM_SIMS', type=int,
                    help='Number of simulations to render per computer')
args = parser.parse_args()


# Parameters which can change per ball
per_ball_parameter_space = {
    "x":[0.1*i for i in range(1,10)],
    "y":[0.1*i for i in range(1,10)],
    "z":[0.1*i for i in range(1,10)],
    "dx":[0.1*i for i in range(-5,5)],
    "dy":[0.1*i for i in range(-5,5)],
    "dz":[0.1*i for i in range(-5,5)],
    "radius":[0.1*i for i in range(1,4)],
    "foreground_color":['#{0:x}{0:x}{0:x}'.format(x) for x in range(15,-1,-1)],
}

# Global parameters
parameter_space = {
    "num_balls":[1, 2, 3],
#    "gx":[0.1*i for i in range(0,5)],
#    "gy":[0.1*i for i in range(0,5)],
#    "gz":[0.1*i for i in range(0,5)],
    "background_color":['#{0:x}{0:x}{0:x}'.format(x) for x in range(0,16)],
}

rng = np.random.RandomState(42)
random.seed(42)

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


# Create combined parameter space (expand by max_num_balls)
for key in per_ball_parameter_space:
    for i in range(max(list(parameter_space["num_balls"]))):
        parameter_space[key+str(i)] = per_ball_parameter_space[key]

def get_env(space, idx):
    '''Constructs the nth combination of the parameter space'''
    keys = list(space.keys())
    lens = [len(v) for v in space.values()]

    out = {}
    count = idx
    for i in range(len(lens)):
        if i < len(lens)-1:
            val = reduce(operator.mul,[a for a in lens[i+1:]])
            out[keys[i]] = space[keys[i]][int(count // val)]
            count = count % val
        else:
            out[keys[i]] = space[keys[i]][count]
    return out

sampler_len = reduce(operator.mul,[len(a) for a in parameter_space.values()])
split_idx = 0
files = []
simulation_num=0

for i in range(args.num_splits):
    files.append(open(os.path.join(args.output_path,"parameter_space"+str(i)+".jsonl"),'w'))


pbar = tqdm(total=args.number_of_simulations)
while simulation_num < args.number_of_simulations:
    random_idx = int(random.random() *(sampler_len-1))
    params = get_env(parameter_space, random_idx)

    good_simulation = True
    for i in range(params["num_balls"]):

        # Check if too close to boundary
        if params["radius"+str(i)] > params["x"+str(i)] or \
           params["radius"+str(i)] > params["y"+str(i)] or \
           params["radius"+str(i)] > params["z"+str(i)] or \
           params["radius"+str(i)] > (1-params["x"+str(i)]) or \
           params["radius"+str(i)] > (1-params["y"+str(i)]) or \
           params["radius"+str(i)] > (1-params["z"+str(i)]):
            # print("Rejecting: Too close to boundary!")
            good_simulation = False
            break

        # Check if too close to other balls
        good_ball = True
        for j in range(i):
            distance_between_balls = math.sqrt((params["x"+str(i)]-params["x"+str(j)])**2 + (params["y"+str(i)] - params["y"+str(j)]) **2 + (params["z"+str(i)] - params["z"+str(j)]) **2)
            if distance_between_balls < params["radius"+str(j)]+params["radius"+str(i)]:
                # print("Rejecting: Too close to other balls!")
                good_ball = False
                break
        if not good_ball:
            good_simulation = False
            break

        # Check if ball colour same as background colour
        if params["background_color"] == params["foreground_color"+str(i)]:
            # print("Rejecting: Colors match!")
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
        try:
            params["simulation_num"] = "0"*(len(str(args.number_of_simulations))-len(str(simulation_num)))+str(simulation_num)
            files[split_idx].write(json.dumps(params)+"\n")
            split_idx = (split_idx+1)%args.num_splits
            simulation_num+=1
            pbar.update(1)
        except:
            breakpoint()
pbar.close()
