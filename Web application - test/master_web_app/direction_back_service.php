<?php
$myfile = fopen("test.php", "w") or die("Unable to open file!");
$txt = "back";
fwrite($myfile, $txt);
echo $txt;
fclose($myfile);
?>