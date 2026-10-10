<?php
session_start();
if (!isset($_SESSION['authenticated']) || $_SESSION['authenticated'] !== true) {
    header("Location: index.php");
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>CyberVault Portal - Admin Dashboard</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="dashboard-container">
        <header>
            <h2>CyberVault Internal Operations Portal</h2>
            <div class="user-badge">User: <strong><?php echo htmlspecialchars($_SESSION['username']); ?></strong> | Role: <?php echo htmlspecialchars($_SESSION['role']); ?></div>
        </header>

        <main>
            <div class="card success-card">
                <h3>System Access Granted</h3>
                <p>Authentication bypass detected in internal access gateway.</p>
                
                <div class="flag-box">
                    <span>RECOVERED CHALLENGE FLAG:</span>
                    <code>CTF{web_input_exploited}</code>
                </div>
            </div>

            <div class="card info-card">
                <h4>Incident Investigation Context</h4>
                <p>The audit team confirms that improper input sanitization in the authentication query permitted arbitrary SQL execution.</p>
                <p><a href="logout.php" class="btn-secondary">Log Out / End Session</a></p>
            </div>
        </main>
    </div>
</body>
</html>