<?php
$servername = "localhost";
$username = "lc_dev";
$password = "lc_P0swd";
$dbname = "lc_dev_db";
$conn = mysqli_connect($url, $username, $password, $dbname);
if (!$conn) {
    die('Could not connect to MySQL: ' . mysqli_connect_error());
}
?>