CREATE TABLE sectors (
    sector_id INT AUTO_INCREMENT,
    name VARCHAR(20) UNIQUE NOT NULL,
    PRIMARY KEY(sector_id)
);


CREATE TABLE markets (
    market_id INT AUTO_INCREMENT,
    name VARCHAR(20) UNIQUE NOT NULL,
    sector_id INT NOT NULL,
    PRIMARY KEY(market_id)
);


CREATE TABLE systems (
    sys_id INT AUTO_INCREMENT,
    sys_name VARCHAR(20) UNIQUE NOT NULL,
    winrate DECIMAL(5,4) NOT NULL,
    rr_ratio DECIMAL(4,2) NOT NULL,
    PRIMARY KEY(sys_id)
);


CREATE TABLE trades (
    trade_id INT,
    market_id INT NOT NULL,
    lot_size DECIMAL(5,2) NOT NULL,
    open_price DECIMAL(10,4) NOT NULL,
    close_price DECIMAL(10,4) NOT NULL,
    percent_risk DECIMAL(4,2) NOT NULL,
    stoploss DECIMAL(10,4) NOT NULL,
    status ENUM('OPEN', 'CLOSED', 'PENDING'),
    percent_profit DECIMAL(4,2) NOT NULL,
    sys_id INT NOT NULL,
    direction ENUM('BUY', 'SELL'),
    open_time DATETIME NOT NULL,
    close_time DATETIME NOT NULL,
    PRIMARY KEY(trade_id),
    FOREIGN KEY(market_id) 
        REFERENCES markets(market_id)
        ON DELETE CASCADE,
    FOREIGN KEY(sys_id) 
        REFERENCES systems(sys_id) 
        ON DELETE CASCADE
);


ALTER TABLE markets
    ADD FOREIGN KEY(sector_id)
    REFERENCES sectors(sector_id)
    ON DELETE CASCADE;