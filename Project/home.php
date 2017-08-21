<?php
 ob_start();
 session_start();
 require_once 'dbconnect.php';
 
 // if session is not set this will redirect to login page
 if( !isset($_SESSION['user']) ) {
  header("Location: index.php");
  exit;
 }
 // select loggedin users detail
 $res=mysql_query("SELECT * FROM users WHERE userId=".$_SESSION['user']);
 $userRow=mysql_fetch_array($res);
?>
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>Welcome - <?php echo $userRow['userEmail']; ?></title>
<link rel="stylesheet" href="assets/css/bootstrap.min.css" type="text/css"  />
<link rel="stylesheet" href="style.css" type="text/css" />
</head>
<body>
dd

 <nav class="navbar navbar-default navbar-fixed-top">
      <div class="container">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <!--span class="sr-only">Toggle navigation</span-->
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <!--
          <a class="navbar-brand" href="http://www.codingcage.com">Coding Cage</a>
          -->
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav">
            <li class="active"><a href="http://www.tesco.com">Welcome to Tesco</a></li>
          </ul>
          <ul class="nav navbar-nav navbar-right">
            
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">
     <span class="glyphicon glyphicon-user"></span>&nbsp;Hi' <?php echo $userRow['userEmail']; ?>&nbsp;<span class="caret"></span></a>
              <ul class="dropdown-menu">
                <li><a href="logout.php?logout"><span class="glyphicon glyphicon-log-out"></span>&nbsp;Sign Out</a></li>
              </ul>
            </li>
          </ul>
        </div><!--/.nav-collapse -->
      </div>
    </nav--> 

 <div id="wrapper">

 <div class="container">
    
     <div class="page-header">
     <h3>My Offers</h3>
     <?php 
require_once('dbconnect.php');  
 $sql="SELECT * FROM  Discounts";
 $sql1="SELECT * FROM buying_list WHERE userId=".$_SESSION['user'];
$result1=mysql_query($sql1);
while($row = mysql_fetch_array($result1, MYSQL_ASSOC))
$pref= $row['pref_Products'];

$myarray= explode(',', $pref);
//print_r($myarray);
//echo $myarray[0];
$tpnb=$myarray[0];
echo $tpnb;

$result=mysql_query($sql);
while($row = mysql_fetch_array($result, MYSQL_ASSOC)){
  if ($row['TPNB']==tpnb) {
    if($row['offer']!='0')
      echo $row['TPNB'];
  }

}

     ?>
     </div>
        
      <div>
      <h3>Other Offers</h3>
      <?php

$sql="SELECT * FROM  Discounts";

$result=mysql_query($sql);
while($row = mysql_fetch_array($result, MYSQL_ASSOC)){
    if($row['offer']!='0'){
      echo $row['TPNB'];
      echo "<br>";
    }


}

?>


      </div>  
    
    </div>
    
    </div>
    
    <script src="assets/jquery-1.11.3-jquery.min.js"></script>
    <script src="assets/js/bootstrap.min.js"></script>
    
</body>
</html>
<?php ob_end_flush(); ?>
