CREATE TABLE IF NOT EXISTS `dbt`.`users`(
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `first_name` VARCHAR(128) NOT NULL,
    `last_name` VARCHAR(128) NOT NULL,
    `date_of_birth` DATE NOT NULL,
    `gender` VARCHAR(8) NOT NULL,
    `email` VARCHAR(128) NOT NULL,
    `phone` VARCHAR(15) NOT NULL,
    PRIMARY KEY(`user_id`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `dbt`.`travel_packs`(
    `pack_id` INT NOT NULL AUTO_INCREMENT,
    `origin` VARCHAR(128) NOT NULL,
    `destination` VARCHAR(128) NOT NULL,
    `num_days` INT NOT NULL,
    `iteneary_costs` INT NOT NULL,
    `departure_timestamp` DATE NOT NULL,
    `return_timestamp` DATE NOT NULL,
    `slots_left` INT NOT NULL DEFAULT 3,
    PRIMARY KEY(`pack_id`)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `dbt`.`user_packs`(
    `pack_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    FOREIGN KEY (pack_id) REFERENCES travel_packs(pack_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
) ENGINE = InnoDB;

CREATE TABLE IF NOT EXISTS `dbt`.`sites`(
    `site_id` INT NOT NULL AUTO_INCREMENT,
    `site_name` VARCHAR(128) NOT NULL,
	`address` VARCHAR(256) NOT NULL,
    `entry_fee` FLOAT NOT NULL,
    PRIMARY KEY (site_id)
) ENGINE = InnoDB;