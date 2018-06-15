

<?php
if (!ini_get("display_errors")) {
    ini_set("display_errors", "1");
}
$file = 'game_config.txt';

$gametype= $_POST['gametype']."|";

$order = $gametype.trim($_POST['order'])."|";
// Write the contents back to the file



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

$timeout = $order.sprintf("%02d", $ora)." ".sprintf("%02d", $min)." ".sprintf("%02d", $sec);


if (isset($_POST['choosen'])){
    
    $timeout = $timeout."|".$_POST['choosen'];
}



file_put_contents($file, $timeout);




header('Location: start_BOMB.php');
?>

