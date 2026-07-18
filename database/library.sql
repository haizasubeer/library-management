DROP DATABASE IF EXISTS library_management;
CREATE DATABASE library_management;
USE library_management;

CREATE TABLE categories (
    Category_ID   INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Category_Name VARCHAR(100) NOT NULL,
    Description   TEXT,
    Created_At    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE books (
    Book_ID          INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ISBN             VARCHAR(20) NOT NULL UNIQUE,
    Title            VARCHAR(255) NOT NULL,
    Author           VARCHAR(150) NOT NULL,
    Category_ID      INT NOT NULL,
    Publisher        VARCHAR(150) NULL,
    Publication_Year YEAR NULL,
    Total_Copies     INT NOT NULL DEFAULT 1,
    Available_Copies INT NOT NULL DEFAULT 1,
    Shelf_Number     VARCHAR(20) NULL,
    Added_On         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_books_cat FOREIGN KEY (Category_ID) REFERENCES categories(Category_ID),
    CONSTRAINT chk_total_copies CHECK (Total_Copies >= 0),
    CONSTRAINT chk_available_copies CHECK (Available_Copies >= 0 AND Available_Copies <= Total_Copies)
);

CREATE TABLE members (
    Member_ID       INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Full_Name       VARCHAR(150) NOT NULL,
    Gender          ENUM('Male','Female','Other') NOT NULL,
    Email           VARCHAR(150) NOT NULL UNIQUE,
    Phone           VARCHAR(15) NOT NULL UNIQUE ,
    Address         TEXT,
    Membership_Date DATE NOT NULL DEFAULT (CURRENT_DATE),
    Membership_Type ENUM('Standard','Premium','Student') DEFAULT 'Standard',
    Status          ENUM('Active','Inactive','Suspended') DEFAULT 'Active'
);

CREATE TABLE librarians (
    Librarian_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name         VARCHAR(150) NOT NULL,
    Username     VARCHAR(50) NOT NULL,
    Password     VARCHAR(255) NOT NULL,
    Email        VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE borrow_records (
    Borrow_ID     INT AUTO_INCREMENT PRIMARY KEY,
    Member_ID     INT NOT NULL,
    Book_ID       INT NOT NULL,
    Librarian_ID  INT,
    Borrow_Date   DATE DEFAULT (CURRENT_DATE),
    Due_Date      DATE NOT NULL,
    Return_Date   DATE,
    Fine_Amount   DECIMAL(8,2) DEFAULT 0.00,
    Borrow_Status ENUM('Borrowed','Returned','Overdue') DEFAULT 'Borrowed',
    
    CONSTRAINT fk_borrow_member FOREIGN KEY (Member_ID) REFERENCES members(Member_ID),
    CONSTRAINT fk_borrow_book FOREIGN KEY (Book_ID) REFERENCES books(Book_ID),
    CONSTRAINT fk_borrow_librarian FOREIGN KEY (Librarian_ID) REFERENCES librarians(Librarian_ID)
);