<?php
error_reporting(0);
if (isset($_GET['id'])){
	$id = $_GET['id'];
	$db = new Sqlite3("level7_a9ad04871db8d352466b5e5b6f234fbe.db");
	try {
		$result = $db->query("SELECT * FROM users WHERE id=(\"$id\");")->fetchArray();
		echo "Hello {$result['username']}!";
	} catch (Exception $e) {}

}else{
	header("Location: ?id=1");
}
?>