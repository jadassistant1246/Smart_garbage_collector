CREATE DATABASE collector;
USE collector;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
	phone VARCHAR(15) UNIQUE,
	vehicle_no VARCHAR(20) UNIQUE,
    address TEXT,
    email VARCHAR(100) UNIQUE,
    area VARCHAR(50),
    password VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
select * from users;





