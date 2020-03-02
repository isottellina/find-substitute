-- creation.sql --- 
-- 
-- Filename: creation.sql
-- Author: Louise <louise>
-- Created: Tue Feb 18 22:56:42 2020 (+0100)
-- Last-Updated: Mon Mar  2 02:45:56 2020 (+0100)
--          By: Louise <louise>
--

DROP TABLE IF EXISTS Searches;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Categories;

CREATE TABLE Categories (
       id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
       category_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Products (
       id INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
       product_name VARCHAR(255) NOT NULL,
       nutriscore CHAR(1) NOT NULL,
       category INT NOT NULL,
       shops VARCHAR(512),
       url VARCHAR(368),
       
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
