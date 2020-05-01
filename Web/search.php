<html>
	<head>
		<meta charset="utf-8" />
		<title>电影搜索</title>
		<link rel="stylesheet" href="css/search.css"/>
		<meta name="referrer" content="never">
	</head>
	<body>
<?php
require_once("class/search_class.php");
$info = new video_info();

$keywords = trim($_GET['words']);
$con = mysqli_connect("localhost", "root", "root", "movie"); //使用mysqli_connect函数连接数据库服务器
if(mysqli_connect_errno($con)) //判断是否连接上数据库服务器
{ 
    echo "连接数据库服务器失败 " . mysqli_connect_error(); 
}
//设置编码
mysqli_query($con,"set character set 'utf8'");
mysqli_query($con,"set names 'utf8'");

$sql = "SELECT * FROM movie WHERE title LIKE '%" . $keywords . "%' LIMIT 0, 30"; //SQL语句
$result = mysqli_query($con, $sql); //使用mysqli_query函数执行sql
//从结果集中取得所有行作为关联数组或数字数组
if($row = mysqli_fetch_all($result)){
	echo "<p>共搜索到". count($row) ."个与【<font color=\"red\">". $keywords ."</font>】有关的内容</p>";
	for($i=0; $i<count($row); $i++){
		echo "<div class=\"video\"><a href=\"http://www.okzy.co/index.php?m=vod-search&wd=". $keywords ."\" title=\"". $row[$i][2] ."\" ><div class=\"img\" style=\"background-image: url(https://images.weserv.nl/?url=". $row[$i][4] .");\"></div></a><div class=\"info\"><h3><a href=\"http://www.okzy.co/index.php?m=vod-search&wd=". $keywords ."\">". $row[$i][2] ."</a><span class=\"data\"> ". $row[$i][5] ."</span></h3><span class=\"actor\">". $info->actor($row[$i][9]) ."</span><span class=\"description\"><p>". $row[$i][6] ."</p><span><span class=\"more\"><a href=\"https://movie.douban.com/subject/". $row[$i][1] ."\">查看详情</a></span></div></div>";
	}
} else {
	echo "<p>没有找到相关结果</p>";
}
//释放结果集
mysqli_free_result($result);

//断开服务器连接
mysqli_close($con);
?>
</body>
</html>