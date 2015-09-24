<?php
/**
 * Auto-generated code below aims at helping you parse
 * the standard input according to the problem statement.
 **/

fscanf(STDIN, "%d",
    $L
);
fscanf(STDIN, "%d",
    $H
);
$T = stream_get_line(STDIN, 256, "\n");
// On transforme le message:
// - on met en majuscule la chaine
// - on remplace tout les caracteres non lettres [A-Z] par l'ascii art '?' (qui est le symbole ascii art defini juste apres 'Z')
// - on transforme la chaine de caractere en tableau
$arrT = str_split(preg_replace("#[^A-Z]#", chr(ord("Z")+1), strtoupper($T)));  
// boucle sur la hauteur des lettres
for ($i = 0; $i < $H; $i++)
{
    // recuperation des donnes d'entrees => 1 ligne horizontale de l'alphabet ASCII A-Z + ?
    $ROW = stream_get_line(STDIN, 1024, "\n");
    // resultat pour une ligne horizontale
    // chaine vide au depart
    $ANSWER_ROW = "";
    // url: http://php.net/manual/fr/control-structures.foreach.php
    // pour chaque lettre dans le message:
    // - on recupere l'indice relatif dans l'ascii art
    // - on recupere la sous-chaine d'une ligne horizontale representant le caractere en ascii art
    foreach ($arrT as $c) $ANSWER_ROW .= substr($ROW, (ord($c) - ord('A'))*$L, $L);
    // on affiche la ligne horizontale (concatenation des lignes horizontales de chaque lettre en ascii art)
    echo("$ANSWER_ROW\n");
}
?>
