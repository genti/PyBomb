<?php
if (!ini_get("display_errors")) {
    ini_set("display_errors", "1");
}



$wires=4; #max 7 fili

$wires_custom_array=array(4,27,22,25); 
$human_horder=array(1,2,3,4);

$file_wires = "wires.txt";
$current_W = file_get_contents($file_wires);
$custom_order=array_filter(explode(" ",trim($current_W)));

$file_time = "time.txt";
$current_T = file_get_contents($file_time);
$time_array=explode(" ",$current_T);


if(count($custom_order)>0 && count($custom_order) != $wires){
    file_put_contents($file, "");
    header("Location: index.php");
} 

$bomb_running=FALSE;
if (file_exists("/home/pi/TIMER_RUNNING"))
{
      $bomb_running=TRUE;  
}


?>
<!DOCTYPE html>
<html lang="it">
  <head>
    <meta charset="utf-8">
    <title>NARCOS softair team - BOMB prototype -</title>
   
    <link rel="stylesheet" href="css/reset.css">
    <link rel="stylesheet" href="css/style_new.css">
    <link rel="stylesheet" href="jquery-ui/jquery-ui.theme.min.css">

<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0" />
  <script src="jquery-ui/external/jquery/jquery.js"></script>
  <script src="jquery-ui/jquery-ui.min.js"></script>
<script src="jquery.ui.mobile.js"></script>
    <meta name="keywords" content="softair,airsoft,joule,AEG,iguardianidelpo,team" />



 <script>
 var str="";
  $( function() {
      
     <?php  if (!$bomb_running){ ?> 
      
      $("#switch").click(function(){ 
      
        if(confirm("Sei sicuro di voler armare la bomba?")){
            $(this).toggleClass("on");
            window.location="start_BOMB.php";
        
        }}
        
        )
        
  <?php } ?>
      
      
      
      
      
      $(".wire").each(function(){
                str=str+" "+this.id;                
                $("#wire_new_order").val(str);
            });
      
   // $("#wires").draggable();
    $( "#sortabale" ).sortable({
      revert: true,
      start: function(){ str="";},
      stop: function( event, ui ) { 
            $(".wire").each(function(){
                str=str+" "+this.id;                
                $("#wire_new_order").val(str);
            });
      }

    });
   
     $( "ul, li" ).disableSelection();
  } );
  </script>
  </head>
  <body>
    <!-- page content -->
    
    <div id="main">
       <h1 id="title"> Narcos PyBomb </h1>
              
        <?php if (!$bomb_running){?>  
      
        
        <div id="input">
        <h2>Detonation time</h2>
            <form action="save_time.php" method="POST">
                <input type="text" name="HH" value="<?= isset($time_array[0]) ? $time_array[0] : "" ?>" maxlength="2" />:<input  value="<?= isset($time_array[1]) ? $time_array[1] : "" ?>" type="text" name="MM" maxlength="2"/>:<input value="<?= isset($time_array[2]) ? $time_array[2] : "00" ?>" type="text" name="SS" maxlength="2"/> | <input class="btn" type="submit" value="GO" />
            </form>
            
        </div>

        <div class="clear"></div>
        <div id="game_mode">
            <h2>Game mode</h2>
            <form action="save_gametype.php" method="POST">
                <select name="game">
                    <option value="0">Disinnesco con N fili</option>
                    <option value="1">Disinnesco con 1 filo</option>
                    <option value="2">Innesco (a chiave)</option>
                </select>
                <input class="btn" type="submit" value="Salva" />
            </form>
            </div>
        
        <div class="clear"></div>
        
        <div id="wires">
        <form action="save_wires.php" method="POST">
            <h2>Wire correct cutting order <span>(drag to sort)</span> </h2>
            
           
            <ul id="sortabale">
            <?php if (count($custom_order) > 0){
               
                foreach ($custom_order as $k=>&$value) { ?>
                     <li class="wire draggable" id="<?=$value?>">#<?=$human_horder[array_search($value, $wires_custom_array)]?></li>
               <?php  }
                
                
            }else{
                for($i=0;$i<$wires;$i++){ 
                ?>
                   <li class="wire draggable" id="<?=$wires_custom_array[$i]?>">#<?=$human_horder[$i]?></li>
            <?php
            } }
            ?>
            </ul>
            <span class="hr"></span>
            <input type="text" id="wire_new_order" class="hidden" value="<?=$current_W?>" name="order"/>
            <input type="submit" class="btn" value="SALVA" />
            </form>
        </div>
        
        
        
       
            
            <div id="switch" class="">
                    PREPARE
            </div>
           
     
        
        
        
       <?php } else { ?>
       <h1 id="running"> BOMB IS READY </h1>
       <?php } ?>
    </div>
    
    
  </body>
</html>