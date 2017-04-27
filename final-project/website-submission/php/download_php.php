
<?php

if (isset($_GET['file'])) {
  session_start();
  if (isset($_SESSION['logged_in'])){
    $logged_msg = "file accessed:" . $_GET['file'] . " from " . $_SERVER['REMOTE_ADDR'] . " " . $_SERVER['HTTP_USER_AGENT'];
    error_log($logged_msg);
    $file_parts = pathinfo("/var/www/html/".$_GET['file']);
    if(@$file_parts['extension'] == "jpg"){
      header('Content-Type: image/jpeg');
    }
    if(@$file_parts['extension'] == "png"){
      header('Content-Type: image/png');
    }

    @readfile("/var/www/html/".$_GET['file']);
  }
  else {
    die();
  }
}

include('header.php');
?>