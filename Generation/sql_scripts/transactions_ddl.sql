DELIMITER //

CREATE PROCEDURE open_trade(
    IN id INT,
    IN market VARCHAR(20),
    IN sector VARCHAR(20),
    IN lotsize DECIMAL(5,2),
    IN open_price DECIMAL(10,4),
    IN open_time DATETIME,
    IN trade_dir ENUM('BUY', 'SELL'),
    IN percent_risk DECIMAL(4,2),
    IN system VARCHAR(20),
    IN stoploss DECIMAL(10,4),
    IN status ENUM('OPEN', 'CLOSED', 'PENDING')
)
BEGIN
    DECLARE commit_message VARCHAR(255) DEFAULT 'Transaction opened successfully';

    -- Start the transaction
    START TRANSACTION;

    IF (SELECT sector_id FROM sectors WHERE name = sector) = NULL THEN
        INSERT INTO sectors (name) VALUES (sector);
    END IF;

    IF (SELECT market_id FROM markets WHERE name = market) = NULL THEN
        INSERT INTO markets (name, sector_id) 
        (market, (SELECT sector_id FROM sectors WHERE name = sector));
    END IF;

    INSERT INTO trades(trade_id, market_id, lot_size, open_price, direction, percent_risk, stoploss, status, sys_id, open_time)
    (id, (SELECT market_id FROM markets WHERE name = market), lotsize, open_price, trade_dir, percent_risk, stoploss, status, (SELECT sys_id FROM systems WHERE name = system), open_time)
        
    -- Commit the transaction
    COMMIT;
    SELECT commit_message AS 'Result';

END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE close_trade(
    IN id INT,
    IN closing_price DECIMAL(10,4),
    IN profit DECIMAL(4,2),
    IN closing_time DATETIME
)
BEGIN
    DECLARE rollback_message VARCHAR(255) DEFAULT 'Transaction rolled back: Insufficient funds';
    DECLARE commit_message VARCHAR(255) DEFAULT 'Transaction committed successfully';

    -- Start the transaction
    START TRANSACTION;

    -- Attempt to debit money from account 1
    UPDATE trades 
    SET close_price = closing_price,
        percent_profit = profit,
        close_time = closing_time
    WHERE trade_id = id;

    -- Commit the transaction
    COMMIT;
    SELECT commit_message AS 'Result';
END //

DELIMITER ;