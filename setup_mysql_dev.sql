-- Prepares a MySQL server for the project
-- Creates the database hbnb_dev_db if it does not exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
-- Creates the user hbnb_dev with the password hbnb_dev_pwd
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
-- Gives hbnb_dev all privileges on hbnb_dev_db only
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
-- Gives hbnb_dev SELECT privilege on performance_schema only
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
-- Gives hbnb_dev the USAGE privilege on the server
GRANT USAGE ON *.* TO 'hbnb_dev'@'localhost';
FLUSH PRIVILEGES;
