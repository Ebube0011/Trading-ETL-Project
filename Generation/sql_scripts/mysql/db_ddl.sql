-- create the user to access the database
CREATE USER 'main_user'
IDENTIFIED BY 'password';

-- grant privileges to the user
GRANT ALL PRIVILEGES
ON *.*
TO 'main_user'
WITH GRANT OPTION;

-- flush
FLUSH PRIVILEGES;



-- create the database
CREATE DATABASE trend_data;



-- use the database
USE trend_data;

-- create the tables
CREATE TABLE trade (
    trade_id INT AUTO_INCREMENT,
    operation VARCHAR(10) NOT NULL,
    profit DECIMAL(5,4) NOT NULL,
    sector VARCHAR(20) NOT NULL,
    market VARCHAR(20) NOT NULL,
    PRIMARY KEY(trade_id)
);











-- insert values into the created table
INSERT INTO trade(operation, profit, sector, market)
VALUES ('buy',0.0000,'Non-Agric','Palladium'),
    ('buy',0.0000,'Non-Agric','XauUsd');
