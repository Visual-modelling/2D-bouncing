#!/bin/env python

'''
Generate simulations
===================
Randomly sample from the parameter space
'''

import yaml
import json
import time
import os
import math
import numpy as np
import random
from simulate import simulate

import argparse
parser = argparse.ArgumentParser(description='Generate ball simulations')
parser.add_argument("param_space_file",type=str,
                    help="File containing the parameters to render")
parser.add_argument("--segmentation_map", action="store_true",
                    help="Render a segmentation map")
args = parser.parse_args()


output_path = os.path.dirname(args.param_space_file)

num_timesteps_per_simulation = 100
image_size = 64

for params in open(args.param_space_file):
    params = json.loads(params)
    simulation_num = params["simulation_num"]
    print("Simulation",simulation_num,params)
    print()
    print()
    timesteps = simulate(num_timesteps_per_simulation,**params)

    # Make directory
    formatted_name = simulation_num
    formatted_name = os.path.join(output_path,formatted_name)
    os.mkdir(formatted_name)
    if args.segmentation_map:
        os.mkdir(os.path.join(formatted_name, "mask"))

    # Write positions.csv file
    with open(os.path.join(formatted_name,"positions.csv"),'w') as f:
        header = "timestep,"\
            +",".join(["x"+str(i) for i in range(params["num_balls"])])+","\
            +",".join(["y"+str(i) for i in range(params["num_balls"])])+","\
            +",".join(["z"+str(i) for i in range(params["num_balls"])])
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
        filename = "frame_"+"{:03d}".format(t[0])+".png"
        base = os.path.dirname(__file__)
        if base == "":
            base = "./"

        versions = [""]
        if args.segmentation_map:
            versions.append(" --segmentation_map")
        for s in versions:
            cmd = "blender -b '"+os.path.join(base, "base.blend")+"' -P "+os.path.join(base, "blend.py")+" --"
            cmd += " -r "+" ".join([str(v) for v in params["radius"]])
            cmd += " -fg \""+ "\" \"".join(params["foreground_color"])+"\""
            cmd += s
            cmd += " -X "+" ".join([str(v) for v in t[1]])
            cmd += " -Y "+" ".join([str(v) for v in t[2]])
            cmd += " -Z "+" ".join([str(v) for v in t[3]])
            # cmd += " -Y"+str(t[2][j])
            # cmd += " -Z"+str(t[3][j])
            if s == "":
                cmd += " -filename " + os.path.join(formatted_name, filename[:-4])
            else:
                cmd += " -filename " + os.path.join(formatted_name, "mask", filename[:-4])
            os.system(cmd)

    # Add metadata
    with open(os.path.join(formatted_name,"config.yml"),'w') as f:
        params["date"] = time.time()
        yaml.dump(params,f)

    # Just for preview - make a gif
    os.system("convert -delay 20 "+formatted_name+"/*.png "+formatted_name+"/simulation.gif")
    if args.segmentation_map:
        os.system("convert -delay 20 "+formatted_name+"/mask/*.png "+formatted_name+"/mask/simulation.gif")
