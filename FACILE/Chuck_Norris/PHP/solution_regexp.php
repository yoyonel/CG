<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

$MESSAGE = stream_get_line(STDIN, 100, "\n");

// Write an action using echo(). DON'T FORGET THE TRAILING \n
// To debug (equivalent to var_dump): error_log(var_export($var, true));
// url: http://php.net/manual/fr/function.sprintf.php
$str_to_bin = function ($c) { return sprintf("%07b", ord($c)); };
// url: http://php.net/manual/fr/function.implode.php
// -> implode — Rassemble les éléments d'un tableau en une chaîne
$MESSAGE_BINARY = implode(array_map($str_to_bin, str_split($MESSAGE)));
// The regex matches any character -> . in a capture group ()
// plus as much identical characters as possible following it -> \1*
$pattern = '/(.)\1*/';
// url: http://php.net/manual/fr/function.perg-match-all.php
preg_match_all($pattern, $MESSAGE_BINARY, $m);
$bin_to_chuck = function($unar, $nb_occur) { return (($unar == "1" ? "0 " : "00 ") . str_repeat("0", $nb_occur)); };
$MESSAGE_OUT = "";
// url: http://php.net/manual/fr/control-structures.foreach.php
foreach ($m[1] as $indice => $unar) { $MESSAGE_OUT .= $bin_to_chuck($unar, strlen($m[0][$indice])) . " "; }
echo rtrim($MESSAGE_OUT, " ");  // remove the last ' ' separator
?>
