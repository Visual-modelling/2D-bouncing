#!/bin/env sh
#
# Add random maskining



if [ "$#" -ne 1 ]; then
    echo "Usage: $0 DATASET" 1>&2; exit 1;
fi

cp -r $1 $1_masked
out=$1_masked
for video in $out/*/
do
    echo $video

    width=$(identify -format "%w" "$video/frame_000.png")> /dev/null
    height=$(identify -format "%h" "$video/frame_000.png")> /dev/null

    #loop every video
    x1=$(shuf -i 1-$width -n 1)
    x2=$(shuf -i $(($x1))-$width -n 1)
    y1=$(shuf -i 1-$height -n 1)
    y2=$(shuf -i $(($y1))-$height -n 1)
    echo 1$x1 $y1
    echo 2$x2 $y2

    for frame in $video/*.png
    do
        convert $frame -fill white -draw "rectangle $x1,$y1 $x2,$y2" $frame
    done

done

exit


# loop every frame
