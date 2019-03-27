CREATE TABLE IF NOT EXISTS `links` (
    `id` INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    `key` VARCHAR(256) NOT NULL UNIQUE,
    `target` VARCHAR(1024) NOT NULL
) COLLATE 'utf8mb4_bin';

CREATE TABLE IF NOT EXISTS `users` (
    `id` BIGINT UNSIGNED PRIMARY KEY,
    `name` VARCHAR(128) NULL DEFAULT NULL
) COLLATE 'utf8mb4_general_ci';
