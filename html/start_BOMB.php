<?php 

$command='/var/www/html/BOMB_WRAPPER.sh > /dev/null' ; 

exec($command, $output);

sleep(2);
header('Location: ' . $_SERVER['HTTP_REFERER']);

?>