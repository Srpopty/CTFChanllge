<?php
error_reporting(0);
if (isset($_GET['id'])){
	$id = $_GET['id'];
	$db = new Sqlite3("level6_745ca30961f76181c5d100b3b4bd902f.db");
	$result = $db->query("SELECT * FROM users WHERE id=$id;")->fetchArray();
	echo "Hello {$result['username']}!";
}else{
	header("Location: /lev3l_$6_.php?id=1");
}
?>