<html lang="zh-CN">
  <head>
    <meta charset="utf-8">
<?php
$error=$_FILES['pic']['error'];
$tmpName=$_FILES['pic']['tmp_name'];
$name=$_FILES['pic']['name'];
$size=$_FILES['pic']['size'];
$type=$_FILES['pic']['type'];
try{
	if($name!=="")
	{
		$name1=substr($name,-4);
		if(($name1!==".gif") and ($name1!==".jpg"))
		{
			echo "hehe";
			echo "<script language=javascript>alert('不允许的文件类型！');history.go(-1)</script>";
			exit;
		}
		if($type!=="image/jpeg"&&$type!=="image/gif")
		{
			//echo mime_content_type($tmpName);
			echo "<script language=javascript>alert('不允许的文件类型！');history.go(-1)</script>";
			exit;
		}
		if(is_uploaded_file($tmpName)){
			$time=time();
			$rootpath='uploads/'.$time.$name1;
			if(!move_uploaded_file($tmpName,$rootpath)){
				echo "<script language='JavaScript'>alert('文件移动失败!');window.location='index.php?page=submit'</script>";
				exit;
			}
			else{
				sleep(2);				
				if ($type=='image/jpeg')
				{
					$im = @imagecreatefromjpeg($rootpath);
					if(!$im){
					  $im = imagecreatetruecolor(150, 30);
					  $bg = imagecolorallocate($im, 255, 255, 255);
					  $text_color = imagecolorallocate($im, 0, 0, 255);
					  imagefilledrectangle($im, 0, 0, 150, 30, $bg);
					  imagestring($im, 3, 5, 5, "Error loading image", $text_color);
					} else {
						$time=time();
						$new_rootpath='uploads/'.$time.$name1;
						imagejpeg($im,$new_rootpath);
						imagedestroy($im);
					}
				}
				else if ($type=='image/gif')
				{
					$im = @imagecreatefromgif($rootpath);
					if(!$im){
					  $im = imagecreatetruecolor(150, 30);
					  $bg = imagecolorallocate($im, 255, 255, 255);
					  $text_color = imagecolorallocate($im, 0, 0, 255);
					  imagefilledrectangle($im, 0, 0, 150, 30, $bg);
					  imagestring($im, 3, 5, 5, "Error loading image", $text_color);
					} else {
						$time=time();
						$new_rootpath='uploads/'.$time.$name1;
						imagegif($im,$new_rootpath);
						imagedestroy($im);
					}
				}
				unlink($rootpath);
			}
		}
		echo "图片ID：".$time;
	}
}
catch(Exception $e)
{
	echo "ERROR";
}
//
 ?>
 </html>
