import os
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
USER = os.getenv("NEO4J_USER", "neo4j")
PASS = os.getenv("NEO4J_PASS", "testtest")
DB   = os.getenv("NEO4J_DATABASE", "spotify")

driver = GraphDatabase.driver(URI, auth=(USER, PASS))

def run(q, params=None):
    with driver.session(database=DB) as s:
        return list(s.run(q, params or {}))

def upsert_track(t):
    q = """
    MERGE (tr:Track {id:$id})
      ON CREATE SET tr.name=$name, tr.popularity=$pop
      ON MATCH  SET tr.name=$name, tr.popularity=$pop
    WITH tr
    MERGE (ar:Artist {id:$artist_id})
      ON CREATE SET ar.name=$artist_name
      ON MATCH  SET ar.name=$artist_name
    MERGE (tr)-[:BY_ARTIST]->(ar)
    """
    run(q, t)

def init_schema():
    for q in [
        "CREATE CONSTRAINT user_id IF NOT EXISTS FOR (u:User) REQUIRE u.id IS UNIQUE",
        "CREATE CONSTRAINT track_id IF NOT EXISTS FOR (t:Track) REQUIRE t.id IS UNIQUE",
        "CREATE CONSTRAINT artist_id IF NOT EXISTS FOR (a:Artist) REQUIRE a.id IS UNIQUE",
    ]:
        run(q)
