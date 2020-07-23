import bpy
import sys
import argparse

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
parser.add_argument("X", type=float, default=0,
                    help="x position of ball")
parser.add_argument("Y", type=float, default=0,
                    help="y position of ball")
parser.add_argument("filename", type=str, default=0,
                    help="filename of output")
args = parser.parse_args()

pi = 3.14159265
fov = 39.6


def makeMaterial(name, diffuse, specular):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = diffuse
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

red = makeMaterial('mat1',(1,1,0,0),(1,1,1))
bpy.ops.mesh.primitive_uv_sphere_add(location=(args.X,args.Y,0.5), radius=args.radius)
setMaterial(bpy.context.object, red)

# Set Scenes camera and output filename
#bpy.data.scenes["Scene"].render.file_format = 'PNG'
bpy.data.scenes["Scene"].render.filepath = args.filename

# Render Scene and store the scene
bpy.ops.render.render( write_still=True )
