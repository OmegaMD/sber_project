
--CREATE TABLE Users(UserID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Login TEXT NOT NULL, Type NOT NULL);
--INSERT INTO Users(Login, Type)
--VALUES ("Tom", "user");
--DELETE FROM Users
--WHERE Login = "Tom";
SELECT * FROM Users;


--CREATE TABLE Partners(PartnerID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT , Name TEXT NOT NULL, Contacts TEXT, Description TEXT);
--INSERT INTO Partners(Name, Contacts, Description)
--VALUES ("Спортмастер", "phone number", "спортивный магазин");
--UPDATE Partners SET Description = "Торговый центр" WHERE Name = "Мега";

SELECT * FROM Partners;

--CREATE TABLE Places(PlaceID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Partner INTEGER NOT NULL, Adress TEXT, FOREIGN KEY(Partner) REFERENCES Partners(PartnerID));
--INSERT INTO Places(Partner, Adress)
--VALUES ("Мега", "адрес2");
SELECT * FROM Places;

--CREATE TABLE Reviews(User INTEGER NOT NULL, Place INTEGER NOT NULL, Contents TEXT NOT NULL, FOREIGN KEY(User) REFERENCES Users(UserID), FOREIGN KEY(Place) REFERENCES Places(PlaceID));
--INSERT INTO Reviews(User, Place, Contents)
--VALUES (2, 1, "perfect!");
SELECT * FROM Reviews;

--CREATE TABLE Sales(Partner INTEGER NOT NULL, Amount TEXT NOT NULL, Description TEXT, FOREIGN KEY(Partner) REFERENCES Partners(PartnerID));
--INSERT INTO Sales(Partner, Amount, Description)
--VALUES (3, "3%", "in a sportmaster");
SELECT * FROM Sales;











