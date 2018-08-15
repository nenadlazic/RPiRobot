<?php
$myfile = fopen("test.php", "w") or die("Unable to open file!");
$txt = "forward";
fwrite($myfile, $txt);
echo $txt;
fclose($myfile);
?>