-- creation.sql --- 
-- 
-- Filename: creation.sql
-- Author: Louise <louise>
-- Created: Tue Feb 18 22:56:42 2020 (+0100)
-- Last-Updated: Sun Mar  1 23:20:59 2020 (+0100)
--          By: Louise <louise>
--

CREATE TABLE IF NOT EXISTS Categories (
       id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
       category_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Products (
       id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
       product_name VARCHAR(100) NOT NULL,
       nutriscore CHAR(1) NOT NULL,
       category INT NOT NULL,
       shops VARCHAR(255),
       url VARCHAR(255),
       
       CONSTRAINT fk_category
       FOREIGN KEY(category)
       REFERENCES Categories(id)
);

CREATE TABLE IF NOT EXISTS Searches (
       id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
       product_searched INT NOT NULL,
       product_given INT NOT NULL,

       CONSTRAINT fk_searched
       FOREIGN KEY(product_searched)
       REFERENCES Products(id),

       CONSTRAINT fk_given
       FOREIGN KEY(product_given)
       REFERENCES Products(id)
);
