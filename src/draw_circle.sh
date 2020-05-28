#!/bin/bash
# Draw a circle

########################
# Get arguments
usage() {
  echo "Usage: $0 [-i <image>] [-r <radius>] [-f <foreground_color>] [-b <background_color>] X Y FILENAME" 1>&2;
  echo "    -i <image>             Filename of an existing image. If given, the ball will be drawn over this image"
  echo "    -r <radius>            Radius of the ball in pixels"
  echo "    -f <foreground_color>  Foreground colour of the ball. Can be a colour name (e.g. black or white) or a hex code)"
  echo "    -b <background_color>  Background color (ignored if -i passed). Can be a colour name (e.g. black or white) or a hex code)"
  echo "    X                      X Position of ball in pixels"
  echo "    Y                      Y Position of ball in pixels"
  echo "    FILENAME               Output filename"
  exit 1;
}

# defaults
radius=10
foreground=white
background=black
image_size=64
prev_image=none

while getopts "r:f:b:" flag; do
case "$flag" in
    i) prev_image=$OPTARG;;
    r) radius=$OPTARG;;
    f) foreground=$OPTARG;;
    b) background=$OPTARG;;
    *) usage;;
esac
done

x=${@:$OPTIND:1}
y=${@:$OPTIND+1:1}
filename=${@:$OPTIND+2:1}

if [ -z "${x}" ] || [ -z "${y}" ] || [ -z "${filename}" ]; then
    usage
fi

########################
# Draw

edge=$(($radius+$x))
if [ $prev_image == none ]; then
  # Add background
  convert -size ${image_size}x${image_size} xc:$background -fill $foreground -draw "circle $x,$y $edge,$y"  $filename
else
  # Draw on top of existing image
  convert $prev_image -fill $foreground -draw "circle $x,$y $edge,$y"  $filename
fi
