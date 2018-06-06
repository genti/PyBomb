<?php 

$command='./BOMB_WRAPPER.sh $' ; 

exec($command, $output);

sleep(2);
header('Location: ' . $_SERVER['HTTP_REFERER']);

?>