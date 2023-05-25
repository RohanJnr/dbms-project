DELIMITER //

CREATE TRIGGER check_seats_trigger
BEFORE INSERT ON user_packs
FOR EACH ROW
BEGIN
    DECLARE available_seats INT;

    -- Get the number of available seats
    SELECT slots_left INTO available_seats FROM travel_packs WHERE pack_id = NEW.pack_id;

    -- Check if the number of available seats is greater than 0
    IF available_seats > 0 THEN
        -- Reduce the number of available seats by 1
        SET available_seats = available_seats - 1;
        -- Update the seats_available value in the flight table
        UPDATE travel_packs SET slots_left = available_seats WHERE pack_id = NEW.pack_id;
    ELSE
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No available seats for the selected flight.';
    END IF;
END //

DELIMITER ;


DELIMITER //

CREATE TRIGGER check_phone_number_trigger
BEFORE INSERT OR UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.phone REGEXP '^(9|8|7|6)[0-9]{9}$' = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid Indian phone number format.';
    END IF;
END //

DELIMITER ;