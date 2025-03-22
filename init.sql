-- Création des bases de données
CREATE DATABASE IF NOT EXISTS user_service_db;
CREATE DATABASE IF NOT EXISTS rooms_db;
CREATE DATABASE IF NOT EXISTS reservation_db;
CREATE DATABASE IF NOT EXISTS payment_db;

-- Création de l'utilisateur 'sef' et attribution des privilèges
CREATE USER IF NOT EXISTS 'sef'@'%' IDENTIFIED BY '373040Sefa@';
GRANT ALL PRIVILEGES ON user_service_db.* TO 'sef'@'%';
GRANT ALL PRIVILEGES ON rooms_db.* TO 'sef'@'%';
GRANT ALL PRIVILEGES ON reservation_db.* TO 'sef'@'%';
GRANT ALL PRIVILEGES ON payment_db.* TO 'sef'@'%';

-- Appliquer les privilèges
FLUSH PRIVILEGES;

-- Utiliser la base de données des utilisateurs (user_service_db)
USE user_service_db;

-- Création de la table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(200) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    status ENUM('proprietaire', 'locataire') NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_modified DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    suspension_end DATETIME
);

-- Utiliser la base de données des chambres (rooms_db)
USE rooms_db;

-- Création de la table des chambres
CREATE TABLE IF NOT EXISTS rooms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    price FLOAT NOT NULL,
    location VARCHAR(100) NOT NULL,
    distance FLOAT NOT NULL,
    owner_id INT NOT NULL,
    status VARCHAR(20) DEFAULT 'disponible'
);

-- Création de la table des images des chambres
CREATE TABLE IF NOT EXISTS images (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id INT NOT NULL,
    image_data LONGBLOB NOT NULL,
    image_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (room_id) REFERENCES rooms(id) ON DELETE CASCADE
);

-- Utiliser la base de données des réservations (reservation_db)
USE reservation_db;

-- Création de la table des réservations
CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    room_id INT NOT NULL,
    reservation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES user_service_db.users(id),
    FOREIGN KEY (room_id) REFERENCES rooms_db.rooms(id)
);

-- Utiliser la base de données des paiements (payment_db)
USE payment_db;

-- Création de la table des paiements
CREATE TABLE IF NOT EXISTS payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payer_id INT NOT NULL,
    room_id INT NOT NULL,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (payer_id) REFERENCES user_service_db.users(id),
    FOREIGN KEY (room_id) REFERENCES rooms_db.rooms(id)
);

-- Appliquer les privilèges
FLUSH PRIVILEGES;

