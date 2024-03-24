INSERT OR REPLACE INTO Limits (User_Id, Saw_Count)
VALUES (?, (SELECT Saw_Count FROM "Limits" WHERE User_Id = ?) + ?);
