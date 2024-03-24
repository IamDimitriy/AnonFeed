SELECT Topic_Id, Question, Topic_Sequence
FROM Topics
WHERE Author_User_Id = ?
ORDER BY Topic_Sequence ASC;