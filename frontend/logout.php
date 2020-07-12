<?php
session_start();
session_destroy();
unset($_SESSION['name']);
unset($_SESSION['loggedin']);
// Redirect to the login page:
header('Location: index.php');
?>