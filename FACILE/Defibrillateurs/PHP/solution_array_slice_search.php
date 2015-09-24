<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

fscanf(STDIN, "%s",
    $LON
);
fscanf(STDIN, "%s",
    $LAT
);
fscanf(STDIN, "%d",
    $N
);

$tab_dis = array();
$tab_nom = array();

function DISTANCE($LongA , $LongB , $LatA , $LatB )
{
    $LongA  = deg2rad( $LongA );
    $LongB  = deg2rad( $LongB);
    $LatA   = deg2rad( $LatA);
    $LatB   = deg2rad( $LatB);
    
    $x = ( $LongB - $LongA ) * cos( ($LatA + $LatB)*0.5 );
  
    $y = ( $LatB - $LatA );
    
    return sqrt($x*$x + $y*$y) * 6371;
}

$LON_A = floatval(str_replace( ',' , '.' , $LON));
$LAT_A = floatval(str_replace( ',' , '.' , $LAT));

for ($i = 0; $i < $N; $i++)
{
    
    $DEFIB = stream_get_line(STDIN, 256, "\n");
    
    $tab_DEFIB = explode( ';' , $DEFIB );
    
    $LON_B = floatval(str_replace( ',' , '.' , array_slice($tab_DEFIB, -2, 1)[0]));
    $LAT_B = floatval(str_replace( ',' , '.' , array_slice($tab_DEFIB, -1, 1)[0]));
    
    $d = DISTANCE( $LON_A , $LON_B , $LAT_A, $LAT_B );
    
    $tab_dis[$tab_DEFIB[0]]      =  $d;
    $tab_nom[$tab_DEFIB[0]]      =  $tab_DEFIB[1];
}

$value =  min($tab_dis);
$indice =  array_search($value , $tab_dis);

echo $tab_nom[$indice]."\n";


?>

