// Constraints, make sure nodes are unique
CREATE CONSTRAINT ON (s:Subject) ASSERT s.id IS UNIQUE;
CREATE CONSTRAINT ON (v:Voter) ASSERT v.name IS UNIQUE;
CREATE CONSTRAINT ON (p:Party) ASSERT p.name IS UNIQUE;

// Nodes creation - use MERGE for upsert, ensuring uniqueness
LOAD CSV WITH HEADERS FROM "file:///data.csv" AS row
MERGE (n:Subject {id: row.id}) 
ON CREATE SET n.subject = row.subject, n.time = datetime(row.time), n.result = row.result
MERGE (voter:Voter {name: row.name})
MERGE (party:Party {name: row.party})

// Edges creation, again using MERGE so only one relationship of a given type will ever be created between a pair of nodes
MERGE (voter)-[:VOTED_FOR {vote: row.vote}]->(n)
MERGE (voter)-[:BELONGS_TO]->(party)
MERGE (party)-[:PRESENT]->(n);