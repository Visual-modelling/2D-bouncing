#!/bin/env sh
#
#
# Applies a random blur to each sequence
# - Replace -blur with -gaussian-blur if you want the more mathmatically correct (but x10 slower) version
# - There is minimal difference in reality


if [ "$#" -ne 1 ]; then
    echo "Usage: $0 PATH_TO_DATASET" 1>&2; exit 1;
fi

cp -r $1 $1_blurred
out=$1_blurred

for video in $out/*/
do
    echo $video
    blur_amount=`shuf -i0-5 -n1` # Blur with sigman between 0-5 (change this to vary blur amount)

    for frame in $video/*.png
    do
        convert $frame -blur 0x$blur_amount $frame
        echo convert $frame -blur 0x$blur_amount $frame
    done

done
