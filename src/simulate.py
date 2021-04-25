import os
import argparse
import math




def simulate(num_time_steps,radius=[0.1],x=[0.5], y=[0.5], dx=[0.0], dy=[0.0], gx=0, gy=0,**kwargs):
    '''Run simulation'''

    # Check all lists are the same length
    assert len(x) == len(y) == len(radius) == len(dx) == len(dy), "X,Y,radius,dx,dy must be the same length"


    dt = 0.0001
    output_every = 1000

    simulation_output = []
    t = 0
    bounces = {"wall": 0, "ball-ball": 0}
    while len(simulation_output) < num_time_steps:
        t += 1
        for i in range(len(x)):
            # Calc force
            fx = gx# * args.mass
            fy = gy# * args.mass

            # Calc velocity
            dx[i] += fx#/args.ball_mass
            dy[i] += fy#/args.ball_mass

            # Update position
            x[i] += dx[i] * dt
            y[i] += dy[i] * dt

        for i in range(len(x)):

            # Ball collisions
            for j in range(i,len(x)):
                if i != j:
                    distance_between_balls = math.sqrt( (x[i]-x[j])**2 + (y[i]-y[j]) **2)
                    if distance_between_balls < radius[i] + radius[j]: # if collision
                        bounces["ball-ball"] += 1
                        dxi_temp = dx[i]
                        dyi_temp = dy[i]
                        dx[i] = (dx[i] * ( 1 - 1) + ( 2 * 1 * dx[j])) / (1 + 1)
                        dy[i] = (dy[i] * ( 1 - 1) + ( 2 * 1 * dy[j])) / (1 + 1)
                        dx[j] = (dx[j] * ( 1 - 1) + ( 2 * 1 * dxi_temp)) / (1 + 1)
                        dy[j] = (dy[j] * ( 1 - 1) + ( 2 * 1 * dyi_temp)) / (1 + 1)

            # Wall collisions
            if (x[i] <= radius[i]):
                bounces["wall"] += 1
                x[i] = radius[i]
                dx[i] *= -1
            elif (x[i] >= 1-radius[i]):
                bounces["wall"] += 1
                x[i] = 1-radius[i]
                dx[i] *= -1
            if (y[i] <= radius[i]):
                bounces["wall"] += 1
                y[i] = radius[i]
                dy[i] *= -1
            elif (y[i] >= 1-radius[i]):
                bounces["wall"] += 1
                y[i] = 1-radius[i]
                dy[i] *= -1

        if t % output_every == 0:
            simulation_output.append((len(simulation_output),x.copy(),y.copy()))
    return simulation_output, bounces

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Calculate the positions of a ball')
    parser.add_argument('--x', metavar='X', type=float,nargs="*",
                        default=[0.5],
                        help='Starting X coordinate of the ball. Must be between 0-1.')
    parser.add_argument('--y', metavar='Y', type=float,nargs="*",
                        default=[0.5],
                        help='Starting Y coordinate of the ball. Must be between 0-1.')
    parser.add_argument('--dx', metavar='DX', type=float,nargs="*",
                        default=[0],
                        help='Starting X-component of velocity')
    parser.add_argument('--dy', metavar='DY', type=float,nargs="*",
                        default=[0],
                        help='Starting Y-component of velocity')
    parser.add_argument('--radius', metavar='R', type=float,nargs="*",
                        default=[0.1],
                        help='Radius of the ball')

    # Change mass is equiv to change in G for a single ball
    #parser.add_argument('--mass', metavar='M', type=int,
    #                        default=1
    #                        help='Mass of the ball')
    parser.add_argument('--gravity_x', metavar='GX', type=float,
                        default=0,
                        help='X-component of gravitational force')
    parser.add_argument('--gravity_y', metavar='GY', type=float,
                        default=0,
                        help='Y-component of gravitational force')
    args = parser.parse_args()

    # Create a test dataset
    output = simulate(100,args.radius,args.x,args.y,args.dx,args.dy,args.gravity_x,args.gravity_y)[0]
    for t,o in enumerate(output):
        print("\t".join([str(v) for v in o]))

#         filename = "test/frame_"+"{:02d}".format(t)+".png"
#         os.system("./draw_circle.sh -r "+str(round(args.radius[0]*img_size))+" "+str(round(o[1][0]*img_size))+" "+str(round(o[2][0]*img_size))+" "+filename)
#         for i in range(1,len(o[1])):
#             os.system("./draw_circle.sh -i "+filename+" -r "+str(round(args.radius[i]*img_size))+" "+str(round(o[1][i]*img_size))+" "+str(round(o[2][i]*img_size))+" "+filename)
