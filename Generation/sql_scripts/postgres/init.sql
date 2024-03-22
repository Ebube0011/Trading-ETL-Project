CREATE SCHEMA landing_area; 
CREATE SCHEMA staging_area;

USE landing_area;

CREATE TABLE <tb_name> (
    <col_1> INT <constraint>,
    <col_2> CHAR(20),
    <col_3> DECIMAL(6,2),
    <col_4> DECIMAL(6,2),
    <col_5> DATE,
    PRIMARY KEY(<col_1>, ...),
    FOREIGN KEY(<col_2>) 
    REFERENCES <tb_name2>(<col_3>) 
    <f_constraint>, 
    FOREIGN KEY ...
);

            
USE staging_area;

CREATE TABLE Fact_Sales (
    <col_1> INT <constraint>,
    <col_2> CHAR(20),
    <col_3> DECIMAL(6,2),
    <col_4> DECIMAL(6,2),
    <col_5> DATE,
    PRIMARY KEY(<col_1>, ...),
    FOREIGN KEY(<col_2>) 
    REFERENCES <tb_name2>(<col_3>) 
    <f_constraint>, 
    FOREIGN KEY ...
);

CREATE TABLE Supplier (
    <col_1> INT <constraint>,
    <col_2> CHAR(20),
    <col_3> DECIMAL(6,2),
    <col_4> DECIMAL(6,2),
    <col_5> DATE,
    PRIMARY KEY(<col_1>, ...),
    FOREIGN KEY(<col_2>) 
    REFERENCES <tb_name2>(<col_3>) 
    <f_constraint>, 
    FOREIGN KEY ...
);

CREATE TABLE Item (
    <col_1> INT <constraint>,
    <col_2> CHAR(20),
    <col_3> DECIMAL(6,2),
    <col_4> DECIMAL(6,2),
    <col_5> DATE,
    PRIMARY KEY(<col_1>, ...),
    FOREIGN KEY(<col_2>) 
    REFERENCES <tb_name2>(<col_3>) 
    <f_constraint>, 
    FOREIGN KEY ...
);

CREATE TABLE Date (
    <col_1> INT <constraint>,
    <col_2> CHAR(20),
    <col_3> DECIMAL(6,2),
    <col_4> DECIMAL(6,2),
    <col_5> DATE,
    PRIMARY KEY(<col_1>, ...),
    FOREIGN KEY(<col_2>) 
    REFERENCES <tb_name2>(<col_3>) 
    <f_constraint>, 
    FOREIGN KEY ...
);