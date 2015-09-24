<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/


// game loop
while (TRUE)
{
    fscanf(STDIN, "%d %d",
        $spaceX,
        $spaceY
    );
    $maxMountainH = 0;
    $idMaxMountainH = 0;
    for ($i = 0; $i < 8; $i++)
    {
        fscanf(STDIN, "%d",
            $mountainH // represents the height of one mountain, from 9 to 0. Mountain heights are provided from left to right.
        );
        if ($mountainH > $maxMountainH) {
            $maxMountainH = $mountainH;
            $idMaxMountainH = $i;
        }
    }

    // Write an action using echo(). DON'T FORGET THE TRAILING \n
    // To debug (equivalent to var_dump): error_log(var_export($var, true));

    //echo("HOLD\n"); // either:  FIRE (ship is firing its phase cannons) or HOLD (ship is not firing).
    echo(($spaceX == $idMaxMountainH ? "FIRE" : "HOLD") . "\n");
}
?>
