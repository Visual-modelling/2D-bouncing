import os
import argparse




def simulate(num_time_steps,radius=0.1,x=0.5, y=0.5, dx=0, dy=0, gx=0, gy=0):
    '''Run simulation'''


    dt = 0.0001
    output_every = 1000

    simulation_output = []
    t = 0
    while len(simulation_output) < num_time_steps:
        t += 1
        # Calc force
        fx = gx# * args.mass
        fy = gy# * args.mass

        # Calc velocity
        dx += fx#/args.ball_mass
        dy += fy#/args.ball_mass

        # Update position
        x += dx * dt
        y += dy * dt

        # Wall collisions
        if (x <= radius):
            x = radius
            dx *= -1
        elif (x >= 1-radius):
            x = 1-radius
            dx *= -1
        if (y <= radius):
            y = radius
            dy *= -1
        elif (y >= 1-radius):
            y = 1-radius
            dy *= -1

        if t % output_every == 0:
            simulation_output.append((len(simulation_output),x,y))
    return simulation_output

if __name__ == "__main__":


    parser = argparse.ArgumentParser(description='Calculate the positions of a ball')
    parser.add_argument('--x', metavar='X', type=float,
                        default=0.5,
                        help='Starting X coordinate of the ball. Must be between 0-1.')
    parser.add_argument('--y', metavar='Y', type=float,
                        default=0.5,
                        help='Starting Y coordinate of the ball. Must be between 0-1.')
    parser.add_argument('--dx', metavar='DX', type=float,
                        default=0,
                        help='Starting X-component of velocity')
    parser.add_argument('--dy', metavar='DY', type=float,
                        default=0,
                        help='Starting Y-component of velocity')
    parser.add_argument('--radius', metavar='R', type=float,
                        default=0.1,
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

    output = simulate(num_time_steps,args.radius,args.x,args.y,args.dx,args.dy,args.gravity_x,args.gravity_y)
    for o in output:
        print("\t".join([str(v) for v in o]))

#os.system("./drawCircle.sh "+str(round(ball_x*100))+" "+str(round(ball_y*100))+" output/frame_"+"{:02d}".format(t)+".png")
