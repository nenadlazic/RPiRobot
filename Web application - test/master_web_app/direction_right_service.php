<?php
$myfile = fopen("test.php", "w") or die("Unable to open file!");
$txt = "right";
fwrite($myfile, $txt);
echo $txt;
fclose($myfile);
?>