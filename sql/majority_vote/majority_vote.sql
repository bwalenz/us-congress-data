/* 
This SQL script makes two different tables:

1. majority_votes: a table that lists the majority vote by party for each vote.
2. majority_vote_common_table: basically, a denormalized table that joins majority_votes
with common_republicans/democrats to make a fast lookup for how a person votes
with the majority. Note that the common_[republicans/democrats] table is itself the result
of denormalization and is roughly three tables joined: votes, person_votes, person. 
*/  

DROP TABLE majority_votes;

CREATE TABLE majority_votes (
    votes   INTEGER,
    vote VARCHAR(50),
    vote_id VARCHAR(20) REFERENCES votes(id),
    date date,
    party VARCHAR(50)
);

WITH vote_counts AS 
(SELECT count(1) as cnt, vote, vote_id, date FROM
common_republicans 
GROUP BY vote, vote_id, date)

INSERT INTO majority_votes 
SELECT A.votes, B.vote, B.vote_id, B.date,'Republican' FROM vote_counts B 
INNER JOIN 
(SELECT max(cnt) as votes, vote_id FROM vote_counts GROUP BY vote_id) A
ON A.vote_id = B.vote_id WHERE A.votes = B.cnt;

WITH vote_counts AS 
(SELECT count(1) as cnt, vote, vote_id, date FROM
common_democrats
GROUP BY vote, vote_id, date)

INSERT INTO majority_votes 
SELECT A.votes, B.vote, B.vote_id, B.date, 'Democrat' FROM vote_counts B 
INNER JOIN 
(SELECT max(cnt) as votes, vote_id FROM vote_counts GROUP BY vote_id) A
ON A.vote_id = B.vote_id AND A.votes = B.cnt;

DROP TABLE majority_vote_common_table;

CREATE TABLE majority_vote_common_table AS
(SELECT cr.vote as cr_vote, mvr.vote as mvr_vote, cr.vote_id, cr.date, cr.person_id, mvr.party
FROM common_republicans cr 
INNER JOIN majority_votes mvr 
ON cr.vote_id = mvr.vote_id WHERE cr.vote = mvr.vote);

INSERT INTO majority_vote_common_table 
SELECT cr.vote as cr_vote, mvr.vote as mvr_vote, cr.vote_id, cr.date, cr.person_id, mvr.party 
FROM common_democrats cr
INNER JOIN majority_votes mvr on cr.vote_id = mvr.vote_id WHERE cr.vote = mvr.vote;



