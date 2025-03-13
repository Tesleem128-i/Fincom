CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    payment_mode ENUM('cash', 'bank', 'crypto') NOT NULL,
    role ENUM('individual', 'family', 'company') NOT NULL,
    type ENUM('income', 'expense') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    date DATE NOT NULL
)