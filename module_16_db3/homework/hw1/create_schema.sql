PRAGMA foreig_keys = ON;

DROP TABLE IF EXISTS `actors`;
DROP TABLE IF EXISTS `movie`;
DROP TABLE IF EXISTS `movie_cast`;
DROP TABLE IF EXISTS `oscar_awarded`;
DROP TABLE IF EXISTS `director`;
DROP TABLE IF EXISTS `movie_direction`;

CREATE TABLE `actors` (
    `act_id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `act_first_name` VARCHAR(50) NOT NULL,
    `act_last_name` VARCHAR(50) NOT NULL,
    `act_gender` VARCHAR(1) NOT NULL
);

CREATE TABLE `movie` (
    `mov_id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `mov_title` VARCHAR(50) NOT NULL
);

CREATE TABLE `movie_cast` (
    `act_id` INTEGER NOT NULL REFERENCES `actors` (`act_id`) ON DELETE CASCADE,
    `mov_id` INTEGER NOT NULL REFERENCES `movie` (`mov_id`) ON DELETE CASCADE,
    `role` VARCHAR(50) NOT NULL
);

CREATE TABLE `oscar_awarded` (
    `award_id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `mov_id` INTEGER NOT NULL REFERENCES `movie` (`mov_id`) ON DELETE CASCADE
);

CREATE TABLE `director` (
    `dir_id` INTEGER PRIMARY KEY AUTOINCREMENT,
    `dir_firct_name` VARCHAR(50) NOT NULL,
    `dir_last_name` VARCHAR(50) NOT NULL
);

CREATE TABLE `movie_direction` (
    `dir_id` INTEGER NOT NULL REFERENCES `director` (`dir_id`) ON DELETE CASCADE,
    `mov_id` INTEGER NOT NULL REFERENCES `movie` (`mov_id`) ON DELETE CASCADE
);
