<?php

if(isset($_GET['source'])){
    highlight_file(__FILE__);
    exit;
}

ini_set("display_error", false);
error_reporting(0);

include_once("flag.php");

// Do you know what it is doing?
function check($n) {
    $n = strval($n);
    $i = 0;
    $j = strlen($n) - 1;
    while($i < $j) {
        if($n[$i] !== $n[$j])
            return false;
        $i++;
        $j--;
    }
    return true;
}

$msg = "";
$request = [];

foreach([$_GET, $_POST] as $global_var) {
    foreach($global_var as $key => $value) {
        $value = trim($value);
        is_string($value) && is_numeric($value) && $request[$key] = addslashes($value);
    }
}

if($request["number"]) {
    if ($request["number"] != intval($request["number"])) {
        $msg = "Number must be integer!";
    } elseif ($request["number"][0] === "+" || $request["number"][0] === "-") {
        $msg = "No symbol!";
    } elseif (intval($request["number"]) != intval(strrev($request["number"]))) {
        $msg = "Do you know what is the palindrome number?";
    } else {
        if(check($request["number"])) {
            $msg = "You did not pass the check! Sorry I can not give you the flag.";
        } else {
          $msg = "Here is your flag: ".$flag;
        }
    }
}else{
    header("hint: ?source");
    die("Enjoy yourself!");
}

echo $msg;

?>