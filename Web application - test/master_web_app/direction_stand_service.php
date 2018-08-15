<?php
$myfile = fopen("test.php", "w") or die("Unable to open file!");
$txt = "stand";
fwrite($myfile, $txt);
echo $txt;
fclose($myfile);
?>