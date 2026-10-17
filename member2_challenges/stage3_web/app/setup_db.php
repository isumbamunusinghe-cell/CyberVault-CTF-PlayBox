<?php
$dbFile = '/var/www/html/cybervault.db';

// Create or open DB
$db = new SQLite3($dbFile);

$db->exec("CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);");

// Ensure clean table state
$db->exec("DELETE FROM users;");

// Insert standard user and unreachable admin
$db->exec("INSERT INTO users (username, password, role) VALUES ('admin', 'xK9#mQ!9vL1029348123', 'Administrator');");
$db->exec("INSERT INTO users (username, password, role) VALUES ('jsmith', 'Pass1234!', 'Staff');");

// Set permissions so web server can write
chmod($dbFile, 0666);
?>