<?php
$myfile = fopen("test.php", "w") or die("Unable to open file!");
$txt = "left";
fwrite($myfile, $txt);
echo $txt;
fclose($myfile);
?>