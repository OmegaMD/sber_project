
--CREATE TABLE Users(UserID INTEGER NOT NULL PRIMARY KEY, Login TEXT NOT NULL, Type NOT NULL);
--INSERT INTO Users(UserID, Login, Type)
--VALUES (1, "Zinaida", "user");
SELECT * FROM Users;

--CREATE TABLE Partners(PartnerID INTEGER NOT NULL PRIMARY KEY, Name TEXT NOT NULL, Contacts TEXT, Description TEXT);
--INSERT INTO Partners(PartnerID, Name, Contacts, Description)
--VALUES (1, "Буше", "phone number", "кондитерская");
SELECT * FROM Partners;

--CREATE TABLE Places(PlaceID INTEGER NOT NULL PRIMARY KEY, Partner INTEGER NOT NULL, Adress TEXT, FOREIGN KEY(Partner) REFERENCES Partners(PartnerID));
--INSERT INTO Places(PlaceID, Partner, Adress)
--VALUES (1, "Буше", "адрес");
SELECT * FROM Places;

--CREATE TABLE Reviews(User INTEGER NOT NULL, Place INTEGER NOT NULL, Contents TEXT NOT NULL, FOREIGN KEY(User) REFERENCES Users(UserID), FOREIGN KEY(Place) REFERENCES Places(PlaceID));
--INSERT INTO Reviews(User, Place, Contents)
--VALUES (1, 1, "great!");
SELECT * FROM Reviews;

--CREATE TABLE Sales(Partner INTEGER NOT NULL, Amount TEXT NOT NULL, Description TEXT, FOREIGN KEY(Partner) REFERENCES Partners(PartnerID));
--INSERT INTO Sales(Partner, Amount, Description)
--VALUES (1, "20%", "every evening after 8pm");
SELECT * FROM Sales;




