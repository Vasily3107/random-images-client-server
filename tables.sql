CREATE DATABASE test_db;
USE test_db;

CREATE TABLE Users (
--  column:      type:              constraints:
    uuid         UNIQUEIDENTIFIER   PRIMARY KEY,
    [login]      VARCHAR(255)       UNIQUE NOT NULL,
    [password]   VARCHAR(255)       NOT NULL
);								      
								      
CREATE TABLE Administrators (	      
--  column:      type:              constraints:
    uuid         UNIQUEIDENTIFIER   PRIMARY KEY,
    [login]      VARCHAR(255)       UNIQUE NOT NULL,
    [password]   VARCHAR(255)       NOT NULL
);								      
								      
CREATE TABLE UserLogs (			      
--  column:      type:              constraints:
    uuid         UNIQUEIDENTIFIER   PRIMARY KEY,
    user_uuid    UNIQUEIDENTIFIER   FOREIGN KEY REFERENCES Users(uuid),
    [message]    NVARCHAR(MAX),
    [url]        NVARCHAR(MAX),
    [date]       DATETIME2
);
