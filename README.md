<!-- README.md --- 
;; 
;; Filename: README.md
;; Author: Louise <louise>
;; Created: Sun Feb 16 20:07:33 2020 (+0100)
;; Last-Updated: Wed Feb 26 17:38:59 2020 (+0100)
;;           By: Louise <louise>
 -->
# Readme

## Install

Configurating and running the program is done so: 

 - Install MySQL, set it up and create a database and an user who can access it
 - Copy conf.ini.tmpl to conf.ini
 - Put the name of the database, the name of the user and the password in conf.ini
 - Create a virtual environment by running `virtualenv -p python3 env && . env/bin/activate`
 - Install the dependencies by running `pip install -r requirements.txt`
 - Run the script with `python3 main.py` 

## Use

Once configured, using the program is straightforward:
 - The program will ask you whether you want to find a new substitute or
 find one you have previously searched, you have to select the option you want
 - If you want to find a new substitute, some categories will be presented to
 you and you have to choose one
 - After having selected a category, you will be presented with some of the
 products in this category, and you will have to choose one
 - The program suggets a substitute, and you have the option to save your
 search in the database
 - On the first menu, if you chose to find the products you have previously
 searched, they will be displayed.
