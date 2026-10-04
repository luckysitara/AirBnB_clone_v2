-- Prepares a MySQL server for the project tests
-- Creates the database hbnb_test_db if it does not exist
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
-- Creates the user hbnb_test with the password hbnb_test_pwd
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
-- Gives hbnb_test all privileges on hbnb_test_db only
GRANT ALL PRIVILEGES ON hbnb_test_db.* TO 'hbnb_test'@'localhost';
-- Gives hbnb_test SELECT privilege on performance_schema only
GRANT SELECT ON performance_schema.* TO 'hbnb_test'@'localhost';
-- Gives hbnb_test the USAGE privilege on the server
GRANT USAGE ON *.* TO 'hbnb_test'@'localhost';
FLUSH PRIVILEGES;
