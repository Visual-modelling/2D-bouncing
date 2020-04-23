#!/bin/bash
# Draw a circle on a black background

########################
# Get arguments
usage() { echo "Usage: $0 [-r <radius>] [-f <foreground_color>] [-b <background_color>] X Y FILENAME" 1>&2; exit 1; }

# defaults
radius=10
foreground=white
background=black
image_size=64

while getopts "r:f:b:" flag; do
case "$flag" in
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
convert -size ${image_size}x${image_size} xc:$background -fill $foreground -draw "circle $x,$y $edge,$y"  $filename
