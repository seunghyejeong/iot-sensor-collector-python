CREATE DATABASE IF NOT EXISTS cp;
USE cp;

CREATE USER 'cp-user'@'localhost' identified by 'master';
CREATE USER 'cp-user'@'%' identified by 'master';
GRANT ALL PRIVILEGES ON cp.* to 'cp-user'@'localhost';
GRANT ALL PRIVILEGES ON cp.* to 'cp-user'@'%';

CREATE TABLE IF NOT EXISTS acceleration_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    x DOUBLE,
    y DOUBLE,
    z DOUBLE,
    latitude DOUBLE,
    longitude DOUBLE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=INNODB;
