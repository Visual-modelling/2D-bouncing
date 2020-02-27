#!/bin/bash
# Draw a circle on a black background

########################
# Get arguments
usage() { echo "Usage: $0 [-r <radius>] X Y FILENAME" 1>&2; exit 1; }

radius=10 # default radius
image_size=100

while getopts "r:" flag; do
case "$flag" in
    r) radius=$OPTARG;;
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
convert -size ${image_size}x${image_size} xc:black -fill white -stroke black -draw "circle $x,$y $edge,$y"  $filename
