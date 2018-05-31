<?php
$file = 'wires.txt';
// Open the file to get existing content
//$current = file_get_contents($file);
// Append a new person to the file
$current = trim($_POST['order']);
// Write the contents back to the file
file_put_contents($file, $current);

header('Location: ' . $_SERVER['HTTP_REFERER']);
?>