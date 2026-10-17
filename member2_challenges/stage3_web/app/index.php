<?php
session_start();
require_once 'setup_db.php';

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    $db = new SQLite3('/var/www/html/cybervault.db');

    // INTENTIONALLY VULNERABLE RAW SQL QUERY (Assignment 1 CV-03)
    $query = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
    
    $result = $db->query($query);

    if ($result && ($row = $result->fetchArray(SQLITE3_ASSOC))) {
        $_SESSION['authenticated'] = true;
        $_SESSION['username'] = $row['username'];
        $_SESSION['role'] = $row['role'];
        header("Location: dashboard.php");
        exit;
    } else {
        $error = "Invalid credentials. Incident logging is active.";
    }
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CyberVault Portal - Login</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="login-card">
        <h2>CyberVault Solutions</h2>
        <p class="subtitle">Internal Employee Authentication Portal</p>
        
        <?php if ($error): ?>
            <div class="alert"><?php echo htmlspecialchars($error); ?></div>
        <?php endif; ?>

        <form method="POST" action="index.php">
            <div class="form-group">
                <label>Username</label>
                <input type="text" name="username" placeholder="Employee ID / Username" required autocomplete="off">
            </div>
            <div class="form-group">
                <label>Password</label>
                <input type="password" name="password" placeholder="Password" required>
            </div>
            <button type="submit" class="btn">Authenticate</button>
        </form>
        <div class="footer-note">Notice: Unauthorized access attempts are monitored and recorded.</div>
    </div>
</body>
</html>