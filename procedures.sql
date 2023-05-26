DELIMITER //

CREATE PROCEDURE GetPriceStats()
BEGIN
    DECLARE min_price DECIMAL(10, 2);
    DECLARE max_price DECIMAL(10, 2);
    DECLARE avg_price DECIMAL(10, 2);

    SELECT MIN(iteneary_costs) INTO min_price FROM travel_packs;
    SELECT MAX(iteneary_costs) INTO max_price FROM travel_packs;
    SELECT AVG(iteneary_costs) INTO avg_price FROM travel_packs;

    SELECT min_price AS min_price, max_price AS max_price, avg_price AS avg_price;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE GetPriceRangeData(IN input_price DECIMAL(10, 2), IN range_value DECIMAL(10, 2))
BEGIN
    DECLARE min_price DECIMAL(10, 2);
    DECLARE max_price DECIMAL(10, 2);

    SET min_price = input_price - range_value;
    SET max_price = input_price + range_value;

    SELECT * FROM travel_packs
    WHERE iteneary_costs >= min_price AND iteneary_costs <= max_price;
END //

DELIMITER ;