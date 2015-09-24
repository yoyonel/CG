<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 * ---
 * Hint: You can use the debug stream to print initialTX and initialTY, if Thor seems not follow your orders.
 **/

fscanf(STDIN, "%d %d %d %d",
    $lightX, // the X position of the light of power
    $lightY, // the Y position of the light of power
    $initialTX, // Thor's starting X position
    $initialTY // Thor's starting Y position
);

$dx = $lightX - $initialTX;
$dy = $lightY - $initialTY;

$abs_dx = abs($dx);
$abs_dy = abs($dy);

$nb_steps_diag = min($abs_dx, $abs_dy);

$command_y = $dy > 0 ? "S" : "N";
$command_x = $dx > 0 ? "E" : "W";

$command_diag = $command_y . $command_x . "\n";
$command_card = ($abs_dx > $abs_dy ? $command_x : $command_y) . "\n";

//error_log(var_export($command_diag, true));
//error_log(var_export($command_card, true));
//error_log(var_export($nb_steps_diag, true));

// game loop
while (TRUE)
{
    fscanf(STDIN, "%d",
        $remainingTurns
    );
    
    echo($nb_steps_diag > 0 ? $command_diag : $command_card);
    $nb_steps_diag --;
}
?>
