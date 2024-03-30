// Wipe DB
MATCH (n) DETACH DELETE n

// # Basic queries
// List of subjects
MATCH (s:Subject)
RETURN s.subject

// How many different voters for each party
MATCH (p:Party)
RETURN p, SIZE((p)<-[:BELONGS_TO]-(:Voter)) as count
ORDER BY count DESC

// Stats of voting for specific voter
MATCH (v:Voter {name: 'Petr Vokřál'})-[vote:VOTED_FOR]->(:Subject)
RETURN
    v.name,
    SUM(CASE WHEN vote.vote = 'Ano' THEN 1 ELSE 0 END) AS Ano,
    SUM(CASE WHEN vote.vote = 'Ne' THEN 1 ELSE 0 END) AS Ne,
    SUM(CASE WHEN vote.vote = 'Zdržel se' THEN 1 ELSE 0 END) AS ZdrzelSe,
    SUM(CASE WHEN vote.vote = 'None' THEN 1 ELSE 0 END) AS Nepritomen

// % of absence
MATCH (v:Voter {name: 'Markéta Vaňková'})-[vote:VOTED_FOR]->(:Subject)
WITH v.name AS name, SUM(CASE WHEN vote.vote = 'None' THEN 1 ELSE 0 END) AS Nepritomen, COUNT(vote.vote) AS Celkem
RETURN
    name,
    Celkem - Nepritomen AS Pritomen,
    Nepritomen,
    (Nepritomen*100.0)/Celkem AS Absence

// Number of voters by party who were present during specific voting
MATCH (s:Subject {id: 'Z9/09-130'})<-[vote:VOTED_FOR]-(v:Voter)
WHERE NOT vote.vote = 'None'
MATCH (v)-[:BELONGS_TO]->(p:Party)-[:PRESENT]->(s)
RETURN p.name AS Party, COUNT(v) as NumberOfPresentVoters
ORDER BY NumberOfPresentVoters DESC

// # Interesting queries
// Subjects that were voted for the most
MATCH (s:Subject)<-[:VOTED_FOR]-()
RETURN s.time, s.subject, COUNT(*) AS voteCount
ORDER BY voteCount DESC LIMIT 10

// Voters who changed parties (or their parties renamed)
MATCH (v:Voter)-[:BELONGS_TO]->(party:Party)
WITH v.name AS name, COLLECT(DISTINCT party.name) AS partyNames
WHERE SIZE(partyNames) > 1
RETURN name, SIZE(partyNames) AS partyNum, partyNames
ORDER BY partyNum DESC LIMIT 10
