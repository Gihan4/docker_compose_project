-- create_prices_table.sql
CREATE DATABASE IF NOT EXIST db_prices;
USE db_prices;

CREATE TABLE prices (
  id INT AUTO_INCREMENT PRIMARY KEY,
  cryptocurrency VARCHAR(255) NOT NULL,
  price DECIMAL(18, 2) NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
