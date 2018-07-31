<?php
	require("header.php");
	$page="";
	if (isset($_GET['page']))
	{
		$page=strtolower($_GET['page']);
		$page=str_replace("#", "", $page);
		$page=str_replace("'", "", $page);
		$page=$page.".php";
	}
	else
		$page="main.php";
	include($page);
?>