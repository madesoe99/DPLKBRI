/* Generating enumeration eJenisPenerimaanManfaat */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eJenisPenerimaanManfaat';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisPenerimaanManfaat', 'B', 'Pensiun Biasa');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisPenerimaanManfaat', 'D', 'Pensiun Dipercepat');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisPenerimaanManfaat', 'C', 'Pensiun Cacat');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eJenisPenerimaanManfaat', 'J', 'Pensiun Janda / Anak');