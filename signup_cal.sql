create database hicup;
use hicup;
CREATE TABLE signup (
    ID INT IDENTITY(1,1) PRIMARY KEY,     -- auto-generated ID
    First_name NVARCHAR(50) NOT NULL,
    Last_name NVARCHAR(50) NOT NULL,
    Email NVARCHAR(100) UNIQUE NOT NULL,
    Password NVARCHAR(256) NOT NULL
);
select*from signup;