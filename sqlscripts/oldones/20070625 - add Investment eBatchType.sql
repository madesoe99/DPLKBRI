/* Generating enumeration eBatchType */

DELETE FROM Enum_Varchar WHERE Enum_Name = 'eBatchType';

INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBatchType', 'R', 'Registration');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBatchType', 'T', 'Transaction');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBatchType', 'P', 'Premi');
INSERT INTO Enum_Varchar (Enum_Name, Enum_Value, Enum_Description) VALUES ('eBatchType', 'I', 'Investment');