<?php
$myfile = fopen("test.php", "w") or die("Unable to open file!");
$txt = 'Hello ' . htmlspecialchars($_POST["name"]) . '!';
fwrite($myfile, $txt);
fclose($myfile);

?>