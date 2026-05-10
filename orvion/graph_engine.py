from neo4j import GraphDatabase
from orvion.config import settings
import logging

class GraphEngine:
    def __init__(self):
        if settings.NEO4J_URI:
            self.driver = GraphDatabase.driver(
                settings.NEO4J_URI, 
                auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
            )
        else:
            self.driver = None
            logging.warning("Neo4j URI not configured. Graph features will be disabled.")

    def close(self):
        if self.driver:
            self.driver.close()

    def update_agent_reputation(self, agent_address: str, job_id: str, amount: float, status: str):
        """Update agent reputation and transaction history in the graph"""
        if not self.driver:
            return

        with self.driver.session() as session:
            session.execute_write(self._update_graph, agent_address, job_id, amount, status)

    @staticmethod
    def _update_graph(tx, agent_address, job_id, amount, status):
        # Create or update Agent node
        tx.run("""
            MERGE (a:Agent {address: $address})
            ON CREATE SET a.reputation = 0.0, a.total_volume = 0.0
        """, address=agent_address)

        # Create Job node
        tx.run("""
            MERGE (j:Job {job_id: $job_id})
            SET j.amount = $amount, j.status = $status
        """, job_id=job_id, amount=amount, status=status)

        # Create relationship
        tx.run("""
            MATCH (a:Agent {address: $address}), (j:Job {job_id: $job_id})
            MERGE (a)-[r:EXECUTED]->(j)
        """, address=agent_address, job_id=job_id)

        # Update reputation if confirmed
        if status == "confirmed":
            tx.run("""
                MATCH (a:Agent {address: $address})
                SET a.reputation = a.reputation + 0.1,
                    a.total_volume = a.total_volume + $amount
            """, address=agent_address, amount=amount)

    def get_agent_trust_score(self, agent_address: str):
        """Calculate trust score based on graph relationships"""
        if not self.driver:
            return 0.0
        
        with self.driver.session() as session:
            result = session.run("""
                MATCH (a:Agent {address: $address})
                RETURN a.reputation as reputation
            """, address=agent_address)
            record = result.single()
            return record["reputation"] if record else 0.0

graph_engine = GraphEngine()
