<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

fscanf(STDIN, "%d",
    $road // the length of the road before the gap.
);
fscanf(STDIN, "%d",
    $gap // the length of the gap.
);
fscanf(STDIN, "%d",
    $platform // the length of the landing platform.
);

// game loop
while (TRUE)
{
    fscanf(STDIN, "%d",
        $speed // the motorbike's speed.
    );
    fscanf(STDIN, "%d",
        $coordX // the position on the road of the motorbike.
    );

    if($coordX >= ($gap+$road)) {
        echo("SLOW\n");
    }
    else {
        if($speed <= $gap) echo("SPEED\n");
        else if ($speed > $gap+1) echo("SLOW\n");
        else if ($coordX + $speed < $road) echo("WAIT\n");
        else echo("JUMP\n");
    }
}
?>

