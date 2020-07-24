import bpy
import sys
import argparse
import re

class ArgumentParserForBlender(argparse.ArgumentParser):
    def _get_argv_after_doubledash(self):
        try:
            idx = sys.argv.index("--")
            return sys.argv[idx+1:] # the list after '--'
        except ValueError as e: # '--' not in the list:
            return []

    def parse_args(self):
        return super().parse_args(args=self._get_argv_after_doubledash())

parser = ArgumentParserForBlender()
parser.add_argument("-r", "--radius",
                    type=float,
                    help="raidus of ball")
parser.add_argument("-fg", "--foreground-color",
                    type=str,
                    help="Hex code of the ball color")
parser.add_argument("X", type=float, default=0,
                    help="x position of ball")
parser.add_argument("Y", type=float, default=0,
                    help="y position of ball")
parser.add_argument("filename", type=str, default=0,
                    help="filename of output")
args = parser.parse_args()

pi = 3.14159265
fov = 39.6


def hex_to_rgb(hx, hsl=False):
    """Converts a HEX code into RGB or HSL.
    Args:
        hx (str): Takes both short as well as long HEX codes.
        hsl (bool): Converts the given HEX code into HSL value if True.
    Return:
        Tuple of length 3 consisting of either int or float values."""
    if re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$').match(hx):
        div = 255.0 if hsl else 0
        if len(hx) <= 4:
            return tuple(int(hx[i]*2, 16) / div if div else
                         int(hx[i]*2, 16) for i in (1, 2, 3))
        else:
            return tuple(int(hx[i:i+2], 16) / div if div else
                         int(hx[i:i+2], 16) for i in (1, 3, 5))
    else:
        raise ValueError(f'"{hx}" is not a valid HEX code.')

def makeMaterial(name, hex_code, specular):
    '''Create a blender material'''
    color = tuple(list(hex_to_rgb(hex_code))+[0])
    color = tuple([i/255 for i in color])
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color
    mat.specular_color = specular
    mat.specular_intensity = 0.5
    return mat

def setMaterial(ob, mat):
    me = ob.data
    me.materials.append(mat)

scene = bpy.data.scenes["Scene"]

# Set render resolution
scene.render.resolution_x = 480
scene.render.resolution_y = 359

# Set camera fov in degrees
scene.camera.data.angle = fov*(pi/180.0)

# Set camera rotation in euler angles
scene.camera.rotation_mode = 'XYZ'
scene.camera.rotation_euler[0] = 63.6*(pi/180.0)
scene.camera.rotation_euler[1] = 0.0*(pi/180.0)
scene.camera.rotation_euler[2] = 46.7*(pi/180.0)

# Set camera translation
scene.camera.location.x = 3.55889
scene.camera.location.y = -2.50579
scene.camera.location.z = 2.51831

red = makeMaterial('mat1',args.foreground_color,(1,1,1))
bpy.ops.mesh.primitive_uv_sphere_add(location=(args.X,args.Y,0.5), radius=args.radius)
setMaterial(bpy.context.object, red)

# Enable GPUs
bpy.context.scene.cycles.device = 'GPU'
bpy.ops.render.render(True)
# TODO: Does this work?


# Render Scene and store the scene
bpy.data.scenes["Scene"].render.filepath = args.filename
bpy.ops.render.render( write_still=True )
