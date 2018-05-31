<?php
$file = 'time.txt';

$ora=$_POST['HH'];
if ($ora == ''){
    $ora=0;
}
if ($ora>24){
    $ora=24;
    
}

$min=$_POST['MM'];
if ($min == ''){
    $min=0;
}
if ($min>59){
    $min=59;  
}

$sec=$_POST['SS'];
if ($sec == ''){
    $sec=0;
}
if ($sec>59){
    $sec=59;  
}

$current = $ora." ".$min." ".$sec;


file_put_contents($file, $current);


header('Location: ' . $_SERVER['HTTP_REFERER']);
?>