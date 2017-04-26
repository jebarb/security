<?php
  # Create 'APIKEY token'
  $data = '== SecureToken LoggedIn=True Publisher=False ==';

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
  echo $key ."<br>\n";
  $rawkey = $key;
  $key = md5($key, True);
  $iv = md5($key, True);
  echo $data . "<br>\n";
  # Encrypt it
  $encrypted = openssl_encrypt($data, 'aes-128-cbc', $key, False, $iv);
  setcookie('PHPSESSID', "ASDF", time() + (86400 * 7) ,"/");
  setcookie('APIKEY_TOKEN', $encrypted, time() + (86400 * 7));
  setcookie('REALKEY', $rawkey, time() + (86400 * 7));
?>