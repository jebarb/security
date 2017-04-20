<?php
# Start a php-managed 'session'
@session_start();
# Protect against 'session fixation' :)
if (!isset($_SESSION['initiated'])) {
 @session_regenerate_id();
 $_SESSION['initiated'] = true;
}
# Protect against 'session hijacking' :)
if (isset($_SESSION['HTTP_USER_AGENT'])) {
 if ($_SESSION['HTTP_USER_AGENT'] != md5($_SERVER['HTTP_USER_AGENT']))
  session_unset();
 else
  $_SESSION['HTTP_USER_AGENT'] = md5($_SERVER['HTTP_USER_AGENT']);
}
# Logout, if requested
if (isset($_GET['logout']))
 session_unset();

# If a user attempts to log in, verify their credentials
$createToken = False;
if (isset($_POST['reset'])) {
  if (isset($_POST['user']) and $_POST['user'] != '') {
    echo "Redirecting to password reset page, <a href=\"forgotpw.php?user=".htmlspecialchars($_POST['user'])."> click here</a> if you are not automatically redirected.";
    header('Location: forgotpw.php?user='.htmlspecialchars($_POST['user']));
  } else {
    echo "You need to enter a valid username to reset.";
  }
}
else if (isset($_POST['user']) and isset($_POST['pass'])) {
 $dbh = new mysqli('localhost',"dbadmin","secure","secureweb");
 if(mysqli_connect_errno()) {
  echo "Connection Failed: " . mysqli_connect_errno();
  die();
 }
 # Protect against SQL injection with prepared statements :)
 $stmt = $dbh->prepare(
  "SELECT userid,username FROM users".
  " WHERE username=? AND password=?");
 if ($stmt) {
  $hash = md5($_POST['user'].sha1($_POST['user'].md5($_POST['pass'])));
#debug
#  echo $hash . " ";;
  $stmt->bind_param('ss', $_POST['user'], $hash);
  $stmt->execute();
  $stmt->bind_result($userid, $username);
  if ($stmt->fetch()) {
   $_SESSION['logged_in'] = True;
   $_SESSION['user'] = $_POST['user'];
   $_SESSION['userid'] = $userid;
   $createToken = True;
  } else {
   echo "<b>Invalid username and/or password!</b>";
  }
  $stmt->close();
 }

}

# If a valid user is logged in, generate tokens for them
if ($createToken == True) {
$logged_msg = "LOGIN:" . $_POST['user'] . " from " . $_SERVER['REMOTE_ADDR'] . " " . $_SERVER['HTTP_USER_AGENT'];
error_log($logged_msg); 

# First grab the token information
$query = "SELECT upload ".
         "FROM users ".
         "WHERE username='".$_SESSION['user']."'";
$result=$dbh->query($query);
$num=$result->num_rows;
if ($num <= 0) {
 echo 'a database error occurred';
 die();
}
$row = $result->fetch_assoc();
$isPublisher=$row['upload'];

if ($isPublisher == 1)
 $publishValue = 'Publisher=True';
else
 $publishValue = 'Publisher=False';

# Create 'APIKEY token'
$data = '== SecureToken LoggedIn=True '.$publishValue.' ==';

# Generate the key
$key = '';
$key .= '::' . $_SERVER['REQUEST_TIME'];
$key .= '::' . $_SERVER['HTTP_USER_AGENT'];
$key .= '::' . getmypid();
$key .= '::' . $_SERVER['SERVER_ADDR'];
$key .= '::' . $_SERVER['SERVER_PORT'];
$key .= '::' . $_SERVER['REMOTE_ADDR'];
$key .= '::' . $_SERVER['REMOTE_PORT'];
$key .= '::' . getmyuid();
$key .= '::' . getmygid();
#print "key = $key\n";
$key = md5($key, True);
$iv = md5($key, True);
#print "APIKEY_TOKEN=". $data . "<br>";
# Encrypt it
$encrypted = openssl_encrypt($data, 'aes-128-cbc', $key, False, $iv);
setcookie('APIKEY_TOKEN', $encrypted, time() + (86400 * 7));
$_SESSION['APIKEY_TOKEN_key'] = $key;
$_SESSION['APIKEY_TOKEN_iv'] = $iv;
$dbh->close();


# Create 'PWD_STORE' token
#need superdbadmin acccess from now on.
 $dbh = new mysqli('localhost',"superdbadmin","supersecure","secureweb");
 if(mysqli_connect_errno()) {
  echo "Connection Failed: " . mysqli_connect_errno();
  die();
 }
$query = "SELECT api_keys.key FROM api_keys WHERE userid=".$_SESSION['userid'];
$result = $dbh->query($query);
$num = $result->num_rows;
if ($num <= 0) {
 echo 'a database error occurred';
 die();
}
$row = $result->fetch_assoc();
if ($num > 0) {
  $apikey=$row['key'];
}
$subresult=$dbh->query("SELECT encryption_key FROM stuff");
$subnum = $subresult->num_rows;
if ($subnum <= 0) {
  echo 'a database error occurred';
  die();
}
$subrow = $subresult->fetch_assoc();
$key=$subrow['encryption_key'];
$subresult=$dbh->query("SELECT secret FROM fabian");
$subnum = $subresult->num_rows;
if ($subnum <= 0) {
  echo 'a database error occurred';
  die();
}
$subrow = $subresult->fetch_assoc();
$secret=$subrow['secret'];
$data = '== SecureToken LoggedIn=True ApiKey='.$apikey.' Secret='.$secret.' ==';
#print "PWD_STORE_TOKEN=". $data . "<br>";
$salt = openssl_random_pseudo_bytes(3);
$encrypted = 
  openssl_encrypt($data, 'rc4', $salt.$key, False, '');

setcookie('PWD_STORE_token', $encrypted, time() + (86400 * 7));
setcookie('PWD_STORE_token_salt', $salt, time() + (86400 * 7));



#Create 'SAFE2_token'
$query = "SELECT encryption_key FROM fabian";
$result = $dbh->query($query);
$num = $result->num_rows;
if ($num <= 0) {
 echo 'a database error occurred';
 die();
}

$row = $result->fetch_assoc();
$key = $row['encryption_key'];


$query = "SELECT safe_access ".
         "FROM users ".
         "WHERE username='".$_SESSION['user']."'";
$result=$dbh->query($query);
$num=$result->num_rows;
if ($num <= 0) {
 echo 'a database error occurred';
 die();
}
$row = $result->fetch_assoc();
$hasAccess=$row['safe_access'];

if ($hasAccess == 1)
 $accessValue = 'Safe=True';
else
 $accessValue = 'Safe=False';

$data = '== SecureToken LoggedIn=True '.$accessValue.' ==';
#print "SAFE2_TOKEN=". $data . "<br>";
# Generate the key
$key = md5($key, True);
$iv = md5($key, True);

# Encrypt it
$encrypted = openssl_encrypt($data, 'aes-128-cbc', $key, False, $iv);
setcookie('SAFE2_TOKEN', $encrypted, time() + (86400 * 7));
$_SESSION['SAFE2_TOKEN_key'] = $key;
$_SESSION['SAFE2_TOKEN_iv'] = $iv;
$dbh->close();

}
?>