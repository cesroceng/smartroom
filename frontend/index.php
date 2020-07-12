<?php include "dbConfig.php";

$msg = "";
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
	  session_start();
    $name = $_POST["username"];
    $password = md5($_POST["password"]);
	 if ($name == '' || $password == '') {
        $msg = "You must enter all fields";
    } else {
        $sql = "SELECT * FROM users WHERE username = '$name' AND password = '$password'";
        $query = mysqli_query($link,$sql);

        if ($query === false) {
            echo "Could not successfully run query ($sql) from DB: " . mysql_error();
            exit;
        }

        if (mysqli_num_rows($query) > 0) {
         
            $_SESSION['loggedin'] = TRUE;
						$_SESSION['name'] = $_POST['username'];
            header('Location: home.php');
            exit;
        }

        $msg = "Username and password do not match";
    }
}
?>
<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<title>SmartCities Project</title>
	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.1/css/all.css">
	<link href="style.css" rel="stylesheet" type="text/css">
</head>
<body>
	<div class="login">
			<h1>Login to SmartCities Project</h1>
			<form action="<?= $_SERVER['PHP_SELF'] ?>" method="post">
				<label for="username">
					<i class="fas fa-user"></i>
				</label>
				<input type="text" name="username" placeholder="Username" id="username" required>
				<label for="password">
					<i class="fas fa-lock"></i>
				</label>
				<input type="password" name="password" placeholder="Password" id="password" required>
				<input type="submit" value="Login">
			</form>
	</div>
</body>
</html>
