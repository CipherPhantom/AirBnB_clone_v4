-- This script prepares a MySQL server for the project (TEST)

-- Creates database
CREATE DATABASE IF NOT EXISTS hbnb_test_db;

-- Creates user
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';

-- Grant user prvileges
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
