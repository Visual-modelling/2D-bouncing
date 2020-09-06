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
parser.add_argument("--segmentation_map", action="store_true",
                    help="Render a segmentation map")
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
scene.render.resolution_x = 64
scene.render.resolution_y = 64

# Set camera fov in degrees
scene.camera.data.angle = fov*(pi/180.0)

# Set camera rotation in euler angles
scene.camera.rotation_mode = 'XYZ'
scene.camera.rotation_euler[0] = 63.6*(pi/180.0)
scene.camera.rotation_euler[1] = 0.0*(pi/180.0)
scene.camera.rotation_euler[2] = 46.7*(pi/180.0)

# Set camera translation
# scene.camera.location.x = 3.55889
# scene.camera.location.y = -2.50579
# scene.camera.location.z = 2.51831

scene.camera.location.x = 2.0
scene.camera.location.y = -0.9558
scene.camera.location.z = 1.4083

bpy.ops.mesh.primitive_uv_sphere_add(location=(args.X,args.Y,0.5), radius=args.radius)

ball_col = makeMaterial('mat1',args.foreground_color,(1,1,1))
setMaterial(bpy.context.object, ball_col)

# Enable GPUs
bpy.context.scene.cycles.device = 'GPU'
bpy.ops.render.render(True)
# TODO: Does this work?

if args.segmentation_map:
    # Remove the cube
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['Cube'].select_set(True)
    bpy.ops.object.delete()

    # Render with transparent background
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'

# Render Scene and store the scene
render_filename = args.filename
if args.segmentation_map:
    render_filename = render_filename + "_tmp"
bpy.data.scenes["Scene"].render.filepath = render_filename
bpy.ops.render.render( write_still=True )

if args.segmentation_map:
    # Convert the rgba image (with alpha channel) to a mask
    import os
    os.system("convert "+args.filename+"_tmp.png -alpha extract "+args.filename+".png")
    os.unlink(args.filename+"_tmp.png")
