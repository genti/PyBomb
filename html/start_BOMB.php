<?php 

$command='/usr/bin/screen -S test -d -m /usr/bin/python /home/pi/scripts/PyBomb/mode_oneWire.py' ; 

exec($command, $output);

sleep(1);
header('Location: ' . $_SERVER['HTTP_REFERER']);

?>