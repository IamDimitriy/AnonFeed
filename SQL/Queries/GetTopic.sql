SELECT Question, Topic_Sequence, Topic_Id, Author_User_Id
FROM Topics
WHERE Topic_Id = ?
LIMIT 1;
