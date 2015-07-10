/*
 Creates two lookup tables for identifying all the votes by a specific party.
These are used in the majority_votes.sql file to quickly create the majority vote
by party.
*/

CREATE TABLE common_democrats AS 
(SELECT vote, vote_id, votes.date, person_votes.person_id 
from person_votes JOIN
persons ON person_votes.person_id = persons.id
JOIN person_roles ON person_roles.person_id = persons.id
JOIN votes ON votes.id = person_votes.vote_id
WHERE votes.date BETWEEN person_roles.start_date and person_roles.end_date
AND person_roles.party = 'Democrat');

CREATE TABLE common_republicans AS 
(SELECT vote, vote_id, votes.date, person_votes.person_id 
from person_votes JOIN
persons ON person_votes.person_id = persons.id
JOIN person_roles ON person_roles.person_id = persons.id
JOIN votes ON votes.id = person_votes.vote_id
WHERE votes.date BETWEEN person_roles.start_date and person_roles.end_date
AND person_roles.party = 'Republican');

