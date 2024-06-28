<?php
session_start();
extract($_POST);
include("database.php");
if (isset($_POST['signup'])) {
    $username = mysqli_real_escape_string($conn, $_POST['username']);
    $email = mysqli_real_escape_string($conn, $_POST['email']);
    $password = mysqli_real_escape_string($conn, $_POST['password']);
    $sql = mysqli_query($conn, "SELECT * FROM accounts WHERE email='$email'");
    if (mysqli_num_rows($sql) > 0) {
        echo "Email Id Already Exists";
        exit;
    } else {
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);
        $query = "INSERT INTO accounts (username, email, password) VALUES ('$username', '$email', '$hashed_password')";
        $sql = mysqli_query($conn, $query);
        if ($sql) {
            header("Location: auth.php?status=success");
            exit;
        } else {
            echo "Could Not Perform the Query";
        }
    }
}


if (isset($_POST['login'])) {
    $username = mysqli_real_escape_string($conn, $_POST['username']);
    $password = mysqli_real_escape_string($conn, $_POST['password']);

    $sql = mysqli_query($conn, "SELECT * FROM accounts WHERE username='$username'");
    $row = mysqli_fetch_array($sql);
    
    if (is_array($row) && password_verify($password, $row['password'])) {
        $_SESSION["id"] = $row['id'];
        $_SESSION["email"] = $row['email'];
        $_SESSION["username"] = $row['username'];

        header("Location: alerts.html");
        exit;
    } else {
        echo "Invalid Email ID/Password";
    }
}

mysqli_close($conn);
?>