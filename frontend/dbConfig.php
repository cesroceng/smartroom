<?php

define ("DB_HOST", "127.0.0.1"); // set database host

define ("DB_USER","root"); // set database user

define ("DB_PASS","smartcities"); // set database password

define ("DB_NAME","smartcities"); // set database name


$link = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);

if ($link->connect_errno) {
   die("Couldn't make connection: " . $link->connect_error);
}

#$link = mysqli_connect(DB_HOST, DB_USER, DB_PASS, DB_NAME) or die("Couldn't make connection: " . );


?>
